import { create } from "zustand";

interface Player {
  id: number;
  username: string;
  xp: number;
  level: number;
  current_zone: number;
  daily_streak: number;
  best_combo: number;
  total_attempts: number;
  total_correct: number;
}

interface AuthState {
  token: string | null;
  player: Player | null;
  setAuth: (token: string, player: Player) => void;
  updatePlayer: (p: Partial<Player>) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  token: localStorage.getItem("token"),
  player: (() => {
    try { return JSON.parse(localStorage.getItem("player") || "null"); }
    catch { return null; }
  })(),
  setAuth: (token, player) => {
    localStorage.setItem("token", token);
    localStorage.setItem("player", JSON.stringify(player));
    set({ token, player });
  },
  updatePlayer: (p) =>
    set((s) => {
      const updated = s.player ? { ...s.player, ...p } : null;
      if (updated) localStorage.setItem("player", JSON.stringify(updated));
      return { player: updated };
    }),
  logout: () => {
    localStorage.removeItem("token");
    localStorage.removeItem("player");
    set({ token: null, player: null });
  },
}));

interface GameState {
  hp: number;
  combo: number;
  startTime: number | null;
  resetHp: () => void;
  loseHp: () => void;
  incrementCombo: () => void;
  resetCombo: () => void;
  setStartTime: () => void;
  getElapsedMs: () => number;
}

export const useGameStore = create<GameState>((set, get) => ({
  hp: 3,
  combo: 1,
  startTime: null,
  resetHp: () => set({ hp: 3 }),
  loseHp: () => set((s) => ({ hp: Math.max(0, s.hp - 1) })),
  incrementCombo: () => set((s) => ({ combo: s.combo + 1 })),
  resetCombo: () => set({ combo: 1 }),
  setStartTime: () => set({ startTime: Date.now() }),
  getElapsedMs: () => {
    const s = get().startTime;
    return s ? Date.now() - s : 5000;
  },
}));
