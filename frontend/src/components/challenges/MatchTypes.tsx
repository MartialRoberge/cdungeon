import { useState } from "react";
import { motion } from "framer-motion";
import { sounds } from "../../utils/sound";

interface Value { id: string; display: string; }
interface TypeSlot { id: string; label: string; }

interface Props {
  payload: {
    values: Value[];
    types: TypeSlot[];
    correct_answer: Record<string, string>;
  };
  onAnswer: (ans: Record<string, string>) => void;
  disabled: boolean;
}

export default function MatchTypes({ payload, onAnswer, disabled }: Props) {
  const [matches, setMatches] = useState<Record<string, string>>({});
  const [dragging, setDragging] = useState<string | null>(null);
  const [selected, setSelected] = useState<string | null>(null);

  const assign = (valueId: string, typeId: string) => {
    sounds.click();
    setMatches((prev) => {
      const cleared = Object.fromEntries(Object.entries(prev).filter(([, v]) => v !== typeId));
      return { ...cleared, [valueId]: typeId };
    });
    setSelected(null);
    setDragging(null);
  };

  const submit = () => {
    if (Object.keys(matches).length === payload.values.length) onAnswer(matches);
  };

  const assignedValues = new Set(Object.keys(matches));
  const remaining = payload.values.length - Object.keys(matches).length;

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-2 gap-4">
        {/* Values */}
        <div className="space-y-2">
          <p className="text-xs font-mono mb-1" style={{ color: "#3a3a5c" }}>VALEURS</p>
          {payload.values.map((v) => {
            const isAssigned = assignedValues.has(v.id);
            const isSelected = selected === v.id;
            return (
              <motion.div
                key={v.id}
                draggable={!disabled && !isAssigned}
                onDragStart={() => { setDragging(v.id); setSelected(null); }}
                onDragEnd={() => setDragging(null)}
                onClick={() => {
                  if (disabled || isAssigned) return;
                  sounds.click();
                  setSelected(selected === v.id ? null : v.id);
                }}
                whileHover={!disabled && !isAssigned ? { x: 2 } : {}}
                whileTap={!disabled && !isAssigned ? { scale: 0.97 } : {}}
                className="rounded-xl px-3 py-2 text-sm font-mono transition-all duration-150"
                style={{
                  background: isSelected ? "rgba(0,255,136,0.08)" : "#161625",
                  border: `1px solid ${isSelected ? "rgba(0,255,136,0.4)" : isAssigned ? "#1e1e35" : "#2a2a40"}`,
                  color: isAssigned ? "#3a3a5c" : "#ffb800",
                  opacity: isAssigned ? 0.4 : 1,
                  cursor: isAssigned || disabled ? "default" : "pointer",
                }}
              >
                {v.display}
              </motion.div>
            );
          })}
        </div>

        {/* Types (drop zones) */}
        <div className="space-y-2">
          <p className="text-xs font-mono mb-1" style={{ color: "#3a3a5c" }}>TYPES C</p>
          {payload.types.map((t) => {
            const assignedValue = payload.values.find((v) => matches[v.id] === t.id);
            const canReceive = (dragging || selected) && !assignedValue;
            return (
              <motion.div
                key={t.id}
                onDragOver={(e) => e.preventDefault()}
                onDrop={() => { if (dragging) assign(dragging, t.id); }}
                onClick={() => { if (selected) assign(selected, t.id); }}
                animate={canReceive ? { borderColor: "rgba(0,255,136,0.35)" } : {}}
                className="rounded-xl px-3 py-2 min-h-[42px] flex items-center justify-between transition-all duration-150"
                style={{
                  background: assignedValue ? "rgba(0,255,136,0.05)" : "#161625",
                  border: `1px dashed ${assignedValue ? "rgba(0,255,136,0.3)" : "#2a2a40"}`,
                  cursor: (dragging || selected) ? "pointer" : "default",
                }}
              >
                <span className="text-sm font-mono font-bold" style={{ color: "#00ff88" }}>{t.label}</span>
                {assignedValue && (
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-mono" style={{ color: "#ffb800" }}>{assignedValue.display}</span>
                    {!disabled && (
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          sounds.click();
                          setMatches((p) => { const n = { ...p }; delete n[assignedValue.id]; return n; });
                        }}
                        className="text-xs transition-colors duration-150"
                        style={{ color: "#3a3a5c" }}
                        onMouseEnter={(e) => (e.currentTarget.style.color = "#ff3355")}
                        onMouseLeave={(e) => (e.currentTarget.style.color = "#3a3a5c")}
                      >
                        ✕
                      </button>
                    )}
                  </div>
                )}
              </motion.div>
            );
          })}
        </div>
      </div>

      {/* Hint */}
      {!disabled && (
        <p className="text-xs text-center" style={{ color: "#3a3a5c" }}>
          Glisse ou sélectionne une valeur, puis clique sur son type
        </p>
      )}

      <motion.button
        onClick={submit}
        disabled={disabled || remaining > 0}
        whileHover={remaining === 0 && !disabled ? { scale: 1.01 } : {}}
        whileTap={remaining === 0 && !disabled ? { scale: 0.98 } : {}}
        className="w-full rounded-xl py-3 text-sm font-bold transition-all duration-200"
        style={{
          background: remaining === 0 && !disabled ? "#00ff88" : "transparent",
          color: remaining === 0 && !disabled ? "#080810" : "#3a3a5c",
          border: `1px solid ${remaining === 0 && !disabled ? "#00ff88" : "#1e1e35"}`,
          opacity: disabled ? 0.4 : 1,
          cursor: remaining > 0 || disabled ? "not-allowed" : "pointer",
        }}
      >
        {remaining > 0 ? `${remaining} association${remaining > 1 ? "s" : ""} restante${remaining > 1 ? "s" : ""}` : "✓ Valider"}
      </motion.button>
    </div>
  );
}
