# Gợi ý nội dung và hình ảnh cho Slide 4: Giao diện Dashboard và Bản đồ vùng nuôi

## Cấu trúc đề xuất cho slide

### **SLIDE 4.1: Tổng quan kiến trúc Dashboard**

#### Nội dung nên có:

**1. Tiêu đề:** "4.1. Kiến trúc hệ thống Dashboard"

**2. Sơ đồ kiến trúc 3 tầng (Three-tier Architecture):**
```
┌─────────────────────────────────────┐
│   Tầng trình bày (Presentation)     │
│   - Streamlit Web Interface         │
│   - Widgets tương tác               │
│   - Bản đồ Folium                   │
└─────────────────────────────────────┘
              ↕
┌─────────────────────────────────────┐
│   Tầng xử lý nghiệp vụ (Business)   │
│   - Module dự báo (forecast.py)     │
│   - Module tính HSI (hsi.py)         │
│   - Module địa lý (geo.py)          │
└─────────────────────────────────────┘
              ↕
┌─────────────────────────────────────┐
│   Tầng dữ liệu (Data Layer)         │
│   - CSV dữ liệu quan trắc           │
│   - Model .pkl đã huấn luyện        │
│   - Dữ liệu bán kính ảnh hưởng      │
└─────────────────────────────────────┘
```

**3. Công nghệ sử dụng:**
- **Streamlit:** Framework xây dựng giao diện web
- **Folium:** Thư viện tạo bản đồ tương tác
- **Plotly:** Thư viện vẽ biểu đồ tương tác
- **Python:** Ngôn ngữ lập trình backend

**4. Ưu điểm:**
- ✅ Tính mô-đun hóa (Modularity)
- ✅ Khả năng mở rộng (Scalability)
- ✅ Dễ bảo trì và nâng cấp

---

### **SLIDE 4.2: Các thành phần giao diện chính**

#### Nội dung nên có:

**1. Tiêu đề:** "4.2. Các thành phần giao diện Dashboard"

**2. Layout tổng quan (có thể dùng screenshot thực tế):**

