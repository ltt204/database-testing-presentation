# OrangeHRM Database Testing - Data Generator
Repo này chứa các công cụ và script để dựng môi trường và tự động sinh dữ liệu giả lập (mock data) phục vụ cho việc kiểm thử cơ sở dữ liệu (Database Testing) của hệ thống OrangeHRM.

Các script được viết bằng Node.js, sử dụng thư viện faker để tạo dữ liệu ngẫu nhiên và mysql2 để tương tác trực tiếp với database.

## Yêu cầu hệ thống (Prerequisites)
Trước khi bắt đầu, hãy đảm bảo máy của bạn đã cài đặt:

- Docker & Docker Compose

- Node.js (Khuyên dùng phiên bản LTS mới nhất)

## Cài đặt & Thiết lập môi trường (Setup)
### 1. Cấu hình biến môi trường
Sao chép file cấu hình mẫu .env.example thành .env:

```Bash

cp .env.example .env

```

Mở file .env và cập nhật các thông số nếu cần thiết (hoặc giữ nguyên mặc định):

- MYSQL_ROOT_PASSWORD: Mật khẩu root của MySQL.
 
- MYSQL_USER: Tên user database (ví dụ: orangehrm).

- MYSQL_PASSWORD: Mật khẩu cho user trên.

- MYSQL_DATABASE: Tên database (ví dụ: orangehrm).

### 2. Khởi chạy Docker Containers
Dựng database (MySQL), ứng dụng OrangeHRM và phpMyAdmin bằng Docker Compose:

```Bash
docker-compose up -d
```

Sau khi chạy xong, các dịch vụ sẽ hoạt động tại:

- OrangeHRM: http://localhost:8080

- phpMyAdmin: http://localhost:8081

- MySQL: Host localhost, Port 3306

### 3. Cài đặt OrangeHRM
Trước khi chạy bất kỳ script sinh dữ liệu nào, bạn phải hoàn tất cài đặt OrangeHRM để hệ thống tạo các bảng trong database.

Truy cập http://localhost:8080.

Làm theo các bước cài đặt trên giao diện web Orange HRM Installer.

Ở bước cấu hình Database:

- Database Host: orangehrm_db (Lưu ý: dùng tên service trong docker, không dùng localhost tại bước này).

- Database Port: 3306

- Database Name: Nhập giống giá trị MYSQL_DATABASE trong file .env.

- OrangeHRM User/Password: Nhập giống MYSQL_USER / MYSQL_PASSWORD trong file .env.

### 4. Cài đặt thư viện Node.js
Tại thư mục gốc của dự án, chạy lệnh sau để tải các thư viện cần thiết (mysql2, @faker-js/faker, ...):

```Bash
npm install
```
#### Hướng dẫn chạy Script sinh dữ liệu
Dự án bao gồm các script để sinh dữ liệu cho các module khác nhau.

**Cấu hình kết nối Database cho Script**
**Lưu ý**: Các script (message.js, generate-employees.js,...) đang được cấu hình kết nối database. Hãy đảm bảo thông tin trong code hoặc biến môi trường khớp với file .env bạn đã tạo.

- Host: localhost (khi chạy script từ máy local của bạn).

- Port: 3306.

- User/Password: Khớp với file .env.

##### 1. Generate dữ liệu Tuyển dụng (Recruitment)
Script recruitment.js sẽ tạo dữ liệu về: Vị trí tuyển dụng (Vacancies), Ứng viên (Candidates), Lịch phỏng vấn và Lịch sử ứng viên.

```Bash
node recruitment.js
```

Script này sẽ tự động tạo Job Title mới nếu chưa có.

##### 2. Generate dữ liệu Nhân viên (Employees)
Script nhat-report/generate-employees.js sẽ tạo hồ sơ nhân viên giả lập.

```Bash
node nhat-report/generate-employees.js
```
Lưu ý: Cần có Job Titles trong hệ thống trước khi chạy script này (có thể chạy message.js trước hoặc tạo thủ công).

##### 3. Generate dữ liệu HR Administration
Script nhat-report/hr-admin/hr-admin-gen.js sẽ tạo dữ liệu cho một vài chức năng liên quan đến HR Administration

```Bash
node nhat-report/hr-admin/hr-admin-gen.js
```

##### 4. Generate dữ liệu ESS
Script nhat-report/ess/ess-gen.js sẽ tạo dữ liệu cho một vài chức năng liên quan đến ESS

```Bash
node nhat-report/ess/ess-gen.js
```


## Kiểm tra dữ liệu
Sau khi chạy script, bạn có thể kiểm tra dữ liệu đã tạo bằng cách:

- Đăng nhập vào OrangeHRM (http://localhost:8080) với tài khoản Admin.

- Truy cập phpMyAdmin (http://localhost:8081) để xem trực tiếp các bảng trong database (ví dụ: hs_hr_employee, ohrm_job_candidate, ohrm_job_vacancy).

## Cấu trúc thư mục
docker-compose.yml: Cấu hình Docker services.

message.js: Script chính sinh dữ liệu Recruitment.

nhat-report/: Chứa các script sinh dữ liệu bổ sung và báo cáo.

.env: Biến môi trường (không commit file này lên git).
