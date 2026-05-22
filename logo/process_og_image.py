"""
OGP用シェア画像を生成する。
hero.jpg（墨絵アート）に「人道」ロゴをオーバーレイして、
1200x630pxのシェア用画像を作成。
"""
import sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from PIL import Image

ROOT = "c:/Users/aidma-1094/OneDrive/pmi-ai/pmi-solutions/kaimaku/hitomichi-interview"
HERO = os.path.join(ROOT, "assets", "hero.jpg")
LOGO = os.path.join(ROOT, "assets", "logo-mark.png")
DST  = os.path.join(ROOT, "assets", "og-image.jpg")

TARGET_W, TARGET_H = 1200, 630

# ----- Step 1: hero.jpg を 1200x630 にセンタークロップ -----
hero = Image.open(HERO).convert("RGB")
w, h = hero.size

# 縦幅630にスケール
scale = TARGET_H / h
new_w = int(w * scale)
hero_scaled = hero.resize((new_w, TARGET_H), Image.LANCZOS)

# 横方向をセンタークロップ or 余白追加
if new_w >= TARGET_W:
    # 横が長い → センタークロップ
    left = (new_w - TARGET_W) // 2
    hero_cropped = hero_scaled.crop((left, 0, left + TARGET_W, TARGET_H))
else:
    # 横が短い → 余白追加（紙の色に近いオフホワイト）
    hero_cropped = Image.new("RGB", (TARGET_W, TARGET_H), (243, 240, 235))
    hero_cropped.paste(hero_scaled, ((TARGET_W - new_w) // 2, 0))


# ----- Step 2: ロゴを左側に配置 -----
logo = Image.open(LOGO).convert("RGBA")
# ロゴをリサイズ（高さ280px程度）
logo_h = 280
logo_w = int(logo.size[0] * logo_h / logo.size[1])
logo = logo.resize((logo_w, logo_h), Image.LANCZOS)

# 左側中央に配置
logo_x = 100
logo_y = (TARGET_H - logo_h) // 2
hero_cropped_rgba = hero_cropped.convert("RGBA")
hero_cropped_rgba.paste(logo, (logo_x, logo_y), logo)


# ----- Step 3: 保存 -----
final = hero_cropped_rgba.convert("RGB")
final.save(DST, "JPEG", quality=90, optimize=True, progressive=True)

print(f"OGP画像生成完了:")
print(f"  {DST}")
print(f"  {final.size[0]}x{final.size[1]}  ({os.path.getsize(DST)/1024:.0f} KB)")
