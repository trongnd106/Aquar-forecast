"""
Demo script: Giải thích cách tính ma trận tương quan từng bước
Sử dụng dữ liệu Quảng Ninh thực tế
"""

import pandas as pd
import numpy as np
from pathlib import Path

# Đường dẫn dữ liệu
DATA_PATH = Path(__file__).parent.parent / "data" / "data_quang_ninh" / "qn_env_clean_ready.csv"

print("=" * 70)
print("DEMO: CÁCH TÍNH MA TRẬN TƯƠNG QUAN")
print("=" * 70)

# Đọc dữ liệu
print("\n1. Đọc dữ liệu...")
df = pd.read_csv(DATA_PATH)
print(f"   - Số bản ghi: {len(df)}")
print(f"   - Số cột: {len(df.columns)}")

# Chọn 2 biến để demo chi tiết
print("\n2. Chọn 2 biến để demo: Temperature và DO")
print("   (Lấy 10 mẫu đầu tiên để dễ theo dõi)")

sample_df = df[['Temperature', 'DO']].head(10).copy()
sample_df['Temperature'] = pd.to_numeric(sample_df['Temperature'], errors='coerce')
sample_df['DO'] = pd.to_numeric(sample_df['DO'], errors='coerce')
sample_df = sample_df.dropna()

print("\n   Dữ liệu mẫu:")
print(sample_df.to_string(index=False))

# ============================================================
# TÍNH THỦ CÔNG TỪNG BƯỚC
# ============================================================
print("\n" + "=" * 70)
print("BƯỚC 1: TÍNH TRUNG BÌNH")
print("=" * 70)

X = sample_df['Temperature'].values
Y = sample_df['DO'].values

X_mean = np.mean(X)
Y_mean = np.mean(Y)

print(f"\nX̄ (Temperature trung bình) = {X_mean:.4f} °C")
print(f"Ȳ (DO trung bình) = {Y_mean:.4f} mg/L")

# ============================================================
print("\n" + "=" * 70)
print("BƯỚC 2: TÍNH ĐỘ LỆCH TỪ TRUNG BÌNH")
print("=" * 70)

X_dev = X - X_mean
Y_dev = Y - Y_mean

print("\n   Bảng tính độ lệch:")
print("   " + "-" * 60)
print(f"   {'Mẫu':<6} {'Xi':<10} {'Xi - X̄':<12} {'Yi':<10} {'Yi - Ȳ':<12}")
print("   " + "-" * 60)
for i in range(len(X)):
    print(f"   {i+1:<6} {X[i]:<10.2f} {X_dev[i]:<12.4f} {Y[i]:<10.2f} {Y_dev[i]:<12.4f}")

# ============================================================
print("\n" + "=" * 70)
print("BƯỚC 3: TÍNH TÍCH (Xi - X̄)(Yi - Ȳ)")
print("=" * 70)

products = X_dev * Y_dev
sum_products = np.sum(products)

print("\n   Bảng tính tích:")
print("   " + "-" * 60)
print(f"   {'Mẫu':<6} {'(Xi - X̄)':<12} {'(Yi - Ȳ)':<12} {'Tích':<12}")
print("   " + "-" * 60)
for i in range(len(X)):
    print(f"   {i+1:<6} {X_dev[i]:<12.4f} {Y_dev[i]:<12.4f} {products[i]:<12.4f}")

print(f"\n   Tổng Σ[(Xi - X̄)(Yi - Ȳ)] = {sum_products:.4f}")

# ============================================================
print("\n" + "=" * 70)
print("BƯỚC 4: TÍNH TỔNG BÌNH PHƯƠNG ĐỘ LỆCH")
print("=" * 70)

sum_X_squared = np.sum(X_dev ** 2)
sum_Y_squared = np.sum(Y_dev ** 2)

print(f"\n   Σ(Xi - X̄)² = {sum_X_squared:.4f}")
print(f"   Σ(Yi - Ȳ)² = {sum_Y_squared:.4f}")

# ============================================================
print("\n" + "=" * 70)
print("BƯỚC 5: TÍNH HỆ SỐ TƯƠNG QUAN")
print("=" * 70)

denominator = np.sqrt(sum_X_squared * sum_Y_squared)
r_manual = sum_products / denominator

print(f"\n   Tử số: Σ[(Xi - X̄)(Yi - Ȳ)] = {sum_products:.4f}")
print(f"   Mẫu số: √[Σ(Xi - X̄)² × Σ(Yi - Ȳ)²] = √({sum_X_squared:.4f} × {sum_Y_squared:.4f})")
print(f"   Mẫu số: {denominator:.4f}")
print(f"\n   HỆ SỐ TƯƠNG QUAN r = {sum_products:.4f} / {denominator:.4f} = {r_manual:.4f}")

