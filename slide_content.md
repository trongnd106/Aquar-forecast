# Nội dung hoàn thiện cho các slide PowerPoint

## SLIDE 10: 2. Bộ dữ liệu và tiền xử lý dữ liệu

### Tiêu đề: 2. Bộ dữ liệu và tiền xử lý dữ liệu

---

### 2.1. Bộ dữ liệu Hong Kong (HK Dataset)

**Nguồn dữ liệu:**
- 8 khu vực quan trắc ven biển Hong Kong
- Thời gian: 1986-2023 (hơn 10.000 mẫu)
- Độ sâu: Tầng mặt (Surface) và Tầng trung (Middle)

**Các bước tiền xử lý:**

1. **Chuẩn hóa cấu trúc dữ liệu**
   - Chuyển tên cột về dạng chuẩn (lowercase, loại bỏ ký tự đặc biệt)
   - Xử lý giá trị LOD (Limit of Detection): `<0.01` → `0.005`

2. **Tổng hợp theo thời gian**
   - Tổng hợp trung bình theo tháng → theo quý
   - Giảm nhiễu ngắn hạn, làm nổi bật xu hướng

3. **Chuẩn hóa lược đồ thuộc tính**
   - Ánh xạ về 21 biến môi trường chuẩn
   - Bổ sung dữ liệu tổng hợp cho các biến thiếu:
     * H₂S: Phân phối log-normal
     * Alkalinity: Phân phối chuẩn cắt ngưỡng
     * Transparency, COD: Phân phối log-normal

4. **Tạo bộ dữ liệu cuối cùng**
   - Hàu (Oyster): Dữ liệu tầng mặt
   - Cá giò (Cobia): Dữ liệu tầng trung
   - Format: CSV theo quý với 21 biến

---

### 2.2. Bộ dữ liệu Việt Nam (VN Dataset)

**Nguồn dữ liệu:**
- Vùng biển Quảng Ninh
- Thời gian: 2021-2024 (khoảng 1.200 mẫu)
- Nhiều trạm quan trắc phân bố không gian

**Các bước tiền xử lý:**

1. **Chuẩn hóa định dạng thời gian**
   - Chuyển đổi "Quý 1 năm 2021" → datetime chuẩn (YYYY-MM-DD)
   - Sử dụng Regular Expression để parsing

2. **Xử lý giá trị thiếu và ngoại lai**
   - Xử lý LOD: Giá trị `<x` → `x/2`
   - Nội suy tuyến tính theo thời gian cho từng trạm
   - Điền giá trị thiếu bằng median của trạm

3. **Tạo biến trễ (Lag Features)**
   - Lag 1: Giá trị quý trước (tính quán tính)
   - Lag 4: Giá trị cùng kỳ năm trước (tính mùa vụ)
   - Loại bỏ 4 quý đầu tiên (không đủ dữ liệu lag)

4. **Kiểm tra tính nhất quán Schema**
   - Đảm bảo số lượng cột và thứ tự biến khớp với HK Dataset
   - Điều kiện: `Shape(X_VN) ≡ Shape(X_HK)`

**Kết quả:**
- Dữ liệu huấn luyện: Q1/2022 → Q4/2023
- Dữ liệu kiểm thử: Năm 2024

---

## SLIDE 12: 3. Xây dựng mô hình dự đoán - Base Model

### Tiêu đề: 3. Xây dựng mô hình dự đoán - Base Model

---

### 3.1. Thiết lập bài toán Multi-output Regression

**Mục tiêu:**
- Dự báo đồng thời 11 chỉ số môi trường
- Mô hình hóa hệ thống thống nhất (không phá vỡ tính liên kết sinh-lý-hóa)

**Vector đầu ra:**
```
y = [DO, Temp, pH, Salinity, NH₃, H₂S, BOD₅, TSS, 
     Coliform, COD, Alkalinity, Transparency]
```

**Kiến trúc:**
- Sử dụng `MultiOutputRegressor` (Scikit-learn)
- 11 mô hình XGBoost độc lập, chia sẻ không gian đặc trưng
- Mỗi mô hình học cấu trúc cây riêng phù hợp với đặc thù biến

---

### 3.2. Cấu hình tham số tối ưu

| Tham số | Giá trị | Vai trò |
|---------|---------|---------|
| `n_estimators` | 1000 | Đảm bảo khả năng học các mẫu phức tạp |
| `learning_rate` | 0.05 | Kiểm soát tốc độ hội tụ, ngăn chặn Overfitting |
| `max_depth` | 5 | Giới hạn độ phức tạp của tương tác biến số |
| `subsample` | 0.8 | Tăng tính ngẫu nhiên (Row-sampling) |
| `colsample_bytree` | 0.8 | Tăng tính ngẫu nhiên (Feature-sampling) |
| `objective` | reg:squarederror | Hàm mất mát RMSE |

**Chiến lược:**
- Số lượng cây lớn (1000) + Tốc độ học thấp (0.05) = Học từ từ và bền bỉ
- Độ sâu vừa phải (5) = Nắm bắt tương tác bậc cao mà không học nhiễu
- Stochastic sampling (0.8) = Tăng tính đa dạng, tổng quát hóa tốt hơn

