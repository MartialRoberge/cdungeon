import { motion } from "framer-motion";
import { sounds } from "../../utils/sound";

interface Segment { type: "code" | "newline"; text?: string; }

interface Props {
  payload: {
    code_segments: Segment[];
    options: string[];
    correct_answer: string;
  };
  onAnswer: (ans: string) => void;
  disabled: boolean;
}

export default function FillBlank({ payload, onAnswer, disabled }: Props) {
  return (
    <div className="space-y-5">
      {/* Code with gap */}
      <div className="rounded-xl p-4" style={{ background: "#080810", border: "1px solid #1e1e35" }}>
        <div className="text-sm font-mono leading-loose" style={{ color: "#a0a0c0" }}>
          {payload.code_segments.map((seg, i) => {
            if (seg.type === "newline") return <br key={i} />;
            if (seg.text === "___") {
              return (
                <motion.span
                  key={i}
                  animate={{ borderColor: ["rgba(0,255,136,0.3)", "rgba(0,255,136,0.8)", "rgba(0,255,136,0.3)"] }}
                  transition={{ duration: 1.8, repeat: Infinity }}
                  className="inline-block min-w-[64px] text-center mx-1 px-2 rounded"
                  style={{
                    border: "2px solid rgba(0,255,136,0.5)",
                    background: "rgba(0,255,136,0.07)",
                    color: "#00ff88",
                  }}
                >
                  ?
                </motion.span>
              );
            }
            return <span key={i}>{seg.text}</span>;
          })}
        </div>
      </div>

      {/* Options */}
      <div className="grid grid-cols-2 gap-2">
        {payload.options.map((opt) => (
          <motion.button
            key={opt}
            disabled={disabled}
            onClick={() => { sounds.click(); onAnswer(opt); }}
            whileHover={!disabled ? { scale: 1.02 } : {}}
            whileTap={!disabled ? { scale: 0.97 } : {}}
            className="rounded-xl p-3 text-center font-bold font-mono text-sm transition-colors duration-150"
            style={{
              background: "#161625",
              border: "1px solid #1e1e35",
              color: "#00ff88",
              opacity: disabled ? 0.4 : 1,
              cursor: disabled ? "not-allowed" : "pointer",
            }}
            onMouseEnter={(e) => { if (!disabled) { (e.currentTarget as HTMLElement).style.borderColor = "rgba(0,255,136,0.35)"; (e.currentTarget as HTMLElement).style.background = "rgba(0,255,136,0.06)"; } }}
            onMouseLeave={(e) => { (e.currentTarget as HTMLElement).style.borderColor = "#1e1e35"; (e.currentTarget as HTMLElement).style.background = "#161625"; }}
          >
            {opt}
          </motion.button>
        ))}
      </div>
    </div>
  );
}
