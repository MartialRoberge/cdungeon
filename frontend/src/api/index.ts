import client from "./client";

// Auth
export const register = (username: string, password: string) =>
  client.post("/auth/register", { username, password }).then((r) => r.data);
export const login = (username: string, password: string) =>
  client.post("/auth/login", { username, password }).then((r) => r.data);

// Player
export const getMe = () => client.get("/player/me").then((r) => r.data);
export const getMyBadges = () => client.get("/player/badges").then((r) => r.data);

// Dungeon
export const getZones = () => client.get("/dungeon/zones").then((r) => r.data);
export const getZoneRooms = (zoneNumber: number) =>
  client.get(`/dungeon/zones/${zoneNumber}/rooms`).then((r) => r.data);
export const getRoom = (roomId: string) =>
  client.get(`/dungeon/rooms/${roomId}`).then((r) => r.data);

// Attempt
export const submitAttempt = (roomId: string, answer: unknown, combo: number, timeMs: number) =>
  client.post(`/rooms/${roomId}/attempt`, { answer, combo, time_ms: timeMs }).then((r) => r.data);

// Leaderboard
export const getLeaderboard = (by = "xp") =>
  client.get(`/leaderboard?by=${by}`).then((r) => r.data);

// Share
export const getShareUrl = () => `${client.defaults.baseURL}/share/me`;
