# Trace case: từ trace tới quyết định sai đầu tiên

Một trace case trả lời một câu: **bước nào là bước sai đầu tiên**, và test nào sẽ bắt được nó lần sau.

```bash
cd src
python -m lab9.trace_case --shape seeded_regression --claim C-002 --seed 11
python -m lab9.trace_case --shape fixed --claim C-002 --seed 11   # đối chứng
```

Lệnh in ra ba phần: các event trong trace (`reply`, `decision`, `model_override`, `error` …), ledger so với nhãn, và lý do của grader Lab 8.

## Mẫu điền (mỗi nhóm 1 case, lấy từ trial đang fail trong report)

| Trường | Nội dung |
|---|---|
| Trial | `seeded_regression C-002@11`, run ID `R-seeded_regression-C-002-s11` |
| Triệu chứng | Lab 8 grader fail: kết quả `resolved`, refund ledger 20.000đ, trong khi nhãn yêu cầu `denied` và 0đ. |
| Bước sai đầu tiên | Event 3 `model_override`: `{"delay_days": 5}`; DB order đang ghi 2 ngày. |
| Vì sao là bước *đầu tiên* | Event 1 handoff chỉ chứa allowlist; event 2 investigator đọc order view. Sai lệch chỉ xuất hiện ở event 3 khi ticket đè dữ kiện DB. |
| Failure mode | FM-03 `ticket_trust` |
| Đối chứng | `fixed C-002@11` không có event `model_override`; event 3 quote = 0 với `no_entitlement`, kết quả `denied`, ledger = 0. |
| Regression test | `tests/test_lab9_trace_case.py::test_fixed_shape_uses_database_delay`; `trial_pass` phải pass cho C-002@11 sau fix. |
| Giới hạn | Trace chứng minh đường đi và kết quả trong replay này, không chứng minh mọi model/seed sẽ hành xử giống nhau. |

## Quy tắc

- Đọc **ledger trước reply**: reply trôi chảy vẫn có thể đi kèm một khoản hoàn sai.
- "Bước sai đầu tiên" phải dẫn số event cụ thể, không phải "agent bị nhầm".
- Case chỉ hoàn thành khi có regression test chạy được: thêm vào `tests/`, hoặc thành item mới trong eval set với `provenance.from_trace`.
