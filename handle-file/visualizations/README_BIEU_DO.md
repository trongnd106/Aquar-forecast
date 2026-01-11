# Giải thích chi tiết các biểu đồ visualize dữ liệu Quảng Ninh

## Tổng quan

Bộ dữ liệu Quảng Ninh gồm **1,584 bản ghi** từ **99 trạm quan trắc** trong giai đoạn **2021-2024**, được thu thập theo quý. Các biểu đồ sau đây giúp hiểu rõ về:
- Xu hướng thay đổi theo thời gian
- Sự khác biệt giữa các trạm quan trắc
- Mối quan hệ giữa các thông số môi trường
- Phân bố và thống kê của dữ liệu

---

## 1. Biểu đồ Time Series - Xu hướng theo thời gian
**File: `1_time_series_main_params.png`**

### Mục đích
Theo dõi xu hướng thay đổi của các thông số môi trường chính (DO, Temperature, pH, Salinity) qua thời gian từ 2021-2024.

### Cách đọc
- **Đường màu xanh dương**: Giá trị trung bình của tất cả các trạm quan trắc tại mỗi quý
- **Vùng màu xanh nhạt (band)**: Khoảng giá trị từ Min đến Max, thể hiện độ phân tán của dữ liệu
- **Trục X**: Thời gian (theo quý)
- **Trục Y**: Giá trị của từng thông số

### Ý nghĩa
- **Xu hướng tăng/giảm**: Nhận biết xu hướng dài hạn của từng thông số
- **Biến động theo mùa**: Quan sát sự thay đổi theo mùa (nếu có)
- **Độ phân tán**: Band rộng = dữ liệu phân tán nhiều giữa các trạm; band hẹp = dữ liệu đồng nhất
- **Bất thường**: Các điểm lệch khỏi xu hướng có thể là dấu hiệu của sự kiện đặc biệt

### Ứng dụng
- Đánh giá chất lượng môi trường theo thời gian
- Phát hiện xu hướng suy thoái hoặc cải thiện
- Lập kế hoạch giám sát và can thiệp

---

## 2. Biểu đồ Box Plot - So sánh giữa các trạm
**File: `2_station_comparison.png`**

### Mục đích
So sánh phân bố giá trị của các thông số môi trường giữa 6 trạm quan trắc có nhiều dữ liệu nhất.

### Cách đọc Box Plot
Mỗi box plot gồm:
- **Đường ngang giữa box (median)**: Giá trị trung vị - 50% dữ liệu nằm trên/ dưới giá trị này
- **Cạnh dưới box (Q1)**: Tứ phân vị thứ nhất - 25% dữ liệu nhỏ hơn giá trị này
- **Cạnh trên box (Q3)**: Tứ phân vị thứ ba - 75% dữ liệu nhỏ hơn giá trị này
- **Whiskers (râu)**: Khoảng giá trị hợp lý (thường là 1.5 × IQR từ Q1/Q3)
- **Điểm ngoài whiskers**: Các giá trị ngoại lai (outliers)

### Ý nghĩa
- **Vị trí box**: Trạm có box cao hơn = giá trị trung bình cao hơn
- **Kích thước box**: Box lớn = độ phân tán lớn, dữ liệu không ổn định
- **Vị trí median**: Median lệch về một phía = phân bố lệch (skewed)
- **Outliers**: Nhiều điểm ngoại lai = có các giá trị bất thường

### Ứng dụng
- Xác định trạm có điều kiện môi trường tốt/xấu
- So sánh chất lượng nước giữa các khu vực
- Phát hiện trạm có vấn đề cần ưu tiên xử lý

---

## 3. Heatmap Correlation - Ma trận tương quan
**File: `3_correlation_heatmap.png`**

### Mục đích
Hiển thị mối quan hệ tuyến tính giữa các thông số môi trường (21 biến).

### Cách đọc
- **Màu đỏ**: Tương quan dương (r > 0) - hai biến tăng/giảm cùng nhau
- **Màu xanh**: Tương quan âm (r < 0) - một biến tăng thì biến kia giảm
- **Màu trắng/vàng nhạt**: Tương quan yếu (r ≈ 0)
- **Số trong ô**: Hệ số tương quan Pearson (từ -1 đến +1)
- **Chỉ hiển thị tam giác dưới**: Tránh trùng lặp (ma trận đối xứng)

