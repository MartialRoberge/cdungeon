import { motion, AnimatePresence } from "framer-motion";
import type { Variants } from "framer-motion";
import { useEffect } from "react";
import type { BadgeOut } from "../../types";
import { sounds } from "../../utils/sound";
import { burstParticles, shakeScreen } from "../../utils/particles";

type FeedbackPhase = "idle" | "correct" | "wrong" | "cleared" | "boss_cleared" | "dead";

interface Props {
  phase: FeedbackPhase;
  xpEarned?: number;
  combo?: number;
  newLevel?: number | null;
  explanation?: string;
  hintScroll?: string | null;
  badge?: BadgeOut | null;
  zoneName?: string;
  onNext: () => void;
  onRetry: () => void;
  onExit: () => void;
}

const ICON_MAP: Record<string, string> = {
  boot:"👟",house:"🏠",sword:"⚔️",gear:"⚙️",shield:"🛡️",arrow:"🏹",
  wand:"🪄",crown:"👑",scroll:"📜",trophy:"🏆",star:"⭐",lightning:"⚡",
  clock:"⏱️",bug:"🐛",fire_1:"🔥",fire_2:"🔥🔥",fire_3:"🔥🔥🔥",
  calendar_3:"📅",calendar_7:"🗓️",eye:"👁️",
};

const overlay: Variants = { hidden: { opacity: 0 }, visible: { opacity: 1 }, exit: { opacity: 0 } };
const card: Variants = {
  hidden: { opacity: 0, scale: 0.9, y: 20 },
  visible: { opacity: 1, scale: 1, y: 0, transition: { type: "spring", stiffness: 400, damping: 28 } },
  exit: { opacity: 0, scale: 0.95, y: 10, transition: { duration: 0.15 } },
};

export default function FeedbackOverlay({ phase, xpEarned, combo, newLevel, explanation, hintScroll, badge, zoneName, onNext, onRetry, onExit }: Props) {
  useEffect(() => {
    if (phase === "correct") {
      sounds.correct();
      if (newLevel) setTimeout(() => sounds.levelUp(), 300);
      if (badge) setTimeout(() => sounds.badge(), 500);
      // Burst from center of screen
      const el = document.querySelector(".challenge-area");
      const rect = el?.getBoundingClientRect();
      burstParticles(
        rect ? rect.left + rect.width / 2 : window.innerWidth / 2,
        rect ? rect.top + rect.height / 2 : window.innerHeight / 2,
        "#00ff88", 28
      );
    } else if (phase === "wrong") {
      sounds.wrong();
      sounds.hpLost();
      shakeScreen(5, 300);
    } else if (phase === "cleared") {
      sounds.roomClear();
      burstParticles(window.innerWidth / 2, window.innerHeight / 2, "#00ff88", 40);
    } else if (phase === "boss_cleared") {
      sounds.bossDefeated();
      setTimeout(() => burstParticles(window.innerWidth / 2, window.innerHeight / 2, "#ffb800", 60), 100);
      setTimeout(() => burstParticles(window.innerWidth / 3, window.innerHeight / 2, "#ff3355", 40), 300);
      setTimeout(() => burstParticles((window.innerWidth * 2) / 3, window.innerHeight / 2, "#00ff88", 40), 500);
    } else if (phase === "dead") {
      shakeScreen(10, 600);
    }
  }, [phase]);

  return (
    <AnimatePresence>
      {phase !== "idle" && (
        <motion.div
          key={phase}
          variants={overlay}
          initial="hidden" animate="visible" exit="exit"
          transition={{ duration: 0.2 }}
          className="fixed inset-0 z-40 flex items-center justify-center p-4"
          style={{ background: "rgba(8,8,16,0.75)", backdropFilter: "blur(8px)" }}
        >
          <motion.div variants={card} initial="hidden" animate="visible" exit="exit" className="w-full max-w-sm">
            {phase === "correct" && <CorrectCard xpEarned={xpEarned} combo={combo} newLevel={newLevel} badge={badge} onNext={onNext} />}
            {phase === "wrong" && <WrongCard explanation={explanation} hint={hintScroll} onNext={onNext} />}
            {phase === "cleared" && <ClearedCard badge={badge} onNext={onNext} onExit={onExit} />}
            {phase === "boss_cleared" && <BossClearedCard zoneName={zoneName} badge={badge} onNext={onNext} onExit={onExit} />}
            {phase === "dead" && <DeadCard onRetry={onRetry} onExit={onExit} />}
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}

function CorrectCard({ xpEarned, combo, newLevel, badge, onNext }: { xpEarned?: number; combo?: number; newLevel?: number | null; badge?: BadgeOut | null; onNext: () => void }) {
  return (
    <div className="card-accent space-y-4 text-center">
      <motion.div initial={{ scale: 0 }} animate={{ scale: 1 }} transition={{ type: "spring", stiffness: 600, damping: 20, delay: 0.1 }} className="text-5xl">✓</motion.div>
      <div>
        <h2 className="font-bold text-xl text-white">Correct</h2>
        <div className="flex justify-center gap-3 mt-2">
          {xpEarned ? (
            <motion.span initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }} className="badge-pill-accent text-sm font-mono">
              +{xpEarned} XP
            </motion.span>
          ) : null}
          {combo && combo > 1 ? (
            <motion.span initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }} className="badge-pill-warn">
              ×{combo} combo
            </motion.span>
          ) : null}
        </div>
      </div>
      {newLevel && (
        <motion.div initial={{ opacity: 0, scale: 0.8 }} animate={{ opacity: 1, scale: 1 }} transition={{ delay: 0.35, type: "spring" }} className="rounded-xl p-3" style={{ background: "rgba(255,184,0,0.08)", border: "1px solid rgba(255,184,0,0.2)" }}>
          <p className="font-bold text-sm" style={{ color: "#ffb800" }}>⬆ NIVEAU {newLevel}</p>
        </motion.div>
      )}
      {badge && <BadgeCard badge={badge} delay={0.45} />}
      <button onClick={onNext} className="btn-accent w-full" style={{ marginTop: "8px" }}>Continuer</button>
    </div>
  );
}

