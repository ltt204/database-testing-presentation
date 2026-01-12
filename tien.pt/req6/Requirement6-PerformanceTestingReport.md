# Requirement 6 - Performance Testing Report

## 1. Tổng quan (Overview)

Báo cáo này trình bày kết quả kiểm thử hiệu năng (Performance Testing) cho tính năng **Recruitment: Create Candidate** của hệ thống OrangeHRM. Kiểm thử được thực hiện theo yêu cầu, sử dụng công cụ **Apache JMeter** với 3 kịch bản chính: **Load Testing**, **Stress Testing**, và **Spike Testing**, cùng với kịch bản mở rộng **Limit Testing** để tìm ngưỡng chịu đựng của hệ thống.

Dữ liệu kiểm thử được tham số hóa (Data Driven) thông qua file CSV, đảm bảo tính thực tế của dữ liệu đầu vào.

### 1.1. Mục tiêu & Kỹ thuật
*   **Load Testing**: Đánh giá hiệu năng hệ thống dưới tải người dùng dự kiến (10 users).
*   **Stress Testing**: Đánh giá giới hạn chịu đựng của hệ thống bằng cách tăng tải lên mức cao (100 users).
*   **Spike Testing**: Đánh giá khả năng xử lý của hệ thống khi lượng truy cập tăng đột biến cực lớn (500 users/1s).
*   **Limit Testing (Mới)**: Tăng tải cực đại (1000 - 2000 users) để tìm "điểm gãy" (Breaking Point) của hệ thống.

### 1.2. Đối tượng kiểm thử (SUT)
*   **API Endpoint**: `POST /api/v2/recruitment/candidates`
*   **Chức năng**: Tạo mới hồ sơ ứng viên.
*   **Payload**: JSON (First Name, Last Name, Email lấy từ file CSV).

## 2. Môi trường kiểm thử (Test Environment)

### 2.1. Server (SUT)
*   **Application**: OrangeHRM (Open Source).
*   **URL**: `http://localhost:8080/web/index.php`
*   **Web Server**: Localhost (Apache/PHP).
*   **Database**: MySQL.

### 2.2. Client (Test Runner)
*   **OS**: Linux.
*   **Tool**: Apache JMeter 5.6.3.
*   **Java Version**: 11+.
*   **Network**: Localhost loopback.

## 3. Quy trình thực hiện (Test Execution Process)

1.  **Preparation**:
    *   Tạo Test Plan (`req6/performance_test.jmx`).
    *   Chuẩn bị dữ liệu (`req6/data/candidates.csv`).
    *   Lấy Authentication Cookie (`_orangehrm`) hợp lệ.

2.  **Execution Scenarios**:
    *   **Load**: 10 Threads, Ramp-up 10s.
    *   **Stress**: 100 Threads, Ramp-up 10s.
    *   **Spike**: 500 Threads, Ramp-up 1s.
    *   **Limit 1**: 1000 Threads, Ramp-up 1s.
    *   **Limit 2**: 2000 Threads, Ramp-up 1s.

## 4. Kết quả kiểm thử (Test Results)

Kết quả dưới đây được ghi nhận từ lần chạy thực tế vào ngày 13/01/2026.

### 4.1. Bảng tổng hợp (Summary Table)

| Test Type | Users (Threads) | Total Req | Avg Time (s) | Max Time (s) | Throughput (req/s) | Error Rate | Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Load** | 10 | 50 | **0.035** | 0.089 | 10.6 | **0.00%** | **PASS** |
| **Stress** | 100 | 1000 | **1.39** | 10.19 | 35.5 | **0.00%** | **PASS** |
| **Spike** | 500 | 500 | **5.75** | 10.20 | 44.6 | **0.00%** | **WARM** |
| **Limit 1** | 1000 | 1000 | **9.31** | 18.27 | 52.0 | **0.00%** | **WARN** |
| **Limit 2** | 2000 | 2000 | **18.24** | 35.43 | 53.0 | **0.00%** | **WARN** |

### 4.2. Phân tích chi tiết (Detailed Analysis)

#### Load Testing (10 Users)
*   Hệ thống hoạt động hoàn hảo. Thời gian phản hồi tức thì (35ms).

#### Stress Testing (100 Users)
*   Độ trễ bắt đầu tăng đáng kể (~1.4s) do server phải xếp hàng xử lý (Request Queueing). Tuy nhiên, mọi request đều được phục vụ thành công.

#### Spike Testing (500 Users)
*   Khi có lượng truy cập đột biến đập vào trong 1s, hệ thống vẫn không sập. PHP Server process quản lý tốt việc xếp hàng, nhưng người dùng phải chờ trung bình ~6s.

#### Limit Testing (1000 - 2000 Users)
*   **Thử nghiệm cực hạn**: Hệ thống cho thấy độ ổn định ở mức đáng kinh ngạc về mặt Availability (Sẵn sàng). Tại 2000 users đồng thời, **tỷ lệ lỗi vẫn là 0%**.
*   **Vấn đề Latency**: Thời gian chờ tăng tuyến tính với số lượng user. Tại mức 2000 users, người dùng cuối cùng phải chờ tới **35 giây**.
*   **Kết luận Limit**: "Điểm gãy" của hệ thống này không phải là Server Crash (500 Internal Error) mà là **Client Timeout**. Mặc dù server vẫn trả lời sau 35s, nhưng hầu hết trình duyệt/ứng dụng client sẽ ngắt kết nối trước thời điểm đó (thường timeout mặc định là 30s).

## 5. Kết luận & Khuyến nghị (Recommendations)

1.  **Độ ổn định (Availability)**: Hệ thống OrangeHRM (trên cấu hình này) ưu tiên tính toàn vẹn và độ sẵn sàng hơn tốc độ. Nó không chủ động từ chối kết nối (dropload) mà cố gắng xử lý tất cả, dẫn đến độ trễ cao.
2.  **Khuyến nghị**:
    *   **Web Server Tuning**: Cấu hình Max Clients/Workers để giới hạn số lượng xử lý đồng thời, tránh để request xếp hàng quá lâu gây treo hệ thống.
    *   **Caching**: Sử dụng Redis/Memcached để cache các truy vấn database, giảm tải cho MySQL khi đọc dữ liệu.
    *   **Asynchronous Processing**: Với tác vụ ghi (Create Candidate), có thể đẩy vào Queue (RabbitMQ) để xử lý bất đồng bộ, trả về kết quả 202 Accepted ngay lập tức cho người dùng.
