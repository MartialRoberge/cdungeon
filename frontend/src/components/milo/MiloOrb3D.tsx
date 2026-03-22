import { useEffect, useRef, useState } from "react";
import * as THREE from "three";

interface MiloOrb3DProps {
  state: "idle" | "listening" | "processing" | "speaking";
  audioLevel: number;
  size?: number;
}

// Milo colors — dark teal matching the reference orb
const COLORS = {
  core: new THREE.Color("#1a6b5a"),
  mid: new THREE.Color("#0d4a40"),
  edge: new THREE.Color("#071f1b"),
  glow: new THREE.Color("#5ec4a8"),
};

const vertexShader = `
  uniform float uTime;
  uniform float uAudioLevel;
  uniform float uAudioVelocity;
  uniform float uNoiseStrength;
  uniform float uReactivePhase;
  uniform float uMode;

  varying vec3 vNormal;
  varying vec3 vPosition;
  varying float vDisplacement;

  vec4 permute(vec4 x) { return mod(((x*34.0)+1.0)*x, 289.0); }
  vec4 taylorInvSqrt(vec4 r) { return 1.79284291400159 - 0.85373472095314 * r; }

  float snoise(vec3 v) {
    const vec2 C = vec2(1.0/6.0, 1.0/3.0);
    const vec4 D = vec4(0.0, 0.5, 1.0, 2.0);
    vec3 i = floor(v + dot(v, C.yyy));
    vec3 x0 = v - i + dot(i, C.xxx);
    vec3 g = step(x0.yzx, x0.xyz);
    vec3 l = 1.0 - g;
    vec3 i1 = min(g.xyz, l.zxy);
    vec3 i2 = max(g.xyz, l.zxy);
    vec3 x1 = x0 - i1 + C.xxx;
    vec3 x2 = x0 - i2 + C.yyy;
    vec3 x3 = x0 - D.yyy;
    i = mod(i, 289.0);
    vec4 p = permute(permute(permute(
      i.z + vec4(0.0, i1.z, i2.z, 1.0))
      + i.y + vec4(0.0, i1.y, i2.y, 1.0))
      + i.x + vec4(0.0, i1.x, i2.x, 1.0));
    float n_ = 1.0/7.0;
    vec3 ns = n_ * D.wyz - D.xzx;
    vec4 j = p - 49.0 * floor(p * ns.z * ns.z);
    vec4 x_ = floor(j * ns.z);
    vec4 y_ = floor(j - 7.0 * x_);
    vec4 x = x_ * ns.x + ns.yyyy;
    vec4 y = y_ * ns.x + ns.yyyy;
    vec4 h = 1.0 - abs(x) - abs(y);
    vec4 b0 = vec4(x.xy, y.xy);
    vec4 b1 = vec4(x.zw, y.zw);
    vec4 s0 = floor(b0) * 2.0 + 1.0;
    vec4 s1 = floor(b1) * 2.0 + 1.0;
    vec4 sh = -step(h, vec4(0.0));
    vec4 a0 = b0.xzyw + s0.xzyw * sh.xxyy;
    vec4 a1 = b1.xzyw + s1.xzyw * sh.zzww;
    vec3 p0 = vec3(a0.xy, h.x);
    vec3 p1 = vec3(a0.zw, h.y);
    vec3 p2 = vec3(a1.xy, h.z);
    vec3 p3 = vec3(a1.zw, h.w);
    vec4 norm = taylorInvSqrt(vec4(dot(p0,p0), dot(p1,p1), dot(p2,p2), dot(p3,p3)));
    p0 *= norm.x; p1 *= norm.y; p2 *= norm.z; p3 *= norm.w;
    vec4 m = max(0.6 - vec4(dot(x0,x0), dot(x1,x1), dot(x2,x2), dot(x3,x3)), 0.0);
    m = m * m;
    return 42.0 * dot(m*m, vec4(dot(p0,x0), dot(p1,x1), dot(p2,x2), dot(p3,x3)));
  }

  void main() {
    vNormal = normalize(normalMatrix * normal);
    vPosition = position;
    float breathTime = uTime * 0.1;
    float breathe = snoise(position * 0.35 + breathTime * 0.3) * 0.07;
    breathe += snoise(position * 0.6 + breathTime * 0.5 + 50.0) * 0.05;
    breathe += snoise(position * 0.9 + breathTime * 0.4 + 100.0) * 0.03;
    breathe += sin(uTime * 0.35) * 0.015;

    float idleWave = snoise(position * 0.5 + uTime * 0.08) * 0.3;
    float idleDisp = idleWave * uNoiseStrength * 0.4;

    float listenWave = snoise(position * 0.8 + vec3(uReactivePhase * 0.4, 0.0, 0.0));
    float listenWave2 = snoise(position * 1.2 + vec3(0.0, uReactivePhase * 0.3, uTime * 0.1));
    float velocityRipple = snoise(position * 2.0 + uTime * 2.0) * uAudioVelocity * 0.5;
    float listenDisp = (listenWave * 0.4 + listenWave2 * 0.3 + velocityRipple) * uNoiseStrength;

    float thinkWave = snoise(position * 0.5 + uTime * 0.3);
    float thinkWave2 = snoise(position * 0.8 + uTime * 0.2 + 30.0) * 0.5;
    float processDisp = (thinkWave + thinkWave2) * uNoiseStrength * 0.5;

    float speakPulse = sin(uReactivePhase * 3.0) * 0.3;
    float speakWave = snoise(position * 0.6 + vec3(uReactivePhase * 0.5, uTime * 0.2, 0.0));
    float speakDetail = snoise(position * 1.5 + uTime * 0.5) * 0.2;
    float speakDisp = (speakPulse + speakWave * 0.5 + speakDetail) * uNoiseStrength;

    float idleWeight = 1.0 - smoothstep(0.0, 1.0, uMode);
    float listenWeight = smoothstep(0.0, 1.0, uMode) * (1.0 - smoothstep(1.0, 2.0, uMode));
    float processWeight = smoothstep(1.0, 2.0, uMode) * (1.0 - smoothstep(2.0, 3.0, uMode));
    float speakWeight = smoothstep(2.0, 3.0, uMode);

    float reactiveDisp = idleDisp * idleWeight + listenDisp * listenWeight + processDisp * processWeight + speakDisp * speakWeight;
    float totalDisplacement = breathe + reactiveDisp;
    vDisplacement = totalDisplacement;
    vec3 newPosition = position + normal * totalDisplacement;
    gl_Position = projectionMatrix * modelViewMatrix * vec4(newPosition, 1.0);
  }
`;