function WrongCard({ explanation, hint, onNext }: { explanation?: string; hint?: string | null; onNext: () => void }) {
  return (
    <div className="card-danger space-y-4">
      <div className="text-center">
        <motion.div initial={{ scale: 0 }} animate={{ scale: 1 }} transition={{ type: "spring", stiffness: 500, damping: 22, delay: 0.05 }} className="text-4xl mb-2">✗</motion.div>
        <h2 className="font-bold text-lg" style={{ color: "#ff3355" }}>Raté</h2>
      </div>
      {explanation && (
        <div className="code-block text-xs leading-relaxed" style={{ color: "#a0a0c0" }}>
          <p className="label mb-2">Explication</p>
          {explanation}
        </div>
      )}
      {hint && (
        <div className="rounded-xl p-3" style={{ background: "rgba(255,184,0,0.06)", border: "1px solid rgba(255,184,0,0.15)" }}>
          <p className="label mb-1" style={{ color: "#ffb800" }}>💡 Conseil</p>
          <p className="text-xs" style={{ color: "#a0a0c0" }}>{hint}</p>
        </div>
      )}
      <button onClick={onNext} className="btn-danger w-full">Réessayer</button>
    </div>
  );
}

function ClearedCard({ badge, onNext, onExit }: { badge?: BadgeOut | null; onNext: () => void; onExit: () => void }) {
  return (
    <div className="card-accent space-y-4 text-center">
      <motion.div initial={{ rotate: -10, scale: 0 }} animate={{ rotate: 0, scale: 1 }} transition={{ type: "spring", stiffness: 400, damping: 18 }} className="text-5xl">🎉</motion.div>
      <h2 className="font-bold text-xl text-white">Salle libérée</h2>
      {badge && <BadgeCard badge={badge} delay={0.3} />}
      <button onClick={onNext} className="btn-accent w-full">Salle suivante</button>
      <button onClick={onExit} className="btn-ghost w-full text-sm">Retour à la zone</button>
    </div>
  );
}

function BossClearedCard({ zoneName, badge, onNext, onExit }: { zoneName?: string; badge?: BadgeOut | null; onNext: () => void; onExit: () => void }) {
  return (
    <div className="space-y-4 text-center rounded-2xl p-6" style={{ background: "#0f0f1a", border: "1px solid rgba(255,184,0,0.3)", boxShadow: "0 0 60px rgba(255,184,0,0.1)" }}>
      <motion.div initial={{ scale: 0, rotate: -15 }} animate={{ scale: 1, rotate: 0 }} transition={{ type: "spring", stiffness: 300, damping: 15, delay: 0.1 }} className="text-6xl">🏆</motion.div>
      <div>
        <h2 className="font-bold text-2xl text-white">Boss vaincu</h2>
        {zoneName && <p className="text-sm mt-1" style={{ color: "#ffb800" }}>{zoneName} — terminée</p>}
      </div>
      {badge && <BadgeCard badge={badge} delay={0.4} />}
      <button onClick={onNext} className="btn-accent w-full text-base py-3">Zone suivante →</button>
      <button onClick={onExit} className="btn-ghost w-full text-sm">Retour à la carte</button>
    </div>
  );
}

function DeadCard({ onRetry, onExit }: { onRetry: () => void; onExit: () => void }) {
  return (
    <div className="card-danger space-y-4 text-center">
      <motion.div animate={{ rotate: [0, -5, 5, -3, 3, 0] }} transition={{ duration: 0.5, delay: 0.1 }} className="text-6xl">💀</motion.div>
      <div>
        <h2 className="font-bold text-xl text-white">Game Over</h2>
        <p className="text-sm text-dg-muted mt-1">Tu n'as plus de vies.</p>
      </div>
      <button onClick={onRetry} className="btn-danger w-full">Recommencer</button>
      <button onClick={onExit} className="btn-ghost w-full text-sm">Quitter la salle</button>
    </div>
  );
}

function BadgeCard({ badge, delay = 0 }: { badge: BadgeOut; delay?: number }) {
  const icon = ICON_MAP[badge.icon_key] || "🏅";
  return (
    <motion.div
      initial={{ opacity: 0, y: 10, scale: 0.9 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      transition={{ delay, type: "spring", stiffness: 400, damping: 25 }}
      className="rounded-xl p-3 text-left"
      style={{ background: "rgba(255,184,0,0.07)", border: "1px solid rgba(255,184,0,0.2)" }}
    >
      <p className="label mb-1.5" style={{ color: "#ffb800" }}>Badge débloqué</p>
      <div className="flex items-center gap-3">
        <span className="text-2xl">{icon}</span>
        <div>
          <p className="font-bold text-sm text-white">{badge.name}</p>
          <p className="text-xs text-dg-muted">{badge.description}</p>
        </div>
      </div>
    </motion.div>
  );
}
