import { useState } from "react";
import { motion } from "framer-motion";
import { sounds } from "../../utils/sound";

interface Card { id: string; text: string; }

interface Props {
  payload: {
    cards: Card[];
    display_order: string[];
    correct_answer: string[];
  };
  onAnswer: (ans: string[]) => void;
  disabled: boolean;
}

export default function SortOrder({ payload, onAnswer, disabled }: Props) {
  const initial = payload.display_order.map((id) => payload.cards.find((c) => c.id === id)!);
  const [order, setOrder] = useState<Card[]>(initial);
  const [dragIdx, setDragIdx] = useState<number | null>(null);
  const [overIdx, setOverIdx] = useState<number | null>(null);

  const handleDragStart = (i: number) => { sounds.click(); setDragIdx(i); };
  const handleDragOver = (e: React.DragEvent, i: number) => { e.preventDefault(); setOverIdx(i); };
  const handleDrop = (i: number) => {
    if (dragIdx === null || dragIdx === i) { setDragIdx(null); setOverIdx(null); return; }
    const newOrder = [...order];
    const [item] = newOrder.splice(dragIdx, 1);
    newOrder.splice(i, 0, item);
    setOrder(newOrder);
    setDragIdx(null);
    setOverIdx(null);
  };

  return (
    <div className="space-y-4">
      <p className="text-xs font-mono" style={{ color: "#6a6a8a" }}>
        Glisse les blocs pour les remettre dans l'ordre correct ↕
      </p>

      <div className="space-y-2">
        {order.map((card, i) => (
          <motion.div
            key={card.id}
            draggable={!disabled}
            onDragStart={() => handleDragStart(i)}
            onDragOver={(e) => handleDragOver(e, i)}
            onDrop={() => handleDrop(i)}
            onDragEnd={() => { setDragIdx(null); setOverIdx(null); }}
            layout
            className="flex items-center gap-3 rounded-xl px-4 py-3 transition-colors duration-100"
            style={{
              background: overIdx === i && dragIdx !== i ? "rgba(0,255,136,0.06)" : "#161625",
              border: `1px solid ${overIdx === i && dragIdx !== i ? "rgba(0,255,136,0.3)" : "#1e1e35"}`,
              opacity: dragIdx === i ? 0.35 : 1,
              cursor: disabled ? "default" : "grab",
              transform: overIdx === i && dragIdx !== i ? "scale(1.01)" : "scale(1)",
            }}
          >
            <span className="text-base select-none shrink-0" style={{ color: "#2a2a40" }}>⠿</span>
            <span className="font-mono text-xs w-5 text-center font-bold shrink-0" style={{ color: "#ffb800" }}>
              {i + 1}
            </span>
            <code className="text-sm flex-1 font-mono" style={{ color: "#a0a0c0" }}>{card.text}</code>
          </motion.div>
        ))}
      </div>

      <motion.button
        onClick={() => { sounds.click(); onAnswer(order.map((c) => c.id)); }}
        disabled={disabled}
        whileHover={!disabled ? { scale: 1.01 } : {}}
        whileTap={!disabled ? { scale: 0.98 } : {}}
        className="w-full rounded-xl py-3 text-sm font-bold transition-all duration-200"
        style={{
          background: disabled ? "transparent" : "#00ff88",
          color: disabled ? "#3a3a5c" : "#080810",
          border: `1px solid ${disabled ? "#1e1e35" : "#00ff88"}`,
          cursor: disabled ? "not-allowed" : "pointer",
          opacity: disabled ? 0.4 : 1,
        }}
      >
        ✓ Valider l'ordre
      </motion.button>
    </div>
  );
}
