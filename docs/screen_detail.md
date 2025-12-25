# 5.3 Mô tả các màn hình - Library Management System

---

## 5.3.1 Màn hình đăng nhập

### a. Giao diện
*(Chèn ảnh chụp màn hình)*

### b. Mô tả các đối tượng trên màn hình

|  STT  | Tên               | Kiểu        | Ràng buộc            | Chức năng                         |
| :---: | ----------------- | ----------- | -------------------- | --------------------------------- |
|   1   | txtUsername       | TextBox     | Bắt buộc, không rỗng | Nhập tên đăng nhập                |
|   2   | txtPassword       | PasswordBox | Bắt buộc, không rỗng | Nhập mật khẩu                     |
|   3   | btnLogin          | Button      | -                    | Thực hiện đăng nhập               |
|   4   | lnkForgotPassword | Link        | -                    | Chuyển đến màn hình quên mật khẩu |
|   5   | lnkRegister       | Link        | -                    | Chuyển đến màn hình đăng ký       |

### c. Danh sách biến cố và xử lý tương ứng

|  STT  | Biến cố                 | Xử lý                                                                                                |
| :---: | ----------------------- | ---------------------------------------------------------------------------------------------------- |
|   1   | Click btnLogin          | Kiểm tra thông tin đăng nhập. Nếu hợp lệ → chuyển đến trang chủ. Nếu không → hiển thị thông báo lỗi. |
|   2   | Click lnkForgotPassword | Chuyển đến màn hình Quên mật khẩu                                                                    |
|   3   | Click lnkRegister       | Chuyển đến màn hình Đăng ký tài khoản                                                                |

---

## 5.3.2 Màn hình Quên mật khẩu

### a. Giao diện
*(Chèn ảnh chụp màn hình)*

### b. Mô tả các đối tượng trên màn hình

|  STT  | Tên            | Kiểu    | Ràng buộc                        | Chức năng                    |
| :---: | -------------- | ------- | -------------------------------- | ---------------------------- |
|   1   | txtUsername    | TextBox | Bắt buộc, không rỗng             | Nhập tên đăng nhập           |
|   2   | txtEmail       | TextBox | Bắt buộc, định dạng email hợp lệ | Nhập email đăng ký           |
|   3   | btnSubmit      | Button  | -                                | Gửi yêu cầu đặt lại mật khẩu |
|   4   | lnkBackToLogin | Link    | -                                | Quay lại trang đăng nhập     |

### c. Danh sách biến cố và xử lý tương ứng

|  STT  | Biến cố              | Xử lý                                                                                                                                         |
| :---: | -------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
|   1   | Click btnSubmit      | Kiểm tra username và email. Nếu hợp lệ → gửi email chứa link đặt lại mật khẩu → chuyển đến màn hình "Đã gửi email". Nếu không → hiển thị lỗi. |
|   2   | Click lnkBackToLogin | Chuyển về màn hình Đăng nhập                                                                                                                  |

---

## 5.3.3 Màn hình Đã gửi email

### a. Giao diện
*(Chèn ảnh chụp màn hình)*

### b. Mô tả các đối tượng trên màn hình

|  STT  | Tên            | Kiểu  | Ràng buộc | Chức năng                       |
| :---: | -------------- | ----- | --------- | ------------------------------- |
|   1   | lblMessage     | Label | -         | Hiển thị thông báo đã gửi email |
|   2   | lnkBackToLogin | Link  | -         | Quay lại trang đăng nhập        |

### c. Danh sách biến cố và xử lý tương ứng

|  STT  | Biến cố              | Xử lý                        |
| :---: | -------------------- | ---------------------------- |
|   1   | Click lnkBackToLogin | Chuyển về màn hình Đăng nhập |

---

## 5.3.4 Màn hình Đặt lại mật khẩu

### a. Giao diện
*(Chèn ảnh chụp màn hình)*

### b. Mô tả các đối tượng trên màn hình

|  STT  | Tên                | Kiểu        | Ràng buộc                                                                 | Chức năng                  |
| :---: | ------------------ | ----------- | ------------------------------------------------------------------------- | -------------------------- |
|   1   | txtNewPassword     | PasswordBox | Bắt buộc, tối thiểu 8 ký tự, chứa chữ hoa, chữ thường, số, ký tự đặc biệt | Nhập mật khẩu mới          |
|   2   | txtConfirmPassword | PasswordBox | Bắt buộc, phải trùng với mật khẩu mới                                     | Xác nhận mật khẩu mới      |
|   3   | btnResetPassword   | Button      | -                                                                         | Thực hiện đặt lại mật khẩu |

### c. Danh sách biến cố và xử lý tương ứng

|  STT  | Biến cố                | Xử lý                                                                                                                                 |
| :---: | ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
|   1   | Click btnResetPassword | Kiểm tra mật khẩu mới và xác nhận. Nếu hợp lệ → cập nhật mật khẩu → chuyển đến màn hình "Hoàn tất đặt lại". Nếu không → hiển thị lỗi. |

---

## 5.3.5 Màn hình Hoàn tất đặt lại

### a. Giao diện
*(Chèn ảnh chụp màn hình)*

### b. Mô tả các đối tượng trên màn hình

|  STT  | Tên        | Kiểu  | Ràng buộc | Chức năng                             |
| :---: | ---------- | ----- | --------- | ------------------------------------- |
|   1   | lblMessage | Label | -         | Hiển thị thông báo đặt lại thành công |
|   2   | lnkLogin   | Link  | -         | Chuyển đến trang đăng nhập            |

### c. Danh sách biến cố và xử lý tương ứng

|  STT  | Biến cố        | Xử lý                        |
| :---: | -------------- | ---------------------------- |
|   1   | Click lnkLogin | Chuyển về màn hình Đăng nhập |

---

## 5.3.6 Màn hình Trang chủ

### a. Giao diện
*(Chèn ảnh chụp màn hình)*

### b. Mô tả các đối tượng trên màn hình

|  STT  | Tên               | Kiểu     | Ràng buộc | Chức năng                                         |
| :---: | ----------------- | -------- | --------- | ------------------------------------------------- |
|   1   | lblWelcome        | Label    | -         | Hiển thị lời chào và tên người dùng               |
|   2   | cardTotalReaders  | StatCard | -         | Hiển thị tổng số độc giả, click → DS độc giả      |
|   3   | cardTotalBooks    | StatCard | -         | Hiển thị tổng số đầu sách, click → Tra cứu sách   |
|   4   | cardActiveBorrows | StatCard | -         | Hiển thị số sách đang mượn, click → DS phiếu mượn |
|   5   | cardOverdueBooks  | StatCard | -         | Hiển thị số sách quá hạn, click → BC sách trả trễ |
|   6   | menuReaderMgmt    | MenuCard | -         | Menu quản lý độc giả                              |
|   7   | menuBookMgmt      | MenuCard | -         | Menu quản lý sách                                 |
|   8   | menuBorrowMgmt    | MenuCard | -         | Menu mượn/trả sách                                |
|   9   | menuReceiptReport | MenuCard | -         | Menu thu tiền & báo cáo                           |

### c. Danh sách biến cố và xử lý tương ứng

