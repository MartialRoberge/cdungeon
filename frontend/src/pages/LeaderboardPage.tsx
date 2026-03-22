import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import type { Variants } from "framer-motion";
import { getLeaderboard } from "../api";
import { sounds } from "../utils/sound";

interface Row { rank: number; username: string; level: number; value: number; is_me: boolean; }

const container: Variants = { hidden: {}, visible: { transition: { staggerChildren: 0.04 } } };
const row: Variants = {
  hidden: { opacity: 0, x: -12 },
  visible: { opacity: 1, x: 0, transition: { type: "spring", stiffness: 300, damping: 26 } },
};

export default function LeaderboardPage() {
  const [rows, setRows] = useState<Row[]>([]);
  const [by, setBy] = useState<"xp" | "combo" | "streak">("xp");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setLoading(true);
    getLeaderboard(by).then(setRows).finally(() => setLoading(false));
  }, [by]);

  const tabs: { key: "xp" | "combo" | "streak"; label: string }[] = [
    { key: "xp", label: "XP Total" },
    { key: "combo", label: "Combo" },
    { key: "streak", label: "Streak" },
  ];

  const formatValue = (v: number) => {
    if (by === "combo") return `×${v}`;
    if (by === "streak") return `${v}j`;
    return `${v} XP`;
  };

  return (
    <div className="min-h-screen pt-16 pb-8 px-4" style={{ background: "#080810" }}>
      <div className="max-w-lg mx-auto space-y-4">

        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.35 }}
          className="text-center py-6"
        >
          <h1 className="text-2xl font-bold font-mono tracking-widest" style={{ color: "#00ff88" }}>CLASSEMENT</h1>
        </motion.div>

        {/* Tabs */}
        <div className="rounded-2xl p-1 flex gap-1" style={{ background: "#0f0f1a", border: "1px solid #1e1e35" }}>
          {tabs.map((t) => (
            <button
              key={t.key}
              onClick={() => { sounds.click(); setBy(t.key); }}
              className="flex-1 py-2.5 sm:py-2 text-xs font-semibold rounded-xl transition-all duration-200"
              style={{
                background: by === t.key ? "#00ff88" : "transparent",
                color: by === t.key ? "#080810" : "#3a3a5c",
              }}
            >
              {t.label}
            </button>
          ))}
        </div>

        {/* Rows */}
        <AnimatePresence mode="wait">
          {!loading && (
            <motion.div
              key={by}
              variants={container}
              initial="hidden"
              animate="visible"
              exit={{ opacity: 0 }}
              className="space-y-2"
            >
              {rows.map((r) => (
                <motion.div
                  key={r.username}
                  variants={row}
                  className="rounded-2xl p-4 flex items-center gap-4"
                  style={{
                    background: r.is_me ? "rgba(0,255,136,0.04)" : "#0f0f1a",
                    border: `1px solid ${r.is_me ? "rgba(0,255,136,0.2)" : "#1e1e35"}`,
                    boxShadow: r.is_me ? "0 0 20px rgba(0,255,136,0.05)" : "none",
                  }}
                >
                  {/* Rank */}
                  <div className="w-8 text-center shrink-0">
                    {r.rank <= 3 ? (
                      <span className="text-lg">{["🥇","🥈","🥉"][r.rank - 1]}</span>
                    ) : (
                      <span className="text-xs font-mono" style={{ color: "#3a3a5c" }}>#{r.rank}</span>
                    )}
                  </div>

                  {/* Info */}
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2">
                      <span className="font-semibold text-sm truncate" style={{ color: r.is_me ? "#00ff88" : "white" }}>
                        {r.username}
                      </span>
                      {r.is_me && (
                        <span className="text-xs px-1.5 py-0.5 rounded font-mono" style={{ background: "rgba(0,255,136,0.1)", color: "#00ff88", border: "1px solid rgba(0,255,136,0.2)" }}>
                          toi
                        </span>
                      )}
                    </div>
                    <p className="text-xs mt-0.5" style={{ color: "#3a3a5c" }}>Niv. {r.level}</p>
                  </div>

                  {/* Value */}
                  <span
                    className="font-bold font-mono text-sm shrink-0"
                    style={{ color: r.rank === 1 ? "#ffb800" : r.is_me ? "#00ff88" : "#6a6a8a" }}
                  >
                    {formatValue(r.value)}
                  </span>
                </motion.div>
              ))}

              {rows.length === 0 && (
                <motion.p
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="text-center py-12 text-sm"
                  style={{ color: "#3a3a5c" }}
                >
                  Aucun joueur encore.
                </motion.p>
              )}
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}