---

### 3.3. Kết quả huấn luyện trên HK Dataset

**Đánh giá:** RMSE (Root Mean Square Error)

| Nhóm chỉ số | Biến | RMSE | Đánh giá |
|-------------|------|------|----------|
| **Vật lý** | pH | 0.0701 | Xuất sắc |
| | DO | 0.3795 mg/L | Tốt |
| | Temperature | 0.4346 °C | Tốt |
| | Salinity | 0.6151 ‰ | Chấp nhận được |
| **Hóa học** | NH₃ | 0.0012 mg/L | Xuất sắc |
| | H₂S | 0.0066 mg/L | Xuất sắc |
| | BOD₅ | 0.2366 mg/L | Tốt |
| **Vi sinh** | TSS | 1.2926 mg/L | Trung bình |
| | Transparency | 6.1968 cm | Cao |
| | Coliform | 1585.07 MPN | Cao* (*Do thang đo lớn) |

**Kết luận:**
- ✅ Học thành công quy luật vật lý-hóa học bất biến
- ✅ Tạo nền tảng tri thức vững chắc cho Transfer Learning
- ✅ Sẵn sàng cho bước Fine-tuning trên dữ liệu Việt Nam

---

## SLIDE 13: 3. Xây dựng mô hình dự đoán - Fine-tuned Model

### Tiêu đề: 3. Xây dựng mô hình dự đoán - Fine-tuned Model

---

### 3.1. Chiến lược Học chuyển giao (Transfer Learning)

**Vấn đề:**
- Dữ liệu Việt Nam nhỏ (1.200 mẫu) → Nguy cơ Overfitting
- Chuỗi thời gian ngắn (4 năm) → Thiếu tri thức tổng quát

**Giải pháp:**
- **Miền nguồn (Source):** HK Dataset (10.000+ mẫu, nhiều thập kỷ)
- **Miền đích (Target):** VN Dataset (1.200 mẫu, 2021-2024)
- **Cơ chế:** Warm Start + Incremental Learning

---

### 3.2. Quy trình Fine-tuning

**Giai đoạn 1: Pre-training (Base Model)**
```
M_base = Train(XGBoost, HK_Dataset)
→ Học quy luật vật lý-hóa học phổ quát
→ Xây dựng cấu trúc cây quyết định
```

**Giai đoạn 2: Fine-tuning**
```
M_finetuned = M_base + η · Σ f_new(VN_Dataset)
```

**Cơ chế:**
- Kế thừa tham số: Sử dụng `xgb_model=old_booster`
- Học phần dư: Các cây mới dự báo sai số (residuals)
- Giảm tốc độ học: `η = 0.01` (từ 0.05) → Tránh Catastrophic Forgetting

**Công thức cập nhật:**
```
F_final(x) = Σ T_HK(x) + η · Σ T_new(x)
           [Kiến thức nền]  [Kiến thức thích nghi]
```

---

### 3.3. Điều chỉnh tốc độ học

**Vấn đề Catastrophic Forgetting:**
- Tốc độ học cao → Ghi đè tri thức cũ
- Mất khả năng tổng quát hóa

**Giải pháp:**
- **Base Model:** `learning_rate = 0.05`
- **Fine-tuned Model:** `learning_rate = 0.01` (giảm 5 lần)

**Ý nghĩa:**
- ✅ Giới hạn không gian tìm kiếm → Di chuyển bước nhỏ
- ✅ Tăng độ mịn xấp xỉ → Loại bỏ nhiễu, giữ xu hướng
- ✅ Cân bằng Stability (ổn định) và Plasticity (linh hoạt)

---

### 3.4. Kết quả so sánh

**Cải thiện hiệu năng (RMSE):**

| Biến | RMSE (HK) | RMSE (VN) | Cải thiện |
|------|-----------|-----------|-----------|
| **pH** | 0.0686 | 0.0341 | **+50.3%** ✅ |
| **DO** | 0.3687 | 0.2831 | **+23.2%** ✅ |
| **Salinity** | 0.6077 | 0.4501 | **+25.9%** ✅ |
| **Transparency** | 5.8198 | 2.1295 | **+63.4%** ✅ |
| Temperature | 0.4327 | 0.7465 | -72.5% ⚠️ |

**Kết luận:**
- ✅ Tối ưu hóa cục bộ: Cải thiện độ chính xác cho các chỉ số sống còn
- ✅ Thích nghi ngữ cảnh: Điều chỉnh thang đo phản ánh đặc thù Việt Nam
- ✅ Mô hình chuyên biệt hóa cho vùng biển Quảng Ninh

---

## Ghi chú cho việc trình bày:

1. **Slide 10:** Tập trung vào quy trình tiền xử lý, có thể dùng sơ đồ flow chart
2. **Slide 12:** Nhấn mạnh kết quả RMSE, có thể dùng bảng so sánh màu sắc
3. **Slide 13:** So sánh trước/sau fine-tuning, highlight phần cải thiện

