# Giải thích chi tiết cách tính Ma trận Tương quan (Correlation Matrix)

## 1. Tổng quan

**Ma trận tương quan** (Correlation Matrix) là một bảng vuông hiển thị hệ số tương quan giữa các cặp biến. Trong dữ liệu môi trường, nó giúp hiểu mối quan hệ tuyến tính giữa các thông số như DO, Temperature, pH, Salinity, v.v.

---

## 2. Hệ số tương quan Pearson (Pearson Correlation Coefficient)

### 2.1. Công thức toán học

Hệ số tương quan Pearson giữa hai biến X và Y được tính bằng:

```
r = Σ[(Xi - X̄)(Yi - Ȳ)] / √[Σ(Xi - X̄)² × Σ(Yi - Ȳ)²]
```

Hoặc dạng rút gọn:

```
r = Cov(X, Y) / (σX × σY)
```

Trong đó:
- **r**: Hệ số tương quan (từ -1 đến +1)
- **Xi, Yi**: Giá trị của biến X và Y tại quan sát thứ i
- **X̄, Ȳ**: Giá trị trung bình của X và Y
- **Cov(X, Y)**: Hiệp phương sai (Covariance)
- **σX, σY**: Độ lệch chuẩn của X và Y

### 2.2. Công thức hiệp phương sai (Covariance)

```
Cov(X, Y) = Σ[(Xi - X̄)(Yi - Ȳ)] / (n - 1)
```

Hoặc:

```
Cov(X, Y) = E[(X - E[X])(Y - E[Y])]
```

---

## 3. Các bước tính toán chi tiết

### Ví dụ: Tính tương quan giữa Temperature và DO

Giả sử có 5 mẫu dữ liệu:

| Mẫu | Temperature (°C) | DO (mg/L) |
|-----|------------------|-----------|
| 1   | 22.0             | 7.4       |
| 2   | 30.2             | 6.95      |
| 3   | 32.4             | 6.25      |
| 4   | 25.0             | 6.83      |
| 5   | 22.6             | 6.41      |

### Bước 1: Tính trung bình

```
X̄ (Temperature) = (22.0 + 30.2 + 32.4 + 25.0 + 22.6) / 5 = 26.44°C
Ȳ (DO) = (7.4 + 6.95 + 6.25 + 6.83 + 6.41) / 5 = 6.768 mg/L
```

### Bước 2: Tính độ lệch từ trung bình

| Mẫu | Xi - X̄ | Yi - Ȳ |
|-----|--------|--------|
| 1   | -4.44  | 0.632  |
| 2   | 3.76   | 0.182  |
| 3   | 5.96   | -0.518 |
| 4   | -1.44  | 0.062  |
| 5   | -3.84  | -0.358 |

### Bước 3: Tính tích (Xi - X̄)(Yi - Ȳ)

| Mẫu | (Xi - X̄)(Yi - Ȳ) |
|-----|------------------|
| 1   | -4.44 × 0.632 = -2.806 |
| 2   | 3.76 × 0.182 = 0.684  |
| 3   | 5.96 × (-0.518) = -3.087 |
| 4   | -1.44 × 0.062 = -0.089 |
| 5   | -3.84 × (-0.358) = 1.375 |

**Tổng**: Σ[(Xi - X̄)(Yi - Ȳ)] = -2.806 + 0.684 - 3.087 - 0.089 + 1.375 = **-3.923**

### Bước 4: Tính tổng bình phương độ lệch

**Cho X (Temperature):**
- Σ(Xi - X̄)² = (-4.44)² + (3.76)² + (5.96)² + (-1.44)² + (-3.84)²
- = 19.71 + 14.14 + 35.52 + 2.07 + 14.75 = **86.19**

**Cho Y (DO):**
- Σ(Yi - Ȳ)² = (0.632)² + (0.182)² + (-0.518)² + (0.062)² + (-0.358)²
- = 0.399 + 0.033 + 0.268 + 0.004 + 0.128 = **0.992**

### Bước 5: Tính hệ số tương quan

```
r = -3.923 / √(86.19 × 0.992)
r = -3.923 / √85.50
r = -3.923 / 9.247
r = -0.424
```

**Kết quả**: r = **-0.424** → Tương quan âm trung bình

---

## 4. Giải thích ý nghĩa

### 4.1. Phạm vi giá trị

- **r = +1.0**: Tương quan dương hoàn hảo (X tăng → Y tăng tuyến tính)
- **r = 0.0**: Không có tương quan tuyến tính
- **r = -1.0**: Tương quan âm hoàn hảo (X tăng → Y giảm tuyến tính)

### 4.2. Mức độ tương quan

