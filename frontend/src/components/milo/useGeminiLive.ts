import { useRef, useCallback, useState, useEffect } from "react";
import { GoogleGenAI, Modality, type Session } from "@google/genai";
import { useMiloStore } from "./miloStore";
import type { MiloContext } from "./miloStore";

type OrbState = "idle" | "listening" | "processing" | "speaking";

const MODEL = "gemini-2.5-flash-native-audio-latest";

// Shared playback AudioContext — must be created/resumed after user gesture
let playCtx: AudioContext | null = null;
function ensurePlayCtx(): AudioContext {
  if (!playCtx || playCtx.state === "closed") playCtx = new AudioContext({ sampleRate: 24000 });
  if (playCtx.state === "suspended") playCtx.resume();
  return playCtx;
}

export function useGeminiLive() {
  const [orbState, setOrbState] = useState<OrbState>("idle");
  const [audioLevel, setAudioLevel] = useState(0);
  const [voiceActive, setVoiceActive] = useState(false);

  const sessionRef = useRef<Session | null>(null);
  const connectedRef = useRef(false);
  const connectingRef = useRef(false);

  // Mic refs
  const streamRef = useRef<MediaStream | null>(null);
  const micCtxRef = useRef<AudioContext | null>(null);
  const workletRef = useRef<ScriptProcessorNode | null>(null);
  const rafRef = useRef(0);

  // Playback refs
  const audioQueueRef = useRef<Float32Array[]>([]);
  const playingRef = useRef(false);
  const speakRafRef = useRef(0);

  const contextRef = useRef<MiloContext | null>(null);
  const { context } = useMiloStore();
  useEffect(() => {
    // When room context changes, close old session so next interaction
    // creates a fresh one with the correct system prompt.
    if (contextRef.current?.roomId && context?.roomId && contextRef.current.roomId !== context.roomId) {
      sessionRef.current?.close();
      sessionRef.current = null;
      connectedRef.current = false;
    }
    contextRef.current = context;
  }, [context]);

  // ====== Connect ======
  const connect = useCallback(async (): Promise<boolean> => {
    if (connectedRef.current && sessionRef.current) return true;
    if (connectingRef.current) {
      // Wait for ongoing connect
      for (let i = 0; i < 80; i++) {
        await new Promise(r => setTimeout(r, 100));
        if (connectedRef.current) return true;
      }
      return false;
    }

    const apiKey = import.meta.env.VITE_GEMINI_API_KEY as string | undefined;
    if (!apiKey) { console.error("[Milo] No API key"); return false; }

    connectingRef.current = true;

    try {
      const ai = new GoogleGenAI({ apiKey });

      const session = await ai.live.connect({
        model: MODEL,
        config: {
          responseModalities: [Modality.AUDIO],
          systemInstruction: { parts: [{ text: buildPrompt(contextRef.current) }] },
        },
        callbacks: {
          onopen: () => { console.log("[Milo] WS open"); },
          onmessage: (msg: Record<string, unknown>) => handleMessage(msg),
          onerror: (e: unknown) => { console.error("[Milo] error:", e); },
          onclose: () => {
            console.log("[Milo] WS closed");
            connectedRef.current = false;
            sessionRef.current = null;
          },
        },
      });

      sessionRef.current = session;
      connectedRef.current = true;
      connectingRef.current = false;
      console.log("[Milo] connected");
      return true;
    } catch (e) {
      console.error("[Milo] connect failed:", e);
      connectingRef.current = false;
      return false;
    }
  }, []);

  // ====== Handle incoming messages ======
  const handleMessage = useCallback((msg: Record<string, unknown>) => {
    if (msg.setupComplete) return; // SDK handles this

    const sc = msg.serverContent as {
      modelTurn?: { parts?: { inlineData?: { data?: string }; text?: string }[] };
      turnComplete?: boolean;
    } | undefined;

    if (!sc) return;

    // Process parts
    if (sc.modelTurn?.parts) {
      for (const part of sc.modelTurn.parts) {
        if (part.inlineData?.data) {
          // Audio chunk — queue for playback
          setOrbState("speaking");
          audioQueueRef.current.push(b64ToF32(part.inlineData.data));
          drainQueue();
        }
        if (part.text) {
          // Text transcript — skip internal reasoning (starts with **)
          const t = part.text.trim();
          if (t && !t.startsWith("**")) {
            useMiloStore.getState().addMessage({ role: "milo", text: t });
          }
        }
      }
    }

    // Turn done
    if (sc.turnComplete) {
      setTimeout(() => {
        if (!playingRef.current && audioQueueRef.current.length === 0) {
          setOrbState("idle");
          setAudioLevel(0);
        }
      }, 300);
    }
  }, []);

  // ====== Audio playback queue ======
  const drainQueue = useCallback(() => {
    if (playingRef.current || audioQueueRef.current.length === 0) return;
    playingRef.current = true;

    const next = () => {
      const chunk = audioQueueRef.current.shift();
      if (!chunk) {
        playingRef.current = false;
        cancelAnimationFrame(speakRafRef.current);
        setOrbState("idle");
        setAudioLevel(0);
        return;
      }

      const ctx = ensurePlayCtx();
      const buf = ctx.createBuffer(1, chunk.length, 24000);
      buf.getChannelData(0).set(chunk);
      const src = ctx.createBufferSource();
      src.buffer = buf;
      src.connect(ctx.destination);

      // Animate orb while playing
      const anim = () => {
        const t = performance.now() / 1000;
        setAudioLevel(Math.max(0, Math.min(1,
          0.35 + Math.sin(t * 8) * 0.28 + Math.sin(t * 3.5) * 0.22 +
          Math.sin(t * 1.2) * 0.18 + (Math.random() - 0.5) * 0.12
        )));
        speakRafRef.current = requestAnimationFrame(anim);
      };
      speakRafRef.current = requestAnimationFrame(anim);

      src.onended = () => { cancelAnimationFrame(speakRafRef.current); next(); };
      src.start();
    };
    next();
  }, []);

  // ====== Send text (via Live = instant voice response) ======
  const sendText = useCallback(async (text: string) => {
    const q = text.trim();
    if (!q) return;
    ensurePlayCtx();

    useMiloStore.getState().addMessage({ role: "user", text: q });
    setOrbState("processing");

    const ok = await connect();
    if (!ok || !sessionRef.current) {
      useMiloStore.getState().addMessage({ role: "milo", text: "Connexion impossible." });
      setOrbState("idle");
      return;
    }

    sessionRef.current.sendClientContent({
      turns: [{ role: "user", parts: [{ text: q }] }],
      turnComplete: true,
    });
  }, [connect]);

  // ====== Push-to-talk: hold to record ======
  const startListening = useCallback(async () => {
    if (voiceActive) return;
    ensurePlayCtx();

    const ok = await connect();
    if (!ok || !sessionRef.current) {
      useMiloStore.getState().addMessage({ role: "milo", text: "Connexion impossible." });
      return;
    }

    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        audio: { sampleRate: 16000, channelCount: 1, echoCancellation: true, noiseSuppression: true },
      });
      streamRef.current = stream;

      const actx = new AudioContext({ sampleRate: 16000 });
      micCtxRef.current = actx;
      const source = actx.createMediaStreamSource(stream);

      // Analyser for orb
      const analyser = actx.createAnalyser();
      analyser.fftSize = 256;
      analyser.smoothingTimeConstant = 0.8;
      source.connect(analyser);
      const freq = new Uint8Array(analyser.frequencyBinCount);

      // Stream PCM to Gemini
      const proc = actx.createScriptProcessor(4096, 1, 1);
      workletRef.current = proc;
      source.connect(proc);
      proc.connect(actx.destination);

      proc.onaudioprocess = (e) => {
        // Orb level
        analyser.getByteFrequencyData(freq);
        let s = 0;
        for (let i = 0; i < freq.length; i++) s += freq[i] * freq[i];
        setAudioLevel(Math.min(Math.sqrt(s / freq.length) / 128, 1));

        // Send to Gemini
        const pcm = e.inputBuffer.getChannelData(0);
        const b64 = f32ToB64PCM16(pcm);
        try {
          sessionRef.current?.sendRealtimeInput({
            media: { mimeType: "audio/pcm;rate=16000", data: b64 },
          });
        } catch { /* session closed */ }
      };

      setVoiceActive(true);
      setOrbState("listening");
    } catch {
      useMiloStore.getState().addMessage({ role: "milo", text: "Micro refuse." });
    }
  }, [voiceActive, connect]);

  // ====== Release = stop recording, Gemini responds ======
  const stopListening = useCallback(() => {
    if (!voiceActive) return;

    workletRef.current?.disconnect();
    workletRef.current = null;
    streamRef.current?.getTracks().forEach(t => t.stop());
    streamRef.current = null;
    micCtxRef.current?.close();
    micCtxRef.current = null;
    cancelAnimationFrame(rafRef.current);

    setVoiceActive(false);
    setAudioLevel(0);
    setOrbState("processing");

    // Tell Gemini the user is done speaking
    try {
      sessionRef.current?.sendClientContent({ turnComplete: true });
    } catch { /* ignore */ }
  }, [voiceActive]);

  // ====== Spacebar push-to-talk ======
  useEffect(() => {
    const down = (e: KeyboardEvent) => {
      if (e.code === "Space" && !e.repeat && !["INPUT", "TEXTAREA"].includes(document.activeElement?.tagName || "")) {
        e.preventDefault();
        startListening();
      }
    };
    const up = (e: KeyboardEvent) => {
      if (e.code === "Space" && !["INPUT", "TEXTAREA"].includes(document.activeElement?.tagName || "")) {
        e.preventDefault();
        stopListening();
      }
    };
    window.addEventListener("keydown", down);
    window.addEventListener("keyup", up);
    return () => { window.removeEventListener("keydown", down); window.removeEventListener("keyup", up); };
  }, [startListening, stopListening]);

  // Cleanup
  useEffect(() => () => {
    cancelAnimationFrame(rafRef.current);
    cancelAnimationFrame(speakRafRef.current);
    workletRef.current?.disconnect();
    streamRef.current?.getTracks().forEach(t => t.stop());
    sessionRef.current?.close();
  }, []);

  return { orbState, audioLevel, voiceActive, sendText, startListening, stopListening };
}