|  STT  | Biến cố                       | Xử lý                                             |
| :---: | ----------------------------- | ------------------------------------------------- |
|   1   | Click cardTotalReaders        | Chuyển đến màn hình Danh sách độc giả             |
|   2   | Click cardTotalBooks          | Chuyển đến màn hình Tra cứu sách                  |
|   3   | Click cardActiveBorrows       | Chuyển đến màn hình DS phiếu mượn                 |
|   4   | Click cardOverdueBooks        | Chuyển đến màn hình BC sách trả trễ               |
|   5   | Click menuReaderMgmt items    | Chuyển đến các màn hình quản lý độc giả tương ứng |
|   6   | Click menuBookMgmt items      | Chuyển đến các màn hình quản lý sách tương ứng    |
|   7   | Click menuBorrowMgmt items    | Chuyển đến các màn hình mượn/trả tương ứng        |
|   8   | Click menuReceiptReport items | Chuyển đến các màn hình thu tiền & báo cáo        |

---

## 5.3.7 Màn hình Thông tin cá nhân

### a. Giao diện
*(Chèn ảnh chụp màn hình)*

### b. Mô tả các đối tượng trên màn hình

|  STT  | Tên                | Kiểu        | Ràng buộc                                           | Chức năng                                     |
| :---: | ------------------ | ----------- | --------------------------------------------------- | --------------------------------------------- |
|   1   | lblUsername        | Label       | -                                                   | Hiển thị tên đăng nhập (không chỉnh sửa được) |
|   2   | txtEmail           | TextBox     | Định dạng email hợp lệ                              | Nhập/sửa email                                |
|   3   | txtPhoneNumber     | TextBox     | Định dạng số điện thoại                             | Nhập/sửa số điện thoại                        |
|   4   | txtLastName        | TextBox     | -                                                   | Nhập/sửa họ                                   |
|   5   | txtFirstName       | TextBox     | -                                                   | Nhập/sửa tên                                  |
|   6   | dateDateOfBirth    | DatePicker  | -                                                   | Chọn ngày sinh                                |
|   7   | txtAddress         | TextArea    | -                                                   | Nhập/sửa địa chỉ                              |
|   8   | txtPosition        | TextBox     | Chỉ Admin mới sửa được                              | Hiển thị/sửa chức vụ                          |
|   9   | txtOldPassword     | PasswordBox | -                                                   | Nhập mật khẩu cũ (để đổi MK)                  |
|  10   | txtNewPassword     | PasswordBox | Tối thiểu 8 ký tự, có chữ hoa, thường, số, đặc biệt | Nhập mật khẩu mới                             |
|  11   | txtConfirmPassword | PasswordBox | Phải trùng mật khẩu mới                             | Xác nhận mật khẩu mới                         |
|  12   | btnSave            | Button      | -                                                   | Lưu thay đổi                                  |
|  13   | btnBack            | Button      | -                                                   | Quay lại trang chủ                            |

### c. Danh sách biến cố và xử lý tương ứng

|  STT  | Biến cố       | Xử lý                                                                                                                                      |
| :---: | ------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
|   1   | Click btnSave | Kiểm tra dữ liệu nhập. Nếu hợp lệ → cập nhật thông tin cá nhân và/hoặc mật khẩu → hiển thị thông báo thành công. Nếu không → hiển thị lỗi. |
|   2   | Click btnBack | Chuyển về màn hình Trang chủ                                                                                                               |

---

## 5.3.8 Màn hình Đổi mật khẩu

### a. Giao diện
*(Chèn ảnh chụp màn hình)*

### b. Mô tả các đối tượng trên màn hình

|  STT  | Tên                | Kiểu        | Ràng buộc                                                       | Chức năng              |
| :---: | ------------------ | ----------- | --------------------------------------------------------------- | ---------------------- |
|   1   | txtOldPassword     | PasswordBox | Bắt buộc                                                        | Nhập mật khẩu hiện tại |
|   2   | txtNewPassword     | PasswordBox | Bắt buộc, tối thiểu 8 ký tự, chứa chữ hoa, thường, số, đặc biệt | Nhập mật khẩu mới      |
|   3   | txtConfirmPassword | PasswordBox | Bắt buộc, phải trùng mật khẩu mới                               | Xác nhận mật khẩu mới  |
|   4   | btnChangePassword  | Button      | -                                                               | Thực hiện đổi mật khẩu |
|   5   | btnCancel          | Button      | -                                                               | Hủy và quay lại        |

### c. Danh sách biến cố và xử lý tương ứng

|  STT  | Biến cố                 | Xử lý                                                                                                                                              |
| :---: | ----------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
|   1   | Click btnChangePassword | Kiểm tra mật khẩu cũ. Kiểm tra mật khẩu mới và xác nhận. Nếu hợp lệ → cập nhật mật khẩu → hiển thị thông báo thành công. Nếu không → hiển thị lỗi. |
|   2   | Click btnCancel         | Hủy thay đổi và quay về màn hình trước                                                                                                             |

---

## 5.3.9 Màn hình Lập thẻ độc giả

### a. Giao diện
*(Chèn ảnh chụp màn hình)*

### b. Mô tả các đối tượng trên màn hình

|  STT  | Tên               | Kiểu       | Ràng buộc                             | Chức năng                                     |
| :---: | ----------------- | ---------- | ------------------------------------- | --------------------------------------------- |
|   1   | lblAgeRule        | Label      | -                                     | Hiển thị quy định độ tuổi (min_age - max_age) |
|   2   | lblReaderTypeRule | Label      | -                                     | Hiển thị danh sách loại độc giả               |
|   3   | lblValidityRule   | Label      | -                                     | Hiển thị thời hạn thẻ (tháng)                 |
|   4   | txtReaderName     | TextBox    | Bắt buộc, không rỗng                  | Nhập họ và tên độc giả                        |
|   5   | cboReaderType     | ComboBox   | Bắt buộc                              | Chọn loại độc giả                             |
|   6   | dateDateOfBirth   | DatePicker | Bắt buộc, tuổi từ min_age đến max_age | Chọn ngày sinh                                |
|   7   | txtEmail          | TextBox    | Bắt buộc, định dạng email hợp lệ      | Nhập email                                    |
|   8   | dateCardCreation  | DatePicker | Bắt buộc                              | Chọn ngày lập thẻ                             |
|   9   | cboProvince       | ComboBox   | Bắt buộc                              | Chọn Tỉnh/Thành phố                           |
|  10   | cboDistrict       | ComboBox   | Bắt buộc                              | Chọn Quận/Huyện                               |
|  11   | cboWard           | ComboBox   | Bắt buộc                              | Chọn Phường/Xã                                |
|  12   | txtStreetDetail   | TextBox    | -                                     | Nhập số nhà, tên đường                        |
|  13   | btnSubmit         | Button     | -                                     | Lập thẻ độc giả                               |
|  14   | btnViewList       | Button     | -                                     | Chuyển đến DS độc giả                         |

### c. Danh sách biến cố và xử lý tương ứng

|  STT  | Biến cố                                | Xử lý                                                                                                               |
| :---: | -------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
|   1   | Change cboProvince                     | Load danh sách Quận/Huyện tương ứng                                                                                 |
|   2   | Change cboDistrict                     | Load danh sách Phường/Xã tương ứng                                                                                  |
|   3   | Change cboWard / Input txtStreetDetail | Ghép chuỗi địa chỉ đầy đủ                                                                                           |
|   4   | Click btnSubmit                        | Kiểm tra tuổi và dữ liệu. Nếu hợp lệ → tạo thẻ độc giả mới → chuyển đến Chi tiết độc giả. Nếu không → hiển thị lỗi. |
|   5   | Click btnViewList                      | Chuyển đến màn hình Danh sách độc giả                                                                               |

