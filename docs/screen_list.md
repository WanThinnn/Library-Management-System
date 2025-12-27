# Danh sách màn hình - Library Management System

Bảng dưới đây liệt kê tất cả các màn hình trong hệ thống Quản lý Thư viện, đồng bộ với [Chương 6 - Cài đặt và Thử nghiệm](./chapter6_installation_testing.md).

---

## 1. Xác thực & Tài khoản (6 màn hình)

|  STT  | Màn hình          | Loại màn hình      | Chức năng                                                   |
| :---: | ----------------- | ------------------ | ----------------------------------------------------------- |
|   1   | Đăng nhập         | Nhập liệu          | Cho phép người dùng đăng nhập vào hệ thống (username/email) |
|   2   | Đăng ký tài khoản | Nhập liệu          | Đăng ký tài khoản mới, chờ Quản lý kích hoạt                |
|   3   | Quên mật khẩu     | Nhập liệu          | Nhập email để yêu cầu đặt lại mật khẩu                      |
|   4   | Đặt lại mật khẩu  | Nhập liệu          | Nhập mật khẩu mới từ link trong email                       |
|   5   | Trang chủ         | Màn hình chính     | Hiển thị tổng quan hệ thống, thống kê, menu chức năng       |
|   6   | Thông tin cá nhân | Tra cứu, Nhập liệu | Xem và chỉnh sửa thông tin tài khoản, đổi mật khẩu          |

---

## 2. Quản lý Độc giả - YC1 (5 màn hình)

|  STT  | Màn hình              | Loại màn hình | Chức năng                                             |
| :---: | --------------------- | ------------- | ----------------------------------------------------- |
|   7   | Lập thẻ độc giả       | Nhập liệu     | Tạo mới thẻ độc giả, validate tuổi theo QĐ1           |
|   8   | Danh sách độc giả     | Tra cứu       | Hiển thị, tìm kiếm, lọc, phân trang danh sách độc giả |
|   9   | Chi tiết độc giả      | Tra cứu       | Xem thông tin chi tiết, lịch sử mượn trả của độc giả  |
|  10   | Sửa thông tin độc giả | Nhập liệu     | Chỉnh sửa thông tin độc giả, validate tuổi            |
|  11   | Xóa độc giả           | Xác nhận      | Xác nhận xóa độc giả (kiểm tra ràng buộc)             |

---

## 3. Quản lý Sách - YC2, YC3 (10 màn hình)

|  STT  | Màn hình              | Loại màn hình  | Chức năng                                          |
| :---: | --------------------- | -------------- | -------------------------------------------------- |
|  12   | Chọn phương thức nhập | Màn hình chính | Chọn nhập sách thủ công hoặc từ Excel              |
|  13   | Nhập sách thủ công    | Nhập liệu      | Nhập thông tin sách mới, validate năm XB theo QĐ2  |
|  14   | Nhập sách từ Excel    | Nhập liệu      | Import sách hàng loạt từ file Excel                |
|  15   | DS phiếu nhập sách    | Tra cứu        | Hiển thị danh sách các phiếu nhập sách             |
|  16   | Chi tiết phiếu nhập   | Tra cứu        | Xem chi tiết một phiếu nhập sách                   |
|  17   | Hủy phiếu nhập sách   | Xác nhận       | Hủy phiếu nhập (kiểm tra thời hạn, sách đang mượn) |
|  18   | Tra cứu sách          | Tra cứu        | Tìm kiếm theo tên, tác giả, thể loại, NXB          |
|  19   | Chi tiết sách         | Tra cứu        | Xem thông tin chi tiết, số lượng còn lại           |
|  20   | Sửa thông tin sách    | Nhập liệu      | Chỉnh sửa tất cả các trường thông tin sách         |
|  21   | Xóa sách              | Xác nhận       | Xác nhận xóa sách (kiểm tra sách đang mượn)        |

---

## 4. Mượn sách - YC4 (4 màn hình)