### Giải thích hệ số tương quan
- **|r| > 0.7**: Tương quan mạnh
- **0.4 < |r| < 0.7**: Tương quan trung bình
- **|r| < 0.4**: Tương quan yếu

### Ý nghĩa
- **Tương quan dương mạnh**: 
  - Ví dụ: Temperature và DO có thể tương quan âm (nhiệt độ cao → oxy hòa tan thấp)
  - Các kim loại nặng có thể tương quan dương (cùng nguồn ô nhiễm)
- **Tương quan âm**: 
  - Ví dụ: Salinity và Transparency có thể tương quan
- **Tương quan yếu**: Các biến độc lập

### Ứng dụng
- **Feature selection**: Loại bỏ các biến tương quan cao (multicollinearity) khi xây dựng mô hình
- **Hiểu cơ chế**: Phát hiện các thông số có liên quan đến nhau
- **Dự đoán**: Sử dụng biến tương quan cao để dự đoán biến khác

---

## 4. Biểu đồ Kim loại nặng - Time Series
**File: `4_heavy_metals.png`**

### Mục đích
Theo dõi xu hướng nồng độ kim loại nặng (As, Cd, Pb, Cu) theo thời gian - các chất độc hại quan trọng.

### Cách đọc
Tương tự biểu đồ time series #1:
- **Đường màu đỏ**: Giá trị trung bình theo quý
- **Vùng màu đỏ nhạt**: Khoảng Min-Max
- **Trục Y**: Nồng độ (mg/L) - thường rất nhỏ (0.001-0.01 mg/L)

### Ý nghĩa
- **Xu hướng tăng**: Cảnh báo ô nhiễm tích tụ
- **Xu hướng giảm**: Cải thiện chất lượng môi trường
- **Biến động lớn**: Có thể do hoạt động công nghiệp, giao thông
- **So sánh với QCVN**: Kiểm tra xem có vượt ngưỡng cho phép không

### Ngưỡng QCVN 10:2023/BTNMT (tham khảo)
- **As**: ≤ 0.02 mg/L
- **Cd**: ≤ 0.005 mg/L
- **Pb**: ≤ 0.05 mg/L
- **Cu**: ≤ 0.2 mg/L

### Ứng dụng
- Đánh giá rủi ro sức khỏe
- Xác định nguồn ô nhiễm
- Lập kế hoạch xử lý

---

## 5. Biểu đồ Phân bố số lượng mẫu theo trạm
**File: `5_station_distribution.png`**

### Mục đích
Hiển thị số lượng mẫu được thu thập tại mỗi trạm quan trắc.

### Cách đọc
- **Bar chart ngang**: Mỗi thanh = một trạm
- **Chiều dài thanh**: Số lượng mẫu
- **Màu sắc**: Phân biệt trạm (gradient màu)
- **Số trên thanh**: Giá trị chính xác

### Ý nghĩa
- **Trạm có nhiều mẫu**: Dữ liệu đáng tin cậy hơn, có thể phân tích chi tiết
- **Trạm có ít mẫu**: Cần thận trọng khi đánh giá, có thể thiếu dữ liệu
- **Phân bố không đều**: Một số trạm được quan trắc thường xuyên hơn

### Ứng dụng
- Đánh giá chất lượng dữ liệu
- Xác định trạm cần bổ sung quan trắc
- Cân nhắc khi phân tích (weighted analysis)

---

## 6. Biểu đồ Xu hướng theo Quý
**File: `6_quarterly_trends.png`**

### Mục đích
Phân tích sự thay đổi theo mùa của các thông số môi trường (tổng hợp qua tất cả các năm).

### Cách đọc
- **Bar chart**: Mỗi cột = một quý (Q1-Q4)
- **Chiều cao cột**: Giá trị trung bình
- **Thanh lỗi (error bar)**: Độ lệch chuẩn (±1 SD)
- **Q1**: Quý 1 (Tháng 1-3) - Mùa xuân
- **Q2**: Quý 2 (Tháng 4-6) - Mùa hè
- **Q3**: Quý 3 (Tháng 7-9) - Mùa thu
- **Q4**: Quý 4 (Tháng 10-12) - Mùa đông