---

## 5.3.10 Màn hình Danh sách độc giả

### a. Giao diện
*(Chèn ảnh chụp màn hình)*

### b. Mô tả các đối tượng trên màn hình

|  STT  | Tên            | Kiểu        | Ràng buộc | Chức năng                              |
| :---: | -------------- | ----------- | --------- | -------------------------------------- |
|   1   | txtSearch      | TextBox     | -         | Nhập từ khóa tìm kiếm (tên hoặc email) |
|   2   | cboReaderType  | ComboBox    | -         | Lọc theo loại độc giả                  |
|   3   | btnSearch      | Button      | -         | Thực hiện tìm kiếm                     |
|   4   | btnClearFilter | Button      | -         | Xóa bộ lọc                             |
|   5   | btnCreateNew   | Button      | -         | Chuyển đến Lập thẻ mới                 |
|   6   | lblResultCount | Label       | -         | Hiển thị số lượng kết quả              |
|   7   | tblReaderList  | Table       | -         | Bảng danh sách độc giả                 |
|   8   | colMa          | TableColumn | -         | Cột mã độc giả                         |
|   9   | colHoTen       | TableColumn | -         | Cột họ tên (link đến chi tiết)         |
|  10   | colLoaiDG      | TableColumn | -         | Cột loại độc giả                       |
|  11   | colTuoi        | TableColumn | -         | Cột tuổi                               |
|  12   | colEmail       | TableColumn | -         | Cột email                              |
|  13   | colNgayLapThe  | TableColumn | -         | Cột ngày lập thẻ                       |
|  14   | colHanThe      | TableColumn | -         | Cột hạn thẻ + badge hết hạn            |
|  15   | colTrangThai   | TableColumn | -         | Cột trạng thái (Hoạt động/Khóa)        |
|  16   | btnView        | Button      | -         | Nút xem chi tiết (mỗi dòng)            |

### c. Danh sách biến cố và xử lý tương ứng

|  STT  | Biến cố               | Xử lý                                                         |
| :---: | --------------------- | ------------------------------------------------------------- |
|   1   | Click btnSearch       | Lọc danh sách theo từ khóa và loại độc giả → hiển thị kết quả |
|   2   | Click btnClearFilter  | Xóa bộ lọc → hiển thị tất cả độc giả                          |
|   3   | Click btnCreateNew    | Chuyển đến màn hình Lập thẻ độc giả                           |
|   4   | Click colHoTen (link) | Chuyển đến màn hình Chi tiết độc giả                          |
|   5   | Click btnView         | Chuyển đến màn hình Chi tiết độc giả                          |

---

## 5.3.11 Màn hình Chi tiết độc giả

### a. Giao diện
*(Chèn ảnh chụp màn hình)*

### b. Mô tả các đối tượng trên màn hình

|  STT  | Tên              | Kiểu   | Ràng buộc | Chức năng                                   |
| :---: | ---------------- | ------ | --------- | ------------------------------------------- |
|   1   | lblMaDocGia      | Label  | -         | Hiển thị mã độc giả                         |
|   2   | lblLoaiDocGia    | Label  | -         | Hiển thị loại độc giả                       |
|   3   | lblHoTen         | Label  | -         | Hiển thị họ và tên                          |
|   4   | lblNgaySinh      | Label  | -         | Hiển thị ngày sinh và tuổi                  |
|   5   | lblEmail         | Label  | -         | Hiển thị email                              |
|   6   | lblDiaChi        | Label  | -         | Hiển thị địa chỉ                            |
|   7   | lblNgayLapThe    | Label  | -         | Hiển thị ngày lập thẻ                       |
|   8   | lblNgayHetHan    | Label  | -         | Hiển thị ngày hết hạn + badge trạng thái    |
|   9   | lblTrangThai     | Label  | -         | Hiển thị trạng thái thẻ (Hoạt động/Đã khóa) |
|  10   | lblTongNo        | Label  | -         | Hiển thị tổng nợ phạt                       |
|  11   | tblSachDangMuon  | Table  | -         | Bảng danh sách sách đang mượn (async load)  |
|  12   | lblTongSachMuon  | Label  | -         | Hiển thị tổng số sách đang mượn             |
|  13   | lblPhaiTraTruoc  | Label  | -         | Hiển thị ngày phải trả sớm nhất             |
|  14   | btnCreateAnother | Button | -         | Chuyển đến Lập thẻ độc giả khác             |
|  15   | btnBackToList    | Button | -         | Quay lại danh sách độc giả                  |

### c. Danh sách biến cố và xử lý tương ứng

|  STT  | Biến cố                | Xử lý                                                            |
| :---: | ---------------------- | ---------------------------------------------------------------- |
|   1   | Page Load              | Gọi API lấy thông tin sách đang mượn của độc giả → hiển thị bảng |
|   2   | Click btnCreateAnother | Chuyển đến màn hình Lập thẻ độc giả                              |
|   3   | Click btnBackToList    | Chuyển về màn hình Danh sách độc giả                             |
|   4   | Auto Refresh (30s)     | Tự động refresh thông tin sách đang mượn                         |

---

## 5.3.12 Màn hình Sửa thông tin độc giả

### a. Giao diện
*(Chèn ảnh chụp màn hình)*

### b. Mô tả các đối tượng trên màn hình

|  STT  | Tên             | Kiểu       | Ràng buộc                        | Chức năng                            |
| :---: | --------------- | ---------- | -------------------------------- | ------------------------------------ |
|   1   | lblMaDocGia     | Label      | -                                | Hiển thị mã độc giả (không sửa được) |
|   2   | txtReaderName   | TextBox    | Bắt buộc, không rỗng             | Sửa họ và tên                        |
|   3   | cboReaderType   | ComboBox   | Bắt buộc                         | Sửa loại độc giả                     |
|   4   | dateDateOfBirth | DatePicker | Bắt buộc, tuổi hợp lệ            | Sửa ngày sinh                        |
|   5   | txtEmail        | TextBox    | Bắt buộc, định dạng email hợp lệ | Sửa email                            |
|   6   | txtAddress      | TextArea   | -                                | Sửa địa chỉ                          |
|   7   | chkIsActive     | CheckBox   | -                                | Bật/tắt trạng thái hoạt động         |
|   8   | btnSave         | Button     | -                                | Lưu thay đổi                         |
|   9   | btnCancel       | Button     | -                                | Hủy và quay lại                      |

### c. Danh sách biến cố và xử lý tương ứng

|  STT  | Biến cố         | Xử lý                                                                                                                                     |
| :---: | --------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
|   1   | Click btnSave   | Kiểm tra dữ liệu. Nếu hợp lệ → cập nhật thông tin độc giả → hiển thị thông báo thành công → chuyển về Chi tiết. Nếu không → hiển thị lỗi. |
|   2   | Click btnCancel | Hủy thay đổi → quay về màn hình Chi tiết độc giả                                                                                          |

---

## 5.3.13 Màn hình Tra cứu sách

### a. Giao diện
*(Chèn ảnh chụp màn hình)*

### b. Mô tả các đối tượng trên màn hình

