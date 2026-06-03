#!/usr/bin/env python
import zipfile
from pathlib import Path
import shutil
import sys

BASE_DIR = Path("/data/work")
zip_path = BASE_DIR / "hover_net-master.zip"
target_dir = BASE_DIR / "hover_net"

print(f"ZIP path  : {zip_path}")
print(f"Target dir: {target_dir}")

if not zip_path.is_file():
    print(f"[ERROR] File ZIP tidak ditemukan: {zip_path}")
    sys.exit(1)

if target_dir.exists():
    print(f"[ERROR] Folder target sudah ada: {target_dir}")
    print("Hapus / rename dulu folder tersebut kalau ingin ekstrak ulang.")
    sys.exit(1)

# 1) Ekstrak ZIP ke /data/work
print("[INFO] Mengekstrak zip ke /data/work ...")
with zipfile.ZipFile(zip_path, "r") as zf:
    zf.extractall(BASE_DIR)

# 2) Cari folder hasil ekstrak (hover_net-master atau semacamnya)
candidates = [p for p in BASE_DIR.iterdir() if p.is_dir() and p.name.startswith("hover_net")]
print("[INFO] Kandidat folder hasil ekstrak:", [c.name for c in candidates])

src_dir = None
for c in candidates:
    # pilih folder yang bukan target_dir dan bukan folder lama
    if c.name != "hover_net":
        src_dir = c
        break

if src_dir is None:
    print("[ERROR] Tidak menemukan folder hasil ekstrak yang cocok (hover_net-*)")
    sys.exit(1)

print(f"[INFO] Rename {src_dir} -> {target_dir}")
src_dir.rename(target_dir)

print("[SUKSES] Repo HoverNet siap di:", target_dir)
