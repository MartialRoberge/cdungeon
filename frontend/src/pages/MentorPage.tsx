import { useState, useRef, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { sounds } from "../utils/sound";

interface Message {
  role: "user" | "mentor";
  text: string;
}

const STUB_REPLIES: string[] = [
  "Bonne question ! Le C est un langage compilé bas niveau — chaque ligne que tu écris devient directement des instructions machine.",
  "Pour comprendre les pointeurs, pense à une adresse postale : le pointeur contient l'adresse, pas la valeur elle-même.",
  "Un segfault arrive quand tu accèdes à une zone mémoire qui ne t'appartient pas. Vérifie que tes pointeurs sont initialisés avant d'être déréférencés.",
  "La pile (stack) grandit vers le bas en mémoire. Les variables locales y vivent et sont détruites quand la fonction retourne.",
  "malloc() alloue sur le tas (heap), dont tu es responsable. Chaque malloc doit avoir son free() correspondant, sinon c'est une fuite mémoire.",
];

// TODO: Brancher l'API Claude ici.
// Remplacer cette fonction par un appel à POST /mentor/chat { question }
// qui appellera l'API Anthropic avec claude-sonnet-4-6 et le contexte pédagogique C.
async function askMentor(_question: string): Promise<string> {
  await new Promise((r) => setTimeout(r, 900));
  return STUB_REPLIES[Math.floor(Math.random() * STUB_REPLIES.length)];
}

const SUGGESTIONS = [
  "C'est quoi un pointeur ?",
  "Différence malloc vs stack ?",
  "Comment fonctionne scanf ?",
  "Qu'est-ce qu'un buffer overflow ?",
];

export default function MentorPage() {
  const [messages, setMessages] = useState<Message[]>([{
    role: "mentor",
    text: "Salut ! Je suis ton guide C. Pose-moi n'importe quelle question sur le langage C, la mémoire, les pointeurs… Je suis là pour t'aider à progresser.",
  }]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const send = async (text: string) => {
    const q = text.trim();
    if (!q || loading) return;
    sounds.click();
    setInput("");
    setMessages((prev) => [...prev, { role: "user", text: q }]);
    setLoading(true);
    const reply = await askMentor(q);
    setMessages((prev) => [...prev, { role: "mentor", text: reply }]);
    setLoading(false);
  };

  return (
    <div className="min-h-screen pt-16 pb-0 flex flex-col" style={{ background: "#080810" }}>
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3 }}
        className="px-4 py-5 text-center shrink-0"
      >
        <div className="text-3xl mb-1">🧙</div>
        <h1 className="font-bold text-base text-white">C Mentor</h1>
        <p className="text-xs mt-0.5" style={{ color: "#3a3a5c" }}>Pose ta question sur le langage C</p>
      </motion.div>

      {/* Chat area */}
      <div className="flex-1 overflow-y-auto px-4 space-y-3 pb-4" style={{ maxHeight: "calc(100vh - 220px)" }}>
        {/* Suggestions (first load only) */}
        {messages.length === 1 && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.2 }}
            className="flex flex-wrap gap-2 justify-center pt-2 pb-3"
          >
            {SUGGESTIONS.map((s) => (
              <button
                key={s}
                onClick={() => send(s)}
                className="text-xs px-3 py-1.5 rounded-xl transition-all duration-150"
                style={{ background: "#161625", border: "1px solid #1e1e35", color: "#6a6a8a" }}
                onMouseEnter={(e) => { (e.currentTarget as HTMLElement).style.borderColor = "rgba(0,255,136,0.25)"; (e.currentTarget as HTMLElement).style.color = "#00ff88"; }}
                onMouseLeave={(e) => { (e.currentTarget as HTMLElement).style.borderColor = "#1e1e35"; (e.currentTarget as HTMLElement).style.color = "#6a6a8a"; }}
              >
                {s}
              </button>
            ))}
          </motion.div>
        )}

        <AnimatePresence initial={false}>
          {messages.map((msg, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.2 }}
              className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
            >
              <div
                className="max-w-[85%] rounded-2xl px-4 py-3 text-sm leading-relaxed"
                style={
                  msg.role === "user"
                    ? { background: "rgba(0,255,136,0.1)", border: "1px solid rgba(0,255,136,0.2)", color: "#e0e0f0" }
                    : { background: "#0f0f1a", border: "1px solid #1e1e35", color: "#a0a0c0" }
                }
              >
                {msg.role === "mentor" && (
                  <span className="text-xs font-mono mr-2" style={{ color: "#3a3a5c" }}>🧙</span>
                )}
                {msg.text}
              </div>
            </motion.div>
          ))}
        </AnimatePresence>

        {loading && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="flex justify-start"
          >
            <div className="rounded-2xl px-4 py-3" style={{ background: "#0f0f1a", border: "1px solid #1e1e35" }}>
              <motion.div
                animate={{ opacity: [0.3, 1, 0.3] }}
                transition={{ duration: 1.2, repeat: Infinity }}
                className="text-xs font-mono"
                style={{ color: "#3a3a5c" }}
              >
                …
              </motion.div>
            </div>
          </motion.div>
        )}

        <div ref={bottomRef} />
      </div>

      {/* Input */}
      <div
        className="shrink-0 px-4 py-3"
        style={{ borderTop: "1px solid #1e1e35", background: "rgba(8,8,16,0.9)", backdropFilter: "blur(12px)" }}
      >
        <div className="max-w-xl mx-auto flex gap-2">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && send(input)}
            placeholder="Pose ta question…"
            className="flex-1 rounded-xl px-4 py-2.5 text-sm outline-none transition-all duration-150"
            style={{
              background: "#0f0f1a",
              border: "1px solid #1e1e35",
              color: "white",
            }}
            onFocus={(e) => (e.currentTarget.style.borderColor = "rgba(0,255,136,0.3)")}
            onBlur={(e) => (e.currentTarget.style.borderColor = "#1e1e35")}
          />
          <button
            onClick={() => send(input)}
            disabled={!input.trim() || loading}
            className="rounded-xl px-4 py-2.5 text-sm font-bold transition-all duration-150"
            style={{
              background: input.trim() && !loading ? "#00ff88" : "#161625",
              color: input.trim() && !loading ? "#080810" : "#3a3a5c",
              border: "1px solid transparent",
              cursor: input.trim() && !loading ? "pointer" : "not-allowed",
            }}
          >
            →
          </button>
        </div>
      </div>
    </div>
  );
}
