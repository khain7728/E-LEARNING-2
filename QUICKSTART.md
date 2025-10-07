# HƯỚNG DẪN CHẠY NHANH E-LEARNING-2

## Cài đặt (nếu cần)
```bash
pip install matplotlib numpy
```

## Test 1: Client chưa tối ưu

### Terminal 1 - Server:
```bash
cd Server
python server.py
```

### Terminal 2 - Client unoptimized:
```bash  
cd Client
python client_unoptimized.py
```
*Chạy khoảng 10-15 giây rồi nhấn Ctrl+C để dừng*

---

## Test 2: Client đã tối ưu

### Terminal 1 - Server (chạy lại):
```bash
cd Server  
python server.py
```

### Terminal 2 - Client optimized:
```bash
cd Client
python client_optimized.py
```
*Chạy khoảng 10-15 giây rồi nhấn Ctrl+C để dừng*

---

## Phân tích kết quả:
```bash
cd Analysis
python analyze_results.py
```

## Kết quả sẽ có:
- ✅ Báo cáo so sánh trên console  
- ✅ File `udp_optimization_report.txt`
- ✅ File `metrics_comparison.csv`
- ✅ Biểu đồ `udp_delay_comparison.png` (nếu có matplotlib)

## Kết quả mong đợi:
- **Delay giảm 30-50%** 
- **Jitter giảm 40-60%**
- **Tỷ lệ mất gói giảm đáng kể**