|  STT  | Tên            | Kiểu     | Ràng buộc | Chức năng             |
| :---: | -------------- | -------- | --------- | --------------------- |
|   1   | txtSearchText  | TextBox  | -         | Nhập từ khóa tìm kiếm |
|   2   | cboCategory    | ComboBox | -         | Lọc theo thể loại     |
|   3   | cboAuthor      | ComboBox | -         | Lọc theo tác giả      |
|   4   | cboStatus      | ComboBox | -         | Lọc theo tình trạng   |
|   5   | btnSearch      | Button   | -         | Thực hiện tìm kiếm    |
|   6   | btnClearFilter | Button   | -         | Xóa bộ lọc            |
|   7   | tblBookList    | Table    | -         | Bảng danh sách sách   |
|   8   | btnChiTiet     | Button   | -         | Nút xem chi tiết      |

### c. Danh sách biến cố và xử lý tương ứng

|  STT  | Biến cố              | Xử lý                           |
| :---: | -------------------- | ------------------------------- |
|   1   | Click btnSearch      | Lọc danh sách theo các tiêu chí |
|   2   | Click btnClearFilter | Xóa bộ lọc, hiển thị tất cả     |
|   3   | Click btnChiTiet     | Chuyển đến Chi tiết sách        |

---

## 5.3.14 Màn hình Chi tiết sách

### a. Giao diện
*(Chèn ảnh chụp màn hình)*

### b. Mô tả các đối tượng trên màn hình

|  STT  | Tên        | Kiểu   | Ràng buộc | Chức năng                |
| :---: | ---------- | ------ | --------- | ------------------------ |
|   1   | lblMaSach  | Label  | -         | Hiển thị mã sách         |
|   2   | lblTenSach | Label  | -         | Hiển thị tên sách        |
|   3   | lblTheLoai | Label  | -         | Hiển thị thể loại        |
|   4   | lblTacGia  | Label  | -         | Hiển thị tác giả         |
|   5   | lblNXB     | Label  | -         | Hiển thị nhà xuất bản    |
|   6   | lblSoLuong | Label  | -         | Hiển thị số lượng        |
|   7   | btnEdit    | Button | -         | Chuyển đến Sửa thông tin |
|   8   | btnBack    | Button | -         | Quay lại danh sách       |

### c. Danh sách biến cố và xử lý tương ứng

|  STT  | Biến cố       | Xử lý                         |
| :---: | ------------- | ----------------------------- |
|   1   | Click btnEdit | Chuyển đến Sửa thông tin sách |
|   2   | Click btnBack | Quay về Tra cứu sách          |

---

## 5.3.15 Màn hình Sửa thông tin sách

### a. Giao diện
*(Chèn ảnh chụp màn hình)*

### b. Mô tả các đối tượng trên màn hình

|  STT  | Tên            | Kiểu             | Ràng buộc | Chức năng       |
| :---: | -------------- | ---------------- | --------- | --------------- |
|   1   | txtBookTitle   | TextBox          | Bắt buộc  | Sửa tên sách    |
|   2   | cboCategory    | ComboBox         | Bắt buộc  | Sửa thể loại    |
|   3   | cboAuthors     | ComboBox (multi) | -         | Sửa tác giả     |
|   4   | txtPublisher   | TextBox          | Bắt buộc  | Sửa NXB         |
|   5   | numPublishYear | NumberBox        | Bắt buộc  | Sửa năm XB      |
|   6   | btnSave        | Button           | -         | Lưu thay đổi    |
|   7   | btnCancel      | Button           | -         | Hủy và quay lại |

### c. Danh sách biến cố và xử lý tương ứng

|  STT  | Biến cố         | Xử lý                          |
| :---: | --------------- | ------------------------------ |
|   1   | Click btnSave   | Kiểm tra và cập nhật thông tin |
|   2   | Click btnCancel | Hủy, quay về Chi tiết sách     |

---

## 5.3.16 Màn hình Chọn phương thức nhập

### a. Giao diện
*(Chèn ảnh chụp màn hình)*

### b. Mô tả các đối tượng trên màn hình

|  STT  | Tên             | Kiểu   | Ràng buộc | Chức năng                |
| :---: | --------------- | ------ | --------- | ------------------------ |
|   1   | btnManualImport | Button | -         | Chuyển đến Nhập thủ công |
|   2   | btnExcelImport  | Button | -         | Chuyển đến Nhập từ Excel |

### c. Danh sách biến cố và xử lý tương ứng

|  STT  | Biến cố               | Xử lý                         |
| :---: | --------------------- | ----------------------------- |
|   1   | Click btnManualImport | Chuyển đến Nhập sách thủ công |
|   2   | Click btnExcelImport  | Chuyển đến Nhập sách từ Excel |

---

## 5.3.17 Màn hình Nhập sách thủ công

### a. Giao diện
*(Chèn ảnh chụp màn hình)*

### b. Mô tả các đối tượng trên màn hình

|  STT  | Tên            | Kiểu                 | Ràng buộc                  | Chức năng         |
| :---: | -------------- | -------------------- | -------------------------- | ----------------- |
|   1   | txtBookTitle   | TextBox              | Bắt buộc                   | Nhập tên sách     |
|   2   | cboCategory    | ComboBox             | Bắt buộc                   | Chọn thể loại     |
|   3   | cboPublisher   | ComboBox (creatable) | Bắt buộc                   | Chọn/nhập NXB     |
|   4   | numPublishYear | NumberBox            | Bắt buộc, >= năm tối thiểu | Năm xuất bản      |
|   5   | cboLanguage    | ComboBox             | -                          | Chọn ngôn ngữ     |
|   6   | cboAuthors     | ComboBox (multi)     | -                          | Chọn/nhập tác giả |
|   7   | numQuantity    | NumberBox            | Bắt buộc, >= 1             | Số lượng nhập     |
|   8   | numUnitPrice   | NumberBox            | Bắt buộc, >= 0             | Đơn giá           |
|   9   | dateImport     | DatePicker           | Bắt buộc                   | Ngày nhập         |
|  10   | btnSubmit      | Button               | -                          | Lưu phiếu nhập    |

### c. Danh sách biến cố và xử lý tương ứng

|  STT  | Biến cố                      | Xử lý                      |
| :---: | ---------------------------- | -------------------------- |
|   1   | Click btnSubmit              | Tạo phiếu nhập và sách mới |
|   2   | Change cboAuthors (nhập mới) | Thêm tác giả mới           |

---

## 5.3.18 Màn hình Nhập sách từ Excel

### a. Giao diện
*(Chèn ảnh chụp màn hình)*

### b. Mô tả các đối tượng trên màn hình

|  STT  | Tên                 | Kiểu       | Ràng buộc       | Chức năng       |
| :---: | ------------------- | ---------- | --------------- | --------------- |
|   1   | btnDownloadTemplate | Button     | -               | Tải file mẫu    |
|   2   | fileExcel           | FileUpload | Bắt buộc, .xlsx | Chọn file Excel |
|   3   | dateImport          | DatePicker | Bắt buộc        | Ngày nhập       |
|   4   | btnSubmit           | Button     | -               | Upload và xử lý |

### c. Danh sách biến cố và xử lý tương ứng

|  STT  | Biến cố                   | Xử lý                        |
| :---: | ------------------------- | ---------------------------- |
|   1   | Click btnDownloadTemplate | Tải file Excel mẫu           |
|   2   | Click btnSubmit           | Parse file và tạo phiếu nhập |

---

## 5.3.19 Màn hình DS phiếu nhập sách

