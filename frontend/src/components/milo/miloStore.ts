import { create } from "zustand";

export interface MiloMessage {
  role: "user" | "milo";
  text: string;
}

export interface MiloContext {
  roomId?: string;
  title?: string;
  challengeType?: string;
  conceptTags?: string[];
  difficulty?: number;
  questionPrompt?: string;
}

interface MiloState {
  messages: MiloMessage[];
  isLoading: boolean;
  context: MiloContext | null;
  addMessage: (msg: MiloMessage) => void;
  setLoading: (v: boolean) => void;
  setContext: (ctx: MiloContext | null) => void;
  clearMessages: () => void;
}

export const useMiloStore = create<MiloState>((set) => ({
  messages: [],
  isLoading: false,
  context: null,
  addMessage: (msg) => set((s) => ({ messages: [...s.messages, msg] })),
  setLoading: (v) => set({ isLoading: v }),
  setContext: (ctx) => set({ context: ctx }),
  clearMessages: () => set({ messages: [] }),
}));