// ====== System prompt ======

function buildPrompt(ctx: MiloContext | null): string {
  const base = `Tu es Milo, assistant pedagogique du jeu C:\\DUNGEON a l'ECE (Ecole Centrale d'Electronique). Tu aides des eleves de 1ere annee d'ingenieur a apprendre le C.

Regles :
- Jamais la reponse directe. Guide par des questions courtes.
- 1-2 phrases max, droit au but.
- Ne te presente pas. L'eleve te connait.
- Tutoie, sois direct et encourageant.
- Si l'eleve galere, donne un indice precis sur le concept C concerne.
- Adapte-toi : ce sont des ingenieurs, pas des debutants complets.`;

  if (!ctx?.title) return base;

  return `${base}

EXERCICE EN COURS :
Salle "${ctx.title}" — ${ctx.challengeType === "trace_value" ? "tracer l'execution" :
    ctx.challengeType === "find_bug" ? "trouver le bug" :
    ctx.challengeType === "fill_blank" ? "completer le code" :
    ctx.challengeType === "match_types" ? "associer les elements" :
    ctx.challengeType === "sort_order" ? "remettre en ordre" :
    ctx.challengeType === "memory_map" ? "comprendre la memoire" : ctx.challengeType || "exercice"}
Concepts : ${ctx.conceptTags?.join(", ") || "C"}
Difficulte : ${ctx.difficulty || "?"}/5
Enonce : "${ctx.questionPrompt || ""}"

Aide l'eleve sur CET exercice. Sois precis et pertinent.`;
}

// ====== Audio utils ======

function f32ToB64PCM16(f32: Float32Array): string {
  const pcm = new Int16Array(f32.length);
  for (let i = 0; i < f32.length; i++) {
    const s = Math.max(-1, Math.min(1, f32[i]));
    pcm[i] = s < 0 ? s * 0x8000 : s * 0x7fff;
  }
  const u8 = new Uint8Array(pcm.buffer);
  let b = "";
  for (let i = 0; i < u8.length; i++) b += String.fromCharCode(u8[i]);
  return btoa(b);
}

function b64ToF32(b64: string): Float32Array {
  const bin = atob(b64);
  const u8 = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) u8[i] = bin.charCodeAt(i);
  const pcm = new Int16Array(u8.buffer);
  const f32 = new Float32Array(pcm.length);
  for (let i = 0; i < pcm.length; i++) f32[i] = pcm[i] / 0x8000;
  return f32;
}