### a. Giao diện
*(Chèn ảnh chụp màn hình)*

### b. Mô tả các đối tượng trên màn hình

|  STT  | Tên           | Kiểu    | Ràng buộc | Chức năng          |
| :---: | ------------- | ------- | --------- | ------------------ |
|   1   | txtSearch     | TextBox | -         | Tìm kiếm           |
|   2   | btnSearch     | Button  | -         | Thực hiện tìm      |
|   3   | btnCreateNew  | Button  | -         | Tạo phiếu mới      |
|   4   | tblImportList | Table   | -         | Bảng DS phiếu nhập |
|   5   | btnView       | Button  | -         | Xem chi tiết       |

### c. Danh sách biến cố và xử lý tương ứng

|  STT  | Biến cố         | Xử lý                          |
| :---: | --------------- | ------------------------------ |
|   1   | Click btnSearch | Lọc danh sách                  |
|   2   | Click btnView   | Chuyển đến Chi tiết phiếu nhập |

---

## 5.3.20 Màn hình Chi tiết phiếu nhập

### a. Giao diện
*(Chèn ảnh chụp màn hình)*

### b. Mô tả các đối tượng trên màn hình

|  STT  | Tên         | Kiểu   | Ràng buộc | Chức năng     |
| :---: | ----------- | ------ | --------- | ------------- |
|   1   | lblMaPhieu  | Label  | -         | Mã phiếu nhập |
|   2   | lblNgayNhap | Label  | -         | Ngày nhập     |
|   3   | lblTenSach  | Label  | -         | Tên sách      |
|   4   | lblSoLuong  | Label  | -         | Số lượng      |
|   5   | lblTongTien | Label  | -         | Tổng tiền     |
|   6   | btnBack     | Button | -         | Quay lại      |

### c. Danh sách biến cố và xử lý tương ứng

|  STT  | Biến cố       | Xử lý                 |
| :---: | ------------- | --------------------- |
|   1   | Click btnBack | Quay về DS phiếu nhập |

---

## 5.3.21 Màn hình Lập phiếu mượn

### a. Giao diện
*(Chèn ảnh chụp màn hình)*

### b. Mô tả các đối tượng trên màn hình

|  STT  | Tên               | Kiểu       | Ràng buộc | Chức năng         |
| :---: | ----------------- | ---------- | --------- | ----------------- |
|   1   | tabChoMuon        | Tab        | -         | Tab lập phiếu     |
|   2   | tabDocGiaDangMuon | Tab        | -         | Tab xem đang mượn |
|   3   | tabLichSu         | Tab        | -         | Tab lịch sử       |
|   4   | dateBorrowDate    | DatePicker | Bắt buộc  | Ngày mượn         |
|   5   | txtReaderSearch   | TextBox    | -         | Tìm độc giả       |
|   6   | lstReaders        | List       | -         | DS độc giả        |
|   7   | txtBookSearch     | TextBox    | -         | Tìm sách          |
|   8   | lstBooks          | List       | -         | DS sách           |
|   9   | btnSubmit         | Button     | -         | Cho mượn          |

### c. Danh sách biến cố và xử lý tương ứng

|  STT  | Biến cố               | Xử lý          |
| :---: | --------------------- | -------------- |
|   1   | Click lstReaders item | Chọn độc giả   |
|   2   | Click lstBooks item   | Chọn sách      |
|   3   | Click btnSubmit       | Tạo phiếu mượn |

---

## 5.3.22 Màn hình DS phiếu mượn

### a. Giao diện
*(Chèn ảnh chụp màn hình)*

### b. Mô tả các đối tượng trên màn hình

|  STT  | Tên           | Kiểu     | Ràng buộc | Chức năng          |
| :---: | ------------- | -------- | --------- | ------------------ |
|   1   | txtSearch     | TextBox  | -         | Tìm kiếm           |
|   2   | cboStatus     | ComboBox | -         | Lọc trạng thái     |
|   3   | btnSearch     | Button   | -         | Tìm kiếm           |
|   4   | tblBorrowList | Table    | -         | Bảng DS phiếu mượn |
|   5   | btnView       | Button   | -         | Xem chi tiết       |

### c. Danh sách biến cố và xử lý tương ứng

|  STT  | Biến cố         | Xử lý                          |
| :---: | --------------- | ------------------------------ |
|   1   | Click btnSearch | Lọc danh sách                  |
|   2   | Click btnView   | Chuyển đến Chi tiết phiếu mượn |

---

## 5.3.23 Màn hình Chi tiết phiếu mượn

### a. Giao diện
*(Chèn ảnh chụp màn hình)*

### b. Mô tả các đối tượng trên màn hình

|  STT  | Tên            | Kiểu   | Ràng buộc | Chức năng         |
| :---: | -------------- | ------ | --------- | ----------------- |
|   1   | lblMaPhieu     | Label  | -         | Mã phiếu          |
|   2   | lblDocGia      | Label  | -         | Thông tin độc giả |
|   3   | lblSach        | Label  | -         | Thông tin sách    |
|   4   | lblNgayMuon    | Label  | -         | Ngày mượn         |
|   5   | lblNgayPhaiTra | Label  | -         | Ngày phải trả     |
|   6   | lblTrangThai   | Label  | -         | Trạng thái        |
|   7   | btnBack        | Button | -         | Quay lại          |

### c. Danh sách biến cố và xử lý tương ứng

|  STT  | Biến cố       | Xử lý                 |
| :---: | ------------- | --------------------- |
|   1   | Click btnBack | Quay về DS phiếu mượn |

---

## 5.3.24 Màn hình Lập phiếu trả

### a. Giao diện
*(Chèn ảnh chụp màn hình)*

### b. Mô tả các đối tượng trên màn hình

|  STT  | Tên              | Kiểu       | Ràng buộc | Chức năng         |
| :---: | ---------------- | ---------- | --------- | ----------------- |
|   1   | cboReader        | ComboBox   | Bắt buộc  | Chọn độc giả      |
|   2   | dateReturnDate   | DatePicker | Bắt buộc  | Ngày trả          |
|   3   | tblBorrowedBooks | Table      | -         | DS sách đang mượn |
|   4   | chkSelectBook    | CheckBox   | -         | Chọn sách trả     |
|   5   | lblTienPhat      | Label      | -         | Tiền phạt         |
|   6   | btnSubmit        | Button     | -         | Lập phiếu trả     |

### c. Danh sách biến cố và xử lý tương ứng

|  STT  | Biến cố          | Xử lý                      |
| :---: | ---------------- | -------------------------- |
|   1   | Change cboReader | Load DS sách đang mượn     |
|   2   | Click btnSubmit  | Tạo phiếu trả, cập nhật nợ |

---

## 5.3.25 Màn hình DS phiếu trả

### a. Giao diện
*(Chèn ảnh chụp màn hình)*

### b. Mô tả các đối tượng trên màn hình

|  STT  | Tên           | Kiểu    | Ràng buộc | Chức năng         |
| :---: | ------------- | ------- | --------- | ----------------- |
|   1   | txtSearch     | TextBox | -         | Tìm kiếm          |
|   2   | btnSearch     | Button  | -         | Tìm kiếm          |
|   3   | tblReturnList | Table   | -         | Bảng DS phiếu trả |
|   4   | btnView       | Button  | -         | Xem chi tiết      |

### c. Danh sách biến cố và xử lý tương ứng