| |r| | Mức độ | Ý nghĩa |
|---|-----|--------|---------|
| 0.0 - 0.3 | Rất yếu | Hầu như không có mối quan hệ |
| 0.3 - 0.5 | Yếu | Mối quan hệ yếu |
| 0.5 - 0.7 | Trung bình | Mối quan hệ vừa phải |
| 0.7 - 0.9 | Mạnh | Mối quan hệ chặt chẽ |
| 0.9 - 1.0 | Rất mạnh | Mối quan hệ rất chặt chẽ |

### 4.3. Ví dụ với kết quả -0.424

- **Dấu âm**: Temperature tăng → DO giảm (phù hợp với lý thuyết: nhiệt độ cao → oxy hòa tan thấp)
- **Giá trị 0.424**: Tương quan trung bình-yếu
- **Giải thích**: Nhiệt độ chỉ giải thích một phần sự thay đổi của DO, còn có các yếu tố khác

---

## 5. Ma trận tương quan

### 5.1. Cấu trúc

Ma trận tương quan là ma trận vuông đối xứng:

```
        DO    Temp   pH    Salinity
DO       1.00  -0.42  0.15   0.23
Temp    -0.42   1.00  0.08  -0.31
pH       0.15   0.08  1.00   0.12
Salinity 0.23  -0.31  0.12   1.00
```

**Đặc điểm:**
- **Đường chéo = 1.0**: Mỗi biến tương quan hoàn hảo với chính nó
- **Đối xứng**: r(X,Y) = r(Y,X)
- **Kích thước**: n×n (n = số biến)

### 5.2. Cách tính ma trận

Với n biến, cần tính n(n-1)/2 hệ số tương quan (do tính đối xứng).

**Ví dụ với 4 biến:**
- Tổng số hệ số: 4 × 3 / 2 = 6 cặp
- Các cặp: (DO, Temp), (DO, pH), (DO, Salinity), (Temp, pH), (Temp, Salinity), (pH, Salinity)

---

## 6. Công thức ma trận (Matrix Form)

### 6.1. Dữ liệu chuẩn hóa

Để tính ma trận tương quan, trước tiên chuẩn hóa dữ liệu:

```
Z = (X - μ) / σ
```

Trong đó:
- **Z**: Dữ liệu đã chuẩn hóa (z-score)
- **μ**: Trung bình
- **σ**: Độ lệch chuẩn

### 6.2. Ma trận tương quan

Nếu **Z** là ma trận dữ liệu đã chuẩn hóa (mỗi cột có mean=0, std=1):

```
R = (1/(n-1)) × Z^T × Z
```

Trong đó:
- **R**: Ma trận tương quan
- **Z^T**: Chuyển vị của Z
- **n**: Số quan sát

---

## 7. Xử lý dữ liệu thiếu (Missing Values)

### 7.1. Vấn đề

Khi tính correlation, cần xử lý các giá trị NaN (Not a Number):

**Các phương pháp:**
1. **Pairwise deletion**: Chỉ dùng các cặp có đủ dữ liệu
2. **Listwise deletion**: Loại bỏ toàn bộ hàng có bất kỳ giá trị thiếu nào
3. **Imputation**: Điền giá trị thiếu (mean, median, mode)

### 7.2. Trong pandas

```python
# Pairwise deletion (mặc định)
corr_matrix = df.corr()

# Hoặc chỉ dùng các hàng không có giá trị thiếu
corr_matrix = df.dropna().corr()
```

---

## 8. Ví dụ code Python

### 8.1. Tính thủ công

```python
import numpy as np
import pandas as pd

# Dữ liệu mẫu
data = {
    'Temperature': [22.0, 30.2, 32.4, 25.0, 22.6],
    'DO': [7.4, 6.95, 6.25, 6.83, 6.41]
}
df = pd.DataFrame(data)

# Tính thủ công
X = df['Temperature'].values
Y = df['DO'].values

# Trung bình
X_mean = np.mean(X)
Y_mean = np.mean(Y)

# Độ lệch
X_dev = X - X_mean
Y_dev = Y - Y_mean

# Tử số: Σ[(Xi - X̄)(Yi - Ȳ)]
numerator = np.sum(X_dev * Y_dev)

# Mẫu số: √[Σ(Xi - X̄)² × Σ(Yi - Ȳ)²]
denominator = np.sqrt(np.sum(X_dev**2) * np.sum(Y_dev**2))

# Hệ số tương quan
r = numerator / denominator
print(f"Correlation (thủ công): {r:.4f}")

# So sánh với pandas
r_pandas = df['Temperature'].corr(df['DO'])
print(f"Correlation (pandas): {r_pandas:.4f}")
```

### 8.2. Tính ma trận tương quan

