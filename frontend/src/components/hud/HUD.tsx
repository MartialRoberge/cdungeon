import { motion, AnimatePresence } from "framer-motion";
import { Link, useLocation } from "react-router-dom";
import { useGameStore, useAuthStore } from "../../store";
import { useEffect, useState } from "react";

function xpForLevel(l: number) { return 100 * l + 25 * l * (l - 1); }

export default function HUD() {
  const { hp, combo } = useGameStore();
  const { player } = useAuthStore();
  const location = useLocation();
  const [prevHp, setPrevHp] = useState(hp);
  const [hpPop, setHpPop] = useState(false);

  useEffect(() => {
    if (hp < prevHp) { setHpPop(true); setTimeout(() => setHpPop(false), 400); }
    setPrevHp(hp);
  }, [hp]);

  if (!player) return null;

  const level = player.level;
  const xp = player.xp;
  const xpCur = xpForLevel(level);
  const xpNext = xpForLevel(level + 1);
  const progress = Math.min((xp - xpCur) / Math.max(xpNext - xpCur, 1), 1);

  const navItems = [
    { to: "/map", label: "Carte" },
    { to: "/profile", label: "Profil" },
    { to: "/leaderboard", label: "Top" },
  ];

  return (
    <motion.div
      initial={{ y: -60, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.4, ease: "easeOut" }}
      className="fixed top-0 left-0 right-0 z-50 flex items-center gap-2 sm:gap-4 px-3 sm:px-5 py-3"
      style={{
        background: "rgba(8,8,16,0.85)",
        backdropFilter: "blur(20px)",
        borderBottom: "1px solid rgba(255,255,255,0.04)",
      }}
    >
      {/* Logo */}
      <Link to="/map" className="font-mono text-xs sm:text-sm font-bold tracking-widest shrink-0" style={{ color: "#00ff88", textShadow: "0 0 12px rgba(0,255,136,0.3)" }}>
        C:\D
        <span className="hidden sm:inline">UNGEON</span>
      </Link>

      {/* Divider */}
      <div className="w-px h-4 bg-dg-border hidden sm:block" />

      {/* HP */}
      <div className="flex items-center gap-1 sm:gap-1.5">
        {[1, 2, 3].map((i) => (
          <motion.span
            key={i}
            animate={hpPop && i === hp + 1 ? { scale: [1, 1.4, 0.6, 1] } : {}}
            transition={{ duration: 0.3 }}
            style={{ fontSize: "14px", transition: "opacity 0.2s, filter 0.2s" }}
          >
            <span style={{
              display: "inline-block",
              color: i <= hp ? "#ff3355" : "transparent",
              textShadow: i <= hp ? "0 0 8px rgba(255,51,85,0.5)" : "none",
              WebkitTextStroke: i > hp ? "1px #3a3a5c" : "none",
              transition: "all 0.3s",
            }}>♥</span>
          </motion.span>
        ))}
      </div>

      {/* Combo */}
      <AnimatePresence>
        {combo > 1 && (
          <motion.div
            key={combo}
            initial={{ scale: 0.6, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.8, opacity: 0 }}
            transition={{ type: "spring", stiffness: 500, damping: 20 }}
            className={`flex items-center gap-1 px-2 py-0.5 rounded-lg text-xs font-bold font-mono ${
              combo >= 10 ? "combo-glow-10" : combo >= 5 ? "combo-glow-5" : ""
            }`}
            style={{
              background: combo >= 10 ? "rgba(255,51,85,0.12)" : combo >= 5 ? "rgba(255,184,0,0.1)" : "rgba(0,255,136,0.08)",
              border: `1px solid ${combo >= 10 ? "rgba(255,51,85,0.3)" : combo >= 5 ? "rgba(255,184,0,0.25)" : "rgba(0,255,136,0.2)"}`,
              color: combo >= 10 ? "#ff3355" : combo >= 5 ? "#ffb800" : "#00ff88",
            }}
          >
            {combo >= 10 ? "🔥" : "⚡"} ×{combo}
          </motion.div>
        )}
      </AnimatePresence>

      {/* XP bar — hidden on very small screens, compact on mobile */}
      <div className="hidden xs:flex flex-1 max-w-24 sm:max-w-40 flex-col">
        <div className="flex justify-between items-center mb-1">
          <span className="text-xs text-dg-muted font-medium">Niv.{level}</span>
          <span className="text-xs font-mono hidden sm:inline" style={{ color: "#00ff88" }}>{xp} XP</span>
        </div>
        <div className="h-1 rounded-full overflow-hidden" style={{ background: "#1e1e35" }}>
          <motion.div
            className="h-full rounded-full"
            style={{ background: "linear-gradient(90deg, #00cc66, #00ff88)", boxShadow: "0 0 6px rgba(0,255,136,0.4)" }}
            animate={{ width: `${progress * 100}%` }}
            transition={{ duration: 0.8, ease: "easeOut" }}
          />
        </div>
      </div>

      {/* Nav */}
      <nav className="flex gap-0.5 sm:gap-1 ml-auto">
        {navItems.map(({ to, label }) => (
          <Link
            key={to}
            to={to}
            className="text-xs px-2.5 py-2 sm:px-3 sm:py-1.5 rounded-lg transition-all duration-200 font-medium min-w-[44px] text-center"
            style={{
              color: location.pathname === to ? "#00ff88" : "#3a3a5c",
              background: location.pathname === to ? "rgba(0,255,136,0.08)" : "transparent",
            }}
          >
            {label}
          </Link>
        ))}
      </nav>

      {/* User — hidden on mobile */}
      <div className="text-xs font-medium text-dg-muted hidden md:block">{player.username}</div>
    </motion.div>
  );
}
