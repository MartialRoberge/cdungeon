from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import time
from app.config import settings


CACHE_TTL = 3600  # 1 hour


def _font(size: int):
    font_paths = [
        "/System/Library/Fonts/Supplemental/CourierNewBold.ttf",
        "/System/Library/Fonts/Monaco.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf",
    ]
    for fp in font_paths:
        if Path(fp).exists():
            try:
                return ImageFont.truetype(fp, size)
            except Exception:
                continue
    return ImageFont.load_default()


def generate_share_card(player_data: dict) -> Path:
    cache_path = settings.share_cache_dir / f"{player_data['id']}.png"

    # Check cache
    if cache_path.exists():
        age = time.time() - cache_path.stat().st_mtime
        if age < CACHE_TTL:
            return cache_path

    W, H = 600, 314
    img = Image.new("RGB", (W, H), color="#0a0a0f")
    draw = ImageDraw.Draw(img)

    # Background grid lines (subtle)
    for y in range(0, H, 20):
        draw.line([(0, y), (W, y)], fill="#12121a", width=1)
    for x in range(0, W, 20):
        draw.line([(x, 0), (x, H)], fill="#12121a", width=1)

    # Border
    draw.rectangle([(2, 2), (W - 3, H - 3)], outline="#00ff88", width=2)
    draw.rectangle([(6, 6), (W - 7, H - 7)], outline="#00ff8830", width=1)

    # Title bar
    draw.rectangle([(2, 2), (W - 3, 45)], fill="#00ff8815")
    draw.text((16, 12), "C:\\DUNGEON", font=_font(18), fill="#00ff88")
    draw.text((W - 120, 12), "ECE Lyon", font=_font(14), fill="#4a4a6a")

    # Username
    username = player_data.get("username", "???")
    draw.text((16, 60), f">>> {username}", font=_font(22), fill="#ffffff")

    # Level
    level = player_data.get("level", 1)
    xp = player_data.get("xp", 0)
    draw.text((16, 92), f"NIVEAU {level}", font=_font(14), fill="#ffaa00")

    # XP bar
    bar_x, bar_y, bar_w, bar_h = 16, 115, W - 32, 12
    draw.rectangle([(bar_x, bar_y), (bar_x + bar_w, bar_y + bar_h)], fill="#12121a", outline="#2a2a3d")
    from app.services.attempt_service import xp_for_level
    prev = xp_for_level(level)
    next_lvl = xp_for_level(level + 1)
    progress = min((xp - prev) / max(next_lvl - prev, 1), 1.0)
    fill_w = int(bar_w * progress)
    if fill_w > 0:
        draw.rectangle([(bar_x, bar_y), (bar_x + fill_w, bar_y + bar_h)], fill="#00ff88")
    draw.text((bar_x, bar_y + 16), f"{xp} XP  →  {next_lvl} XP pour niveau {level + 1}", font=_font(10), fill="#4a4a6a")

    # Zone progress
    current_zone = player_data.get("current_zone", 1)
    zone_names = ["Stack Village", "Logic Labyrinth", "Function Factory", "Data Fortress",
                  "Pointer Abyss", "String Caverns", "Heap Wastes", "File Sanctum"]
    zone_emojis = ["🏠", "🌀", "⚙️", "🏰", "🕳️", "🔤", "☣️", "📜"]
    draw.text((16, 148), "PROGRESSION :", font=_font(11), fill="#4a4a6a")
    for i in range(8):
        x_pos = 16 + i * 72
        cleared = i + 1 < current_zone
        active = i + 1 == current_zone
        color = "#00ff88" if cleared else ("#ffaa00" if active else "#2a2a3d")
        draw.rectangle([(x_pos, 165), (x_pos + 62, 195)], fill=color if cleared else "#12121a", outline=color)
        short = zone_names[i][:6]
        draw.text((x_pos + 4, 170), short, font=_font(9), fill="#ffffff" if cleared else color)

    # Badges
    badges = player_data.get("badges", [])
    draw.text((16, 210), f"BADGES OBTENUS : {len(badges)}", font=_font(11), fill="#4a4a6a")
    badge_names = [b.get("name", "?") for b in badges[:5]]
    badge_str = "  ·  ".join(badge_names) if badge_names else "Aucun badge encore..."
    draw.text((16, 228), badge_str, font=_font(11), fill="#ffaa00")

    # Stats
    combo = player_data.get("best_combo", 0)
    total = player_data.get("total_attempts", 0)
    correct = player_data.get("total_correct", 0)
    acc = int(correct / total * 100) if total > 0 else 0
    draw.text((16, 255), f"Meilleur combo : x{combo}   |   Précision : {acc}%   |   Tentatives : {total}", font=_font(11), fill="#4a4a6a")

    # Footer
    draw.text((16, H - 28), "Partage ton aventure ! → cdungeon.ece.fr", font=_font(11), fill="#2a2a3d")

    img.save(cache_path, "PNG", optimize=True)
    return cache_path