|  STT  | Biến cố         | Xử lý                         |
| :---: | --------------- | ----------------------------- |
|   1   | Click btnSearch | Lọc danh sách                 |
|   2   | Click btnView   | Chuyển đến Chi tiết phiếu trả |

---

## 5.3.26 Màn hình Chi tiết phiếu trả

### a. Giao diện
*(Chèn ảnh chụp màn hình)*

### b. Mô tả các đối tượng trên màn hình

|  STT  | Tên              | Kiểu   | Ràng buộc | Chức năng         |
| :---: | ---------------- | ------ | --------- | ----------------- |
|   1   | lblMaPhieu       | Label  | -         | Mã phiếu trả      |
|   2   | lblDocGia        | Label  | -         | Thông tin độc giả |
|   3   | lblNgayTra       | Label  | -         | Ngày trả          |
|   4   | tblReturnedBooks | Table  | -         | DS sách đã trả    |
|   5   | lblTongTienPhat  | Label  | -         | Tổng tiền phạt    |
|   6   | btnBack          | Button | -         | Quay lại          |

### c. Danh sách biến cố và xử lý tương ứng

|  STT  | Biến cố       | Xử lý                |
| :---: | ------------- | -------------------- |
|   1   | Click btnBack | Quay về DS phiếu trả |

---

## 5.3.27 Màn hình Lập phiếu thu

### a. Giao diện
*(Chèn ảnh chụp màn hình)*

### b. Mô tả các đối tượng trên màn hình

|  STT  | Tên             | Kiểu       | Ràng buộc            | Chức năng          |
| :---: | --------------- | ---------- | -------------------- | ------------------ |
|   1   | cboReader       | ComboBox   | Bắt buộc             | Chọn độc giả có nợ |
|   2   | lblTongNo       | Label      | -                    | Tổng nợ hiện tại   |
|   3   | numSoTienThu    | NumberBox  | Bắt buộc, <= tổng nợ | Số tiền thu        |
|   4   | datePaymentDate | DatePicker | Bắt buộc             | Ngày thu           |
|   5   | btnSubmit       | Button     | -                    | Lập phiếu thu      |

### c. Danh sách biến cố và xử lý tương ứng

|  STT  | Biến cố          | Xử lý                  |
| :---: | ---------------- | ---------------------- |
|   1   | Change cboReader | Hiển thị tổng nợ       |
|   2   | Click btnSubmit  | Tạo phiếu thu, giảm nợ |

---

## 5.3.28 Màn hình DS phiếu thu

### a. Giao diện
*(Chèn ảnh chụp màn hình)*

### b. Mô tả các đối tượng trên màn hình

|  STT  | Tên            | Kiểu    | Ràng buộc | Chức năng         |
| :---: | -------------- | ------- | --------- | ----------------- |
|   1   | txtSearch      | TextBox | -         | Tìm kiếm          |
|   2   | btnSearch      | Button  | -         | Tìm kiếm          |
|   3   | tblReceiptList | Table   | -         | Bảng DS phiếu thu |
|   4   | btnView        | Button  | -         | Xem chi tiết      |

### c. Danh sách biến cố và xử lý tương ứng

|  STT  | Biến cố         | Xử lý                         |
| :---: | --------------- | ----------------------------- |
|   1   | Click btnSearch | Lọc danh sách                 |
|   2   | Click btnView   | Chuyển đến Chi tiết phiếu thu |

---

## 5.3.29 Màn hình Chi tiết phiếu thu

### a. Giao diện
*(Chèn ảnh chụp màn hình)*

### b. Mô tả các đối tượng trên màn hình

|  STT  | Tên        | Kiểu   | Ràng buộc | Chức năng         |
| :---: | ---------- | ------ | --------- | ----------------- |
|   1   | lblMaPhieu | Label  | -         | Mã phiếu thu      |
|   2   | lblDocGia  | Label  | -         | Thông tin độc giả |
|   3   | lblNgayThu | Label  | -         | Ngày thu          |
|   4   | lblSoTien  | Label  | -         | Số tiền đã thu    |
|   5   | btnBack    | Button | -         | Quay lại          |

### c. Danh sách biến cố và xử lý tương ứng

|  STT  | Biến cố       | Xử lý                |
| :---: | ------------- | -------------------- |
|   1   | Click btnBack | Quay về DS phiếu thu |

---

## 5.3.30 Màn hình BC mượn theo thể loại

### a. Giao diện
*(Chèn ảnh chụp màn hình)*

### b. Mô tả các đối tượng trên màn hình

|  STT  | Tên         | Kiểu     | Ràng buộc | Chức năng     |
| :---: | ----------- | -------- | --------- | ------------- |
|   1   | cboMonth    | ComboBox | Bắt buộc  | Chọn tháng    |
|   2   | cboYear     | ComboBox | Bắt buộc  | Chọn năm      |
|   3   | btnGenerate | Button   | -         | Tạo báo cáo   |
|   4   | tblReport   | Table    | -         | Bảng thống kê |
|   5   | chartReport | Chart    | -         | Biểu đồ       |

### c. Danh sách biến cố và xử lý tương ứng

|  STT  | Biến cố           | Xử lý                              |
| :---: | ----------------- | ---------------------------------- |
|   1   | Click btnGenerate | Truy vấn dữ liệu, hiển thị báo cáo |

---

## 5.3.31 Màn hình BC tình hình mượn

### a. Giao diện
*(Chèn ảnh chụp màn hình)*

### b. Mô tả các đối tượng trên màn hình

|  STT  | Tên         | Kiểu       | Ràng buộc | Chức năng         |
| :---: | ----------- | ---------- | --------- | ----------------- |
|   1   | dateFrom    | DatePicker | Bắt buộc  | Ngày bắt đầu      |
|   2   | dateTo      | DatePicker | Bắt buộc  | Ngày kết thúc     |
|   3   | btnGenerate | Button     | -         | Tạo báo cáo       |
|   4   | lblThongKe  | Label      | -         | Tổng hợp số liệu  |
|   5   | chartByDate | Chart      | -         | Biểu đồ theo ngày |

### c. Danh sách biến cố và xử lý tương ứng

|  STT  | Biến cố           | Xử lý                         |
| :---: | ----------------- | ----------------------------- |
|   1   | Click btnGenerate | Truy vấn và hiển thị thống kê |

---

## 5.3.32 Màn hình BC sách trả trễ

### a. Giao diện
*(Chèn ảnh chụp màn hình)*

### b. Mô tả các đối tượng trên màn hình

|  STT  | Tên         | Kiểu       | Ràng buộc | Chức năng         |
| :---: | ----------- | ---------- | --------- | ----------------- |
|   1   | dateReport  | DatePicker | Bắt buộc  | Ngày báo cáo      |
|   2   | btnGenerate | Button     | -         | Tạo báo cáo       |
|   3   | tblOverdue  | Table      | -         | Bảng sách trả trễ |

### c. Danh sách biến cố và xử lý tương ứng

|  STT  | Biến cố           | Xử lý                    |
| :---: | ----------------- | ------------------------ |
|   1   | Click btnGenerate | Truy vấn DS sách quá hạn |

---

## 5.3.33 Màn hình Thay đổi quy định

### a. Giao diện
*(Chèn ảnh chụp màn hình)*

### b. Mô tả các đối tượng trên màn hình

