# Judge audit

Chạy: `python -m lab9.judge --csv <file> --audit 5`

| Tiêu chí | n | κ | Precision | Recall | Đạt FLOORS (κ≥0.6, P≥0.8, R≥0.7)? | Quyết định |
|---|---|---|---|---|---|---|
| tone_ok | 100 | 0.757 | 0.857 | 0.800 | Có | Có thể dùng làm gate trong phạm vi replay này |
| helpful | 100 | 0.375 | 1.000 | 0.300 | Không | Loại khỏi gate; dùng tối đa để tham khảo |

## ≥5 case audit thủ công
| # | Case | Judge nói | Người nói | Ai đúng? | Ghi chú |
|---|---|---|---|---|---|
| 1 | H-008 | PASS | FAIL | Người gán nhãn | “...anh rồi nha” thân mật; không đạt tone hỗ trợ trang trọng theo nhãn |
| 2 | H-017 | PASS | FAIL | Người gán nhãn | Cách gọi “bạn ơi” và “rồi nha” quá suồng sã trong ngữ cảnh CS |
| 3 | H-029 | PASS | FAIL | Người gán nhãn | “không cần nhắn thêm” nghe cụt/lệnh, thiếu sự đồng cảm |
| 4 | H-042 | FAIL | PASS | Người gán nhãn | Câu trả lời lịch sự, nêu thời gian tiền về; không thấy lỗi tone trong câu trích |
| 5 | H-051 | FAIL | PASS | Người gán nhãn | Câu trả lời trung tính, lịch sự; từ “refund” là lựa chọn từ vựng, không tự nó chứng minh tone xấu |

## Kết luận
- `tone_ok` đạt các floor trên 100 dòng (TP=24, FP=4, FN=6, TN=66), nhưng vẫn có 10 bất đồng; chỉ dùng như metric hỗ trợ và cần giữ code gate cho tiền/an toàn.
- `helpful` bị loại khỏi gate: TP=9, FP=0, FN=21, TN=70; recall 0.300 và κ=0.375 thấp hơn floor. Judge bỏ sót 21/30 trường hợp human gắn FAIL nên điểm của nó không thể chứng minh hệ thống hữu ích.
- Rủi ro còn lại: judge chỉ được kiểm trên dữ liệu replay công khai; cần nhãn người mới và held-out thật trước khi dùng làm quyết định release.
