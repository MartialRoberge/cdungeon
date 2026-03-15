import { useEffect, useState, useCallback } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import { getRoom, submitAttempt } from "../api";
import { useGameStore, useAuthStore } from "../store";
import type { BadgeOut } from "../types";
import ChallengeRouter from "../components/challenges/ChallengeRouter";
import FeedbackOverlay from "../components/feedback/FeedbackOverlay";
import { sounds, initAudio } from "../utils/sound";

type Phase = "loading" | "playing" | "correct" | "wrong" | "cleared" | "boss_cleared" | "dead";
type FeedbackPhase = "idle" | "correct" | "wrong" | "cleared" | "boss_cleared" | "dead";

interface RoomData {
  room_id: string;
  zone_number: number;
  room_number: number;
  is_boss: boolean;
  challenge_type: string;
  title: string;
  question_prompt: string;
  concept_tags: string[];
  difficulty: number;
  payload: Record<string, unknown>;
  is_cleared: boolean;
}

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

  const [phase, setPhase] = useState<Phase>("loading");
  const [room, setRoom] = useState<RoomData | null>(null);
  const [lastResult, setLastResult] = useState<AttemptResult | null>(null);
  const [answering, setAnswering] = useState(false);
  const [showBossIntro, setShowBossIntro] = useState(false);

  const isBoss = room?.is_boss ?? false;

  useEffect(() => {
    initAudio();
    if (!roomId) return;
    resetHp(); resetCombo(); setAnswering(false);
    getRoom(roomId).then((r: RoomData) => {
      setRoom(r);
      if (r.is_boss && !sessionStorage.getItem(`boss_intro_${roomId}`)) {
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

      if (result.correct) {
        incrementCombo();
        updatePlayer({
          xp: result.new_total_xp,
          ...(result.new_level ? { level: result.new_level } : {}),
          ...(result.zone_cleared && room ? { current_zone: room.zone_number + 1 } : {}),
        });
        if (isBoss && result.room_cleared) setPhase("boss_cleared");
        else if (result.room_cleared) setPhase("cleared");
        else setPhase("correct");
      } else {
        resetCombo(); loseHp();
        setPhase(hp <= 1 ? "dead" : "wrong");
      }
      setStartTime();
    } catch { setAnswering(false); }
  }, [roomId, answering, phase, combo, hp, isBoss, room]);

  const handleNext = () => {
    if (phase === "correct" || phase === "wrong") {
      setPhase("playing"); setAnswering(false);
    } else if (phase === "cleared") {
      if (!roomId) return;
      const parts = roomId.match(/z(\d+)_r(\d+)/);
      if (parts) {
        const z = Number(parts[1]), r = Number(parts[2]);
        if (r < 6) navigate(`/room/z${String(z).padStart(2, "0")}_r${String(r + 1).padStart(2, "0")}`);
        else navigate(`/zone/${z}`);
      }
    } else if (phase === "boss_cleared") navigate("/map");
  };

  const handleExit = () => {
    const parts = roomId?.match(/z(\d+)/);
    navigate(parts ? `/zone/${Number(parts[1])}` : "/map");
  };

  const feedbackPhase = ["playing", "loading"].includes(phase) ? "idle" : phase as FeedbackPhase;

  return (
    <div className="min-h-screen pt-16 pb-8 px-4" style={{ background: "#080810" }}>
      {/* Boss intro overlay */}
      <AnimatePresence>
        {showBossIntro && (
          <motion.div
            initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 flex flex-col items-center justify-center"
            style={{ background: "rgba(8,8,16,0.95)", backdropFilter: "blur(4px)" }}
          >
            <motion.div
              initial={{ scale: 0.5, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{ type: "spring", stiffness: 200, damping: 15, delay: 0.2 }}
              className="text-8xl mb-6 flicker"
            >
              💀
            </motion.div>
            <motion.h2
              initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.6 }}
              className="text-3xl font-bold font-mono tracking-widest"
              style={{ color: "#ff3355", textShadow: "0 0 30px rgba(255,51,85,0.5)" }}
            >
              BOSS
            </motion.h2>
            <motion.p
              initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 1.0 }}
              className="text-base mt-2 font-semibold" style={{ color: "#ffffff80" }}
            >
              {room?.title}
            </motion.p>
          </motion.div>
        )}
      </AnimatePresence>

      <motion.div
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: phase === "loading" ? 0 : 1, y: phase === "loading" ? 12 : 0 }}
        transition={{ duration: 0.35 }}
        className="max-w-xl mx-auto space-y-4"
      >
        {/* Room header */}
        <div className="rounded-2xl p-4" style={{
          background: "#0f0f1a",
          border: `1px solid ${isBoss ? "rgba(255,51,85,0.2)" : "#1e1e35"}`,
          boxShadow: isBoss ? "0 0 30px rgba(255,51,85,0.06)" : "none",
        }}>
          <div className="flex items-start justify-between gap-3">
            <div className="flex-1">
              <div className="flex items-center gap-2 mb-1">
                {isBoss && (
                  <span className="text-xs font-mono px-2 py-0.5 rounded-md font-bold" style={{ background: "rgba(255,51,85,0.1)", color: "#ff3355", border: "1px solid rgba(255,51,85,0.2)" }}>
                    BOSS
                  </span>
                )}
                {room?.is_cleared && (
                  <span className="text-xs font-mono px-2 py-0.5 rounded-md" style={{ background: "rgba(0,255,136,0.08)", color: "#00ff88", border: "1px solid rgba(0,255,136,0.2)" }}>
                    ✓ complété
                  </span>
                )}
                <h1 className="font-bold text-base text-white">{room?.title}</h1>
              </div>
              <p className="text-sm" style={{ color: "#6a6a8a" }}>{room?.question_prompt}</p>
            </div>
            <div className="flex gap-1.5 shrink-0">
              {[1, 2, 3].map((i) => (
                <span key={i} style={{ fontSize: "13px", color: i <= hp ? "#ff3355" : "transparent", textShadow: i <= hp ? "0 0 6px rgba(255,51,85,0.4)" : "none", WebkitTextStroke: i > hp ? "1px #3a3a5c" : "none", transition: "all 0.3s" }}>♥</span>
              ))}
            </div>
          </div>

          <div className="flex flex-wrap gap-1.5 mt-3">
            {room?.concept_tags.map((tag) => (
              <span key={tag} className="text-xs px-2 py-0.5 rounded-lg font-mono" style={{ background: "#161625", color: "#3a3a5c", border: "1px solid #1e1e35" }}>
                {tag}
              </span>
            ))}
          </div>
        </div>

        {/* Challenge area */}
        <div className="challenge-area rounded-2xl p-5" style={{ background: "#0f0f1a", border: "1px solid #1e1e35" }}>
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

        <button onClick={handleExit} className="text-xs transition-colors duration-200" style={{ color: "#3a3a5c" }}
          onMouseEnter={(e) => (e.currentTarget.style.color = "#6a6a8a")}
          onMouseLeave={(e) => (e.currentTarget.style.color = "#3a3a5c")}
        >
          ← Retour
        </button>
      </motion.div>

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
