import { useRef, useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { useMiloStore } from "./miloStore";
import { useGeminiLive } from "./useGeminiLive";
import MiloOrb3D from "./MiloOrb3D";

interface Props {
  embedded?: boolean;
  onClose?: () => void;
}

export default function MiloChat({ embedded = false, onClose }: Props) {
  const { messages, context, isLoading } = useMiloStore();
  const { orbState, audioLevel, voiceActive, sendText, startListening, stopListening } = useGeminiLive();
  const [input, setInput] = useState("");
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = () => {
    const q = input.trim();
    if (!q) return;
    setInput("");
    sendText(q);
  };

  const suggestions = context?.conceptTags
    ? [`C'est quoi ${context.conceptTags[0]} ?`, "Donne-moi un indice", "Explique le concept"]
    : ["Aide-moi sur cet exercice", "Je comprends pas"];

  return (
    <div className={`flex flex-col ${embedded ? "h-full" : ""}`}>
      {/* Orb area — hold to talk */}
      <div
        className="relative flex items-center justify-center shrink-0 py-1 select-none"
        style={{ borderBottom: "1px solid #1a1a30", cursor: "pointer" }}
        onMouseDown={startListening}
        onMouseUp={stopListening}
        onMouseLeave={() => { if (voiceActive) stopListening(); }}
        onTouchStart={startListening}
        onTouchEnd={stopListening}
      >
        <MiloOrb3D state={orbState} audioLevel={audioLevel} size={embedded ? 130 : 110} />
        <div className="absolute bottom-1 left-0 right-0 text-center pointer-events-none">
          <img src="/milo-logo.svg" alt="Milo" className="inline-block h-4 opacity-80" style={{ filter: "brightness(1.2)" }} />
          {voiceActive && <span className="ml-2 text-xs font-mono" style={{ color: "#ff3355" }}>● Ecoute...</span>}
          {orbState === "processing" && !voiceActive && <span className="ml-2 text-xs font-mono" style={{ color: "#ffb800" }}>Reflechit...</span>}
          {orbState === "speaking" && <span className="ml-2 text-xs font-mono" style={{ color: "#5ec4a8" }}>Parle...</span>}
        </div>
        {onClose && (
          <button onClick={(e) => { e.stopPropagation(); onClose(); }} className="absolute top-2 right-2 w-10 h-10 rounded-lg flex items-center justify-center text-sm" style={{ color: "#3a3a5c" }}>✕</button>
        )}
      </div>

      {/* Hold hint */}
      {messages.length === 0 && !voiceActive && orbState === "idle" && (
        <div className="text-center py-1.5 pointer-events-none" style={{ borderBottom: "1px solid #1a1a30" }}>
          <p className="text-xs" style={{ color: "#3a3a5c" }}>
            Maintiens l'orbe ou <kbd className="px-1 py-0.5 rounded" style={{ background: "#131320", border: "1px solid #1e1e35" }}>Espace</kbd> pour parler
          </p>
        </div>
      )}

      {/* Concept tags */}
      {context?.conceptTags && messages.length === 0 && (
        <div className="flex flex-wrap gap-1 px-3 py-1.5 justify-center" style={{ borderBottom: "1px solid #1a1a30" }}>
          {context.conceptTags.map(tag => (
            <span key={tag} className="text-xs px-2 py-0.5 rounded-lg font-mono" style={{ background: "rgba(94,196,168,0.05)", color: "#3a3a5c", border: "1px solid #1e1e35" }}>{tag}</span>
          ))}
        </div>
      )}

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-3 py-2 space-y-2" style={{ minHeight: embedded ? 0 : 100 }}>
        {messages.length === 0 && (
          <div className="space-y-3 py-3 text-center">
            <p className="text-xs leading-relaxed" style={{ color: "#4a4a6a" }}>
              Besoin d'aide sur cet exercice ?
            </p>
            <div className="flex flex-wrap gap-1.5 justify-center">
              {suggestions.map(s => (
                <button key={s} onClick={() => sendText(s)} className="text-xs px-3 py-2 rounded-xl transition-all"
                  style={{ background: "#0f0f1e", border: "1px solid #1e1e35", color: "#5a5a7a" }}
                  onMouseEnter={e => { e.currentTarget.style.borderColor = "rgba(94,196,168,0.3)"; e.currentTarget.style.color = "#5ec4a8"; }}
                  onMouseLeave={e => { e.currentTarget.style.borderColor = "#1e1e35"; e.currentTarget.style.color = "#5a5a7a"; }}
                >{s}</button>
              ))}
            </div>
          </div>
        )}

        {messages.map((msg, i) => (
          <motion.div key={i} initial={{ opacity: 0, y: 4 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.1 }}
            className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
          >
            <div className="max-w-[88%] rounded-2xl px-3 py-2 text-sm leading-relaxed whitespace-pre-wrap"
              style={msg.role === "user"
                ? { background: "rgba(94,196,168,0.06)", border: "1px solid rgba(94,196,168,0.1)", color: "#d0d0e0" }
                : { background: "#0d0d1c", border: "1px solid #1a1a2e", color: "#a8a8c8" }
              }
            >
              {msg.role === "milo" && <span className="text-xs mr-1" style={{ color: "#5ec4a8" }}>✦</span>}
              {msg.text}
            </div>
          </motion.div>
        ))}

        {isLoading && (
          <div className="flex justify-start">
            <div className="rounded-2xl px-3 py-2" style={{ background: "#0d0d1c", border: "1px solid #1a1a2e" }}>
              <motion.span animate={{ opacity: [0.3, 1, 0.3] }} transition={{ duration: 1, repeat: Infinity }} className="text-xs font-mono" style={{ color: "#5ec4a8" }}>
                ✦ ...
              </motion.span>
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      {/* Text input */}
      <div className="shrink-0 px-3 py-2" style={{ borderTop: "1px solid #1a1a30" }}>
        <div className="flex gap-1.5">
          <input value={input} onChange={e => setInput(e.target.value)} onKeyDown={e => e.key === "Enter" && handleSend()}
            placeholder="Ecris a Milo..." className="flex-1 rounded-xl px-3 py-2.5 text-sm outline-none"
            style={{ background: "#0f0f1e", border: "1px solid #1e1e35", color: "white", fontFamily: "inherit" }}
            onFocus={e => (e.currentTarget.style.borderColor = "rgba(94,196,168,0.3)")}
            onBlur={e => (e.currentTarget.style.borderColor = "#1e1e35")}
          />
          <button onClick={handleSend} disabled={!input.trim() || isLoading}
            className="w-11 h-11 rounded-xl flex items-center justify-center shrink-0 text-sm font-bold"
            style={{ background: input.trim() && !isLoading ? "#5ec4a8" : "#0f0f1e", color: input.trim() && !isLoading ? "#080810" : "#3a3a5c", cursor: input.trim() && !isLoading ? "pointer" : "not-allowed" }}
          >→</button>
        </div>
      </div>
    </div>
  );
}
