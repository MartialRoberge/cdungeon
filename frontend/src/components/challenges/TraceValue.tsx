import { useState } from "react";
import { motion } from "framer-motion";
import { sounds } from "../../utils/sound";

interface Props {
  payload: {
    code: string;
    correct_answer: string;
  };
  onAnswer: (ans: string) => void;
  disabled: boolean;
}

export default function TraceValue({ payload, onAnswer, disabled }: Props) {
  const [value, setValue] = useState("");
  const lines = payload.code.split("\n");

  const submit = () => {
    if (!value.trim() || disabled) return;
    sounds.click();
    onAnswer(value.trim());
  };

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
        <div className="p-3 space-y-0.5 overflow-x-auto">
          {lines.map((line, i) => (
            <div key={i} className="flex gap-3 px-2 py-0.5">
              <span className="text-xs w-5 text-right shrink-0 select-none font-mono" style={{ color: "#3a3a5c" }}>{i + 1}</span>
              <span className="text-sm font-mono whitespace-pre" style={{ color: "#a0a0c0" }}>
                <CLine text={line} />
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* Answer input */}
      <div className="flex gap-2">
        <input
          value={value}
          onChange={(e) => setValue(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && submit()}
          disabled={disabled}
          placeholder="Ta reponse..."
          className="flex-1 rounded-xl px-4 py-3 text-sm font-mono outline-none"
          style={{
            background: "#161625",
            border: "1px solid #1e1e35",
            color: "#00ff88",
            opacity: disabled ? 0.4 : 1,
          }}
          autoFocus
        />
        <motion.button
          disabled={disabled || !value.trim()}
          onClick={submit}
          whileHover={!disabled && value.trim() ? { scale: 1.03 } : {}}
          whileTap={!disabled && value.trim() ? { scale: 0.97 } : {}}
          className="rounded-xl px-5 py-3 font-bold text-sm"
          style={{
            background: !disabled && value.trim() ? "#00ff88" : "#161625",
            color: !disabled && value.trim() ? "#080810" : "#3a3a5c",
            cursor: !disabled && value.trim() ? "pointer" : "not-allowed",
          }}
        >
          Valider
        </motion.button>
      </div>
    </div>
  );
}

function CLine({ text }: { text: string }) {
  const keywords = /\b(int|float|double|char|void|if|else|while|for|do|return|break|continue|struct|typedef|enum|malloc|calloc|realloc|free|printf|scanf|fprintf|fscanf|fopen|fclose|fgets|fputs|fread|fwrite|fseek|ftell|strlen|strcpy|strcat|strcmp|strncpy|sprintf|sscanf|sizeof|NULL|include|define)\b/g;
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
