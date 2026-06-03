# Converter Tif to Png

import argparse
from pathlib import Path
from PIL import Image, UnidentifiedImageError

Image.MAX_IMAGE_PIXELS = None

def convert_one(src_path: Path, to: str, page: int = 0) -> Path:
    to = to.lower()
    if to not in {"png", "jpg", "jpeg"}:
        raise ValueError("Format tujuan harus salah satu dari: png, jpg, jpeg")

    out_ext = "jpg" if to in {"jpg", "jpeg"} else "png"
    out_path = src_path.with_suffix("." + out_ext)

    try:
        with Image.open(src_path) as im:
            try:
                if getattr(im, "n_frames", 1) > 1:
                    im.seek(page)
            except EOFError:
                raise SystemExit(f"Halaman {page} tidak ada di {src_path}")

            dpi = im.info.get("dpi")
            icc = im.info.get("icc_profile")

            save_kwargs = {}
            if out_ext == "jpg":
                if im.mode in ("RGBA", "LA", "P"):
                    im = im.convert("RGB")
                elif im.mode not in ("RGB", "L"):
                    im = im.convert("RGB")
                # Kualitas tinggi, non-subsampled
                save_kwargs.update(dict(quality=95, subsampling=0, optimize=True))
            else:
                if im.mode == "F":
                    import numpy as np
                    arr = np.array(im, dtype="float32")
                    lo, hi = float(arr.min()), float(arr.max())
                    if hi > lo:
                        arr = (65535.0 * (arr - lo) / (hi - lo)).astype("uint16")
                    else:
                        arr = (arr * 0).astype("uint16")
                    im = Image.fromarray(arr, mode="I;16")
                save_kwargs.update(dict(optimize=True, compress_level=9))

            if dpi: save_kwargs["dpi"] = dpi
            if icc: save_kwargs["icc_profile"] = icc

            im.save(out_path, **save_kwargs)
    except UnidentifiedImageError:
        raise SystemExit(f"File bukan TIFF valid: {src_path}")
    except Image.DecompressionBombError as e:
        raise SystemExit(
            f"Gambar terlalu besar menurut batas Pillow. "
            f"Coba jalankan lagi setelah memastikan Image.MAX_IMAGE_PIXELS=None. Detail: {e}"
        )

    print(f"Sukses: {out_path}")
    return out_path

def main():
    p = argparse.ArgumentParser(
        description="Konversi file .tif ke .png atau .jpg tanpa mengubah resolusi."
    )
    p.add_argument("src", help="Path ke file .tif")
    p.add_argument("--to", default="png", help="Format tujuan: png atau jpg (default: png)")
    p.add_argument("--page", type=int, default=0, help="Index halaman untuk multipage TIFF (default: 0)")
    args = p.parse_args()

    src_path = Path(args.src)
    if not src_path.exists():
        raise SystemExit(f"Tidak ditemukan: {src_path}")

    convert_one(src_path, args.to, args.page)

if __name__ == "__main__":
    main()