|  STT  | Màn hình            | Loại màn hình | Chức năng                                                       |
| :---: | ------------------- | ------------- | --------------------------------------------------------------- |
|  22   | Lập phiếu mượn      | Nhập liệu     | Tạo phiếu mượn sách, validate thẻ còn hạn, số sách tối đa (QĐ4) |
|  23   | DS phiếu mượn       | Tra cứu       | Hiển thị, tìm kiếm, phân trang danh sách phiếu mượn             |
|  24   | Chi tiết phiếu mượn | Tra cứu       | Xem chi tiết phiếu mượn                                         |
|  25   | Hủy phiếu mượn      | Xác nhận      | Hủy phiếu mượn (kiểm tra thời hạn, rollback trạng thái)         |

---

## 5. Trả sách - YC5 (4 màn hình)

|  STT  | Màn hình           | Loại màn hình | Chức năng                                                    |
| :---: | ------------------ | ------------- | ------------------------------------------------------------ |
|  26   | Lập phiếu trả      | Nhập liệu     | Tạo phiếu trả sách, tự động tính tiền phạt nếu trả trễ (QĐ5) |
|  27   | DS phiếu trả       | Tra cứu       | Hiển thị, tìm kiếm, phân trang danh sách phiếu trả           |
|  28   | Chi tiết phiếu trả | Tra cứu       | Xem chi tiết phiếu trả, tiền phạt                            |
|  29   | Hủy phiếu trả      | Xác nhận      | Hoàn tác trả sách (kiểm tra thời hạn, đặt lại trạng thái)    |

---

## 6. Thu tiền phạt - YC6 (4 màn hình)

|  STT  | Màn hình           | Loại màn hình | Chức năng                                           |
| :---: | ------------------ | ------------- | --------------------------------------------------- |
|  30   | Lập phiếu thu      | Nhập liệu     | Tạo phiếu thu tiền phạt, validate số tiền theo QĐ6  |
|  31   | DS phiếu thu       | Tra cứu       | Hiển thị, tìm kiếm danh sách phiếu thu tiền         |
|  32   | Chi tiết phiếu thu | Tra cứu       | Xem chi tiết một phiếu thu                          |
|  33   | Hủy phiếu thu      | Xác nhận      | Hủy phiếu thu (kiểm tra thời hạn, hoàn tiền vào nợ) |

---

## 7. Báo cáo - YC7 (4 màn hình)

|  STT  | Màn hình              | Loại màn hình | Chức năng                                               |
| :---: | --------------------- | ------------- | ------------------------------------------------------- |
|  34   | BC mượn theo thể loại | Báo biểu      | Thống kê số lượt mượn theo thể loại sách, xuất Excel    |
|  35   | BC tình hình mượn     | Báo biểu      | Thống kê tình hình mượn sách theo thời gian, xuất Excel |
|  36   | BC sách trả trễ       | Báo biểu      | Danh sách sách trả trễ hạn và tiền phạt, xuất Excel     |
|  37   | BC tiền phạt thu được | Báo biểu      | Thống kê thu tiền theo thời gian, xuất Excel            |

---

## 8. Thay đổi quy định - YC8 (2 màn hình)

|  STT  | Màn hình          | Loại màn hình | Chức năng                                                             |
| :---: | ----------------- | ------------- | --------------------------------------------------------------------- |
|  38   | Thay đổi quy định | Nhập liệu     | Cấu hình tham số: tuổi độc giả, thời hạn thẻ, ngày mượn, tiền phạt... |
|  39   | Đặt lại quy định  | Xác nhận      | Reset về giá trị mặc định của hệ thống                                |

---

## 9. Quản lý Loại độc giả (4 màn hình)

|  STT  | Màn hình          | Loại màn hình | Chức năng                                      |
| :---: | ----------------- | ------------- | ---------------------------------------------- |
|  40   | DS loại độc giả   | Tra cứu       | Hiển thị danh sách các loại độc giả            |
|  41   | Thêm loại độc giả | Nhập liệu     | Tạo mới loại độc giả                           |
|  42   | Sửa loại độc giả  | Nhập liệu     | Chỉnh sửa loại độc giả đã có                   |
|  43   | Xóa loại độc giả  | Xác nhận      | Xác nhận xóa loại độc giả (kiểm tra ràng buộc) |