|  STT  | Tên                 | Kiểu      | Ràng buộc           | Chức năng            |
| :---: | ------------------- | --------- | ------------------- | -------------------- |
|   1   | numMinAge           | NumberBox | Bắt buộc, > 0       | Tuổi tối thiểu       |
|   2   | numMaxAge           | NumberBox | Bắt buộc, > min_age | Tuổi tối đa          |
|   3   | numCardValidity     | NumberBox | Bắt buộc, > 0       | Thời hạn thẻ (tháng) |
|   4   | numMaxBorrowDays    | NumberBox | Bắt buộc, > 0       | Số ngày mượn tối đa  |
|   5   | numMaxBorrowedBooks | NumberBox | Bắt buộc, > 0       | Số sách mượn tối đa  |
|   6   | numFinePerDay       | NumberBox | Bắt buộc, >= 0      | Tiền phạt/ngày       |
|   7   | numMinPublishYear   | NumberBox | Bắt buộc            | Năm XB tối thiểu     |
|   8   | btnSave             | Button    | -                   | Lưu thay đổi         |

### c. Danh sách biến cố và xử lý tương ứng

|  STT  | Biến cố       | Xử lý                         |
| :---: | ------------- | ----------------------------- |
|   1   | Click btnSave | Kiểm tra và cập nhật quy định |

---

## 5.3.34 Màn hình DS loại độc giả

### a. Giao diện
*(Chèn ảnh chụp màn hình)*

### b. Mô tả các đối tượng trên màn hình

|  STT  | Tên            | Kiểu   | Ràng buộc | Chức năng            |
| :---: | -------------- | ------ | --------- | -------------------- |
|   1   | btnCreateNew   | Button | -         | Tạo loại mới         |
|   2   | tblReaderTypes | Table  | -         | Bảng DS loại độc giả |
|   3   | btnEdit        | Button | -         | Sửa (mỗi dòng)       |
|   4   | btnDelete      | Button | -         | Xóa (mỗi dòng)       |

### c. Danh sách biến cố và xử lý tương ứng

|  STT  | Biến cố            | Xử lý                        |
| :---: | ------------------ | ---------------------------- |
|   1   | Click btnCreateNew | Chuyển đến Thêm loại độc giả |
|   2   | Click btnEdit      | Chuyển đến Sửa loại độc giả  |
|   3   | Click btnDelete    | Chuyển đến Xóa loại độc giả  |

---

## 5.3.35 Màn hình Thêm/Sửa loại độc giả

### a. Giao diện
*(Chèn ảnh chụp màn hình)*

### b. Mô tả các đối tượng trên màn hình

|  STT  | Tên               | Kiểu    | Ràng buộc | Chức năng        |
| :---: | ----------------- | ------- | --------- | ---------------- |
|   1   | txtReaderTypeName | TextBox | Bắt buộc  | Tên loại độc giả |
|   2   | btnSave           | Button  | -         | Lưu              |
|   3   | btnCancel         | Button  | -         | Hủy              |

### c. Danh sách biến cố và xử lý tương ứng

|  STT  | Biến cố         | Xử lý                     |
| :---: | --------------- | ------------------------- |
|   1   | Click btnSave   | Tạo/cập nhật loại độc giả |
|   2   | Click btnCancel | Quay về DS loại độc giả   |

---

## 5.3.36 Màn hình Xóa loại độc giả

### a. Giao diện
*(Chèn ảnh chụp màn hình)*

### b. Mô tả các đối tượng trên màn hình

|  STT  | Tên               | Kiểu   | Ràng buộc | Chức năng          |
| :---: | ----------------- | ------ | --------- | ------------------ |
|   1   | lblConfirmMessage | Label  | -         | Thông báo xác nhận |
|   2   | lblReaderTypeName | Label  | -         | Tên loại sẽ xóa    |
|   3   | btnConfirm        | Button | -         | Xác nhận xóa       |
|   4   | btnCancel         | Button | -         | Hủy                |

### c. Danh sách biến cố và xử lý tương ứng

|  STT  | Biến cố          | Xử lý                   |
| :---: | ---------------- | ----------------------- |
|   1   | Click btnConfirm | Xóa loại độc giả        |
|   2   | Click btnCancel  | Quay về DS loại độc giả |

---

## 5.3.37 Màn hình Quản lý người dùng

### a. Giao diện
*(Chèn ảnh chụp màn hình)*

### b. Mô tả các đối tượng trên màn hình

|  STT  | Tên          | Kiểu   | Ràng buộc | Chức năng          |
| :---: | ------------ | ------ | --------- | ------------------ |
|   1   | btnCreateNew | Button | -         | Tạo người dùng mới |
|   2   | tblUserList  | Table  | -         | Bảng DS người dùng |
|   3   | btnEdit      | Button | -         | Sửa (mỗi dòng)     |
|   4   | btnDelete    | Button | -         | Xóa (mỗi dòng)     |

### c. Danh sách biến cố và xử lý tương ứng

|  STT  | Biến cố            | Xử lý                      |
| :---: | ------------------ | -------------------------- |
|   1   | Click btnCreateNew | Chuyển đến Thêm người dùng |
|   2   | Click btnEdit      | Chuyển đến Sửa người dùng  |
|   3   | Click btnDelete    | Chuyển đến Xóa người dùng  |

---

## 5.3.38 Màn hình Thêm/Sửa người dùng

### a. Giao diện
*(Chèn ảnh chụp màn hình)*

### b. Mô tả các đối tượng trên màn hình

|  STT  | Tên          | Kiểu        | Ràng buộc           | Chức năng     |
| :---: | ------------ | ----------- | ------------------- | ------------- |
|   1   | txtUsername  | TextBox     | Bắt buộc, duy nhất  | Tên đăng nhập |
|   2   | txtEmail     | TextBox     | Định dạng email     | Email         |
|   3   | txtPassword  | PasswordBox | Bắt buộc (thêm mới) | Mật khẩu      |
|   4   | cboUserGroup | ComboBox    | -                   | Nhóm quyền    |
|   5   | chkIsStaff   | CheckBox    | -                   | Là nhân viên  |
|   6   | chkIsActive  | CheckBox    | -                   | Hoạt động     |
|   7   | btnSave      | Button      | -                   | Lưu           |
|   8   | btnCancel    | Button      | -                   | Hủy           |

### c. Danh sách biến cố và xử lý tương ứng

|  STT  | Biến cố         | Xử lý                   |
| :---: | --------------- | ----------------------- |
|   1   | Click btnSave   | Tạo/cập nhật người dùng |
|   2   | Click btnCancel | Quay về DS người dùng   |

---

## 5.3.39 Màn hình Xóa người dùng

### a. Giao diện
*(Chèn ảnh chụp màn hình)*

### b. Mô tả các đối tượng trên màn hình

|  STT  | Tên               | Kiểu   | Ràng buộc | Chức năng             |
| :---: | ----------------- | ------ | --------- | --------------------- |
|   1   | lblConfirmMessage | Label  | -         | Thông báo xác nhận    |
|   2   | lblUsername       | Label  | -         | Tên người dùng sẽ xóa |
|   3   | btnConfirm        | Button | -         | Xác nhận xóa          |
|   4   | btnCancel         | Button | -         | Hủy                   |

### c. Danh sách biến cố và xử lý tương ứng

