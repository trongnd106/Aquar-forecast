#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
gen.py - Xử lý các giá trị dạng "<ngưỡng" trong dữ liệu Excel (left-censored)

Ví dụ:
  python3 gen.py \
    --input "/home/trong/Documents/handle-file/Tong-hop_2021-2024_gop.xlsx" \
    --output "/home/trong/Documents/handle-file/Tong-hop_2021-2024_gop_gen.xlsx" \
    --sheet "Gop_2021_2024" \
    --excel-cols "K,L,M,O,P,R,S,T,V,W,X,Y,Z,AA,AB,AC,AD,AE,AF" \
    --method half \
    --mode replace \
    --seed 42

Ghi chú:
- method=half: thay "<LOD" -> LOD/2 (phổ biến trong dữ liệu môi trường)
- method=uniform: sinh ngẫu nhiên U(0, LOD)
- method=beta: sinh LOD * Beta(a,b) (mặc định a=2,b=8 -> thiên về giá trị nhỏ)
- method=loguniform: sinh log-uniform trong (LOD*min_ratio, LOD)
"""

import argparse
import math
import re
from pathlib import Path
from typing import Iterable, List, Optional, Tuple

import pandas as pd


LT_RE = re.compile(r"^\s*<\s*([0-9]+(?:[.,][0-9]+)?)\s*$")


def excel_col_to_index(col: str) -> int:
    """
    Convert Excel column letter(s) to 0-based index: A->0, B->1, ..., Z->25, AA->26, ...
    """
    s = col.strip().upper()
    if not s or not re.fullmatch(r"[A-Z]+", s):
        raise ValueError(f"Cột Excel không hợp lệ: {col!r}")
    n = 0
    for ch in s:
        n = n * 26 + (ord(ch) - ord("A") + 1)
    return n - 1


def parse_number_maybe(x) -> Optional[float]:
    if x is None or (isinstance(x, float) and pd.isna(x)):
        return None
    s = str(x).strip()
    if not s:
        return None
    # hỗ trợ dấu phẩy thập phân
    s2 = s.replace(",", ".")
    try:
        return float(s2)
    except ValueError:
        return None


def is_left_censored(x) -> Optional[float]:
    """
    Nếu x là dạng '<0.005' hoặc '<0,005' -> trả về LOD (float). Nếu không -> None.
    """
    if x is None or (isinstance(x, float) and pd.isna(x)):
        return None
    s = str(x)
    m = LT_RE.match(s)
    if not m:
        return None
    return float(m.group(1).replace(",", "."))


def gen_from_lod(
    lod: float,
    *,
    method: str,
    rng,
    beta_a: float,
    beta_b: float,
    min_ratio: float,
) -> float:
    if lod <= 0:
        return 0.0

    if method == "half":
        return lod / 2.0
    if method == "uniform":
        return rng.random() * lod
    if method == "beta":
        # random.betavariate có sẵn trong stdlib
        return rng.betavariate(beta_a, beta_b) * lod
    if method == "loguniform":
        lo = max(lod * min_ratio, 1e-12)
        hi = lod
        u = rng.random()
        return math.exp(math.log(lo) + u * (math.log(hi) - math.log(lo)))

    raise ValueError(f"method không hợp lệ: {method!r}")


def parse_excel_cols(s: str) -> List[int]:
    if not s.strip():
        return []
    cols = []
    for part in s.split(","):
        p = part.strip()
        if not p:
            continue
        cols.append(excel_col_to_index(p))
    return cols


def select_columns_by_excel_indices(df: pd.DataFrame, indices: Iterable[int]) -> List[str]:
    cols = []
    for idx in indices:
        if 0 <= idx < len(df.columns):
            cols.append(df.columns[idx])
    # remove duplicates but keep order
    out = []
    seen = set()
    for c in cols:
        if c not in seen:
            out.append(c)
            seen.add(c)
    return out


def auto_detect_columns_with_lt(df: pd.DataFrame) -> List[str]:
    cols = []
    for c in df.columns:
        ser = df[c]
        # scan nhanh: chỉ cần thấy 1 giá trị dạng '<' là chọn cột
        found = False
        for v in ser.head(5000).tolist():  # đủ nhanh cho file lớn
            if is_left_censored(v) is not None:
                found = True
                break
        if found:
            cols.append(c)
    return cols


def process_sheet(
    df: pd.DataFrame,
    *,
    target_cols: List[str],
    method: str,
    mode: str,
    suffix: str,
    rng,
    beta_a: float,
    beta_b: float,
    min_ratio: float,
) -> Tuple[pd.DataFrame, List[Tuple[str, int]]]:
    """
    Returns: (new_df, stats[(col, replaced_count)])
    """
    out = df.copy()
    stats: List[Tuple[str, int]] = []

    for col in target_cols:
        if col not in out.columns:
            continue

        replaced = 0

        def _map(v):
            nonlocal replaced
            lod = is_left_censored(v)
            if lod is not None:
                replaced += 1
                return gen_from_lod(
                    lod,
                    method=method,
                    rng=rng,
                    beta_a=beta_a,
                    beta_b=beta_b,
                    min_ratio=min_ratio,
                )
            # không phải dạng '<...': nếu là số thì parse sang float để model dùng được
            num = parse_number_maybe(v)
            return num if num is not None else v

        if mode == "replace":
            out[col] = out[col].map(_map)
        elif mode == "add":
            new_col = f"{col}{suffix}"
            out[new_col] = out[col].map(_map)
        else:
            raise ValueError(f"mode không hợp lệ: {mode!r}")

        stats.append((str(col), replaced))

    return out, stats


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Sinh giá trị hợp lý cho các ô dạng '<LOD' trong file Excel để phục vụ train/fine-tune."
    )
    ap.add_argument(
        "--input",
        default="/home/trong/Documents/handle-file/Tong-hop_2021-2024_gop.xlsx",
        help="Đường dẫn Excel đầu vào",
    )
    ap.add_argument(
        "--output",
        default="/home/trong/Documents/handle-file/Tong-hop_2021-2024_gop_gen.xlsx",
        help="Đường dẫn Excel đầu ra",
    )
    ap.add_argument(
        "--sheet",
        action="append",
        default=[],
        help="Tên sheet cần xử lý (có thể truyền nhiều lần). Nếu không truyền, xử lý tất cả sheet.",
    )
    ap.add_argument(
        "--header-row",
        type=int,
        default=0,
        help="Dòng header (0-based) khi đọc sheet bằng pandas. Với file gốc Tong-hop.xlsx thường là 1.",
    )
    ap.add_argument(
        "--excel-cols",
        default="",
        help="Danh sách cột theo chữ Excel (vd: 'K,L,M,AA,AB'). Nếu bỏ trống sẽ auto-detect các cột có giá trị dạng '<...'.",
    )
    ap.add_argument(
        "--method",
        choices=["half", "uniform", "beta", "loguniform"],
        default="half",
        help="Phương pháp sinh giá trị cho '<LOD'.",
    )
    ap.add_argument(
        "--mode",
        choices=["replace", "add"],
        default="replace",
        help="replace: thay trực tiếp trong cột; add: tạo thêm cột mới (giữ nguyên cột cũ).",
    )
    ap.add_argument(
        "--suffix",
        default="_gen",
        help="Hậu tố cột mới khi mode=add.",
    )
    ap.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Seed cho ngẫu nhiên (để tái lập).",
    )
    ap.add_argument(
        "--beta-a",
        type=float,
        default=2.0,
        help="Tham số a cho Beta(a,b) khi method=beta.",
    )
    ap.add_argument(
        "--beta-b",
        type=float,
        default=8.0,
        help="Tham số b cho Beta(a,b) khi method=beta.",
    )
    ap.add_argument(
        "--min-ratio",
        type=float,
        default=1e-3,
        help="Tỉ lệ nhỏ nhất (LOD*min_ratio) khi method=loguniform.",
    )
    args = ap.parse_args()

    in_path = Path(args.input)
    out_path = Path(args.output)
    if not in_path.exists():
        raise SystemExit(f"Không tìm thấy file input: {in_path}")

    import random

    rng = random.Random(args.seed)

    xl = pd.ExcelFile(in_path, engine="openpyxl")
    sheets = args.sheet if args.sheet else xl.sheet_names

    excel_indices = parse_excel_cols(args.excel_cols)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    all_stats = []

    with pd.ExcelWriter(out_path, engine="openpyxl") as w:
        for sh in sheets:
            df = pd.read_excel(
                in_path,
                sheet_name=sh,
                header=args.header_row,
                dtype=object,  # giữ string/number linh hoạt
                engine="openpyxl",
            )

            if excel_indices:
                target_cols = select_columns_by_excel_indices(df, excel_indices)
            else:
                target_cols = auto_detect_columns_with_lt(df)

            new_df, stats = process_sheet(
                df,
                target_cols=target_cols,
                method=args.method,
                mode=args.mode,
                suffix=args.suffix,
                rng=rng,
                beta_a=args.beta_a,
                beta_b=args.beta_b,
                min_ratio=args.min_ratio,
            )

            new_df.to_excel(w, index=False, sheet_name=sh[:31])  # Excel giới hạn 31 ký tự
            all_stats.append((sh, stats))

    print("OK")
    print(f"- Input : {in_path}")
    print(f"- Output: {out_path}")
    print(f"- Method: {args.method} | Mode: {args.mode} | Seed: {args.seed}")
    for sh, stats in all_stats:
        total = sum(n for _, n in stats)
        if total == 0:
            print(f"  - Sheet '{sh}': không có giá trị dạng '<...>' trong các cột mục tiêu")
        else:
            top = ", ".join([f"{c}:{n}" for c, n in stats if n][:10])
            print(f"  - Sheet '{sh}': thay {total} ô  (<...) | top: {top}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())


