# Previous Treatment Screen — Phân tích Gap giữa PRD và Code

> Task: [BE TASK] Clarify Previous Treatment Screen API And Exclude Irrelevant History States
> API hiện tại: `GET /api/patient/treatments/history`

---

## 0. Kết luận chính: PRD KHÔNG thiếu — Code implement sai

Sau khi đọc toàn bộ PRD (FR-004, FR-005, FR-006, FR-007, FR-010, FR-011), lifecycle đầy đủ của một case đã được định nghĩa rõ ràng xuyên suốt các FR:

```
PRD Lifecycle (xuyên suốt các FR):
  FR-004: draft → sent → expired/withdrawn/archived/cancelled_other_accepted/cancelled_inquiry_cancelled
  FR-005: → accepted (patient chọn 1 quote)
  FR-006: → confirmed (patient thanh toán deposit) — Booking entity được tạo
  FR-010: → in_progress (provider check-in patient) — Treatment execution
  FR-011: → aftercare (provider hoàn thành treatment, FR-011 activate aftercare)
  FR-011: → completed (aftercare hoàn thành)
```

Tuy nhiên, PRD dùng thuật ngữ status trên **Booking entity**, không phải trên Quote entity. Đây là điểm mấu chốt.

---

## 1. PRD phân biệt rõ Quote vs Booking — Code đang gộp chung

**Theo PRD:**
- **Quote** có status: `draft, sent, expired, withdrawn, archived, accepted, cancelled_other_accepted, cancelled_inquiry_cancelled`
- **Booking** có status: `Accepted → Confirmed → In Progress → Aftercare → Completed | Cancelled` (FR-006 Key Entities)

Quote status kết thúc ở `accepted`. Sau đó, **Booking entity** được tạo và mang status riêng.

**Trong code thực tế:**
- Không có Booking model riêng mang status lifecycle
- Quote model đang gánh luôn cả status của Booking: `quote, accepted, rejected, scheduled, confirmed, inprogress, aftercare, completed, cancelled`
- DB migration comment xác nhận điều này

**Vấn đề:** Code đã merge Quote + Booking status vào cùng 1 field trên Quote table. Điều này không sai về mặt kỹ thuật (có thể là design decision), nhưng tạo ra sự nhầm lẫn khi đọc PRD.

---

## 2. Mapping PRD Status → DB Status

| Giai đoạn | PRD Entity | PRD Status | DB Status (trên quotes table) |
|-----------|-----------|------------|-------------------------------|
| Quote tạo draft | Quote | draft | draft |
| Quote gửi patient | Quote | sent | quote |
| Quote hết hạn | Quote | expired | expired |
| Quote bị rút | Quote | withdrawn | rejected (?) |
| Quote bị hủy (quote khác accepted) | Quote | cancelled_other_accepted | cancelled |
| Quote bị hủy (inquiry cancelled) | Quote | cancelled_inquiry_cancelled | cancelled |
| Patient accept quote | Quote/Booking | accepted | accepted |
| Patient thanh toán deposit | Booking | confirmed | confirmed |
| Lên lịch | Booking | (không rõ) | scheduled |
| Provider check-in | Booking | in_progress | inprogress |
| Treatment xong, aftercare bắt đầu | Booking | aftercare | aftercare |
| Aftercare hoàn thành | Booking | completed | completed |

**Câu hỏi còn lại:**
- `scheduled` trong DB nằm giữa `confirmed` và `inprogress` — PRD không mention status này rõ ràng. Nó có phải là một bước riêng hay chỉ là alias?
- `rejected` trong DB có phải map với `withdrawn` trong PRD không?
- Các loại `cancelled` khác nhau trong PRD (`cancelled_other_accepted`, `cancelled_inquiry_cancelled`) đều map về 1 giá trị `cancelled` trong DB — có cần phân biệt không?

---

## 3. API "Previous Treatment" — Filter cần sửa

API hiện tại filter: `status = 'confirmed'`

Theo PRD, "previous treatment" (treatment đã hoàn thành) nên là:
- `completed` — aftercare đã xong
- Có thể bao gồm `aftercare` — treatment xong, đang aftercare

**Câu hỏi:**
- "Previous Treatment" screen hiển thị treatment ở status nào?
  - Chỉ `completed`?
  - `completed` + `aftercare`?
  - Bao gồm cả `inprogress` (đang điều trị)?
- Treatment bị cancelled sau khi đã inprogress có hiển thị không?

---

## 4. Quote Model thiếu status constants

Quote Model chỉ define 6 constants, thiếu 5 status đang dùng trong DB:

```php
// Có trong Model
STATUS_DRAFT = 'draft'
STATUS_QUOTE = 'quote'        // = PRD "sent"
STATUS_ACCEPTED = 'accepted'
STATUS_CANCELLED = 'cancelled'
STATUS_EXPIRED = 'expired'
STATUS_CONFIRMED = 'confirmed'

// Thiếu trong Model (nhưng có trong DB và code sử dụng)
// STATUS_SCHEDULED = 'scheduled'
// STATUS_INPROGRESS = 'inprogress'
// STATUS_AFTERCARE = 'aftercare'
// STATUS_COMPLETED = 'completed'
// STATUS_REJECTED = 'rejected'
```

Đây là technical debt — code đang dùng string literals thay vì constants.

---

## 5. Figma screen cần field nào?

Response hiện tại trả về:
```
id, quote_id, provider (id/name/country), treatment (id/name/description),
treatment_date, aftercare_status, booking_date, completion_date,
quote_amount, currency, has_review, has_aftercare, created_at
```

**Câu hỏi:**
- Figma design (node 85-14812) yêu cầu hiển thị chính xác field nào?
- Có field nào thừa hoặc thiếu so với Figma?

---

## 6. Dữ liệu null trong response

Sample response cho thấy tất cả records đều có `provider.country: null`, `aftercare_status: "not_started"`, `completion_date: null`.

Nguyên nhân rõ ràng: API filter `status = 'confirmed'` nên lấy về những quote mới thanh toán deposit, chưa thực sự điều trị xong. Đổi filter sang `completed`/`aftercare` sẽ giải quyết vấn đề này.

---

## Tóm tắt

| Vấn đề | Nguyên nhân | Action |
|--------|-------------|--------|
| PRD thiếu status? | Không — PRD đầy đủ, chỉ phân tán qua nhiều FR | Không cần thêm PRD |
| Code thiếu status constants? | Có — Quote Model thiếu 5 constants | BE bổ sung constants |
| API filter sai? | Có — đang filter `confirmed` thay vì `completed`/`aftercare` | BE sửa filter sau khi PM confirm |
| `scheduled` không rõ trong PRD? | Đúng — cần PM clarify | Hỏi PM |
| `rejected` vs `withdrawn`? | Cần PM confirm mapping | Hỏi PM |
| Figma field mapping? | Chưa có | Hỏi PM |
