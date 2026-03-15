#!/bin/bash
# C:\DUNGEON - Script de lancement

echo "🎮 Démarrage de C:\DUNGEON..."
echo ""

# Kill existing processes
pkill -f "uvicorn app.main" 2>/dev/null
pkill -f "vite" 2>/dev/null
sleep 1

# Start backend
echo "🐍 Backend FastAPI → http://localhost:8123"
cd "$(dirname "$0")/backend"
.venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8123 &
BACKEND_PID=$!
sleep 2

# Check backend health
if curl -s http://localhost:8123/ > /dev/null 2>&1; then
    echo "   ✅ Backend OK"
else
    echo "   ❌ Backend failed to start"
    exit 1
fi

# Start frontend
echo "⚛️  Frontend React → http://localhost:5174 (ou 5173)"
cd "$(dirname "$0")/frontend"
npm run dev &
FRONTEND_PID=$!
sleep 3

echo ""
echo "╔══════════════════════════════════════╗"
echo "║      C:\\DUNGEON - PRÊT À JOUER !    ║"
echo "╠══════════════════════════════════════╣"
echo "║  🌐 Ouvrir: http://localhost:5174    ║"
echo "║  📚 API docs: http://localhost:8123/docs ║"
echo "╚══════════════════════════════════════╝"
echo ""
echo "Ctrl+C pour arrêter"

# Wait for interrupt
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; echo 'Arrêté.'" INT
wait
