import { useEffect, useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { motion } from "framer-motion";
import type { Variants } from "framer-motion";
import { getZones } from "../api";
import { sounds } from "../utils/sound";

interface Zone {
  zone_number: number; name: string; emoji: string;
  rooms_total: number; rooms_cleared: number;
  is_unlocked: boolean; is_boss_cleared: boolean; boss_name: string;
}

const ZONE_COLORS = [
  "#00ff88","#3b82f6","#f97316","#eab308",
  "#a855f7","#ec4899","#ef4444","#22d3ee",
];

const container: Variants = { hidden: {}, visible: { transition: { staggerChildren: 0.06 } } };
const item: Variants = { hidden: { opacity: 0, y: 16 }, visible: { opacity: 1, y: 0, transition: { type: "spring", stiffness: 300, damping: 24 } } };

export default function DungeonMapPage() {
  const [zones, setZones] = useState<Zone[]>([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    setLoading(true);
    getZones().then(setZones).finally(() => setLoading(false));
  }, [location.key]);

  if (loading) return <Loading />;

  return (
    <div className="min-h-screen pt-16 pb-12 px-4">
      <div className="max-w-2xl mx-auto">
        <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4 }} className="text-center py-8">
          <h1 className="text-2xl font-bold tracking-tight" style={{ color: "#00ff88" }}>Carte du Donjon</h1>
          <p className="text-sm mt-1" style={{ color: "#3a3a5c" }}>
            {zones.filter((z) => z.is_boss_cleared).length} / {zones.length} zones terminées
          </p>
        </motion.div>

        <motion.div variants={container} initial="hidden" animate="visible" className="grid gap-3">
          {zones.map((zone) => (
            <motion.div key={zone.zone_number} variants={item}>
              <ZoneCard zone={zone} color={ZONE_COLORS[zone.zone_number - 1]} onClick={() => { sounds.click(); navigate(`/zone/${zone.zone_number}`); }} />
            </motion.div>
          ))}
        </motion.div>
      </div>
    </div>
  );
}

function ZoneCard({ zone, color, onClick }: { zone: Zone; color: string; onClick: () => void }) {
  const pct = zone.rooms_total > 0 ? Math.round((zone.rooms_cleared / zone.rooms_total) * 100) : 0;
  const locked = !zone.is_unlocked;

  return (
    <motion.div
      onClick={!locked ? onClick : undefined}
      whileHover={!locked ? { x: 4 } : {}}
      whileTap={!locked ? { scale: 0.98 } : {}}
      transition={{ type: "spring", stiffness: 400, damping: 25 }}
      className="rounded-2xl p-4 flex items-center gap-4 transition-colors duration-200"
      style={{
        background: "#0f0f1a",
        border: `1px solid ${locked ? "#1e1e35" : zone.is_boss_cleared ? `${color}30` : "#1e1e35"}`,
        cursor: locked ? "not-allowed" : "pointer",
        opacity: locked ? 0.35 : 1,
        boxShadow: zone.is_boss_cleared ? `0 0 20px ${color}08` : "none",
      }}
    >
      {/* Emoji / status indicator */}
      <div className="text-3xl shrink-0 w-12 text-center" style={{ filter: locked ? "grayscale(1)" : "none" }}>
        {zone.emoji}
      </div>

      {/* Info */}
      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-2 mb-0.5">
          <span className="font-semibold text-sm text-white truncate">{zone.name}</span>
          {zone.is_boss_cleared && (
            <span className="text-xs font-mono px-1.5 py-0.5 rounded-md" style={{ background: `${color}15`, color, border: `1px solid ${color}30` }}>✓</span>
          )}
          {locked && <span className="text-xs" style={{ color: "#3a3a5c" }}>🔒</span>}
        </div>
        <p className="text-xs" style={{ color: "#3a3a5c" }}>{zone.boss_name}</p>

        {!locked && (
          <div className="mt-2 flex items-center gap-2">
            <div className="flex-1 h-0.5 rounded-full overflow-hidden" style={{ background: "#1e1e35" }}>
              <motion.div
                className="h-full rounded-full"
                style={{ background: color, boxShadow: pct === 100 ? `0 0 6px ${color}` : "none" }}
                initial={{ width: 0 }}
                animate={{ width: `${pct}%` }}
                transition={{ duration: 0.8, ease: "easeOut", delay: 0.1 }}
              />
            </div>
            <span className="text-xs font-mono shrink-0" style={{ color: "#3a3a5c" }}>{zone.rooms_cleared}/{zone.rooms_total}</span>
          </div>
        )}
      </div>

      {!locked && !zone.is_boss_cleared && (
        <div className="text-dg-muted text-sm shrink-0">›</div>
      )}
    </motion.div>
  );
}

function Loading() {
  return (
    <div className="min-h-screen flex items-center justify-center">
      <motion.div animate={{ opacity: [0.3, 1, 0.3] }} transition={{ duration: 1.5, repeat: Infinity }} className="text-center">
        <p className="text-sm font-mono" style={{ color: "#00ff88" }}>Chargement du donjon…</p>
      </motion.div>
    </div>
  );
}
