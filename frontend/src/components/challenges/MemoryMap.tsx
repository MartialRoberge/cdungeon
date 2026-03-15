import { motion } from "framer-motion";
import { sounds } from "../../utils/sound";

interface Cell { address: string; row: number; col: number; }
interface VisualState { [addr: string]: { label: string; value: string; highlight: "var" | "ptr" | "empty" }; }

interface Props {
  payload: {
    grid_size: { rows: number; cols: number };
    addresses: Cell[];
    code_context: string[];
    question: string;
    interaction_mode: "click_cell";
    correct_answer: string;
    visual_state: VisualState;
  };
  onAnswer: (ans: string) => void;
  disabled: boolean;
}

export default function MemoryMap({ payload, onAnswer, disabled }: Props) {
  const { grid_size, addresses, code_context, visual_state } = payload;

  const grid: (Cell | null)[][] = Array.from({ length: grid_size.rows }, () =>
    Array(grid_size.cols).fill(null)
  );
  for (const cell of addresses) {
    grid[cell.row][cell.col] = cell;
  }

  return (
    <div className="space-y-4">
      {/* Code context */}
      <div className="rounded-xl overflow-hidden" style={{ background: "#080810", border: "1px solid #1e1e35" }}>
        <div className="px-3 py-2 flex items-center gap-2" style={{ borderBottom: "1px solid #1e1e35" }}>
          <div className="flex gap-1.5">
            <div className="w-2.5 h-2.5 rounded-full" style={{ background: "#ff3355", opacity: 0.6 }} />
            <div className="w-2.5 h-2.5 rounded-full" style={{ background: "#ffb800", opacity: 0.6 }} />
            <div className="w-2.5 h-2.5 rounded-full" style={{ background: "#00ff88", opacity: 0.6 }} />
          </div>
          <span className="text-xs font-mono" style={{ color: "#3a3a5c" }}>memory.c</span>
        </div>
        <div className="p-3">
          {code_context.map((line, i) => (
            <div key={i} className="text-sm font-mono leading-relaxed" style={{ color: "#a0a0c0" }}>{line}</div>
          ))}
        </div>
      </div>

      <p className="text-sm font-semibold text-white">{payload.question}</p>

      {/* Memory grid */}
      <div
        className="grid gap-2"
        style={{ gridTemplateColumns: `repeat(${grid_size.cols}, 1fr)` }}
      >
        {grid.flat().map((cell, idx) => {
          if (!cell) return <div key={idx} />;
          const info = visual_state[cell.address];
          const hl = info?.highlight || "empty";
          const isClickable = !disabled && hl !== "empty";

          const borderColor = hl === "var" ? "rgba(0,255,136,0.4)" : hl === "ptr" ? "rgba(255,184,0,0.4)" : "#1e1e35";
          const bgColor = hl === "var" ? "rgba(0,255,136,0.07)" : hl === "ptr" ? "rgba(255,184,0,0.07)" : "#0a0a14";
          const labelColor = hl === "var" ? "#00ff88" : hl === "ptr" ? "#ffb800" : "#3a3a5c";

          return (
            <motion.button
              key={cell.address}
              disabled={!isClickable}
              onClick={() => { if (isClickable) { sounds.click(); onAnswer(cell.address); } }}
              whileHover={isClickable ? { scale: 1.05 } : {}}
              whileTap={isClickable ? { scale: 0.97 } : {}}
              className="rounded-xl p-2 text-center transition-all duration-200"
              style={{
                background: bgColor,
                border: `1px solid ${borderColor}`,
                cursor: isClickable ? "pointer" : "default",
                opacity: hl === "empty" ? 0.3 : 1,
              }}
            >
              <div className="text-xs font-mono mb-1" style={{ color: "#3a3a5c" }}>{cell.address}</div>
              {info && (
                <>
                  <div className="font-bold text-sm font-mono" style={{ color: labelColor }}>{info.label}</div>
                  <div className="text-xs font-mono mt-0.5" style={{ color: "#6a6a8a" }}>{info.value}</div>
                </>
              )}
            </motion.button>
          );
        })}
      </div>

      {/* Legend */}
      <div className="flex gap-4 text-xs font-mono" style={{ color: "#3a3a5c" }}>
        <span className="flex items-center gap-1.5">
          <span className="w-3 h-3 rounded" style={{ background: "rgba(0,255,136,0.07)", border: "1px solid rgba(0,255,136,0.4)" }} />
          Variable
        </span>
        <span className="flex items-center gap-1.5">
          <span className="w-3 h-3 rounded" style={{ background: "rgba(255,184,0,0.07)", border: "1px solid rgba(255,184,0,0.4)" }} />
          Pointeur
        </span>
      </div>
    </div>
  );
}
