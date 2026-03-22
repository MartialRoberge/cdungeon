import { useEffect, useState, useCallback } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import { getRoom, submitAttempt } from "../api";
import { useGameStore, useAuthStore } from "../store";
import { useMiloStore } from "../components/milo/miloStore";
import type { BadgeOut } from "../types";
import ChallengeRouter from "../components/challenges/ChallengeRouter";
import FeedbackOverlay from "../components/feedback/FeedbackOverlay";
import MiloChat from "../components/milo/MiloChat";
import { sounds, initAudio } from "../utils/sound";

type Phase = "loading" | "playing" | "correct" | "wrong" | "cleared" | "boss_cleared" | "dead";
type FeedbackPhase = "idle" | "correct" | "wrong" | "cleared" | "boss_cleared" | "dead";

interface RoomData {
  room_id: string;
  zone_number: number;
  room_number: number;
  is_boss: boolean;
  is_mini_boss: boolean;
  challenge_type: string;
  title: string;
  question_prompt: string;
  concept_tags: string[];
  difficulty: number;
  payload: Record<string, unknown>;
  is_cleared: boolean;
}

const ROOMS_PER_ZONE = 15;

interface AttemptResult {
  correct: boolean;
  explanation: string;
  xp_earned: number;
  new_total_xp: number;
  new_level: number | null;
  combo: number;
  hint_scroll: string | null;
  badge_unlocked: BadgeOut | null;
  room_cleared: boolean;
  zone_cleared: boolean;
}

