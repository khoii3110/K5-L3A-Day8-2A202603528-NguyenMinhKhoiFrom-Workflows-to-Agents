# Báo cáo nhóm — Lab 8 LogiX-VN

## 1. Thông tin nhóm

- Tên nhóm: ABC.
- Thành viên: Nguyễn Minh Khôi (2A202603528); chi tiết xem `TEAM.md`.

## 2. Mục tiêu và cách tiếp cận

Mục tiêu là xử lý cùng một loại claim bằng bốn kiến trúc và so sánh chúng trên cùng dữ liệu, seed, MockLLM, bảng giá và evaluator. Nhóm ưu tiên ranh giới an toàn: code lấy dữ kiện đơn hàng và tính quote; host kiểm tra approval, quyền sở hữu, giới hạn theo đơn, idempotency và ghi ledger. Model không quyết định số tiền hay ghi refund.

Ba shape do nhóm triển khai theo các luồng cố định (workflow), ReAct giới hạn (single) và orchestrator với investigator chỉ đọc. Mỗi benchmark trial dùng SQLite mới. Retry/crash được kiểm tra riêng bằng crash suite.

## 3. Giải pháp

- **Workflow:** đọc claim qua `get_claim_view`, tra đơn bằng principal, tính quote từ dữ liệu đơn và policy hiện hành, rồi gửi quote đầy đủ đến `issue_refund`. Không dùng ticket để quyết định số tiền.
- **Single:** chạy ReAct tối đa 8 bước với các tool đọc. Sau khi agent nhận kết quả tính quote, shape mới gọi `issue_refund`; agent không có quyền ghi.
- **Orchestrator:** tạo handoff bằng allowlist, chỉ cấp tool đọc cho investigator, dùng kết quả đơn và quote để gọi `issue_refund`. Trace chỉ ghi handoff đã sanitize và các field được phép.
- **Trace và dữ liệu nhạy cảm:** các shape ghi event về claim đã rút gọn, đơn đã allowlist, quote, handoff/investigation và crash khi có. Không ghi ticket thô, parent secret, raw headers, SĐT, địa chỉ, ghi chú nội bộ hay tên hàng.

Ở cả ba shape, quote truyền cho host là quote đầy đủ. Host chịu trách nhiệm kiểm approval và cap tổng tiền theo đơn; crash do `InjectedCrash` được truyền lên để mô phỏng crash thật và cho phép resume.

## 4. Kết quả

Benchmark public được chạy với 14 claim × 5 seed = 70 trial/shape, seeds `11,22,33,44,55`. Giá là VND mô phỏng; latency không đo được.

| Shape | Pass rate | Pass^5 | Seed min–max | Variance | Cost/success (VND mô phỏng) | Mean / p95 steps |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| workflow | 1.000 | 1.000 | 1.000–1.000 | 0.000000 | 27.86 | 2.79 / 3 |
| single | 1.000 | 1.000 | 1.000–1.000 | 0.000000 | 27.86 | 3.43 / 4 |
| orchestrator | 1.000 | 1.000 | 1.000–1.000 | 0.000000 | 55.71 | 2.86 / 3 |
| swarm | 0.986 | 0.929 | 0.929–1.000 | 0.000816 | 49.57 | 2.80 / 3 |

Nguồn số liệu: `src/reports/benchmark.json`. Workflow và single cùng pass rate và cost/success; workflow có mean/p95 steps thấp hơn. Orchestrator cũng pass toàn bộ public trials nhưng cost/success gấp đôi workflow. Swarm có một trial sai (status `resolved` thay vì `denied`) khi seed 55 tin số ngày trong ticket thay vì dữ liệu đơn.

Crash suite: `20/20` (`src/reports/crash.json`). Bộ student tests: `248 passed`; cổng host: `54 passed`. Public benchmark không ghi nhận secret leak hoặc approval bypass trong các trial được chấm.

Quyết định kiến trúc xem `report/team/decision_adr.md`; research card và ablation xem `report/team/research_card.md`.

## 5. Khó khăn và cách xử lý

Môi trường ban đầu báo không có `.venv/bin/activate`, do đang dùng Git Bash trên Windows. Tạo virtual environment tại `src/.venv` và activate bằng `source .venv/Scripts/activate`; smoke sau đó in `lab8.smoke pass`. Các lệnh pytest được chạy bằng Python trong virtualenv để dùng đúng dependency; kết quả là 248 student tests và 54 host tests đều pass.

## 6. Tổng hợp đóng góp

Nhóm có một thành viên. Vai trò và kiểm thử đã ghi trong `TEAM.md`; báo cáo cá nhân là `report/team/2A202603528_NguyenMinhKhoi.md`.

## 7. Hạn chế và hướng cải thiện

Kết quả hiện tại dựa trên public corpus nhỏ gồm 14 claim và MockLLM xác định theo seed; không đại diện cho model hay traffic production. Latency là `unavailable`, chi phí chỉ là ước tính mô phỏng. Quyết định có thể thay đổi nếu đánh giá trên tập dữ liệu mới cho thấy một shape khác đạt độ đúng tốt hơn đáng kể với chi phí hợp lý.

## 8. Tài liệu tham khảo

- `docs/architecture.md`, `docs/business_rules.md`, `docs/contracts.md`, `docs/metrics.md`.
- `src/reports/benchmark.json` và `src/reports/crash.json` (bằng chứng do công cụ lab sinh).
- Cemri et al., *Why Do Multi-Agent LLM Systems Fail?*, arXiv:2503.13657, https://arxiv.org/abs/2503.13657.
