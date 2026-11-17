# Team

## Thông tin nhóm

- Tên nhóm: ABC
- Lớp: L3A
- Repo nhóm: `K5-L3A-DAY08-ABC-FromWorkflowsToAgents`
- Nhánh nộp: `main`

## Thành viên

| STT | Họ tên | MSSV | Vai trò |
| --: | ------ | ---- | ------- |
|   1 | Nguyễn Minh Khôi | 2A202603528 | Triển khai ba shape, kiểm thử và tổng hợp báo cáo |

Gợi ý chia vai:

- Nhóm 6 người: integration; workflow; single agent; orchestrator; ledger/policy/crash; eval/report.
- Nhóm 4 người: workflow + integration; single; orchestrator + handoff; ledger + evaluation.

## Bảng đóng góp

`python -m lab8.check_submission` đọc bảng này bằng máy: giữ nguyên tiêu đề `## Bảng đóng góp` và các cột. Mỗi người một dòng: commit có nội dung và ít nhất một test đã thêm hoặc sửa.

| Người | Vai | Commit | Test đã thêm hoặc sửa |
| --- | --- | --- | --- |
| Nguyễn Minh Khôi (2A202603528) | Ba shape, kiểm thử, báo cáo |  | Student tests: 248 passed; host tests: 54 passed |

## Cá nhân

Mỗi thành viên đồng thời tạo một báo cáo riêng trong `report/` theo dạng:

```text
report/team/MSSV_HoTen.md
```

Ví dụ: `report/team/20241234_NguyenVanAn.md`.

Sao chép mục dưới đây cho từng thành viên.

## 2A202603528_NguyenMinhKhoi

### Phần việc phụ trách

- Triển khai `workflow`, `single`, `orchestrator`; kiểm thử student và host.
- Tổng hợp benchmark, crash safety và các báo cáo nhóm.

### Đóng góp cụ thể

- Student tests: 248 passed; host tests: 54 passed.
- Public benchmark: workflow đạt pass rate 1.000, pass^5 1.000; crash safety 20/20.

### Bằng chứng

- `src/reports/benchmark.json`; run id dẫn chứng `R-workflow-C-001-s11`.
- `src/reports/crash.json`: crash safety 20/20.
- Các test: `python -m pytest -q -m student -o addopts=` và `python -m pytest -q`.
