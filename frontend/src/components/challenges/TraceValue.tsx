import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { sounds } from "../../utils/sound";

interface CodeLine { line: number; text: string; }
interface AnimStep { after_line: number; variable: string; value: string | number; }

interface Props {
  payload: {
    code_lines: CodeLine[];
    animation_steps: AnimStep[];
    question: string;
    options: (string | number)[];
    correct_answer: string | number;
  };
  onAnswer: (ans: string | number) => void;
  disabled: boolean;
}

export default function TraceValue({ payload, onAnswer, disabled }: Props) {
  const [vars, setVars] = useState<Record<string, string | number>>({});
  const [currentLine, setCurrentLine] = useState(0);
  const [ready, setReady] = useState(false);

  useEffect(() => {
    setVars({}); setCurrentLine(0); setReady(false);
    let i = 0;
    const run = () => {
      if (i >= payload.animation_steps.length) { setReady(true); return; }
      const s = payload.animation_steps[i];
      setCurrentLine(s.after_line);
      setVars((prev) => ({ ...prev, [s.variable]: s.value }));
      i++;
      setTimeout(run, 700);
    };
    const t = setTimeout(run, 500);
    return () => clearTimeout(t);
  }, [payload]);

  return (
    <div className="space-y-4">
      {/* Code viewer */}
      <div className="rounded-xl overflow-hidden" style={{ background: "#080810", border: "1px solid #1e1e35" }}>
        <div className="px-3 py-2 flex items-center gap-2" style={{ borderBottom: "1px solid #1e1e35" }}>
          <div className="flex gap-1.5">
            <div className="w-2.5 h-2.5 rounded-full" style={{ background: "#ff3355", opacity: 0.6 }} />
            <div className="w-2.5 h-2.5 rounded-full" style={{ background: "#ffb800", opacity: 0.6 }} />
            <div className="w-2.5 h-2.5 rounded-full" style={{ background: "#00ff88", opacity: 0.6 }} />
          </div>
          <span className="text-xs font-mono" style={{ color: "#3a3a5c" }}>main.c</span>
        </div>
        <div className="p-3 space-y-0.5">
          {payload.code_lines.map((l) => (
            <motion.div
              key={l.line}
              animate={currentLine === l.line ? { backgroundColor: "rgba(0,255,136,0.07)" } : { backgroundColor: "transparent" }}
              transition={{ duration: 0.2 }}
              className="flex gap-3 px-2 py-0.5 rounded"
              style={{ borderLeft: currentLine === l.line ? "2px solid #00ff88" : "2px solid transparent" }}
            >
              <span className="text-xs w-4 text-right shrink-0 select-none" style={{ color: "#3a3a5c" }}>{l.line}</span>
              <span className="text-sm font-mono" style={{ color: currentLine === l.line ? "#00ff88" : "#a0a0c0" }}>
                <CLine text={l.text} />
              </span>
            </motion.div>
          ))}
        </div>
      </div>

      {/* Variable tracker */}
      <AnimatePresence>
        {Object.keys(vars).length > 0 && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            className="rounded-xl p-3"
            style={{ background: "#0a0a14", border: "1px solid #1e1e35" }}
          >
            <p className="text-xs font-mono mb-2" style={{ color: "#3a3a5c" }}>Variables</p>
            <div className="flex flex-wrap gap-2">
              {Object.entries(vars).map(([k, v]) => (
                <motion.div
                  key={k}
                  initial={{ scale: 0.8, opacity: 0 }}
                  animate={{ scale: 1, opacity: 1 }}
                  transition={{ type: "spring", stiffness: 400, damping: 20 }}
                  className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-mono"
                  style={{ background: "#161625", border: "1px solid #1e1e35" }}
                >
                  <span style={{ color: "#ffb800" }}>{k}</span>
                  <span style={{ color: "#3a3a5c" }}>=</span>
                  <span className="font-bold" style={{ color: "#00ff88" }}>{String(v)}</span>
                </motion.div>
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Question + options */}
      <AnimatePresence>
        {ready && (
          <motion.div
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.25 }}
            className="space-y-3"
          >
            <p className="text-sm font-semibold text-white">{payload.question}</p>
            <div className="grid grid-cols-2 gap-2">
              {payload.options.map((opt) => (
                <motion.button
                  key={String(opt)}
                  disabled={disabled}
                  onClick={() => { sounds.click(); onAnswer(opt); }}
                  whileHover={!disabled ? { scale: 1.02 } : {}}
                  whileTap={!disabled ? { scale: 0.97 } : {}}
                  className="rounded-xl p-3 text-center font-bold font-mono text-sm transition-all duration-150"
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
                  {String(opt)}
                </motion.button>
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

function CLine({ text }: { text: string }) {
  const keywords = /\b(int|float|double|char|void|if|else|while|for|do|return|break|continue|struct|typedef|malloc|free|printf|scanf|NULL|sizeof)\b/g;
  const parts = text.split(keywords);
  return (
    <>
      {parts.map((p, i) =>
        i % 2 === 1
          ? <span key={i} style={{ color: "#a855f7" }}>{p}</span>
          : <span key={i}>{p}</span>
      )}
    </>
  );
}
