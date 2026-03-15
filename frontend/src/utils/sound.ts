let ctx: AudioContext | null = null;

function getCtx(): AudioContext {
  if (!ctx) ctx = new AudioContext();
  if (ctx.state === "suspended") ctx.resume();
  return ctx;
}

function play(frequency: number, type: OscillatorType, duration: number, gainStart: number, gainEnd: number, delay = 0) {
  try {
    const c = getCtx();
    const osc = c.createOscillator();
    const gain = c.createGain();
    osc.connect(gain);
    gain.connect(c.destination);
    osc.type = type;
    osc.frequency.setValueAtTime(frequency, c.currentTime + delay);
    gain.gain.setValueAtTime(gainStart, c.currentTime + delay);
    gain.gain.exponentialRampToValueAtTime(Math.max(gainEnd, 0.001), c.currentTime + delay + duration);
    osc.start(c.currentTime + delay);
    osc.stop(c.currentTime + delay + duration);
  } catch {}
}

export const sounds = {
  click() { play(800, "sine", 0.06, 0.06, 0.001); },
  correct() {
    play(523, "sine", 0.08, 0.12, 0.001);
    play(659, "sine", 0.12, 0.12, 0.001, 0.08);
    play(784, "sine", 0.2, 0.14, 0.001, 0.16);
  },
  wrong() {
    play(200, "sine", 0.15, 0.08, 0.001);
    play(150, "sine", 0.1, 0.05, 0.001, 0.08);
  },
  xpGain() { [0, 0.05, 0.1].forEach((d, i) => play(600 + i * 100, "sine", 0.08, 0.04, 0.001, d)); },
  levelUp() { [523, 659, 784, 1047].forEach((f, i) => play(f, "sine", 0.25, 0.15, 0.001, i * 0.1)); },
  badge() { [880, 1046, 1318, 1568].forEach((f, i) => play(f, "triangle", 0.3, 0.12, 0.001, i * 0.08)); },
  bossEnter() {
    play(80, "sawtooth", 0.8, 0.15, 0.001);
    play(60, "sine", 1.0, 0.1, 0.001, 0.1);
    play(440, "sine", 0.3, 0.08, 0.001, 0.6);
    play(659, "sine", 0.3, 0.1, 0.001, 0.9);
  },
  bossDefeated() { [392, 523, 659, 784, 1047].forEach((f, i) => play(f, "sine", 0.4, 0.18, 0.001, i * 0.12)); },
  roomClear() { play(523, "sine", 0.12, 0.1, 0.001); play(784, "sine", 0.18, 0.12, 0.001, 0.1); },
  combo(n: number) { play(Math.min(400 + n * 40, 900), "sine", 0.05, 0.06, 0.001); },
  hpLost() { play(180, "sawtooth", 0.12, 0.08, 0.001); play(100, "sine", 0.15, 0.05, 0.001, 0.05); },
};

export function initAudio() { getCtx(); }
