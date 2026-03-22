import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import type { Variants } from "framer-motion";
import { useAuthStore } from "../store";
import { getMe, getMyBadges, getShareUrl } from "../api";

const ICON_MAP: Record<string, string> = {
  boot:"👟",house:"🏠",sword:"⚔️",gear:"⚙️",shield:"🛡️",arrow:"🏹",
  wand:"🪄",crown:"👑",scroll:"📜",trophy:"🏆",star:"⭐",lightning:"⚡",
  clock:"⏱️",bug:"🐛",fire_1:"🔥",fire_2:"🔥🔥",fire_3:"🔥🔥🔥",
  calendar_3:"📅",calendar_7:"🗓️",eye:"👁️",
};

const CAT_LABELS: Record<string, string> = {
  progress:"Progression", skill:"Compétence", streak:"Séries", explorer:"Exploration",
};

interface Badge {
  id: string; name: string; description: string; icon_key: string;
  category: string; secret: boolean; earned: boolean; earned_at: string | null;
}

function xpForLevel(l: number) { return 100 * l + 25 * l * (l - 1); }

const container: Variants = { hidden: {}, visible: { transition: { staggerChildren: 0.05 } } };
const item: Variants = { hidden: { opacity: 0, y: 12 }, visible: { opacity: 1, y: 0, transition: { type: "spring", stiffness: 300, damping: 24 } } };

