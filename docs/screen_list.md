# Danh sách màn hình - Library Management System

Bảng dưới đây liệt kê tất cả các màn hình trong hệ thống Quản lý Thư viện.

|           STT            | Màn hình              | Loại màn hình      | Chức năng                                                      |
| :----------------------: | --------------------- | ------------------ | -------------------------------------------------------------- |
| **Xác thực & Tài khoản** |                       |                    |                                                                |
|            1             | Màn hình đăng nhập    | Nhập liệu          | Cho phép người dùng đăng nhập vào hệ thống                     |
|            2             | Quên mật khẩu         | Nhập liệu          | Nhập email để yêu cầu đặt lại mật khẩu                         |
|            3             | Đã gửi email          | Màn hình chính     | Xác nhận đã gửi email đặt lại mật khẩu                         |
|            4             | Đặt lại mật khẩu      | Nhập liệu          | Nhập mật khẩu mới từ link trong email                          |
|            5             | Hoàn tất đặt lại      | Màn hình chính     | Xác nhận đặt lại mật khẩu thành công                           |
|            6             | Màn hình trang chủ    | Màn hình chính     | Hiển thị tổng quan hệ thống, thống kê, menu chức năng          |
|            7             | Thông tin cá nhân     | Tra cứu, Nhập liệu | Xem và chỉnh sửa thông tin tài khoản cá nhân                   |
|            8             | Đổi mật khẩu          | Nhập liệu          | Thay đổi mật khẩu tài khoản đang đăng nhập                     |
|   **Quản lý Độc giả**    |                       |                    |                                                                |
|            9             | Lập thẻ độc giả       | Nhập liệu          | Tạo mới thẻ độc giả với thông tin cá nhân                      |
|            10            | Danh sách độc giả     | Tra cứu            | Hiển thị, tìm kiếm, lọc danh sách độc giả                      |
|            11            | Chi tiết độc giả      | Tra cứu            | Xem thông tin chi tiết của một độc giả                         |
|            12            | Sửa thông tin độc giả | Nhập liệu          | Chỉnh sửa thông tin độc giả đã có                              |
|     **Quản lý Sách**     |                       |                    |                                                                |
|            13            | Tra cứu sách          | Tra cứu            | Tìm kiếm, lọc sách theo nhiều tiêu chí                         |
|            14            | Chi tiết sách         | Tra cứu            | Xem thông tin chi tiết của một đầu sách                        |
|            15            | Sửa thông tin sách    | Nhập liệu          | Chỉnh sửa thông tin sách đã có                                 |
|            16            | Chọn phương thức nhập | Màn hình chính     | Chọn nhập sách thủ công hoặc từ Excel                          |
|            17            | Nhập sách thủ công    | Nhập liệu          | Nhập thông tin sách mới bằng form                              |
|            18            | Nhập sách từ Excel    | Nhập liệu          | Import sách hàng loạt từ file Excel                            |
|            19            | DS phiếu nhập sách    | Tra cứu            | Hiển thị danh sách các phiếu nhập sách                         |
|            20            | Chi tiết phiếu nhập   | Tra cứu            | Xem chi tiết một phiếu nhập sách                               |
|    **Mượn/Trả Sách**     |                       |                    |                                                                |
|            21            | Lập phiếu mượn        | Nhập liệu          | Tạo phiếu mượn sách cho độc giả                                |
|            22            | DS phiếu mượn         | Tra cứu            | Hiển thị, tìm kiếm danh sách phiếu mượn                        |
|            23            | Chi tiết phiếu mượn   | Tra cứu            | Xem chi tiết một phiếu mượn                                    |
|            24            | Lập phiếu trả         | Nhập liệu          | Tạo phiếu trả sách, tính tiền phạt nếu có                      |
|            25            | DS phiếu trả          | Tra cứu            | Hiển thị, tìm kiếm danh sách phiếu trả                         |
|            26            | Chi tiết phiếu trả    | Tra cứu            | Xem chi tiết một phiếu trả                                     |
|  **Thu tiền & Báo cáo**  |                       |                    |                                                                |
|            27            | Lập phiếu thu         | Nhập liệu          | Tạo phiếu thu tiền phạt từ độc giả                             |
|            28            | DS phiếu thu          | Tra cứu            | Hiển thị danh sách phiếu thu tiền                              |
|            29            | Chi tiết phiếu thu    | Tra cứu            | Xem chi tiết một phiếu thu                                     |
|            30            | BC mượn theo thể loại | Báo biểu           | Thống kê số lượt mượn theo thể loại sách                       |
|            31            | BC tình hình mượn     | Báo biểu           | Thống kê tình hình mượn sách theo thời gian                    |
|            32            | BC sách trả trễ       | Báo biểu           | Danh sách sách trả trễ hạn và tiền phạt                        |
|   **Quản lý Hệ thống**   |                       |                    |                                                                |
|            33            | Thay đổi quy định     | Nhập liệu          | Cấu hình các tham số hệ thống (ngày mượn tối đa, tiền phạt...) |
|            34            | DS loại độc giả       | Tra cứu            | Quản lý các loại độc giả trong hệ thống                        |
|            35            | Thêm/Sửa loại độc giả | Nhập liệu          | Tạo mới hoặc chỉnh sửa loại độc giả                            |
|            36            | Xóa loại độc giả      | Nhập liệu          | Xác nhận xóa loại độc giả                                      |
|            37            | Quản lý người dùng    | Tra cứu            | Hiển thị danh sách tài khoản người dùng                        |
|            38            | Thêm/Sửa người dùng   | Nhập liệu          | Tạo mới hoặc chỉnh sửa tài khoản người dùng                    |
|            39            | Xóa người dùng        | Nhập liệu          | Xác nhận xóa tài khoản người dùng                              |
|            40            | Quản lý nhóm quyền    | Tra cứu            | Hiển thị danh sách nhóm quyền                                  |
|            41            | Thêm/Sửa nhóm quyền   | Nhập liệu          | Tạo mới hoặc chỉnh sửa nhóm quyền                              |
|            42            | Xóa nhóm quyền        | Nhập liệu          | Xác nhận xóa nhóm quyền                                        |
|            43            | Ma trận phân quyền    | Tra cứu, Nhập liệu | Xem và gán quyền cho các nhóm người dùng                       |
|            44            | DS chức năng          | Tra cứu            | Hiển thị danh sách chức năng hệ thống                          |
|            45            | Thêm/Sửa chức năng    | Nhập liệu          | Tạo mới hoặc chỉnh sửa chức năng                               |
|            46            | Xóa chức năng         | Nhập liệu          | Xác nhận xóa chức năng                                         |

## Thống kê

| Loại màn hình      | Số lượng |
| ------------------ | :------: |
| Màn hình chính     |    4     |
| Tra cứu            |    16    |
| Nhập liệu          |    24    |
| Báo biểu           |    3     |
| Tra cứu, Nhập liệu |    2     |
| **Tổng cộng**      |  **46**  |

## Chú thích loại màn hình

| Loại           | Mô tả                                      |
| -------------- | ------------------------------------------ |
| Màn hình chính | Màn hình điều hướng, tổng quan, thông báo  |
| Tra cứu        | Hiển thị danh sách, tìm kiếm, xem chi tiết |
| Nhập liệu      | Form nhập dữ liệu, thêm/sửa/xóa thông tin  |
| Báo biểu       | Báo cáo thống kê, biểu đồ                  |