```
┌─────────────────────────────────────────────────────────┐
│  🌊 Dự báo môi trường nước cho Cá giò và Hàu           │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  🔮 Tham số dự báo                                      │
│  [Loài: Cá giò ▼] [Năm: 2026] [Quý: 1] [Số quý: 4]    │
│                                                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  🗺 Bản đồ các trạm quan trắc môi trường                │
│  [Năm: 2026] [Quý: 1] [☑ Hiển thị HSI]                 │
│                                                         │
│  ┌───────────────────────────────────────────────┐   │
│  │                                               │   │
│  │         [BẢN ĐỒ VỚI CÁC ĐIỂM ĐÁNH DẤU]        │   │
│  │                                               │   │
│  │  🟢 Rất phù hợp  🟡 Phù hợp                   │   │
│  │  🟠 Ít phù hợp   🔴 Không phù hợp             │   │
│  │                                               │   │
│  └───────────────────────────────────────────────┘   │
│                                                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  🎯 Tính toán chỉ số HSI chi tiết cho trạm            │
│  [🔍 Tìm kiếm trạm: ________] [📊 Tính HSI]           │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**3. Các thành phần chính:**

**A. Phần cấu hình tham số:**
- Lựa chọn loài (Cá giò / Hàu)
- Thiết lập thời gian dự báo
- Số quý cần dự báo

**B. Phần bản đồ tương tác:**
- Nền ảnh vệ tinh (Esri World Imagery)
- Điểm đánh dấu trạm với mã màu HSI
- Vòng tròn bán kính ảnh hưởng
- Popup thông tin khi click

**C. Phần tính toán HSI:**
- Công cụ tìm kiếm trạm
- Dropdown chọn trạm
- Nút kích hoạt tính toán

---

### **SLIDE 4.3: Bản đồ tương tác và mã màu HSI**

#### Nội dung nên có:

**1. Tiêu đề:** "4.3. Bản đồ tương tác với mã màu HSI"

**2. Hình ảnh đề xuất:**
- **Screenshot bản đồ thực tế** với các điểm đánh dấu màu sắc
- **Legend (Chú giải) màu sắc:**
  - 🟢 **Xanh lá:** HSI ≥ 0.85 (Rất phù hợp)
  - 🟡 **Vàng cam:** 0.75 ≤ HSI < 0.85 (Phù hợp)
  - 🟠 **Cam:** 0.50 ≤ HSI < 0.75 (Ít phù hợp)
  - 🔴 **Đỏ:** HSI < 0.50 (Không phù hợp)

**3. Các tính năng bản đồ:**
- **Vùng ảnh hưởng:** Vòng tròn xanh dương trong suốt quanh mỗi trạm
- **Popup thông tin:** Hiển thị khi click vào điểm đánh dấu
  - Tên trạm
  - Tọa độ địa lý
  - Giá trị HSI
  - Mức đánh giá
  - Bán kính áp dụng (km)
- **Tooltip:** Hiển thị thông tin nhanh khi hover

**4. Tương tác:**
- Click vào điểm đánh dấu → Tự động chọn trạm trong dropdown
- Tự động cập nhật kết quả HSI khi chọn trạm

---

### **SLIDE 4.4: Hiển thị kết quả đa phương thức**

#### Nội dung nên có:

**1. Tiêu đề:** "4.4. Hiển thị kết quả dự báo"

**2. Ba tab hiển thị:**

**Tab 1: 📈 Biểu đồ HSI**
- **Hình ảnh:** Screenshot biểu đồ đường Plotly
- **Nội dung:**
  - Đường xu hướng HSI qua các quý
  - 3 đường ngưỡng (0.85, 0.75, 0.50)
  - Thống kê: HSI trung bình, min, max
- **Màu sắc:** Đường chính màu xanh dương (#2E86AB)

**Tab 2: 🌡️ Biểu đồ các thông số môi trường**
- **Hình ảnh:** Screenshot lưới biểu đồ con (subplot grid)
- **Nội dung:**
  - Lưới 2 cột, nhiều hàng
  - Mỗi biểu đồ: 1 thông số môi trường
  - Bảng thống kê: Trung bình, Min, Max, Độ lệch chuẩn
- **Các thông số:** Nhiệt độ, DO, pH, Độ mặn, NH₄⁺, NO₃⁻, PO₄³⁻, ...

**Tab 3: 📋 Bảng dữ liệu chi tiết**
- **Hình ảnh:** Screenshot bảng dữ liệu
- **Các cột:**
  - Thời gian (Quý/Năm)
  - HSI (3 chữ số thập phân)
  - Đánh giá (Rất phù hợp/Phù hợp/Ít phù hợp/Không phù hợp)
  - Bán kính áp dụng (km, 1 chữ số thập phân)

**3. Tính năng tương tác:**
- Hover để xem giá trị chi tiết
- Zoom và pan trên biểu đồ Plotly
- Export dữ liệu (nếu có)

---

### **SLIDE 4.5: Tối ưu hóa hiệu năng**

#### Nội dung nên có:

**1. Tiêu đề:** "4.5. Tối ưu hóa hiệu năng"

**2. Các kỹ thuật tối ưu:**

**A. Xử lý song song (Parallel Processing)**
```
Trước: Tuần tự → Vài phút
Sau:  Song song (4 luồng) → Vài chục giây
```
- Sử dụng `ThreadPoolExecutor`
- Tối đa 4 luồng đồng thời
- Giảm thời gian tính toán đáng kể

**B. Cơ chế Caching**
- `@st.cache_data` decorator
- Cache dữ liệu đã load
- Cache kết quả chuyển đổi tọa độ
- So sánh hash tham số để quyết định reload

**C. Tương tác động**
- Session state để lưu trạng thái
- Tự động cập nhật khi click bản đồ
- Phản hồi nhanh, mượt mà

**3. Kết quả:**
- ⚡ Thời gian tính toán: Giảm từ vài phút → vài chục giây
- 🚀 Trải nghiệm người dùng: Mượt mà, phản hồi nhanh
- 💾 Tiết kiệm tài nguyên: Cache hiệu quả

---

### **SLIDE 4.6: Ý nghĩa thực tiễn**

#### Nội dung nên có:

**1. Tiêu đề:** "4.6. Ý nghĩa thực tiễn và ứng dụng"

**2. Đối tượng sử dụng:**

**A. Người nuôi trồng thủy sản:**
- 📅 Lập kế hoạch mùa vụ
- 🐟 Chọn thời điểm thả giống tối ưu
- ⚠️ Chuẩn bị biện pháp ứng phó khi môi trường bất lợi
- 📊 Thông tin dự báo dễ hiểu, trực quan

**B. Cơ quan quản lý:**
- 🗺️ Quy hoạch vùng nuôi trồng
- 📍 Xác định khu vực tiềm năng
- 🔍 Giám sát các khu vực rủi ro
- 📈 Hỗ trợ ra quyết định chính sách

**C. Nhà nghiên cứu:**
- 🔬 Khám phá và phân tích dữ liệu
- 📚 Nghiên cứu mối quan hệ môi trường - nuôi trồng
- 🧪 Phát triển mô hình mới

**3. Lợi ích:**
- ✅ Chuyển đổi kết quả nghiên cứu → Công cụ thực tiễn
- ✅ Hỗ trợ quyết định dựa trên dữ liệu
- ✅ Nâng cao hiệu quả và tính bền vững nuôi trồng

---

## Gợi ý hình ảnh cụ thể

### **Hình ảnh nên có trong slide:**

1. **Screenshot toàn màn hình Dashboard** (Slide 4.2)
   - Chụp toàn bộ giao diện khi đang hoạt động
   - Hiển thị đầy đủ các thành phần

2. **Screenshot bản đồ với các điểm đánh dấu** (Slide 4.3)
   - Zoom vào khu vực có nhiều trạm
   - Hiển thị rõ các màu sắc khác nhau
   - Có popup mở để thấy thông tin chi tiết

3. **Screenshot biểu đồ HSI** (Slide 4.4 - Tab 1)
   - Biểu đồ đường với các đường ngưỡng
   - Có thống kê bên dưới

4. **Screenshot lưới biểu đồ thông số môi trường** (Slide 4.4 - Tab 2)
   - Lưới 2x2 hoặc 2x3 biểu đồ
   - Hiển thị nhiều thông số cùng lúc

5. **Sơ đồ kiến trúc 3 tầng** (Slide 4.1)
   - Vẽ bằng PowerPoint hoặc công cụ vẽ sơ đồ
   - Rõ ràng, dễ hiểu

6. **Sơ đồ luồng xử lý** (có thể thêm vào Slide 4.5)
   - Quy trình từ input → xử lý → output
   - Highlight phần tối ưu hóa

---

## Lưu ý khi trình bày

1. **Màu sắc:** Sử dụng màu nhất quán với mã màu HSI trong dashboard
2. **Font chữ:** Đảm bảo dễ đọc, kích thước phù hợp
3. **Screenshot:** Nên chụp ở độ phân giải cao, rõ nét
4. **Animation:** Có thể thêm animation khi chuyển slide để tăng tính sinh động
5. **Demo live:** Nếu có thể, chuẩn bị demo trực tiếp dashboard trong buổi trình bày

---

## Cấu trúc slide đề xuất (tổng cộng 4-6 slide)

- **Slide 4.1:** Kiến trúc hệ thống (1 slide)
- **Slide 4.2:** Các thành phần giao diện (1 slide)
- **Slide 4.3:** Bản đồ tương tác (1 slide)
- **Slide 4.4:** Hiển thị kết quả (1 slide)
- **Slide 4.5:** Tối ưu hóa hiệu năng (1 slide - tùy chọn)
- **Slide 4.6:** Ý nghĩa thực tiễn (1 slide)

**Hoặc gộp lại thành 2-3 slide:**
- **Slide 4.1:** Kiến trúc + Các thành phần chính (1 slide)
- **Slide 4.2:** Bản đồ + Hiển thị kết quả (1 slide)
- **Slide 4.3:** Tối ưu hóa + Ý nghĩa thực tiễn (1 slide)