export default function RoomPage() {
  const { roomId } = useParams<{ roomId: string }>();
  const navigate = useNavigate();
  const { hp, combo, loseHp, incrementCombo, resetCombo, resetHp, setStartTime, getElapsedMs } = useGameStore();
  const { updatePlayer } = useAuthStore();
  const { setContext: setMiloContext, clearMessages: clearMilo, addMessage: addMiloMessage } = useMiloStore();

  const [phase, setPhase] = useState<Phase>("loading");
  const [room, setRoom] = useState<RoomData | null>(null);
  const [lastResult, setLastResult] = useState<AttemptResult | null>(null);
  const [answering, setAnswering] = useState(false);
  const [showBossIntro, setShowBossIntro] = useState(false);
  const [miloCollapsed, setMiloCollapsed] = useState(false);

  const isBoss = room?.is_boss ?? false;
  const isMiniBoss = room?.is_mini_boss ?? false;

  useEffect(() => {
    initAudio();
    if (!roomId) return;
    setPhase("loading");
    setRoom(null);
    setLastResult(null);
    setShowBossIntro(false);
    resetHp(); resetCombo(); setAnswering(false);
    getRoom(roomId).then((r: RoomData) => {
      setRoom(r);
      clearMilo();
      setMiloContext({
        roomId: r.room_id,
        title: r.title,
        challengeType: r.challenge_type,
        conceptTags: r.concept_tags,
        difficulty: r.difficulty,
        questionPrompt: r.question_prompt,
      });
      if ((r.is_boss || r.is_mini_boss) && !sessionStorage.getItem(`boss_intro_${roomId}`)) {
        setShowBossIntro(true);
        sounds.bossEnter();
        setTimeout(() => {
          setShowBossIntro(false);
          sessionStorage.setItem(`boss_intro_${roomId}`, "1");
          setPhase("playing");
          setStartTime();
        }, 2200);
      } else {
        setPhase("playing");
        setStartTime();
      }
    }).catch(() => navigate("/map"));
  }, [roomId]);

  const handleAnswer = useCallback(async (answer: unknown) => {
    if (!roomId || answering || phase !== "playing") return;
    setAnswering(true);
    sounds.click();
    const timeMs = getElapsedMs();

    try {
      const result: AttemptResult = await submitAttempt(roomId, answer, combo, timeMs);
      setLastResult(result);

      // Notify Milo of the result
      if (result.correct) {
        addMiloMessage({ role: "milo", text: result.room_cleared
          ? "Bravo, salle liberee ! Tu veux que je t'explique le concept en detail avant de passer a la suite ?"
          : "Bien joue ! N'hesite pas a me demander pourquoi cette reponse est correcte."
        });
      } else {
        addMiloMessage({ role: "milo", text: "Pas tout a fait... Dis-moi comment tu as raisonne et je t'aide a trouver l'erreur." });
      }

      if (result.correct) {
        if (result.room_cleared) {
          // First time clearing — award combo, XP, navigate
          incrementCombo();
          updatePlayer({
            xp: result.new_total_xp,
            ...(result.new_level ? { level: result.new_level } : {}),
            ...(result.zone_cleared && room ? { current_zone: room.zone_number + 1 } : {}),
          });
          if (isBoss || isMiniBoss) setPhase("boss_cleared");
          else setPhase("cleared");
        } else if (room?.is_cleared) {
          // Replay — already cleared, just navigate to next
          navigateToNext();
          return;
        } else {
          // Correct but room not yet cleared (shouldn't happen with 1-attempt rooms, but safe)
          incrementCombo();
          setPhase("correct");
        }
      } else {
        resetCombo(); loseHp();
        setPhase(hp <= 1 ? "dead" : "wrong");
      }
      setStartTime();
    } catch { setAnswering(false); }
  }, [roomId, answering, phase, combo, hp, isBoss, isMiniBoss, room]);

  const navigateToNext = () => {
    if (!roomId) return;
    const parts = roomId.match(/z(\d+)_r(\d+)/);
    if (!parts) { navigate("/map"); return; }
    const z = Number(parts[1]), r = Number(parts[2]);
    if (r < ROOMS_PER_ZONE) {
      navigate(`/room/z${String(z).padStart(2, "0")}_r${String(r + 1).padStart(2, "0")}`);
    } else {
      navigate(`/zone/${z}`);
    }
  };

  const handleNext = () => {
    if (phase === "correct" || phase === "wrong") {
      setPhase("playing"); setAnswering(false);
    } else if (phase === "cleared") {
      navigateToNext();
    } else if (phase === "boss_cleared") {
      if (isBoss) navigate("/map");
      else navigateToNext();
    }
  };

  const handleExit = () => {
    const parts = roomId?.match(/z(\d+)/);
    navigate(parts ? `/zone/${Number(parts[1])}` : "/map");
  };

  const feedbackPhase = ["playing", "loading"].includes(phase) ? "idle" : phase as FeedbackPhase;

  return (
    <div className="min-h-screen pt-14" style={{ background: "#080810" }}>
      {/* Boss intro overlay */}
      <AnimatePresence>
        {showBossIntro && (
          <motion.div
            initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 flex flex-col items-center justify-center"
            style={{ background: "rgba(8,8,16,0.95)", backdropFilter: "blur(4px)" }}
          >
            <motion.div initial={{ scale: 0.5, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} transition={{ type: "spring", stiffness: 200, damping: 15, delay: 0.2 }} className="text-6xl sm:text-8xl mb-4 sm:mb-6 flicker">
              💀
            </motion.div>
            <motion.h2
              initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.6 }}
              className="text-2xl sm:text-3xl font-bold font-mono tracking-widest"
              style={{ color: room?.is_boss ? "#ff3355" : "#ffb800", textShadow: `0 0 30px ${room?.is_boss ? "rgba(255,51,85,0.5)" : "rgba(255,184,0,0.5)"}` }}
            >
              {room?.is_boss ? "BOSS" : "MINI-BOSS"}
            </motion.h2>
            <motion.p initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 1.0 }} className="text-base mt-2 font-semibold" style={{ color: "#ffffff80" }}>
              {room?.title}
            </motion.p>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Main split layout */}
      <div className="flex flex-col lg:flex-row h-[calc(100vh-56px)]">
        {/* Left: Challenge area */}
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: phase === "loading" ? 0 : 1, y: phase === "loading" ? 12 : 0 }}
          transition={{ duration: 0.35 }}
          className="flex-1 overflow-y-auto px-4 py-4 lg:px-6"
        >
          <div className="max-w-2xl mx-auto space-y-4">
            {/* Room header */}
            <div className="rounded-2xl p-4" style={{
              background: "#0f0f1a",
              border: `1px solid ${isBoss ? "rgba(255,51,85,0.2)" : isMiniBoss ? "rgba(255,184,0,0.15)" : "#1e1e35"}`,
              boxShadow: isBoss ? "0 0 30px rgba(255,51,85,0.06)" : isMiniBoss ? "0 0 20px rgba(255,184,0,0.04)" : "none",
            }}>
              <div className="flex items-start justify-between gap-3">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-1 flex-wrap">
                    {isBoss && (
                      <span className="text-xs font-mono px-2 py-0.5 rounded-md font-bold" style={{ background: "rgba(255,51,85,0.1)", color: "#ff3355", border: "1px solid rgba(255,51,85,0.2)" }}>BOSS</span>
                    )}
                    {isMiniBoss && (
                      <span className="text-xs font-mono px-2 py-0.5 rounded-md font-bold" style={{ background: "rgba(255,184,0,0.1)", color: "#ffb800", border: "1px solid rgba(255,184,0,0.2)" }}>MINI-BOSS</span>
                    )}
                    {room?.is_cleared && (
                      <span className="text-xs font-mono px-2 py-0.5 rounded-md" style={{ background: "rgba(0,255,136,0.08)", color: "#00ff88", border: "1px solid rgba(0,255,136,0.2)" }}>✓</span>
                    )}
                    <h1 className="font-bold text-base text-white">{room?.title}</h1>
                  </div>
                  <p className="text-sm" style={{ color: "#6a6a8a" }}>{room?.question_prompt}</p>
                </div>
                <div className="flex items-center gap-3 shrink-0">
                  {/* Difficulty dots */}
                  <div className="flex gap-0.5">
                    {[1,2,3,4,5].map(d => (
                      <div key={d} className="w-1.5 h-1.5 rounded-full" style={{ background: d <= (room?.difficulty || 0) ? "#ffb800" : "#1e1e35" }} />
                    ))}
                  </div>
                  {/* HP */}
                  <div className="flex gap-1">
                    {[1, 2, 3].map((i) => (
                      <span key={i} style={{ fontSize: "13px", color: i <= hp ? "#ff3355" : "transparent", textShadow: i <= hp ? "0 0 6px rgba(255,51,85,0.4)" : "none", WebkitTextStroke: i > hp ? "1px #3a3a5c" : "none", transition: "all 0.3s" }}>♥</span>
                    ))}
                  </div>
                </div>
              </div>
              <div className="flex flex-wrap gap-1.5 mt-3">
                {room?.concept_tags.map((tag) => (
                  <span key={tag} className="text-xs px-2 py-0.5 rounded-lg font-mono" style={{ background: "#161625", color: "#3a3a5c", border: "1px solid #1e1e35" }}>{tag}</span>
                ))}
              </div>
            </div>

            {/* Challenge */}
            <div className="challenge-area rounded-2xl p-3 sm:p-5" style={{ background: "#0f0f1a", border: "1px solid #1e1e35" }}>
              {phase !== "loading" && room && (
                <ChallengeRouter
                  key={roomId}
                  challengeType={room.challenge_type}
                  payload={room.payload}
                  onAnswer={handleAnswer}
                  disabled={phase !== "playing" || answering}
                />
              )}
            </div>

            <button onClick={handleExit} className="text-xs py-2 px-1 transition-colors duration-200" style={{ color: "#3a3a5c" }}
              onMouseEnter={(e) => (e.currentTarget.style.color = "#6a6a8a")}
              onMouseLeave={(e) => (e.currentTarget.style.color = "#3a3a5c")}
            >
              ← Retour
            </button>

            {/* Mobile: Milo toggle */}
            <button
              onClick={() => setMiloCollapsed(!miloCollapsed)}
              className="lg:hidden w-full rounded-2xl p-3 flex items-center gap-3 transition-all duration-200"
              style={{ background: "#0f0f1a", border: "1px solid rgba(0,255,136,0.15)" }}
            >
              <motion.div
                animate={{ y: [0, -2, 0] }}
                transition={{ duration: 2, repeat: Infinity }}
                className="w-8 h-8 rounded-full flex items-center justify-center shrink-0"
                style={{ background: "radial-gradient(circle at 35% 35%, #00ffaa, #00cc66, #008844)", boxShadow: "0 0 10px rgba(0,255,136,0.3)" }}
              >
                <span className="text-xs">✦</span>
              </motion.div>
              <span className="text-sm font-medium" style={{ color: "#00ff88" }}>
                {miloCollapsed ? "Parler a Milo" : "Masquer Milo"}
              </span>
              <span className="ml-auto text-xs" style={{ color: "#3a3a5c" }}>{miloCollapsed ? "▼" : "▲"}</span>
            </button>

            {/* Mobile: Milo inline */}
            {!miloCollapsed && (
              <div className="lg:hidden rounded-2xl overflow-hidden" style={{ background: "#0b0b18", border: "1px solid rgba(0,255,136,0.15)", height: "min(400px, 60vh)" }}>
                <MiloChat embedded />
              </div>
            )}

            <div className="h-4" />
          </div>
        </motion.div>

        {/* Right: Milo panel (desktop only) */}
        <div className="hidden lg:flex flex-col shrink-0" style={{ width: 380, borderLeft: "1px solid #1e1e35", background: "#0a0a16" }}>
          <MiloChat embedded />
        </div>
      </div>

      <FeedbackOverlay
        phase={feedbackPhase}
        xpEarned={lastResult?.xp_earned}
        combo={lastResult?.combo}
        newLevel={lastResult?.new_level}
        explanation={lastResult?.explanation}
        hintScroll={lastResult?.hint_scroll}
        badge={lastResult?.badge_unlocked}
        onNext={handleNext}
        onRetry={() => { resetHp(); resetCombo(); setAnswering(false); setPhase("playing"); setStartTime(); }}
        onExit={handleExit}
      />
    </div>
  );
}
