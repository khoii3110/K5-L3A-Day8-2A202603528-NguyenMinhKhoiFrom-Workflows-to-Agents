# Báo cáo cá nhân — 2A202603528_NguyenMinhKhoi

## 1. Thông tin thành viên

- Họ tên: Nguyễn Minh Khôi
- MSSV: 2A202603528

## 2. Phần việc phụ trách

Triển khai ba shape `workflow`, `single`, `orchestrator`; chạy kiểm thử student và host; tổng hợp kết quả benchmark, crash suite và báo cáo nhóm.

## 3. Đóng góp cụ thể

- Hoàn thiện các luồng xử lý claim theo contract chung, dùng tool đọc để xác minh dữ liệu và để host kiểm approval/ghi refund.
- Thêm trace an toàn, dùng handoff allowlist cho orchestrator và chuyển tiếp crash để kiểm tra retry/idempotency.
- Chưa có commit riêng; thay đổi đang ở working tree.

## 4. Bằng chứng

- Student tests: `python -m pytest -q -m student -o addopts=` — 248 passed.
- Host tests: `python -m pytest -q` — 54 passed.
- Crash suite: `src/reports/crash.json` — 20/20.
- Public benchmark: `src/reports/benchmark.json`; run id dẫn chứng `R-workflow-C-001-s11`; workflow pass rate 1.000, pass^5 1.000, cost/success mô phỏng 27.86 VND.

## 5. Công cụ AI đã dùng

Đã dùng Copilot trong VS Code để hỗ trợ triển khai ba shape và soạn báo cáo. Kết quả được kiểm tra bằng student tests, host tests và crash suite; các kết quả được ghi trong báo cáo không tự sửa tay file JSON do công cụ lab sinh.

## 6. Tự đánh giá

Các shape đạt toàn bộ public student tests và crash suite. Workflow được chọn làm kiến trúc ít tự chủ nhất vẫn đạt 100% trên public benchmark.