export default function ProfilePage() {
  const { player, setAuth, token } = useAuthStore();
  const [badges, setBadges] = useState<Badge[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([getMe(), getMyBadges()]).then(([me, bgs]) => {
      if (token) setAuth(token, me);
      setBadges(bgs);
    }).finally(() => setLoading(false));
  }, []);

  const handleShare = () => {
    const url = getShareUrl();
    const a = document.createElement("a");
    a.href = url + `?t=${Date.now()}`;
    a.download = `cdungeon_${player?.username}.png`;
    a.click();
  };

  if (!player || loading) return (
    <div className="min-h-screen flex items-center justify-center">
      <motion.div animate={{ opacity: [0.3, 1, 0.3] }} transition={{ duration: 1.5, repeat: Infinity }}>
        <p className="text-sm font-mono" style={{ color: "#00ff88" }}>Chargement…</p>
      </motion.div>
    </div>
  );

  const acc = player.total_attempts > 0
    ? Math.round((player.total_correct / player.total_attempts) * 100) : 0;
  const earnedBadges = badges.filter((b) => b.earned);
  const categories = [...new Set(badges.map((b) => b.category))];

  const level = player.level;
  const xp = player.xp;
  const xpCur = xpForLevel(level);
  const xpNext = xpForLevel(level + 1);
  const progress = Math.min((xp - xpCur) / Math.max(xpNext - xpCur, 1), 1);

  const stats = [
    { label: "Tentatives", value: player.total_attempts, icon: "🎯" },
    { label: "Précision", value: `${acc}%`, icon: "🏹" },
    { label: "Meilleur combo", value: `×${player.best_combo}`, icon: "🔥" },
    { label: "Streak", value: `${player.daily_streak}j`, icon: "📅" },
  ];

  return (
    <div className="min-h-screen pt-16 pb-8 px-4" style={{ background: "#080810" }}>
      <div className="max-w-xl mx-auto space-y-4">

        {/* Player card */}
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.35 }}
          className="rounded-2xl p-5"
          style={{ background: "#0f0f1a", border: "1px solid #1e1e35" }}
        >
          <div className="flex items-start justify-between gap-4">
            <div>
              <h1 className="text-xl font-bold text-white">{player.username}</h1>
              <p className="text-xs mt-0.5" style={{ color: "#6a6a8a" }}>
                Niveau {level} · Zone {player.current_zone}/8
              </p>
            </div>
            <button
              onClick={handleShare}
              className="text-xs px-3 py-2.5 sm:py-1.5 rounded-xl transition-all duration-200 font-medium"
              style={{ background: "rgba(0,255,136,0.08)", color: "#00ff88", border: "1px solid rgba(0,255,136,0.15)" }}
              onMouseEnter={(e) => (e.currentTarget.style.background = "rgba(0,255,136,0.14)")}
              onMouseLeave={(e) => (e.currentTarget.style.background = "rgba(0,255,136,0.08)")}
            >
              📤 Share
            </button>
          </div>

          {/* XP bar */}
          <div className="mt-4 space-y-1.5">
            <div className="flex justify-between text-xs">
              <span style={{ color: "#6a6a8a" }}>Niveau {level}</span>
              <span className="font-mono" style={{ color: "#00ff88" }}>{xp} XP</span>
            </div>
            <div className="h-1.5 rounded-full overflow-hidden" style={{ background: "#1e1e35" }}>
              <motion.div
                className="h-full rounded-full"
                style={{ background: "linear-gradient(90deg, #00cc66, #00ff88)", boxShadow: "0 0 6px rgba(0,255,136,0.4)" }}
                initial={{ width: 0 }}
                animate={{ width: `${progress * 100}%` }}
                transition={{ duration: 1, ease: "easeOut", delay: 0.3 }}
              />
            </div>
            <p className="text-xs text-right" style={{ color: "#3a3a5c" }}>
              {xpNext - xp} XP jusqu'au niveau {level + 1}
            </p>
          </div>
        </motion.div>

        {/* Stats grid */}
        <motion.div
          variants={container}
          initial="hidden"
          animate="visible"
          className="grid grid-cols-2 xs:grid-cols-4 gap-2"
        >
          {stats.map((s) => (
            <motion.div
              key={s.label}
              variants={item}
              className="rounded-2xl p-3 text-center"
              style={{ background: "#0f0f1a", border: "1px solid #1e1e35" }}
            >
              <div className="text-xl mb-1">{s.icon}</div>
              <div className="font-bold text-sm text-white">{s.value}</div>
              <div className="text-xs mt-0.5" style={{ color: "#3a3a5c" }}>{s.label}</div>
            </motion.div>
          ))}
        </motion.div>

        {/* Badges */}
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.35, delay: 0.2 }}
          className="rounded-2xl p-5"
          style={{ background: "#0f0f1a", border: "1px solid #1e1e35" }}
        >
          <div className="flex items-center justify-between mb-4">
            <h2 className="font-bold text-sm text-white">Badges</h2>
            <span className="text-xs font-mono px-2 py-0.5 rounded-lg" style={{ background: "rgba(0,255,136,0.08)", color: "#00ff88", border: "1px solid rgba(0,255,136,0.15)" }}>
              {earnedBadges.length}/{badges.length}
            </span>
          </div>

          <div className="space-y-5">
            {categories.map((cat) => {
              const catBadges = badges.filter((b) => b.category === cat);
              return (
                <div key={cat}>
                  <p className="text-xs font-mono mb-2" style={{ color: "#3a3a5c" }}>
                    {CAT_LABELS[cat] || cat}
                  </p>
                  <div className="grid grid-cols-3 xs:grid-cols-4 gap-2">
                    {catBadges.map((b) => (
                      <motion.div
                        key={b.id}
                        whileHover={b.earned ? { scale: 1.05 } : {}}
                        title={`${b.name}: ${b.description}`}
                        className="rounded-xl p-2 text-center"
                        style={{
                          background: b.earned ? "rgba(0,255,136,0.05)" : "#0a0a14",
                          border: `1px solid ${b.earned ? "rgba(0,255,136,0.2)" : "#161625"}`,
                          opacity: b.earned ? 1 : 0.35,
                          cursor: b.earned ? "default" : "default",
                        }}
                      >
                        <div className="text-xl mb-1">{ICON_MAP[b.icon_key] || "🏅"}</div>
                        <p className="text-xs leading-tight" style={{ color: b.earned ? "#6a6a8a" : "#3a3a5c" }}>
                          {b.name}
                        </p>
                      </motion.div>
                    ))}
                  </div>
                </div>
              );
            })}
          </div>
        </motion.div>
      </div>
    </div>
  );
}