---

## 10. Quản lý Người dùng (4 màn hình)

|  STT  | Màn hình        | Loại màn hình | Chức năng                                             |
| :---: | --------------- | ------------- | ----------------------------------------------------- |
|  44   | DS người dùng   | Tra cứu       | Hiển thị danh sách tài khoản người dùng (chỉ Quản lý) |
|  45   | Thêm người dùng | Nhập liệu     | Tạo mới tài khoản Thủ thư hoặc Quản lý                |
|  46   | Sửa người dùng  | Nhập liệu     | Chỉnh sửa tài khoản, thay đổi vai trò, khóa/mở khóa   |
|  47   | Xóa người dùng  | Xác nhận      | Xác nhận xóa tài khoản (không thể xóa chính mình)     |

---

## 11. Phân quyền (9 màn hình)

|  STT  | Màn hình           | Loại màn hình      | Chức năng                                              |
| :---: | ------------------ | ------------------ | ------------------------------------------------------ |
|  48   | DS nhóm quyền      | Tra cứu            | Hiển thị danh sách nhóm quyền                          |
|  49   | Thêm nhóm quyền    | Nhập liệu          | Tạo mới nhóm quyền                                     |
|  50   | Sửa nhóm quyền     | Nhập liệu          | Chỉnh sửa nhóm quyền đã có                             |
|  51   | Xóa nhóm quyền     | Xác nhận           | Xác nhận xóa nhóm quyền (kiểm tra ràng buộc)           |
|  52   | Ma trận phân quyền | Tra cứu, Nhập liệu | Xem và gán quyền (Xem/Thêm/Sửa/Xóa) cho từng chức năng |
|  53   | DS chức năng       | Tra cứu            | Hiển thị danh sách chức năng hệ thống                  |
|  54   | Thêm chức năng     | Nhập liệu          | Tạo mới chức năng                                      |
|  55   | Sửa chức năng      | Nhập liệu          | Chỉnh sửa chức năng đã có                              |
|  56   | Xóa chức năng      | Xác nhận           | Xác nhận xóa chức năng                                 |

---

## Thống kê tổng hợp

### Theo nhóm chức năng

| Nhóm chức năng          | Số lượng |
| ----------------------- | :------: |
| Xác thực & Tài khoản    |    6     |
| Quản lý Độc giả (YC1)   |    5     |
| Quản lý Sách (YC2, YC3) |    10    |
| Mượn sách (YC4)         |    4     |
| Trả sách (YC5)          |    4     |
| Thu tiền phạt (YC6)     |    4     |
| Báo cáo (YC7)           |    4     |
| Thay đổi quy định (YC8) |    2     |
| Quản lý Loại độc giả    |    4     |
| Quản lý Người dùng      |    4     |
| Phân quyền              |    9     |
| **TỔNG CỘNG**           |  **56**  |

### Theo loại màn hình

| Loại màn hình      | Số lượng |
| ------------------ | :------: |
| Màn hình chính     |    2     |
| Tra cứu            |    16    |
| Nhập liệu          |    22    |
| Báo biểu           |    4     |
| Xác nhận           |    11    |
| Tra cứu, Nhập liệu |    1     |
| **TỔNG CỘNG**      |  **56**  |

---

## Chú thích loại màn hình

| Loại               | Mô tả                                      |
| ------------------ | ------------------------------------------ |
| Màn hình chính     | Màn hình điều hướng, tổng quan, thông báo  |
| Tra cứu            | Hiển thị danh sách, tìm kiếm, xem chi tiết |
| Nhập liệu          | Form nhập dữ liệu, thêm/sửa thông tin      |
| Báo biểu           | Báo cáo thống kê, biểu đồ, xuất Excel      |
| Xác nhận           | Màn hình xác nhận hành động xóa/hủy        |
| Tra cứu, Nhập liệu | Kết hợp xem thông tin và chỉnh sửa         |
