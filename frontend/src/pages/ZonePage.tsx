import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import type { Variants } from "framer-motion";
import { getZoneRooms, getZones } from "../api";
import { sounds } from "../utils/sound";

interface Room {
  room_id: string; room_number: number; name: string;
  challenge_type: string; is_boss: boolean; is_cleared: boolean; attempts_taken: number;
}

const TYPE_ICONS: Record<string, string> = {
  trace_value: "🎬", find_bug: "🐛", fill_blank: "📝",
  match_types: "🔗", sort_order: "📋", memory_map: "🧠",
};

const ZONE_COLORS: Record<number, string> = {
  1: "#00ff88", 2: "#3b82f6", 3: "#f97316", 4: "#eab308",
  5: "#a855f7", 6: "#ec4899", 7: "#ef4444", 8: "#22d3ee",
};

const container: Variants = { hidden: {}, visible: { transition: { staggerChildren: 0.07 } } };
const nodeVariant: Variants = {
  hidden: { opacity: 0, x: -16 },
  visible: { opacity: 1, x: 0, transition: { type: "spring", stiffness: 280, damping: 24 } },
};

export default function ZonePage() {
  const { zoneNumber } = useParams<{ zoneNumber: string }>();
  const zn = Number(zoneNumber);
  const [rooms, setRooms] = useState<Room[]>([]);
  const [zoneMeta, setZoneMeta] = useState<{ name: string; emoji: string; boss_name: string } | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    Promise.all([getZoneRooms(zn), getZones()]).then(([r, zones]: [Room[], {zone_number: number; name: string; emoji: string; boss_name: string}[]]) => {
      setRooms(r);
      const meta = zones.find((z) => z.zone_number === zn);
      if (meta) setZoneMeta(meta);
    });
  }, [zn]);

  const color = ZONE_COLORS[zn] || "#00ff88";

  return (
    <div className="min-h-screen pt-16 pb-8 px-4" style={{ background: "#080810" }}>
      <div className="max-w-xl mx-auto">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.35 }}
          className="py-6"
        >
          <button
            onClick={() => { sounds.click(); navigate("/map"); }}
            className="text-xs mb-4 transition-colors duration-200"
            style={{ color: "#3a3a5c" }}
            onMouseEnter={(e) => (e.currentTarget.style.color = "#6a6a8a")}
            onMouseLeave={(e) => (e.currentTarget.style.color = "#3a3a5c")}
          >
            ← Carte
          </button>

          {zoneMeta && (
            <div className="flex items-center gap-4">
              <span className="text-4xl">{zoneMeta.emoji}</span>
              <div>
                <h1 className="font-bold text-xl text-white">{zoneMeta.name}</h1>
                <p className="text-xs mt-0.5" style={{ color: "#6a6a8a" }}>Boss : {zoneMeta.boss_name}</p>
              </div>
              <div className="ml-auto">
                <span className="text-xs font-mono px-2 py-1 rounded-lg" style={{ background: `${color}12`, color, border: `1px solid ${color}25` }}>
                  Zone {zn}
                </span>
              </div>
            </div>
          )}
        </motion.div>

        {/* Room path */}
        <motion.div variants={container} initial="hidden" animate="visible" className="space-y-1">
          {rooms.map((room, idx) => {
            const accessible = idx === 0 || rooms[idx - 1].is_cleared;
            return (
              <motion.div key={room.room_id} variants={nodeVariant}>
                {idx > 0 && (
                  <div className="flex justify-center my-1">
                    <div
                      className="w-px h-4 rounded-full"
                      style={{ background: rooms[idx - 1].is_cleared ? color : "#1e1e35" }}
                    />
                  </div>
                )}
                <RoomNode
                  room={room}
                  accessible={accessible}
                  color={color}
                  onClick={() => { sounds.click(); navigate(`/room/${room.room_id}`); }}
                />
              </motion.div>
            );
          })}
        </motion.div>
      </div>
    </div>
  );
}

function RoomNode({ room, accessible, color, onClick }: {
  room: Room; accessible: boolean; color: string; onClick: () => void;
}) {
  const icon = room.is_boss ? "💀" : TYPE_ICONS[room.challenge_type] || "❓";
  const bossColor = "#ff3355";

  const borderColor = !accessible
    ? "#1e1e35"
    : room.is_cleared
    ? `${color}40`
    : room.is_boss
    ? "rgba(255,51,85,0.25)"
    : "#1e1e35";

  return (
    <motion.div
      onClick={accessible ? onClick : undefined}
      whileHover={accessible ? { x: 4 } : {}}
      whileTap={accessible ? { scale: 0.98 } : {}}
      transition={{ type: "spring", stiffness: 400, damping: 25 }}
      className="rounded-2xl p-4 flex items-center gap-4"
      style={{
        background: "#0f0f1a",
        border: `1px solid ${borderColor}`,
        cursor: accessible ? "pointer" : "not-allowed",
        opacity: accessible ? 1 : 0.3,
        boxShadow: room.is_cleared && accessible ? `0 0 20px ${color}08` : "none",
      }}
    >
      <div className="text-2xl shrink-0 w-10 text-center" style={{ filter: accessible ? "none" : "grayscale(1)" }}>
        {icon}
      </div>

      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-2 mb-0.5">
          {room.is_boss && (
            <span className="text-xs font-mono px-1.5 py-0.5 rounded font-bold" style={{ background: "rgba(255,51,85,0.1)", color: bossColor, border: "1px solid rgba(255,51,85,0.2)" }}>
              BOSS
            </span>
          )}
          <span className="font-semibold text-sm text-white">{room.name}</span>
          {room.is_cleared && (
            <span className="text-xs font-mono px-1.5 py-0.5 rounded-md" style={{ background: `${color}15`, color, border: `1px solid ${color}30` }}>✓</span>
          )}
          {!accessible && <span className="text-xs" style={{ color: "#3a3a5c" }}>🔒</span>}
        </div>

        <div className="flex items-center gap-2">
          <span className="text-xs font-mono" style={{ color: "#3a3a5c" }}>
            {room.challenge_type.replace("_", " ")}
          </span>
          {room.is_cleared && room.attempts_taken > 0 && (
            <span className="text-xs" style={{ color: "#3a3a5c" }}>
              · {room.attempts_taken} tentative{room.attempts_taken > 1 ? "s" : ""}
            </span>
          )}
        </div>
      </div>

      {accessible && !room.is_cleared && (
        <div className="text-sm shrink-0" style={{ color: "#3a3a5c" }}>›</div>
      )}
    </motion.div>
  );
}