### Ý nghĩa
- **Temperature**: Thường cao nhất Q2-Q3 (mùa hè), thấp nhất Q1-Q4 (mùa đông)
- **DO**: Có thể thấp hơn vào mùa hè (nhiệt độ cao → oxy hòa tan giảm)
- **Salinity**: Có thể thay đổi theo mùa mưa
- **pH**: Thường ổn định hơn, nhưng có thể thay đổi theo mùa

### Ứng dụng
- Hiểu chu kỳ tự nhiên của môi trường
- Lập kế hoạch nuôi trồng theo mùa
- Dự đoán theo mùa

---

## 7. Biểu đồ Thống kê Tổng quan
**File: `7_summary_statistics.png`**

### Mục đích
Tóm tắt các thống kê mô tả (Min, Mean-Std, Mean, Max) của các thông số môi trường chính.

### Cách đọc
- **4 nhóm cột** cho mỗi thông số:
  - **Xanh dương (Min)**: Giá trị nhỏ nhất
  - **Xanh lá (Mean - Std)**: Trung bình trừ 1 độ lệch chuẩn
  - **Cam (Mean)**: Giá trị trung bình
  - **Đỏ (Max)**: Giá trị lớn nhất

### Ý nghĩa các thống kê
- **Min**: Giá trị tốt nhất (cho các chỉ số tích cực như DO) hoặc thấp nhất (cho chất ô nhiễm)
- **Mean**: Giá trị đại diện, trung tâm của phân bố
- **Mean - Std**: Giới hạn dưới của khoảng tin cậy (±1 SD)
- **Max**: Giá trị xấu nhất hoặc cao nhất

### Khoảng cách giữa các cột
- **Khoảng cách lớn Min-Max**: Dữ liệu phân tán nhiều, biến động lớn
- **Khoảng cách nhỏ**: Dữ liệu ổn định, đồng nhất

### Ứng dụng
- Đánh giá nhanh phạm vi giá trị
- So sánh với tiêu chuẩn (QCVN)
- Xác định các thông số cần quan tâm
- Làm cơ sở cho normalization/scaling trong machine learning

---

## Tổng kết: Cách sử dụng các biểu đồ

### Phân tích tổng thể
1. **Bắt đầu với #7 (Thống kê tổng quan)**: Hiểu phạm vi giá trị
2. **Xem #1 (Time Series)**: Nắm xu hướng thời gian
3. **Xem #6 (Quý)**: Hiểu biến động theo mùa

### Phân tích so sánh
1. **#2 (Box Plot)**: So sánh giữa các trạm
2. **#5 (Phân bố mẫu)**: Đánh giá chất lượng dữ liệu

### Phân tích mối quan hệ
1. **#3 (Correlation)**: Tìm mối liên hệ giữa các biến
2. **#4 (Kim loại nặng)**: Theo dõi chất độc hại

### Ứng dụng trong nghiên cứu
- **Feature Engineering**: Sử dụng correlation để chọn biến
- **Data Quality**: Kiểm tra outliers, missing values
- **Model Validation**: So sánh dự đoán với xu hướng thực tế
- **Reporting**: Trình bày kết quả nghiên cứu

---

## Lưu ý khi đọc biểu đồ

1. **Scale khác nhau**: Mỗi thông số có đơn vị và phạm vi khác nhau, không so sánh trực tiếp giá trị số
2. **Outliers**: Các giá trị ngoại lai có thể ảnh hưởng đến trung bình, nên xem xét median
3. **Missing data**: Một số trạm có thể thiếu dữ liệu ở một số quý
4. **Tương quan ≠ Nhân quả**: Correlation không có nghĩa là một biến gây ra biến kia
5. **Thời gian**: Dữ liệu 2021-2024 có thể chưa đủ dài để phát hiện xu hướng dài hạn

---

*Tài liệu này được tạo tự động từ script `visualize_qn_data.py`*

