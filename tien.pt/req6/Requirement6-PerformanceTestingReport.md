# Requirement 6 - Performance Testing Report

## Mục lục

- [Requirement 6 - Performance Testing Report](#requirement-6---performance-testing-report)
  - [Mục lục](#mục-lục)
  - [Thông tin cá nhân \& nhóm](#thông-tin-cá-nhân--nhóm)
    - [Thông tin nhóm 11](#thông-tin-nhóm-11)
  - [1. Tổng quan](#1-tổng-quan)
    - [1.1. Các kỹ thuật kiểm thử hiệu năng](#11-các-kỹ-thuật-kiểm-thử-hiệu-năng)
      - [Chi tiết các kỹ thuật:](#chi-tiết-các-kỹ-thuật)
    - [1.2. System under test](#12-system-under-test)
  - [2. Môi trường kiểm thử](#2-môi-trường-kiểm-thử)
    - [2.1. Server (SUT)](#21-server-sut)
    - [2.2. Client (Test Runner)](#22-client-test-runner)
  - [3. Quy trình thực hiện kiểm thử](#3-quy-trình-thực-hiện-kiểm-thử)
    - [3.1. Cách 1: Sử dụng JMeter GUI](#31-cách-1-sử-dụng-jmeter-gui)
      - [Bước 1: Import Test Plan](#bước-1-import-test-plan)
      - [Bước 2: Cấu hình Thread Group](#bước-2-cấu-hình-thread-group)
      - [Bước 3: Cấu hình Data-Driven Testing (CSV)](#bước-3-cấu-hình-data-driven-testing-csv)
      - [Bước 4: Cấu hình Authentication Cookie](#bước-4-cấu-hình-authentication-cookie)
      - [Bước 5: Chạy Test và Xem Kết Quả](#bước-5-chạy-test-và-xem-kết-quả)
    - [3.2. Cách 2: Sử dụng JMeter CLI (Non-GUI Mode)](#32-cách-2-sử-dụng-jmeter-cli-non-gui-mode)
      - [Các lệnh thực thi cho từng kịch bản:](#các-lệnh-thực-thi-cho-từng-kịch-bản)
  - [4. Kết quả kiểm thử (Test Results)](#4-kết-quả-kiểm-thử-test-results)
    - [4.1. Bảng tổng hợp (Summary Table)](#41-bảng-tổng-hợp-summary-table)
    - [4.2. Phân tích chi tiết (Detailed Analysis)](#42-phân-tích-chi-tiết-detailed-analysis)
      - [4.2.1. Load Testing (10 Users)](#421-load-testing-10-users)
      - [4.2.2. Stress Testing (100 Users)](#422-stress-testing-100-users)
      - [4.2.3. Spike Testing (500 Users)](#423-spike-testing-500-users)
      - [4.2.4. Limit Testing (1000 - 2000 Users)](#424-limit-testing-1000---2000-users)
    - [4.3. Test Execution Screenshots](#43-test-execution-screenshots)
      - [Load Test Results (Summary Report)](#load-test-results-summary-report)
  - [5. Kết luận \& Khuyến nghị](#5-kết-luận--khuyến-nghị)
    - [5.1. Kết luận](#51-kết-luận)
    - [5.2. Khuyến nghị cải thiện](#52-khuyến-nghị-cải-thiện)
  - [6. Phụ lục A: Hướng dẫn cài đặt Apache JMeter](#6-phụ-lục-a-hướng-dẫn-cài-đặt-apache-jmeter)
    - [Yêu cầu hệ thống](#yêu-cầu-hệ-thống)
    - [Cài đặt trên Linux](#cài-đặt-trên-linux)
    - [Cấu hình JVM cho High Load Testing](#cấu-hình-jvm-cho-high-load-testing)
  - [7. Phụ lục B: Hướng dẫn lấy Session Cookie (Authentication)](#7-phụ-lục-b-hướng-dẫn-lấy-session-cookie-authentication)
    - [Cách 1: Sử dụng Script Python (Khuyên dùng)](#cách-1-sử-dụng-script-python-khuyên-dùng)
    - [Cách 2: Lấy thủ công qua Developer Tools (F12)](#cách-2-lấy-thủ-công-qua-developer-tools-f12)
    - [Lưu ý quan trọng về Cookie](#lưu-ý-quan-trọng-về-cookie)


## Thông tin cá nhân & nhóm

- Họ tên: Phan Thanh Tiến
- MSSV: 22120368
- Nhóm 11.

### Thông tin nhóm 11

- Thông tin thành viên: 
  - Giang Đức Nhật - 22120252
  - Phan Thanh Tiến - 22120368
  - Nguyễn Bùi Vương Tiễn - 22120370
  - Lý Trọng Tín - 22120371

- Bảng phân công nhóm:
 
| Tính năng                   | Mô tả                                                             | Thành viên            |
| :-------------------------- | :---------------------------------------------------------------- | :-------------------- |
| HR Administration           | Quản trị hệ thống, cấu trúc tổ chức, user                         | Giang Đức Nhật        |
| Employee Self-Service (ESS) | Cổng thông tin nhân viên tự phục vụ                               | Giang Đức Nhật        |
| **Recruitment**             | **Tuyển dụng, theo dõi ứng viên**                                 | **Phan Thanh Tiến**   |
| **Performance Management**  | **Đánh giá KPI, đề nghị xem xét, lưu lịch sử performance review** | **Phan Thanh Tiến**   |
| Reporting & Analytics       | Báo cáo tùy chỉnh, xuất dữ liệu                                   | Nguyễn Bùi Vương Tiễn |
| Time and Attendance         | Chấm công, Timesheets                                             | Nguyễn Bùi Vương Tiễn |
| Employee Management (PIM)   | Quản lý hồ sơ nhân viên, báo cáo                                  | Lý Trọng Tín          |
| Leave Management            | Quản lý ngày nghỉ, quy tắc nghỉ phép                              | Lý Trọng Tín          |

- Tính năng được phân công kiểm thử hiệu năng: **Recruitment (Create Candidate API)**

## 1. Tổng quan

Báo cáo này trình bày kết quả kiểm thử hiệu năng (Performance Testing) cho tính năng **Recruitment: Create Candidate** của hệ thống OrangeHRM. Kiểm thử được thực hiện sử dụng công cụ **Apache JMeter 5.6.3** với các kịch bản kiểm thử hiệu năng tiêu chuẩn.

### 1.1. Các kỹ thuật kiểm thử hiệu năng

| Kỹ thuật           | Mô tả                                                                 | Mục tiêu                                                          |
| :----------------- | :-------------------------------------------------------------------- | :---------------------------------------------------------------- |
| **Load Testing**   | Đánh giá hiệu năng hệ thống dưới tải người dùng dự kiến (Normal Load) | Xác định thời gian phản hồi và throughput ở điều kiện bình thường |
| **Stress Testing** | Đẩy tải vượt quá mức bình thường để tìm giới hạn của hệ thống         | Xác định điểm mà hệ thống bắt đầu suy giảm hiệu năng              |
| **Spike Testing**  | Tăng tải đột ngột trong thời gian ngắn                                | Đánh giá khả năng phục hồi khi có traffic burst                   |
| **Limit Testing**  | Tăng tải cực đại để tìm "điểm gãy" (Breaking Point)                   | Xác định ngưỡng chịu đựng tối đa của hệ thống                     |

#### Chi tiết các kỹ thuật:

1. **Load Testing (10 Users)**
   - *Mục đích*: Đo lường hiệu năng baseline của API dưới tải bình thường.
   - *Cấu hình*: 10 threads, ramp-up 10 giây, loop 5 lần = 50 requests.
   - *Chỉ số đánh giá*: Response time < 500ms, Error rate = 0%.

2. **Stress Testing (100 Users)**
   - *Mục đích*: Đánh giá hành vi hệ thống khi tải tăng lên 10 lần.
   - *Cấu hình*: 100 threads, ramp-up 10 giây, loop 10 lần = 1000 requests.
   - *Quan sát*: Request queueing, degradation pattern.

3. **Spike Testing (500 Users)**
   - *Mục đích*: Mô phỏng tình huống traffic đột biến (flash crowd).
   - *Cấu hình*: 500 threads, ramp-up 1 giây = 500 requests đồng thời.
   - *Chỉ số quan trọng*: Hệ thống có crash không? Recovery time?

4. **Limit Testing (1000 - 2000 Users)**
   - *Mục đích*: Tìm điểm gãy của hệ thống (Breaking Point).
   - *Cấu hình*: 1000-2000 threads, ramp-up 1 giây.
   - *Kết quả mong đợi*: Xác định được số lượng concurrent users tối đa.

### 1.2. System under test

**API Specifications:**
- **Endpoint**: `POST /api/v2/recruitment/candidates`
- **Chức năng**: Tạo mới hồ sơ ứng viên trong hệ thống.
- **Authentication**: Session Cookie (`_orangehrm`)
- **Content-Type**: `application/json`

**Request Payload Structure:**
```json
{
  "firstName": "TestUser1",
  "lastName": "Perf1",
  "email": "test.user.1@perf.com",
  "contactNumber": null,
  "keywords": null,
  "comment": null,
  "dateOfApplication": "2023-10-15",
  "consentToKeepData": false
}
```

**Expected Response:**
- **Success**: `200 OK` với JSON Object chứa thông tin ứng viên vừa tạo.
- **Failure**: `401 Unauthorized` nếu cookie hết hạn.

## 2. Môi trường kiểm thử

### 2.1. Server

| Thành phần      | Thông tin                             |
| :-------------- | :------------------------------------ |
| **Application** | OrangeHRM 5.x (Open Source)           |
| **Base URL**    | `http://localhost:8080/web/index.php` |
| **Web Server**  | Apache HTTP Server với PHP            |
| **Database**    | MySQL 8.x                             |
| **Deployment**  | Docker Container (localhost)          |

Sau đây là thông tin của máy host server:

| Thành phần           | Thông tin            |
| :------------------- | :------------------- |
| **Operating System** | Linux (Ubuntu 25.10) |
| **CPU**              | Intel Core i5-1135G7 |
| **RAM**              | 24GB DDR4            |
| **Disk**             | SSD 512GB            |

Tuy nhiên, mỗi container sẽ được giới hạn với **1 core CPU và 1GB RAM**.

![alt text](image.png)

### 2.2. Client (Test Runner)

| Thành phần            | Thông tin                      |
| :-------------------- | :----------------------------- |
| **Operating System**  | Linux (Ubuntu/Debian)          |
| **Test Tool**         | Apache JMeter 5.6.3            |
| **Java Version**      | OpenJDK 21+                    |
| **Network**           | Localhost  |
| **Memory Allocation** | JVM Heap: 1GB (-Xms1g -Xmx1g)  |

## 3. Quy trình thực hiện kiểm thử

### 3.1. Cách 1: Sử dụng JMeter GUI

#### Bước 1: Import Test Plan

1. Clone repository về máy:
   ```bash
   git clone <repository-url>
   cd tien.pt/req6
   ```

2. Mở JMeter và import file `performance_test.jmx` bằng cách:
   - File → Open → Chọn `performance_test.jmx`

![Cấu trúc Test Plan trong JMeter](jmeter-test-plan.png)

Hình 1: Cấu trúc Test Plan với các thành phần: CSV Data Set Config, HTTP Header Manager, HTTP Request Defaults, Create Candidate Request, và Summary Report.

#### Bước 2: Cấu hình Thread Group

Điều chỉnh các tham số trong Thread Group theo kịch bản test:

![Cấu hình Thread Group](jmeter-thread-config.png)

Hình 2: Cấu hình Thread Group với các biến `${THREADS}`, `${RAMPUP}`, `${LOOP}` cho phép linh hoạt thay đổi qua CLI.

| Tham số             | Ý nghĩa                                     | Giá trị mặc định |
| :------------------ | :------------------------------------------ | :--------------- |
| `Number of Threads` | Số lượng virtual users đồng thời            | 10               |
| `Ramp-up Period`    | Thời gian để khởi tạo tất cả threads (giây) | 10               |
| `Loop Count`        | Số lần lặp cho mỗi thread                   | 5                |

#### Bước 3: Cấu hình Data-Driven Testing (CSV)

Dữ liệu ứng viên được tham số hóa thông qua file CSV để đảm bảo mỗi request tạo một ứng viên với thông tin khác nhau.

![Cấu hình CSV Data Set](jmeter-csv-config.png)

Hình 3: Cấu hình CSV Data Set Config để đọc dữ liệu từ file `data/candidates.csv`.

**Cấu trúc file `data/candidates.csv`:**
```csv
firstName,lastName,email
TestUser1,Perf1,test.user.1@perf.com
TestUser2,Perf2,test.user.2@perf.com
TestUser3,Perf3,test.user.3@perf.com
...
TestUser50,Perf50,test.user.50@perf.com
```

#### Bước 4: Cấu hình Authentication Cookie

1. Lấy session cookie hợp lệ (Tham khảo Phụ lục B).
2. Cập nhật biến `COOKIE` trong User Defined Variables hoặc qua CLI parameter.

#### Bước 5: Chạy Test và Xem Kết Quả

1. Click nút **Start** (biểu tượng play màu xanh) trên thanh công cụ.
2. Quan sát kết quả realtime trong **View Results Tree** và **Summary Report**.

![Kết quả View Results Tree](jmeter-results-tree.png)

Hình 4: View Results Tree hiển thị từng request với status 200 OK, response time ~35ms, và response body JSON.

### 3.2. Cách 2: Sử dụng JMeter CLI (Non-GUI Mode)

> **Khuyên dùng**: Non-GUI mode cho hiệu năng tốt hơn khi chạy với số lượng threads lớn.

#### Các lệnh thực thi cho từng kịch bản:

```bash
# Di chuyển đến thư mục chứa test plan
cd tien.pt/req6

# Lấy session cookie (chạy trước khi test)
COOKIE=$(python3 ../req7/get_auth_cookie.py | grep "VALID_COOKIE" | cut -d: -f2 | tr -d ' ')

# Load Testing (10 Users, 5 loops)
jmeter -n -t performance_test.jmx \
  -Jthreads=10 -Jrampup=10 -Jloop=5 \
  -Jcookie="orangehrm=$COOKIE" \
  -l load.jtl

# Stress Testing (100 Users, 10 loops)
jmeter -n -t performance_test.jmx \
  -Jthreads=100 -Jrampup=10 -Jloop=10 \
  -Jcookie="orangehrm=$COOKIE" \
  -l stress.jtl

# Spike Testing (500 Users, 1 loop, 1s ramp-up)
jmeter -n -t performance_test.jmx \
  -Jthreads=500 -Jrampup=1 -Jloop=1 \
  -Jcookie="orangehrm=$COOKIE" \
  -l spike.jtl

# Limit Testing 1 (1000 Users)
jmeter -n -t performance_test.jmx \
  -Jthreads=1000 -Jrampup=1 -Jloop=1 \
  -Jcookie="orangehrm=$COOKIE" \
  -l limit_1000.jtl

# Limit Testing 2 (2000 Users)
jmeter -n -t performance_test.jmx \
  -Jthreads=2000 -Jrampup=1 -Jloop=1 \
  -Jcookie="orangehrm=$COOKIE" \
  -l limit_2000.jtl
```

**Giải thích các tham số:**
| Tham số           | Mô tả                                   |
| :---------------- | :-------------------------------------- |
| `-n`              | Non-GUI mode (headless)                 |
| `-t`              | Đường dẫn đến file Test Plan (.jmx)     |
| `-Jthreads=N`     | Override biến THREADS = N               |
| `-Jrampup=N`      | Override biến RAMPUP = N giây           |
| `-Jloop=N`        | Override biến LOOP = N lần              |
| `-Jcookie=VALUE`  | Override biến COOKIE cho authentication |
| `-l filename.jtl` | Lưu kết quả vào file JTL                |

![Kết quả chạy Stress Test trên CLI](jmeter-cli-stress.png)

Hình 5: Output của JMeter CLI khi chạy Stress Test với 100 threads, hiển thị realtime statistics.

## 4. Kết quả kiểm thử (Test Results)

> Kết quả dưới đây được ghi nhận từ lần chạy thực tế vào ngày **13/01/2026**.

### 4.1. Bảng tổng hợp (Summary Table)

| Test Type   | Users | Total Requests | Avg Time (ms) | Min (ms) | Max (ms) | Throughput (req/s) | Error Rate |   Status   |
| :---------- | :---: | :------------: | :-----------: | :------: | :------: | :----------------: | :--------: | :--------: |
| **Load**    |  10   |       50       |    **35**     |    31    |    89    |        10.6        | **0.00%**  | ✅ **PASS** |
| **Stress**  |  100  |      1000      |   **1,389**   |    34    |  10,190  |        35.5        | **0.00%**  | ✅ **PASS** |
| **Spike**   |  500  |      500       |   **5,750**   |   890    |  10,200  |        44.6        | **0.00%**  | ⚠️ **WARN** |
| **Limit 1** | 1000  |      1000      |   **9,310**   |  1,200   |  18,270  |        52.0        | **0.00%**  | ⚠️ **WARN** |
| **Limit 2** | 2000  |      2000      |  **18,240**   |  2,500   |  35,430  |        53.0        | **0.00%**  | ⚠️ **WARN** |

### 4.2. Phân tích chi tiết (Detailed Analysis)

#### 4.2.1. Load Testing (10 Users)

| Metric                | Value      | Đánh giá               |
| :-------------------- | :--------- | :--------------------- |
| Average Response Time | 35ms       | 🟢 Xuất sắc (< 100ms)   |
| Max Response Time     | 89ms       | 🟢 Chấp nhận được       |
| Throughput            | 10.6 req/s | 🟢 Phù hợp với 10 users |
| Error Rate            | 0.00%      | 🟢 Không có lỗi         |

**Nhận xét**: Hệ thống hoạt động hoàn hảo dưới tải bình thường. Thời gian phản hồi tức thì (~35ms) cho thấy API được tối ưu tốt cho use case chuẩn.

#### 4.2.2. Stress Testing (100 Users)

| Metric                | Value      | Đánh giá                     |
| :-------------------- | :--------- | :--------------------------- |
| Average Response Time | 1,389ms    | 🟡 Chấp nhận được nhưng cao   |
| Max Response Time     | 10,190ms   | 🟠 Cần lưu ý (timeout risk)   |
| Throughput            | 35.5 req/s | 🟢 Tăng x3.5 so với Load Test |
| Error Rate            | 0.00%      | 🟢 Không có lỗi               |

**Nhận xét**: 
- Độ trễ tăng đáng kể (~1.4s) do server phải xếp hàng xử lý (Request Queueing).
- Throughput tăng từ 10.6 lên 35.5 req/s cho thấy hệ thống scale được nhưng với trade-off về latency.
- Mọi request đều được phục vụ thành công (0% error).

#### 4.2.3. Spike Testing (500 Users)

| Metric                | Value      | Đánh giá             |
| :-------------------- | :--------- | :------------------- |
| Average Response Time | 5,750ms    | 🟠 Cao, ảnh hưởng UX  |
| Max Response Time     | 10,200ms   | 🔴 Nguy cơ timeout    |
| Throughput            | 44.6 req/s | 🟢 Throughput ổn định |
| Error Rate            | 0.00%      | 🟢 Không có lỗi       |

![Kết quả Spike Test](jmeter-spike-results.png)

Hình 6: Summary Report của Spike Test (500 users) với average response time ~5.7s nhưng 0% error rate.

**Nhận xét**:
- Khi có lượng truy cập đột biến đập vào trong 1 giây, hệ thống **vẫn không crash**.
- PHP Server process quản lý tốt việc xếp hàng, nhưng người dùng phải chờ trung bình ~6 giây.
- Throughput đạt 44.6 req/s cho thấy hệ thống có khả năng scale.

#### 4.2.4. Limit Testing (1000 - 2000 Users)

**Thử nghiệm cực hạn:**

| Users | Avg Time | Max Time | Error Rate | Kết luận            |
| :---: | :------: | :------: | :--------: | :------------------ |
| 1000  |  9.31s   |  18.27s  |   0.00%    | Vẫn hoạt động       |
| 2000  |  18.24s  |  35.43s  |   0.00%    | Vượt client timeout |

**Phát hiện quan trọng:**
1. **Độ ổn định (Availability)**: Hệ thống cho thấy độ ổn định đáng kinh ngạc. Tại 2000 users đồng thời, **tỷ lệ lỗi vẫn là 0%**.

2. **Vấn đề Latency**: Thời gian chờ tăng tuyến tính với số lượng user. Tại mức 2000 users, người dùng cuối cùng phải chờ tới **35 giây**.

3. **Breaking Point**: "Điểm gãy" của hệ thống này không phải là Server Crash (500 Internal Error) mà là **Client Timeout**. Mặc dù server vẫn trả lời sau 35s, nhưng hầu hết trình duyệt/ứng dụng client sẽ ngắt kết nối trước thời điểm đó (thường timeout mặc định là 30s).

### 4.3. Test Execution Screenshots

#### Load Test Results (Summary Report)

![Load Test Summary Report](jmeter-load-results.png)

Hình 7: Kết quả Load Test với 50 samples, average 35ms, 0% error rate.

## 5. Kết luận & Khuyến nghị

### 5.1. Kết luận

| Tiêu chí               | Kết quả                                 | Đánh giá         |
| :--------------------- | :-------------------------------------- | :--------------- |
| **Stability**          | 0% error rate ở mọi mức tải             | 🟢 Xuất sắc       |
| **Scalability**        | Throughput tăng từ 10.6 → 53 req/s      | 🟢 Tốt            |
| **Latency under load** | Tăng tuyến tính, max 35s                | 🟠 Cần cải thiện  |
| **Breaking Point**     | ~2000 concurrent users (client timeout) | 🟡 Chấp nhận được |

### 5.2. Khuyến nghị cải thiện

1. **Web Server Tuning**
   - Cấu hình `MaxClients` / `MaxRequestWorkers` trong Apache để giới hạn số lượng xử lý đồng thời.
   - Tránh để request xếp hàng quá lâu gây treo hệ thống.
   ```apache
   # /etc/apache2/mods-available/mpm_prefork.conf
   MaxRequestWorkers 150
   MaxConnectionsPerChild 10000
   ```

2. **Database Optimization**
   - Sử dụng connection pooling để tối ưu database connections.
   - Index các trường thường xuyên query (email, firstName, lastName).

3. **Caching Layer**
   - Triển khai Redis/Memcached để cache các truy vấn database đọc.
   - Giảm tải cho MySQL khi xử lý concurrent requests.

4. **Asynchronous Processing**
   - Với tác vụ ghi (Create Candidate), có thể đẩy vào Message Queue (RabbitMQ/Redis Queue).
   - Trả về `202 Accepted` ngay lập tức cho người dùng thay vì chờ xử lý xong.

## 6. Phụ lục A: Hướng dẫn cài đặt Apache JMeter

### Yêu cầu hệ thống
- Java JDK 11 hoặc cao hơn
- RAM: Tối thiểu 2GB (khuyên 4GB cho stress testing)

### Cài đặt trên Linux

```bash
# 1. Cài đặt Java (nếu chưa có)
sudo apt update
sudo apt install openjdk-11-jdk -y

# 2. Kiểm tra Java version
java -version

# 3. Tải Apache JMeter
wget https://downloads.apache.org/jmeter/binaries/apache-jmeter-5.6.3.tgz

# 4. Giải nén
tar -xzf apache-jmeter-5.6.3.tgz

# 5. Thêm vào PATH (tùy chọn)
echo 'export PATH=$PATH:~/apache-jmeter-5.6.3/bin' >> ~/.bashrc
source ~/.bashrc

# 6. Chạy JMeter GUI
jmeter

# 7. Hoặc chạy Non-GUI mode
jmeter -n -t test.jmx -l results.jtl
```

### Cấu hình JVM cho High Load Testing

```bash
# Chỉnh sửa file jmeter (hoặc jmeter.bat trên Windows)
# Tăng heap size cho JVM
HEAP="-Xms2g -Xmx4g -XX:MaxMetaspaceSize=512m"
```

## 7. Phụ lục B: Hướng dẫn lấy Session Cookie (Authentication)

Do hệ thống OrangeHRM sử dụng **HttpOnly Cookie** (`_orangehrm`) để bảo mật, việc lấy cookie này thông qua JavaScript console (`document.cookie`) là không thể. Dưới đây là 2 cách để lấy giá trị này.

### Cách 1: Sử dụng Script Python (Khuyên dùng)

Script Python đã được phát triển để tự động login và lấy session cookie.

```bash
# Chạy script
python3 ../req7/get_auth_cookie.py

# Output mẫu
# VALID_COOKIE: abc123xyz...
```

Sau đó sử dụng cookie trong lệnh JMeter:
```bash
jmeter -n -t performance_test.jmx -Jcookie="orangehrm=abc123xyz..." -l results.jtl
```

### Cách 2: Lấy thủ công qua Developer Tools (F12)

1. Mở trang Login OrangeHRM và mở DevTools (F12), chuyển sang tab **Network**.
2. Thực hiện đăng nhập thành công.
3. Trong danh sách Network, tìm request có tên `validate` (Method POST) hoặc `index`.
4. Click vào request, chọn tab **Headers**.
5. Tìm phần **Response Headers** → Copy giá trị của `_orangehrm` (bỏ phần `; path=/...`).

### Lưu ý quan trọng về Cookie

- Session cookie có thời gian sống giới hạn (~30 phút không hoạt động).
- Cần lấy cookie mới trước mỗi lần chạy test nếu session đã hết hạn.
- Kiểm tra response code `401 Unauthorized` để biết cookie đã hết hạn.
