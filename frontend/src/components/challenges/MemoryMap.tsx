import { motion } from "framer-motion";
import { sounds } from "../../utils/sound";

interface Slot { id: string; label: string; }

interface Props {
  payload: {
    scenario: string;
    slots: Slot[];
    correct_answer: string;
  };
  onAnswer: (ans: string) => void;
  disabled: boolean;
}

export default function MemoryMap({ payload, onAnswer, disabled }: Props) {
  const scenarioLines = payload.scenario.split("\n");

  return (
    <div className="space-y-4">
      {/* Scenario / code context */}
      <div className="rounded-xl overflow-hidden" style={{ background: "#080810", border: "1px solid #1e1e35" }}>
        <div className="px-3 py-2 flex items-center gap-2" style={{ borderBottom: "1px solid #1e1e35" }}>
          <div className="flex gap-1.5">
            <div className="w-2.5 h-2.5 rounded-full" style={{ background: "#ff3355", opacity: 0.6 }} />
            <div className="w-2.5 h-2.5 rounded-full" style={{ background: "#ffb800", opacity: 0.6 }} />
            <div className="w-2.5 h-2.5 rounded-full" style={{ background: "#00ff88", opacity: 0.6 }} />
          </div>
          <span className="text-xs font-mono" style={{ color: "#3a3a5c" }}>memory</span>
        </div>
        <div className="p-3">
          {scenarioLines.map((line, i) => (
            <div key={i} className="text-sm font-mono leading-relaxed whitespace-pre-wrap" style={{ color: "#a0a0c0" }}>{line}</div>
          ))}
        </div>
      </div>

      {/* Slots to choose from */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
        {payload.slots.map((slot) => (
          <motion.button
            key={slot.id}
            disabled={disabled}
            onClick={() => { if (!disabled) { sounds.click(); onAnswer(slot.id); } }}
            whileHover={!disabled ? { scale: 1.02 } : {}}
            whileTap={!disabled ? { scale: 0.97 } : {}}
            className="rounded-xl p-3 text-left transition-all duration-150"
            style={{
              background: "#161625",
              border: "1px solid #1e1e35",
              opacity: disabled ? 0.4 : 1,
              cursor: disabled ? "not-allowed" : "pointer",
            }}
            onMouseEnter={(e) => { if (!disabled) { (e.currentTarget as HTMLElement).style.borderColor = "rgba(0,255,136,0.35)"; (e.currentTarget as HTMLElement).style.background = "rgba(0,255,136,0.06)"; } }}
            onMouseLeave={(e) => { (e.currentTarget as HTMLElement).style.borderColor = "#1e1e35"; (e.currentTarget as HTMLElement).style.background = "#161625"; }}
          >
            <span className="text-xs font-mono mr-2" style={{ color: "#3a3a5c" }}>{slot.id}</span>
            <span className="text-sm font-mono font-bold" style={{ color: "#00ff88" }}>{slot.label}</span>
          </motion.button>
        ))}
      </div>
    </div>
  );
}
