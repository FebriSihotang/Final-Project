import os, shutil, pathlib, stat

TARGET = pathlib.Path("/data/work/Mask_Tileswork")

p = TARGET.resolve()
root = pathlib.Path("/data/work").resolve()

if not p.exists():
    print(f"Path tidak ditemukan: {p}")
elif not p.is_dir():
    raise RuntimeError(f"Bukan direktori: {p}")
elif p == root:
    raise RuntimeError("Menolak menghapus root /data/work.")
elif root not in p.parents:
    raise RuntimeError(f"Menolak menghapus di luar {root}: {p}")
else:
    print(f"Siap menghapus: {p}")

def _on_rm_error(func, path, excinfo):
    try:
        os.chmod(path, stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)
        func(path)
    except Exception as e:
        print(f"Gagal menghapus: {path} -> {e}")

# ⚠️ PROSES PENGHAPUSAN PAKSA
shutil.rmtree(p, onerror=_on_rm_error)
print(f"Berhasil dihapus: {p}")