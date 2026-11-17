# Research card

File này nằm cố định ở `report/team/research_card.md`; `python -m lab8.check_submission` đọc cột "Nhóm điền" bằng máy.

Phần này nối tiếp phần mini research ở buổi lý thuyết (slide 62–63). Chọn **một** câu R1–R4, điền 6 dòng, rồi biến nó thành **một ablation** chạy được trong lab: giữ nguyên model (MockLLM), tool, seed, corpus và giá, chỉ thay đổi một biến.

| Câu | Nguồn (thư viện tham khảo, slide 68–69) | Câu hỏi gợi ý cho lab |
| --- | --- | --- |
| R1 · Scaling | Google Research 2026, *Towards a Science of Scaling Agent Systems* | Task claims chủ yếu tuần tự hay song song được? Dự đoán thêm investigator sẽ làm pass rate và cost/success thay đổi thế nào. |
| R2 · Failure taxonomy | MAST, NeurIPS 2025, *Why Do Multi-Agent LLM Systems Fail?* | Các trial fail của swarm (seed 55) thuộc nhóm nào: lỗi giao việc, lệch mục tiêu, hay lỗi kiểm chứng? |
| R3 · Architecture choices | AgentArch, AACL 2026 | Nếu đổi topology mà giữ nguyên mọi thứ khác, biến nào phải cố định để kết luận còn đúng? |
| R4 · Evaluation confounders | EMNLP 2026, *Rethinking Evaluation of MAS Efficiency* | Làm sao chứng minh chênh lệch giữa A/B/C/D là do topology, không phải do prompt, tool hay seed? |

## Phiếu của nhóm

| Field | Hướng dẫn | Nhóm điền |
| --- | --- | --- |
| CÂU | R1 / R2 / R3 / R4 | R2 — Failure taxonomy |
| SOURCE | Paper/blog, năm, URL, loại bằng chứng (benchmark, production report, blog kinh nghiệm) | Cemri et al. (2025), *Why Do Multi-Agent LLM Systems Fail?*, https://arxiv.org/abs/2503.13657; nghiên cứu taxonomy dựa trên phân tích trace. |
| CLAIM | Một kết luận gốc của nguồn. Không viết rộng hơn phạm vi paper | Nguồn giới thiệu MAST: phân tích 150 trace, taxonomy có 14 mode lỗi trong ba nhóm lớn (system design, inter-agent misalignment, task verification); nhóm tác giả báo cáo inter-annotator agreement kappa = 0.88. |
| BOUNDARY | Model / dataset / setup giới hạn kết luận đó | Nghiên cứu phân tích MAST-Data với hơn 1.600 trace từ 7 framework MAS; đây là các trace/framework trong nghiên cứu, không phải bằng chứng rằng cùng tỉ lệ lỗi áp dụng cho bài lab hoặc production. Thí nghiệm của nhóm chỉ có MockLLM xác định, 14 claim public và 5 seed. |
| HYPOTHESIS | Nếu đổi shape A→B (hoặc bật/tắt một thành phần), metric X sẽ đổi theo hướng nào, khoảng bao nhiêu | So swarm với workflow trên cùng public corpus: việc để swarm diễn giải ticket thay vì chỉ dựa dữ liệu đơn có thể gây lỗi kiểm chứng ở các claim mâu thuẫn. Dự đoán swarm có pass rate thấp hơn workflow khoảng 1–2 điểm phần trăm và cost/success cao hơn; workflow giữ 100% pass. |
| METHOD | Biến giữ cố định: model, tools, seed, corpus, giá, evaluator. Biến duy nhất được thay đổi: … | Dùng benchmark public hiện có: cùng MockLLM, corpus 14 claim, seeds 11/22/33/44/55, giá, evaluator và tool registry. Biến so sánh là shape (workflow đối chiếu swarm); mỗi trial dùng SQLite mới. |
| FAILURE / METRIC | Một lỗi dự kiến và cách đo nó: pass rate, pass^5, variance, cost/success, leak, bypass | Lỗi dự kiến: status sai khi ticket mâu thuẫn với order. Đo pass rate, pass^5, seed variance, cost/success và lý do fail; phân loại miss swarm tại C-002/seed 55 là lỗi task verification theo diễn giải của nhóm. |

## Kết quả ablation

- Lệnh đã chạy (copy nguyên văn): `python -m lab8.benchmark --shapes workflow,single,orchestrator,swarm --cases data/public_claims.jsonl --seeds 11,22,33,44,55 --out reports/benchmark.json`
- Run id / file report: `R-workflow-C-001-s11`; kết quả tổng hợp ở `src/reports/benchmark.json`. Lỗi swarm quan sát được ở C-002/seed 55.
- Kết quả so với hypothesis (đúng / sai / không kết luận được), kèm số liệu: phù hợp với dự đoán trên corpus này. Workflow pass 1.000, pass^5 1.000, variance 0, cost/success 27.86 VND; swarm pass 0.986, pass^5 0.929, variance 0.000816, cost/success 49.57 VND. Swarm có một miss (`resolved` thay vì `denied`) ở seed 55. Đây là quan sát trên public benchmark nhỏ, không phải kết luận tổng quát về MAS.
- Giới hạn: MockLLM không phải model sản xuất, latency là `unavailable`.

Muốn đi xa hơn một ablation để lấy điểm cộng thì xem [docs/bonus_topics.md](../../docs/bonus_topics.md).
