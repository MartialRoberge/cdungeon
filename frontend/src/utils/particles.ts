/**
 * Lightweight particle burst system.
 * Spawns a canvas overlay, animates, then removes itself.
 * No deps — pure requestAnimationFrame.
 */

interface Particle {
  x: number; y: number;
  vx: number; vy: number;
  life: number; maxLife: number;
  radius: number;
  color: string;
}

export function burstParticles(
  originX: number,
  originY: number,
  color = "#00ff88",
  count = 24
) {
  const canvas = document.createElement("canvas");
  canvas.style.cssText = `
    position:fixed;top:0;left:0;width:100vw;height:100vh;
    pointer-events:none;z-index:9998;
  `;
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
  document.body.appendChild(canvas);
  const ctx = canvas.getContext("2d")!;

  const particles: Particle[] = Array.from({ length: count }, () => {
    const angle = Math.random() * Math.PI * 2;
    const speed = 2 + Math.random() * 6;
    return {
      x: originX,
      y: originY,
      vx: Math.cos(angle) * speed,
      vy: Math.sin(angle) * speed - 2,
      life: 1,
      maxLife: 0.6 + Math.random() * 0.6,
      radius: 2 + Math.random() * 3,
      color,
    };
  });

  let running = true;

  function frame() {
    if (!running) return;
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    let alive = 0;

    for (const p of particles) {
      p.x += p.vx;
      p.y += p.vy;
      p.vy += 0.15; // gravity
      p.life -= 0.025;
      if (p.life <= 0) continue;
      alive++;
      ctx.globalAlpha = Math.max(0, p.life);
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
      ctx.fillStyle = p.color;
      ctx.fill();
    }

    ctx.globalAlpha = 1;
    if (alive > 0) requestAnimationFrame(frame);
    else {
      canvas.remove();
      running = false;
    }
  }

  requestAnimationFrame(frame);
}

export function shakeScreen(intensity = 6, duration = 400) {
  const el = document.getElementById("root");
  if (!el) return;
  const start = Date.now();
  function frame() {
    const elapsed = Date.now() - start;
    if (elapsed >= duration) { (el as HTMLElement).style.transform = ""; return; }
    const progress = elapsed / duration;
    const amp = intensity * (1 - progress);
    const dx = (Math.random() - 0.5) * amp;
    const dy = (Math.random() - 0.5) * amp;
    (el as HTMLElement).style.transform = `translate(${dx}px, ${dy}px)`;
    requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
}
