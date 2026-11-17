# Decision record

Điền sau dấu `:` trên cùng dòng, không xóa nhãn. Giảng viên và `python -m lab8.check_submission` (chạy trong `src/`) đọc các dòng này bằng máy. Không đổi tên hay dời file này khỏi `report/team/`.
`Shape chọn` phải là đúng một trong: `workflow`, `single`, `orchestrator`, `swarm`. Đây là shape được chấm cổng hidden.

- Shape chọn: workflow
- Commit hash: 034c6c421c198dae67a9211d15e2587d5a378972
- Run id dẫn chứng: R-workflow-C-001-s11 (benchmark: `src/reports/benchmark.json`)
- Pass rate / pass^5 / seed min-max / variance: 1.000 / 1.000 / 1.000–1.000 / 0.000000 (70 trial, 14 claim × 5 seed)
- Cost per success (mô phỏng, VND): 27.86
- Crash safety: 20/20 (`src/reports/crash.json`)
- Secret leak / approval bypass: 0 / 0 trên 70 trial public

## Vì sao shape này

Chọn workflow vì đây là kiến trúc ít tự chủ nhất và vẫn đạt 70/70 trial public, pass^5 = 1.000, variance = 0.000000, với cost/success mô phỏng 27.86 VND. Single cũng đạt 70/70 và cùng cost/success nhưng tốn nhiều bước hơn (mean/p95 3.43/4 so với 2.79/3). Orchestrator không tăng pass rate trên corpus này và tốn 55.71 VND/success. Swarm có một lỗi kiểm chứng ở seed 55, pass rate 0.986, cùng với chi phí cao hơn workflow. Crash suite đạt 20/20.

## Có đáng đổi lấy multi-agent không

Chưa đáng với bằng chứng hiện có: orchestrator không tăng pass rate trên public nhưng tăng gấp đôi cost/success so với workflow. Kết luận sẽ được xem lại nếu tập dữ liệu mới cho thấy investigator cải thiện đáng kể độ đúng/độ an toàn mà chi phí tăng thêm chấp nhận được.

## Trace và bằng chứng

Trace ghi run id và event đã rút gọn: claim chỉ giữ field cần thiết, dữ liệu order qua allowlist, quote, handoff đã sanitize, kết quả investigation đã giới hạn field và event crash nếu phát sinh. Không ghi ticket thô, parent secret, raw headers, SĐT, địa chỉ, ghi chú nội bộ hay tên hàng. Public benchmark đã pass toàn bộ 70 trial workflow, trong đó grader kiểm tra contract và artifact trace.

## Giới hạn

MockLLM không phải model sản xuất; kết quả chỉ áp dụng cho public corpus, seeds, tool và giá mô phỏng đã dùng. Latency là `unavailable`.
