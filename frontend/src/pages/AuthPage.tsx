import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { useAuthStore } from "../store";
import { login, register, getMe } from "../api";
import { initAudio, sounds } from "../utils/sound";

const ZONE_EMOJIS = ["🏠","🌀","⚙️","🏰","🕳️","🔤","☣️","📜"];

export default function AuthPage() {
  const [mode, setMode] = useState<"login"|"register">("login");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const { setAuth } = useAuthStore();
  const navigate = useNavigate();

  const submit = async () => {
    initAudio();
    setError(""); setLoading(true);
    try {
      const data = mode === "login" ? await login(username, password) : await register(username, password);
      setAuth(data.access_token, { id: data.player_id, username: data.username, xp: 0, level: 1, current_zone: 1, daily_streak: 0, best_combo: 0, total_attempts: 0, total_correct: 0 });
      const me = await getMe();
      setAuth(data.access_token, me);
      sounds.roomClear();
      navigate("/map");
    } catch (e: unknown) {
      const err = e as { response?: { data?: { detail?: string } } };
      setError(err.response?.data?.detail || "Erreur de connexion");
    } finally { setLoading(false); }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4 relative overflow-hidden" style={{ background: "#080810" }}>
      <div className="scanlines" />

      {/* Background glow */}
      <div className="absolute inset-0 pointer-events-none">
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] rounded-full opacity-[0.03]" style={{ background: "radial-gradient(circle, #00ff88 0%, transparent 70%)" }} />
      </div>

      <motion.div initial={{ opacity: 0, y: 24 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5, ease: [0.25, 0.46, 0.45, 0.94] }} className="w-full max-w-sm space-y-8 relative">

        {/* Logo block */}
        <div className="text-center space-y-3">
          <motion.div initial={{ scale: 0.8, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} transition={{ delay: 0.1, type: "spring", stiffness: 300 }}>
            <h1 className="text-4xl font-bold font-mono tracking-widest" style={{ color: "#00ff88", textShadow: "0 0 30px rgba(0,255,136,0.3)" }}>C:\DUNGEON</h1>
          </motion.div>
          <p className="text-sm" style={{ color: "#3a3a5c" }}>ECE Lyon — Apprends le C en jouant</p>

          {/* Zone icons */}
          <motion.div className="flex justify-center gap-2 mt-2" initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.3 }}>
            {ZONE_EMOJIS.map((e, i) => (
              <motion.span key={i} initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.35 + i * 0.04 }} className="text-lg" style={{ filter: i < 2 ? "none" : "grayscale(0.7) opacity(0.4)" }}>
                {e}
              </motion.span>
            ))}
          </motion.div>
        </div>

        {/* Auth card */}
        <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }} className="rounded-2xl p-6 space-y-5" style={{ background: "#0f0f1a", border: "1px solid #1e1e35" }}>

          {/* Tabs */}
          <div className="flex rounded-xl p-1 gap-1" style={{ background: "#080810" }}>
            {(["login","register"] as const).map((m) => (
              <button key={m} onClick={() => { setMode(m); setError(""); sounds.click(); }}
                className="flex-1 py-2.5 text-sm font-semibold rounded-lg transition-all duration-200"
                style={{ background: mode === m ? "#00ff88" : "transparent", color: mode === m ? "#080810" : "#3a3a5c" }}
              >
                {m === "login" ? "Connexion" : "Créer un compte"}
              </button>
            ))}
          </div>

          {/* Inputs */}
          <div className="space-y-3">
            <div>
              <label className="label block mb-1.5">Pseudo</label>
              <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} onKeyDown={(e) => e.key === "Enter" && submit()}
                placeholder="ton_pseudo" className="input" maxLength={20} autoComplete="username" />
            </div>
            <div>
              <label className="label block mb-1.5">Mot de passe</label>
              <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} onKeyDown={(e) => e.key === "Enter" && submit()}
                placeholder="••••••••" className="input" autoComplete="current-password" />
            </div>
          </div>

          {error && (
            <motion.div initial={{ opacity: 0, y: -4 }} animate={{ opacity: 1, y: 0 }} className="rounded-xl px-4 py-3 text-sm" style={{ background: "rgba(255,51,85,0.08)", border: "1px solid rgba(255,51,85,0.2)", color: "#ff3355" }}>
              {error}
            </motion.div>
          )}

          <button onClick={submit} disabled={loading || !username || !password} className="btn-accent w-full text-sm py-3 disabled:opacity-30">
            {loading ? "Chargement…" : mode === "login" ? "Entrer dans le donjon →" : "Créer mon compte →"}
          </button>
        </motion.div>

        <motion.p initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.5 }} className="text-center text-xs" style={{ color: "#1e1e35" }}>
          48 challenges · 8 zones · Badges & XP
        </motion.p>
      </motion.div>
    </div>
  );
}