# ============================================================
print("\n" + "=" * 70)
print("SO SÁNH VỚI PANDAS")
print("=" * 70)

r_pandas = sample_df['Temperature'].corr(sample_df['DO'])
print(f"\n   Kết quả tính thủ công: r = {r_manual:.6f}")
print(f"   Kết quả pandas:        r = {r_pandas:.6f}")
print(f"   Chênh lệch:             {abs(r_manual - r_pandas):.10f}")

if abs(r_manual - r_pandas) < 0.0001:
    print("\n   ✓ Kết quả khớp!")
else:
    print("\n   ⚠ Có sự khác biệt nhỏ (do làm tròn)")

# ============================================================
print("\n" + "=" * 70)
print("GIẢI THÍCH Ý NGHĨA")
print("=" * 70)

print(f"\n   Hệ số tương quan: r = {r_manual:.4f}")

if abs(r_manual) < 0.3:
    strength = "rất yếu"
elif abs(r_manual) < 0.5:
    strength = "yếu"
elif abs(r_manual) < 0.7:
    strength = "trung bình"
elif abs(r_manual) < 0.9:
    strength = "mạnh"
else:
    strength = "rất mạnh"

if r_manual < 0:
    direction = "âm (Temperature tăng → DO giảm)"
else:
    direction = "dương (Temperature tăng → DO tăng)"

print(f"   - Mức độ: {strength}")
print(f"   - Hướng: {direction}")
print(f"   - Giải thích: Nhiệt độ giải thích {r_manual**2*100:.1f}% phương sai của DO")

# ============================================================
print("\n" + "=" * 70)
print("TÍNH MA TRẬN TƯƠNG QUAN CHO NHIỀU BIẾN")
print("=" * 70)

# Chọn các biến chính
vars_to_corr = ['DO', 'Temperature', 'pH', 'Salinity', 'NH3', 'PO4']
vars_to_corr = [v for v in vars_to_corr if v in df.columns]

print(f"\n   Các biến được chọn: {', '.join(vars_to_corr)}")

# Chuyển đổi sang numeric
df_corr = df[vars_to_corr].copy()
for col in vars_to_corr:
    df_corr[col] = pd.to_numeric(df_corr[col], errors='coerce')

# Tính ma trận tương quan
corr_matrix = df_corr.corr()

print("\n   Ma trận tương quan:")
print("\n" + corr_matrix.to_string())

# ============================================================
print("\n" + "=" * 70)
print("GIẢI THÍCH MA TRẬN")
print("=" * 70)

print("\n   Đặc điểm của ma trận:")
print("   - Kích thước: {}x{} ({} biến)".format(
    len(corr_matrix), len(corr_matrix), len(corr_matrix)))
print("   - Đường chéo: Tất cả = 1.0 (mỗi biến tương quan hoàn hảo với chính nó)")
print("   - Đối xứng: r(X,Y) = r(Y,X)")
print("   - Số hệ số cần tính: {} cặp".format(
    len(corr_matrix) * (len(corr_matrix) - 1) // 2))

# Tìm các cặp tương quan mạnh
print("\n   Các cặp tương quan mạnh (|r| > 0.5):")
strong_corr = []
for i in range(len(corr_matrix)):
    for j in range(i+1, len(corr_matrix)):
        r_val = corr_matrix.iloc[i, j]
        if abs(r_val) > 0.5:
            var1 = corr_matrix.index[i]
            var2 = corr_matrix.columns[j]
            strong_corr.append((var1, var2, r_val))

if strong_corr:
    for var1, var2, r_val in sorted(strong_corr, key=lambda x: abs(x[2]), reverse=True):
        direction = "dương" if r_val > 0 else "âm"
        print(f"   - {var1} ↔ {var2}: r = {r_val:.3f} ({direction})")
else:
    print("   - Không có cặp nào có |r| > 0.5")

# ============================================================
print("\n" + "=" * 70)
print("CÔNG THỨC TỔNG KẾT")
print("=" * 70)

print("""
   Công thức tính hệ số tương quan Pearson:

   r = Σ[(Xi - X̄)(Yi - Ȳ)] / √[Σ(Xi - X̄)² × Σ(Yi - Ȳ)²]

   Hoặc:

   r = Cov(X, Y) / (σX × σY)

   Trong đó:
   - X̄, Ȳ: Trung bình của X và Y
   - Cov(X, Y): Hiệp phương sai
   - σX, σY: Độ lệch chuẩn của X và Y
""")

print("=" * 70)
print("HOÀN THÀNH!")
print("=" * 70)