|  STT  | Biến cố          | Xử lý                 |
| :---: | ---------------- | --------------------- |
|   1   | Click btnConfirm | Xóa người dùng        |
|   2   | Click btnCancel  | Quay về DS người dùng |

---

## 5.3.40 Màn hình Quản lý nhóm quyền

### a. Giao diện
*(Chèn ảnh chụp màn hình)*

### b. Mô tả các đối tượng trên màn hình

|  STT  | Tên           | Kiểu   | Ràng buộc | Chức năng          |
| :---: | ------------- | ------ | --------- | ------------------ |
|   1   | btnCreateNew  | Button | -         | Tạo nhóm mới       |
|   2   | tblGroupList  | Table  | -         | Bảng DS nhóm quyền |
|   3   | btnEdit       | Button | -         | Sửa (mỗi dòng)     |
|   4   | btnDelete     | Button | -         | Xóa (mỗi dòng)     |
|   5   | btnPermission | Button | -         | Phân quyền         |

### c. Danh sách biến cố và xử lý tương ứng

|  STT  | Biến cố             | Xử lý                         |
| :---: | ------------------- | ----------------------------- |
|   1   | Click btnCreateNew  | Chuyển đến Thêm nhóm quyền    |
|   2   | Click btnEdit       | Chuyển đến Sửa nhóm quyền     |
|   3   | Click btnDelete     | Chuyển đến Xóa nhóm quyền     |
|   4   | Click btnPermission | Chuyển đến Ma trận phân quyền |

---

## 5.3.41 Màn hình Thêm/Sửa nhóm quyền

### a. Giao diện
*(Chèn ảnh chụp màn hình)*

### b. Mô tả các đối tượng trên màn hình

|  STT  | Tên          | Kiểu    | Ràng buộc | Chức năng      |
| :---: | ------------ | ------- | --------- | -------------- |
|   1   | txtGroupName | TextBox | Bắt buộc  | Tên nhóm quyền |
|   2   | btnSave      | Button  | -         | Lưu            |
|   3   | btnCancel    | Button  | -         | Hủy            |

### c. Danh sách biến cố và xử lý tương ứng

|  STT  | Biến cố         | Xử lý                   |
| :---: | --------------- | ----------------------- |
|   1   | Click btnSave   | Tạo/cập nhật nhóm quyền |
|   2   | Click btnCancel | Quay về DS nhóm quyền   |

---

## 5.3.42 Màn hình Xóa nhóm quyền

### a. Giao diện
*(Chèn ảnh chụp màn hình)*

### b. Mô tả các đối tượng trên màn hình

|  STT  | Tên               | Kiểu   | Ràng buộc | Chức năng          |
| :---: | ----------------- | ------ | --------- | ------------------ |
|   1   | lblConfirmMessage | Label  | -         | Thông báo xác nhận |
|   2   | lblGroupName      | Label  | -         | Tên nhóm sẽ xóa    |
|   3   | btnConfirm        | Button | -         | Xác nhận xóa       |
|   4   | btnCancel         | Button | -         | Hủy                |

### c. Danh sách biến cố và xử lý tương ứng

|  STT  | Biến cố          | Xử lý                 |
| :---: | ---------------- | --------------------- |
|   1   | Click btnConfirm | Xóa nhóm quyền        |
|   2   | Click btnCancel  | Quay về DS nhóm quyền |

---

## 5.3.43 Màn hình Ma trận phân quyền

### a. Giao diện
*(Chèn ảnh chụp màn hình)*

### b. Mô tả các đối tượng trên màn hình

|  STT  | Tên                 | Kiểu     | Ràng buộc | Chức năng                      |
| :---: | ------------------- | -------- | --------- | ------------------------------ |
|   1   | cboUserGroup        | ComboBox | Bắt buộc  | Chọn nhóm quyền                |
|   2   | tblPermissionMatrix | Table    | -         | Bảng ma trận chức năng - quyền |
|   3   | chkPermission       | CheckBox | -         | Check/uncheck quyền            |
|   4   | btnSave             | Button   | -         | Lưu phân quyền                 |
|   5   | btnCancel           | Button   | -         | Hủy                            |

### c. Danh sách biến cố và xử lý tương ứng

|  STT  | Biến cố             | Xử lý                       |
| :---: | ------------------- | --------------------------- |
|   1   | Change cboUserGroup | Load quyền hiện có của nhóm |
|   2   | Click btnSave       | Cập nhật quyền cho nhóm     |
|   3   | Click btnCancel     | Quay về DS nhóm quyền       |

---

## 5.3.44 Màn hình DS chức năng

### a. Giao diện
*(Chèn ảnh chụp màn hình)*

### b. Mô tả các đối tượng trên màn hình

|  STT  | Tên             | Kiểu   | Ràng buộc | Chức năng         |
| :---: | --------------- | ------ | --------- | ----------------- |
|   1   | btnCreateNew    | Button | -         | Tạo chức năng mới |
|   2   | tblFunctionList | Table  | -         | Bảng DS chức năng |
|   3   | btnEdit         | Button | -         | Sửa (mỗi dòng)    |
|   4   | btnDelete       | Button | -         | Xóa (mỗi dòng)    |

### c. Danh sách biến cố và xử lý tương ứng

|  STT  | Biến cố            | Xử lý                     |
| :---: | ------------------ | ------------------------- |
|   1   | Click btnCreateNew | Chuyển đến Thêm chức năng |
|   2   | Click btnEdit      | Chuyển đến Sửa chức năng  |
|   3   | Click btnDelete    | Chuyển đến Xóa chức năng  |

---

## 5.3.45 Màn hình Thêm/Sửa chức năng

### a. Giao diện
*(Chèn ảnh chụp màn hình)*

### b. Mô tả các đối tượng trên màn hình

|  STT  | Tên             | Kiểu    | Ràng buộc          | Chức năng     |
| :---: | --------------- | ------- | ------------------ | ------------- |
|   1   | txtFunctionName | TextBox | Bắt buộc           | Tên chức năng |
|   2   | txtFunctionCode | TextBox | Bắt buộc, duy nhất | Mã chức năng  |
|   3   | btnSave         | Button  | -                  | Lưu           |
|   4   | btnCancel       | Button  | -                  | Hủy           |

### c. Danh sách biến cố và xử lý tương ứng

|  STT  | Biến cố         | Xử lý                  |
| :---: | --------------- | ---------------------- |
|   1   | Click btnSave   | Tạo/cập nhật chức năng |
|   2   | Click btnCancel | Quay về DS chức năng   |

---

## 5.3.46 Màn hình Xóa chức năng

### a. Giao diện
*(Chèn ảnh chụp màn hình)*

### b. Mô tả các đối tượng trên màn hình

|  STT  | Tên               | Kiểu   | Ràng buộc | Chức năng            |
| :---: | ----------------- | ------ | --------- | -------------------- |
|   1   | lblConfirmMessage | Label  | -         | Thông báo xác nhận   |
|   2   | lblFunctionName   | Label  | -         | Tên chức năng sẽ xóa |
|   3   | btnConfirm        | Button | -         | Xác nhận xóa         |
|   4   | btnCancel         | Button | -         | Hủy                  |

### c. Danh sách biến cố và xử lý tương ứng

|  STT  | Biến cố          | Xử lý                |
| :---: | ---------------- | -------------------- |
|   1   | Click btnConfirm | Xóa chức năng        |
|   2   | Click btnCancel  | Quay về DS chức năng |

---

**--- HẾT ---**