```python
# Dữ liệu nhiều biến
df = pd.DataFrame({
    'DO': [7.4, 6.95, 6.25, 6.83, 6.41],
    'Temperature': [22.0, 30.2, 32.4, 25.0, 22.6],
    'pH': [7.79, 8.08, 8.1, 8.07, 8.09],
    'Salinity': [29.6, 29.6, 27.6, 29.7, 29.9]
})

# Ma trận tương quan
corr_matrix = df.corr()
print(corr_matrix)

# Vẽ heatmap
import seaborn as sns
import matplotlib.pyplot as plt

sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', center=0)
plt.title('Ma trận tương quan')
plt.show()
```

---

## 9. Ý nghĩa trong dữ liệu môi trường

### 9.1. Tương quan dương mạnh (r > 0.7)

**Ví dụ:**
- **NH3 và PO4**: Cùng nguồn dinh dưỡng (ô nhiễm hữu cơ)
- **Các kim loại nặng**: Cùng nguồn ô nhiễm công nghiệp

**Ứng dụng:**
- Nếu biết một giá trị, có thể dự đoán giá trị kia
- Có thể giảm số biến trong mô hình (feature selection)

### 9.2. Tương quan âm mạnh (r < -0.7)

**Ví dụ:**
- **Temperature và DO**: Nhiệt độ cao → oxy hòa tan thấp
- **Salinity và Transparency**: Độ mặn cao → độ trong có thể thay đổi

**Ứng dụng:**
- Hiểu cơ chế vật lý/hóa học
- Dự đoán ngược chiều

### 9.3. Tương quan yếu (|r| < 0.3)

**Ví dụ:**
- **pH và Temperature**: Thường độc lập
- **CN và As**: Có thể từ nguồn khác nhau

**Ứng dụng:**
- Các biến độc lập, cần giữ lại trong mô hình
- Không thể dự đoán biến này từ biến kia

---

## 10. Lưu ý quan trọng

### 10.1. Tương quan ≠ Nhân quả

**Ví dụ:**
- Temperature và DO có tương quan âm
- Nhưng không có nghĩa là nhiệt độ "gây ra" DO thấp
- Có thể cả hai đều bị ảnh hưởng bởi yếu tố thứ ba (ví dụ: mùa)

### 10.2. Tương quan tuyến tính

- Pearson chỉ đo **tương quan tuyến tính**
- Có thể có mối quan hệ phi tuyến nhưng r ≈ 0
- Nên kiểm tra bằng scatter plot

### 10.3. Outliers

- Một vài giá trị ngoại lai có thể làm sai lệch r
- Nên kiểm tra và xử lý outliers trước khi tính

### 10.4. Sample size

- Với n nhỏ, r có thể không đáng tin cậy
- Nên có ít nhất 30-50 quan sát để có kết quả ổn định

---

## 11. Các loại tương quan khác

### 11.1. Spearman Correlation

- Dùng cho dữ liệu **thứ tự** hoặc **phi tuyến**
- Dựa trên **rank** (thứ hạng) thay vì giá trị thực

```python
# Spearman correlation
r_spearman = df['Temperature'].corr(df['DO'], method='spearman')
```

### 11.2. Kendall Correlation

- Tương tự Spearman, nhưng tính toán khác
- Phù hợp với dữ liệu nhỏ

```python
# Kendall correlation
r_kendall = df['Temperature'].corr(df['DO'], method='kendall')
```

---

## 12. Tóm tắt công thức

### 12.1. Công thức chính

```
r = Σ[(Xi - X̄)(Yi - Ȳ)] / √[Σ(Xi - X̄)² × Σ(Yi - Ȳ)²]
```

### 12.2. Công thức rút gọn

```
r = Cov(X, Y) / (σX × σY)
```

### 12.3. Công thức ma trận

```
R = (1/(n-1)) × Z^T × Z
```

Trong đó Z là ma trận dữ liệu đã chuẩn hóa.

---

## 13. Bài tập thực hành

### Bài 1: Tính thủ công

Cho dữ liệu:
- X = [10, 20, 30, 40, 50]
- Y = [5, 10, 15, 20, 25]

Tính hệ số tương quan giữa X và Y.

**Đáp án**: r = 1.0 (tương quan dương hoàn hảo)

### Bài 2: Giải thích kết quả

Nếu r(Temperature, DO) = -0.65, giải thích ý nghĩa.

**Đáp án**: 
- Tương quan âm trung bình-mạnh
- Nhiệt độ tăng → DO giảm
- Nhiệt độ giải thích khoảng 42% (0.65²) phương sai của DO

---

*Tài liệu này giải thích cách tính ma trận tương quan trong bối cảnh phân tích dữ liệu môi trường biển Quảng Ninh.*

