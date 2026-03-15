import { useState } from "react";
import { motion } from "framer-motion";
import { sounds } from "../../utils/sound";

interface CodeLine { line: number; text: string; is_bug: boolean; }

interface Props {
  payload: {
    code_lines: CodeLine[];
    correct_answer: number;
    bug_explanation: string;
  };
  onAnswer: (ans: number) => void;
  disabled: boolean;
}

export default function FindBug({ payload, onAnswer, disabled }: Props) {
  const [hovered, setHovered] = useState<number | null>(null);

  return (
    <div className="space-y-4">
      <p className="text-xs font-mono" style={{ color: "#6a6a8a" }}>
        Clique sur la ligne qui contient l'erreur ↓
      </p>

      <div className="rounded-xl overflow-hidden" style={{ background: "#080810", border: "1px solid #1e1e35" }}>
        <div className="px-3 py-2 flex items-center gap-2" style={{ borderBottom: "1px solid #1e1e35" }}>
          <div className="flex gap-1.5">
            <div className="w-2.5 h-2.5 rounded-full" style={{ background: "#ff3355", opacity: 0.6 }} />
            <div className="w-2.5 h-2.5 rounded-full" style={{ background: "#ffb800", opacity: 0.6 }} />
            <div className="w-2.5 h-2.5 rounded-full" style={{ background: "#00ff88", opacity: 0.6 }} />
          </div>
          <span className="text-xs font-mono" style={{ color: "#3a3a5c" }}>debug.c</span>
          {!disabled && (
            <motion.span
              animate={{ opacity: [0.4, 1, 0.4] }}
              transition={{ duration: 1.6, repeat: Infinity }}
              className="ml-auto text-xs font-mono"
              style={{ color: "#ff3355" }}
            >
              🔍 inspecte…
            </motion.span>
          )}
        </div>

        <div className="p-1">
          {payload.code_lines.map((l) => (
            <motion.div
              key={l.line}
              onMouseEnter={() => { if (!disabled) setHovered(l.line); }}
              onMouseLeave={() => setHovered(null)}
              onClick={() => { if (!disabled) { sounds.click(); onAnswer(l.line); } }}
              animate={hovered === l.line && !disabled ? { backgroundColor: "rgba(255,51,85,0.07)" } : { backgroundColor: "transparent" }}
              transition={{ duration: 0.15 }}
              className="flex items-center gap-3 px-3 py-1.5 rounded"
              style={{
                cursor: disabled ? "default" : "pointer",
                borderLeft: hovered === l.line && !disabled ? "2px solid rgba(255,51,85,0.5)" : "2px solid transparent",
              }}
            >
              <span className="text-xs w-5 text-right shrink-0 select-none font-mono" style={{ color: "#3a3a5c" }}>{l.line}</span>
              <span className="text-sm font-mono flex-1" style={{ color: "#a0a0c0" }}>{l.text}</span>
              {hovered === l.line && !disabled && (
                <motion.span
                  initial={{ opacity: 0, x: 4 }}
                  animate={{ opacity: 1, x: 0 }}
                  className="text-xs font-mono shrink-0"
                  style={{ color: "rgba(255,51,85,0.7)" }}
                >
                  ← bug ici ?
                </motion.span>
              )}
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  );
}
