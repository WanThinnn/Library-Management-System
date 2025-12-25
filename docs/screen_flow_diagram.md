# Sơ đồ liên kết các màn hình - Library Management System

Sơ đồ dưới đây thể hiện cấu trúc và mối liên kết giữa các màn hình trong hệ thống Quản lý Thư viện.

```mermaid
flowchart LR
    %% Main entry point
    Login["Màn hình đăng nhập"]
    
    %% Password management
    Login --> PWReset["Quên mật khẩu"]
    PWReset --> PWResetDone["Đã gửi email"]
    PWReset --> PWResetConfirm["Đặt lại mật khẩu"]
    PWResetConfirm --> PWResetComplete["Hoàn tất đặt lại"]
    
    %% Main screens after login
    Login --> Home["Màn hình trang chủ"]
    
    %% Profile management
    Home --> Profile["Thông tin cá nhân"]
    Profile --> ChangePassword["Đổi mật khẩu"]
    
    %% ========== QUẢN LÝ ĐỘC GIẢ ==========
    Home --> ReaderMgmt["Quản lý Độc giả"]
    ReaderMgmt --> ReaderCreate["Lập thẻ độc giả"]
    ReaderMgmt --> ReaderList["Danh sách độc giả"]
    ReaderList --> ReaderDetail["Chi tiết độc giả"]
    ReaderDetail --> ReaderEdit["Sửa thông tin độc giả"]
    
    %% ========== QUẢN LÝ SÁCH ==========
    Home --> BookMgmt["Quản lý Sách"]
    BookMgmt --> BookSearch["Tra cứu sách"]
    BookMgmt --> BookImportSelect["Chọn phương thức nhập"]
    
    BookSearch --> BookDetail["Chi tiết sách"]
    BookDetail --> BookEdit["Sửa thông tin sách"]
    
    BookImportSelect --> BookImport["Nhập sách thủ công"]
    BookImportSelect --> BookImportExcel["Nhập sách từ Excel"]
    
    BookMgmt --> BookImportList["DS phiếu nhập sách"]
    BookImportList --> BookImportDetail["Chi tiết phiếu nhập"]
    
    %% ========== MƯỢN/TRẢ SÁCH ==========
    Home --> BorrowMgmt["Quản lý Mượn/Trả"]
    
    BorrowMgmt --> BorrowBook["Lập phiếu mượn"]
    BorrowMgmt --> BorrowList["DS phiếu mượn"]
    BorrowList --> BorrowDetail["Chi tiết phiếu mượn"]
    
    BorrowMgmt --> ReturnBook["Lập phiếu trả"]
    BorrowMgmt --> ReturnList["DS phiếu trả"]
    ReturnList --> ReturnDetail["Chi tiết phiếu trả"]
    
    %% ========== THU TIỀN & BÁO CÁO ==========
    Home --> ReceiptMgmt["Thu tiền & Báo cáo"]
    
    ReceiptMgmt --> ReceiptForm["Lập phiếu thu"]
    ReceiptMgmt --> ReceiptList["DS phiếu thu"]
    ReceiptList --> ReceiptDetail["Chi tiết phiếu thu"]
    
    ReceiptMgmt --> ReportBorrowCategory["BC mượn theo thể loại"]
    ReceiptMgmt --> ReportBorrowSituation["BC tình hình mượn"]
    ReceiptMgmt --> ReportOverdue["BC sách trả trễ"]
    
    %% ========== HỆ THỐNG ==========
    Home --> SystemMgmt["Quản lý Hệ thống"]
    
    SystemMgmt --> ParameterUpdate["Thay đổi quy định"]
    
    %% Reader Types
    SystemMgmt --> ReaderTypeList["DS loại độc giả"]
    ReaderTypeList --> ReaderTypeForm["Thêm/Sửa loại độc giả"]
    ReaderTypeList --> ReaderTypeDelete["Xóa loại độc giả"]
    
    %% User Management
    SystemMgmt --> UserList["Quản lý người dùng"]
    UserList --> UserForm["Thêm/Sửa người dùng"]
    UserList --> UserDelete["Xóa người dùng"]
    
    %% Permission Management
    SystemMgmt --> UserGroupList["Quản lý nhóm quyền"]
    UserGroupList --> UserGroupForm["Thêm/Sửa nhóm quyền"]
    UserGroupList --> UserGroupDelete["Xóa nhóm quyền"]
    UserGroupList --> PermissionMatrix["Ma trận phân quyền"]
    
    %% Function Management
    SystemMgmt --> FunctionList["DS chức năng"]
    FunctionList --> FunctionForm["Thêm/Sửa chức năng"]
    FunctionList --> FunctionDelete["Xóa chức năng"]
    
    %% Styling
    classDef mainScreen fill:#4299e1,stroke:#2b6cb0,color:#fff
    classDef subScreen fill:#48bb78,stroke:#2f855a,color:#fff
    classDef formScreen fill:#ed8936,stroke:#c05621,color:#fff
    classDef detailScreen fill:#9f7aea,stroke:#6b46c1,color:#fff
    classDef reportScreen fill:#f56565,stroke:#c53030,color:#fff
    
    class Login,Home mainScreen
    class ReaderMgmt,BookMgmt,BorrowMgmt,ReceiptMgmt,SystemMgmt subScreen
    class ReaderCreate,BookImport,BookImportExcel,BorrowBook,ReturnBook,ReceiptForm,UserForm,UserGroupForm,FunctionForm,ReaderTypeForm,ParameterUpdate,ChangePassword formScreen
    class ReaderDetail,BookDetail,BorrowDetail,ReturnDetail,ReceiptDetail,BookImportDetail detailScreen
    class ReportBorrowCategory,ReportBorrowSituation,ReportOverdue reportScreen
```

## Chú thích màu sắc

| Màu | Ý nghĩa |
|-----|---------|
| 🔵 Xanh dương | Màn hình chính (Login, Home) |
| 🟢 Xanh lá | Màn hình quản lý (Menu chính) |
| 🟠 Cam | Màn hình form (Thêm/Sửa/Xóa) |
| 🟣 Tím | Màn hình chi tiết |
| 🔴 Đỏ | Màn hình báo cáo |

## Danh sách các màn hình

### Xác thực & Tài khoản
- Đăng nhập
- Quên mật khẩu / Đặt lại mật khẩu
- Thông tin cá nhân
- Đổi mật khẩu

### Quản lý Độc giả
- Lập thẻ độc giả
- Danh sách độc giả
- Chi tiết / Sửa thông tin độc giả

### Quản lý Sách
- Tra cứu sách
- Chi tiết / Sửa thông tin sách
- Nhập sách thủ công / Excel
- Danh sách phiếu nhập

### Mượn/Trả Sách
- Lập phiếu mượn
- Danh sách phiếu mượn / Chi tiết
- Lập phiếu trả
- Danh sách phiếu trả / Chi tiết

### Thu tiền & Báo cáo
- Lập phiếu thu
- Danh sách phiếu thu / Chi tiết
- Báo cáo mượn theo thể loại
- Báo cáo tình hình mượn
- Báo cáo sách trả trễ

### Quản lý Hệ thống
- Thay đổi quy định
- Quản lý loại độc giả
- Quản lý người dùng
- Quản lý nhóm quyền
- Ma trận phân quyền
- Quản lý chức năng
