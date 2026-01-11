```bash
python3 merge.py --input Tong-hop.xlsx --output Tong-hop-21-24.xlsx
python3 gen.py --input Tong-hop-21-24.xlsx --output Tong-hop-21-24-gen.xlsx --sheet Gop_2021_2024 --excel-cols "K,L,M,O,P,R,S,T,V,W,X,Y,Z,AA,AB,AC,AD,
AE,AF" --method half --mode replace --seed 42
```

---

## Tóm tắt bộ dữ liệu Quảng Ninh cho slide

**Bộ dữ liệu Quảng Ninh Dataset** là bộ dữ liệu phản ánh chất lượng nước biển tại các trạm quan trắc ven biển Quảng Ninh, được thu thập theo quý từ năm 2021 đến 2024. Dữ liệu bao gồm các thông số vật lý (nhiệt độ, độ mặn, pH, độ trong), hóa học (oxy hòa tan, amoni, phosphat, kim loại nặng như As, Cd, Pb, Cu, Hg, Zn, Cr) và sinh học (Coliform, TSS) tại nhiều vị trí quan trắc khác nhau (KHM/NB).

Sau bước khám phá và trực quan hóa dữ liệu, bộ dữ liệu được tiền xử lý qua các bước:

**Gộp và sắp xếp dữ liệu**: Gộp dữ liệu từ các sheet theo năm (2021-2024) trong file Tong-hop.xlsx thành một bộ dữ liệu thống nhất, sắp xếp theo trạm quan trắc, năm và quý để đảm bảo tính nhất quán về thời gian và không gian.

**Xử lý giá trị left-censored**: Xử lý các bản ghi chứa giá trị dưới ngưỡng phát hiện (dạng <LOD, ví dụ <0.01) bằng phương pháp half-detection limit, tức thay thế bằng một nửa giá trị ngưỡng (ví dụ <0.01 → 0.005) để phục vụ phân tích định lượng.

**Chuẩn hóa và bổ sung dữ liệu**: 
- Đổi tên các cột sang dạng chuẩn tiếng Anh (ví dụ: "KHM" → "Station", "Quý" → "Quarter", "Nhiệt độ" → "Temperature")
- Kết hợp với dữ liệu tọa độ địa lý (lat, lon) của các trạm quan trắc
- Bổ sung các biến môi trường tổng hợp cần thiết cho mô hình như H₂S, BOD5, Alkalinity thông qua các phân phối thống kê phù hợp (lognormal, normal) dựa trên đặc tính của từng thông số.