const fragmentShader = `
  uniform float uTime;
  uniform float uAudioLevel;
  uniform vec3 uColorCore;
  uniform vec3 uColorMid;
  uniform vec3 uColorEdge;
  uniform vec3 uColorGlow;

  varying vec3 vNormal;
  varying vec3 vPosition;
  varying float vDisplacement;

  void main() {
    vec3 viewDirection = normalize(cameraPosition - vPosition);
    float fresnel = pow(1.0 - abs(dot(vNormal, viewDirection)), 2.5);
    float gradientPos = (vPosition.y + 1.0) / 2.0;
    vec3 baseColor = mix(uColorEdge, uColorCore, gradientPos);
    float dispColor = (vDisplacement + 0.5) * 0.5;
    baseColor = mix(baseColor, uColorMid, dispColor * 0.3);
    float brightness = 0.9 + uAudioLevel * 0.25;
    baseColor *= brightness;
    vec3 glowColor = uColorGlow * fresnel * (0.5 + uAudioLevel * 0.5);
    vec3 finalColor = baseColor + glowColor;
    float alpha = 0.94 + fresnel * 0.06;
    gl_FragColor = vec4(finalColor, alpha);
  }
`;

export default function MiloOrb3D({ state, audioLevel, size = 200 }: MiloOrb3DProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const rendererRef = useRef<THREE.WebGLRenderer | null>(null);
  const materialRef = useRef<THREE.ShaderMaterial | null>(null);
  const meshRef = useRef<THREE.Mesh | null>(null);
  const animationRef = useRef<number>(0);
  const startTimeRef = useRef(performance.now());
  const [ready, setReady] = useState(false);

  const smoothAudioRef = useRef(0);
  const prevAudioRef = useRef(0);
  const audioVelocityRef = useRef(0);
  const reactivePhaseRef = useRef(0);
  const smoothNoiseRef = useRef(0.12);
  const smoothModeRef = useRef(0);
  const stateRef = useRef(state);
  const audioRef = useRef(audioLevel);

  useEffect(() => { stateRef.current = state; }, [state]);
  useEffect(() => { audioRef.current = audioLevel; }, [audioLevel]);

  useEffect(() => {
    if (!containerRef.current) return;
    const t = setTimeout(() => setReady(true), 50);
    return () => clearTimeout(t);
  }, []);

  useEffect(() => {
    if (!containerRef.current || !ready) return;
    const el = containerRef.current;
    const w = el.offsetWidth;
    const h = el.offsetHeight;

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(45, w / h, 0.1, 100);
    camera.position.z = 4.5;

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, premultipliedAlpha: false });
    renderer.setSize(w, h);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.setClearColor(0x000000, 0);
    el.appendChild(renderer.domElement);
    rendererRef.current = renderer;

    const geo = new THREE.IcosahedronGeometry(0.7, 64);
    const mat = new THREE.ShaderMaterial({
      vertexShader,
      fragmentShader,
      uniforms: {
        uTime: { value: 0 },
        uAudioLevel: { value: 0 },
        uAudioVelocity: { value: 0 },
        uNoiseStrength: { value: 0.08 },
        uReactivePhase: { value: 0 },
        uMode: { value: 0 },
        uColorCore: { value: COLORS.core },
        uColorMid: { value: COLORS.mid },
        uColorEdge: { value: COLORS.edge },
        uColorGlow: { value: COLORS.glow },
      },
      transparent: true,
      side: THREE.FrontSide,
    });
    materialRef.current = mat;

    const mesh = new THREE.Mesh(geo, mat);
    scene.add(mesh);
    meshRef.current = mesh;

    const onResize = () => {
      const nw = el.offsetWidth, nh = el.offsetHeight;
      camera.aspect = nw / nh;
      camera.updateProjectionMatrix();
      renderer.setSize(nw, nh);
    };
    window.addEventListener("resize", onResize);

    const animate = () => {
      const t = (performance.now() - startTimeRef.current) / 1000;
      const raw = audioRef.current;
      const cs = stateRef.current;

      smoothAudioRef.current += (raw - smoothAudioRef.current) * 0.08;
      const audio = smoothAudioRef.current;
      const delta = Math.abs(audio - prevAudioRef.current);
      audioVelocityRef.current += (delta * 10 - audioVelocityRef.current) * 0.15;
      prevAudioRef.current = audio;
      const vel = Math.min(audioVelocityRef.current, 1);

      let tMode = 0, tNoise = 0.08, pRate = 0.008, pDecay = 0.015;
      if (cs === "listening") { tMode = 1; tNoise = 0.14 + audio * 0.12; pRate = 0.015 + audio * 0.06; pDecay = 0.004; }
      else if (cs === "processing") { tMode = 2; tNoise = 0.16; pRate = 0.02; pDecay = 0.006; }
      else if (cs === "speaking") { tMode = 3; tNoise = 0.14 + audio * 0.1; pRate = 0.012 + audio * 0.05; pDecay = 0.005; }
      else { tMode = 0; tNoise = 0.1; pRate = 0.005; pDecay = 0.008; }

      smoothModeRef.current += (tMode - smoothModeRef.current) * 0.025;
      if (cs === "idle") reactivePhaseRef.current *= (1 - pDecay);
      else reactivePhaseRef.current += pRate;
      smoothNoiseRef.current += (tNoise - smoothNoiseRef.current) * 0.018;

      if (mat) {
        mat.uniforms.uTime.value = t;
        mat.uniforms.uAudioLevel.value = audio;
        mat.uniforms.uAudioVelocity.value = vel;
        mat.uniforms.uNoiseStrength.value = smoothNoiseRef.current;
        mat.uniforms.uReactivePhase.value = reactivePhaseRef.current;
        mat.uniforms.uMode.value = smoothModeRef.current;
      }

      if (mesh) {
        mesh.rotation.y = t * 0.05;
        mesh.rotation.x = Math.sin(t * 0.08) * 0.05;
        mesh.rotation.z = Math.sin(t * 0.06) * 0.03;
        mesh.position.y = Math.sin(t * 0.3) * 0.02;
        mesh.scale.setScalar(1 + audio * 0.025 + Math.sin(t * 0.4) * 0.008);
      }

      renderer.render(scene, camera);
      animationRef.current = requestAnimationFrame(animate);
    };
    animate();

    return () => {
      window.removeEventListener("resize", onResize);
      cancelAnimationFrame(animationRef.current);
      if (el.contains(renderer.domElement)) el.removeChild(renderer.domElement);
      geo.dispose();
      mat.dispose();
      renderer.dispose();
    };
  }, [ready]);

  return (
    <div className="relative" style={{ width: size, height: size }}>
      {/* Glow halo */}
      <div
        className="absolute pointer-events-none"
        style={{
          top: "50%", left: "50%",
          transform: "translate(-50%, -50%)",
          width: size * 2, height: size * 2,
          borderRadius: "50%",
          background: "radial-gradient(circle, rgba(94,196,168,0.25) 0%, rgba(26,107,90,0.1) 30%, rgba(7,31,27,0.03) 60%, transparent 80%)",
          filter: "blur(30px)",
          opacity: state === "idle" ? 0.3 : 0.6,
          transition: "opacity 0.5s ease",
        }}
      />
      {/* Three.js canvas */}
      <div ref={containerRef} className="absolute inset-0" style={{ zIndex: 2 }} />
    </div>
  );
}
