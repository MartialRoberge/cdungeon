import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { useLocation } from "react-router-dom";
import MiloOrb3D from "./MiloOrb3D";
import MiloChat from "./MiloChat";

export default function MiloOrb() {
  const [open, setOpen] = useState(false);
  const location = useLocation();

  // Don't show on room pages (Milo is embedded there)
  if (location.pathname.startsWith("/room/")) return null;

  return (
    <>
      {/* Floating 3D orb button */}
      <AnimatePresence>
        {!open && (
          <motion.div
            initial={{ scale: 0, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0, opacity: 0 }}
            className="fixed bottom-4 right-4 z-50 cursor-pointer"
            onClick={() => setOpen(true)}
          >
            <MiloOrb3D state="idle" audioLevel={0} size={72} />
          </motion.div>
        )}
      </AnimatePresence>

      {/* Popup panel */}
      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ opacity: 0, scale: 0.9, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.9, y: 20 }}
            transition={{ type: "spring", stiffness: 400, damping: 30 }}
            className="fixed bottom-4 right-4 sm:bottom-4 sm:right-4 z-50 flex flex-col rounded-2xl overflow-hidden"
            style={{
              width: "min(400px, calc(100vw - 32px))",
              height: "min(600px, calc(100vh - 80px))",
              background: "#0a0a16",
              border: "1px solid rgba(0,255,136,0.15)",
              boxShadow: "0 8px 60px rgba(0,0,0,0.6), 0 0 40px rgba(0,255,136,0.06)",
            }}
          >
            <MiloChat onClose={() => setOpen(false)} />
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}
