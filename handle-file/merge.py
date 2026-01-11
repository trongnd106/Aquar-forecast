#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import re
from pathlib import Path
from typing import Dict, List, Tuple

import pandas as pd


TARGET_YEARS = (2021, 2022, 2023, 2024)


def _pick_year_sheets(sheet_names: List[str]) -> Dict[int, str]:
    """
    Map year -> actual sheet name in the workbook (case-insensitive, tolerant of 'năm/Năm').
    """
    out: Dict[int, str] = {}
    for sh in sheet_names:
        m = re.search(r"(20\d{2})", str(sh))
        if not m:
            continue
        year = int(m.group(1))
        if year in TARGET_YEARS and year not in out:
            out[year] = sh
    return out


def _extract_quarter_num(val) -> int | None:
    if val is None or (isinstance(val, float) and pd.isna(val)):
        return None
    s = str(val).strip()
    m = re.search(r"quý\s*(\d)", s, flags=re.IGNORECASE)
    if m:
        try:
            q = int(m.group(1))
            return q if 1 <= q <= 4 else None
        except ValueError:
            return None
    return None


def _extract_khm_num(val) -> int | None:
    if val is None or (isinstance(val, float) and pd.isna(val)):
        return None
    s = str(val).strip()
    m = re.search(r"nb\s*(\d+)", s, flags=re.IGNORECASE)
    if not m:
        return None
    try:
        return int(m.group(1))
    except ValueError:
        return None


def _read_one_year(xlsx_path: Path, sheet_name: str, year: int) -> pd.DataFrame:
    # Header nằm ở dòng thứ 2 trong file mẫu (0-based row index = 1)
    df = pd.read_excel(
        xlsx_path,
        sheet_name=sheet_name,
        header=1,
        dtype=str,  # giữ nguyên các giá trị dạng '<0,03', 'x', v.v.
        engine="openpyxl",
    )

    # Chuẩn hoá tên cột hay dùng
    # (đôi khi có khoảng trắng cuối)
    df.columns = [str(c).strip() for c in df.columns]

    required_cols = ["Vị trí quan trắc", "KHM", "Quý"]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(
            f"Sheet '{sheet_name}' thiếu cột {missing}. Các cột hiện có: {list(df.columns)}"
        )

    # Bỏ dòng QCVN và các dòng trống
    # - dòng QCVN có 'Vị trí quan trắc' = 'QCVN 10:2023/BTNMT'
    # - dữ liệu thật thường có KHM và Quý
    df = df[df["KHM"].notna() & df["Quý"].notna()].copy()

    # Do ô merge ở cột 'Vị trí quan trắc', cần fill xuống
    df["Vị trí quan trắc"] = df["Vị trí quan trắc"].ffill()

    # Thêm năm theo sheet (đúng yêu cầu “năm tương ứng với sheets”)
    df["Năm"] = year

    # Tạo cột sort key (không thay đổi dữ liệu gốc)
    df["Quý_số"] = df["Quý"].map(_extract_quarter_num)
    df["KHM_số"] = df["KHM"].map(_extract_khm_num)

    return df


def merge_tong_hop(input_xlsx: Path) -> Tuple[pd.DataFrame, Dict[int, str]]:
    xl = pd.ExcelFile(input_xlsx, engine="openpyxl")
    year_to_sheet = _pick_year_sheets(xl.sheet_names)

    missing_years = [y for y in TARGET_YEARS if y not in year_to_sheet]
    if missing_years:
        raise ValueError(
            f"Không tìm thấy sheet cho các năm: {missing_years}. "
            f"Sheet hiện có: {xl.sheet_names}"
        )

    parts: List[pd.DataFrame] = []
    for y in TARGET_YEARS:
        sh = year_to_sheet[y]
        parts.append(_read_one_year(input_xlsx, sh, y))

    merged = pd.concat(parts, ignore_index=True)

    # Giữ thứ tự KHM như file gốc (lấy theo năm 2021), fallback theo số NBx nếu có
    khm_order: Dict[str, int] = {}
    if parts and "KHM" in parts[0].columns:
        for i, khm in enumerate(parts[0]["KHM"].dropna().astype(str).unique().tolist()):
            if khm not in khm_order:
                khm_order[khm] = i
    merged["KHM_thứ_tự"] = merged["KHM"].astype(str).map(khm_order)

    # Sort theo đúng mong muốn: NB1 -> NB2 -> ... rồi theo năm -> quý
    merged = merged.sort_values(
        by=["KHM_thứ_tự", "KHM_số", "Năm", "Quý_số", "Vị trí quan trắc"],
        kind="mergesort",  # stable sort
        na_position="last",
    ).reset_index(drop=True)

    return merged, year_to_sheet


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Gộp dữ liệu từ Tong-hop.xlsx (năm 2021-2024), nhóm theo Vị trí quan trắc và sắp xếp theo năm/quý."
    )
    ap.add_argument(
        "--input",
        default="/home/trong/Documents/handle-file/Tong-hop.xlsx",
        help="Đường dẫn file Excel đầu vào",
    )
    ap.add_argument(
        "--output",
        default="/home/trong/Documents/handle-file/Tong-hop_2021-2024_gop.xlsx",
        help="Đường dẫn file Excel đầu ra",
    )
    ap.add_argument(
        "--csv",
        default="",
        help="(Tuỳ chọn) Nếu set, sẽ xuất thêm CSV ra đường dẫn này",
    )
    args = ap.parse_args()

    input_xlsx = Path(args.input)
    output_xlsx = Path(args.output)
    if not input_xlsx.exists():
        raise SystemExit(f"Không tìm thấy file input: {input_xlsx}")

    merged, year_to_sheet = merge_tong_hop(input_xlsx)

    # Xuất “gần như merge thuần”: bỏ các cột phụ dùng để sort
    export_df = merged.drop(columns=["Năm", "Quý_số", "KHM_số", "KHM_thứ_tự"], errors="ignore")

    # Ghi Excel
    output_xlsx.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(output_xlsx, engine="openpyxl") as w:
        export_df.to_excel(w, index=False, sheet_name="Gop_2021_2024")

    if args.csv:
        out_csv = Path(args.csv)
        out_csv.parent.mkdir(parents=True, exist_ok=True)
        export_df.to_csv(out_csv, index=False, encoding="utf-8-sig")

    print("OK")
    print(f"- Input : {input_xlsx}")
    print(f"- Output: {output_xlsx}")
    print(f"- Sheets used: {year_to_sheet}")
    print(f"- Rows: {len(export_df)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


