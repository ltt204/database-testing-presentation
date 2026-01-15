# Requirement 4 - GUI testing report

## Mục lục

- [Requirement 4 - GUI testing report](#requirement-4---gui-testing-report)
  - [Mục lục](#mục-lục)
  - [Thông tin cá nhân \& nhóm](#thông-tin-cá-nhân--nhóm)
    - [Thông tin nhóm 11](#thông-tin-nhóm-11)
  - [1. Tổng quan GUI checklist](#1-tổng-quan-gui-checklist)
  - [2. Quy trình chung kiểm thử GUI](#2-quy-trình-chung-kiểm-thử-gui)
      - [Cách 1: Sử dụng BrowserStack/LambdaTest để kiểm thử trên nhiều trình duyệt và hệ điều hành khác nhau.](#cách-1-sử-dụng-browserstacklambdatest-để-kiểm-thử-trên-nhiều-trình-duyệt-và-hệ-điều-hành-khác-nhau)
      - [Cách 2: Kiểm thử thủ công trên các trình duyệt phổ biến](#cách-2-kiểm-thử-thủ-công-trên-các-trình-duyệt-phổ-biến)
  - [3. Các bug tìm thấy](#3-các-bug-tìm-thấy)
    - [3.1. GUI Recruitment list](#31-gui-recruitment-list)
    - [3.2. GUI Recruitment detail](#32-gui-recruitment-detail)
  - [4. Screenshots khác (success case)](#4-screenshots-khác-success-case)
    - [4.1. GUI Recruitment list](#41-gui-recruitment-list)
      - [Edge](#edge)
      - [Chrome](#chrome)
      - [Firefox](#firefox)


## Thông tin cá nhân & nhóm

- Họ tên: Phan Thanh Tiến
- MSSV: 22120368
- Nhóm 11.

### Thông tin nhóm 11

- Thông tin thành viên: 
  - Giang Đức Nhật - 22120252
  - Phan Thanh Tiến - 22120368
  - Nguyễn Bùi Vương Tiễn - 22120370
  - Lý Trọng Tín - 222120371

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

- Các tính năng được phân công là: 
  - Recruitment
  - Performance Management & Review

## 1. Tổng quan GUI checklist

Trong yêu cầu 4, ta tập trung kiểm thử GUI trên 2 giao diện. Ở đây, 2 màn hình được chọn để kiểm thử là: Màn hình danh sách ứng viên (hay candidate) và màn hình chi tiết ứng viên trong module Recruitment. 

Kết quả kiểm thử cuối cùng vui lòng kiểm tra file excel đính kèm báo cáo này.

Checklist GUI cơ bản sẽ được sử dụng trong các bộ test như sau:

| No.      | Checkpoints                                                                                                                                                       |
| -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1        | GIAO DIỆN NGƯỜI DÙNG                                                                                                                                              |
| 1.1      | LIÊN KẾT                                                                                                                                                          |
| 1.1.1    | Kiểm tra xem liên kết có đưa bạn đến trang mà nó đã nói không?                                                                                                    |
| 1.1.2    | Đảm bảo không có trang mồ côi (trang không có liên kết đến trang đó)                                                                                              |
| 1.1.3    | Đảm bảo không có trang Dead-End (trang không có chứa liên kết đến trang web khác)                                                                                 |
| 1.2      | MÀU SẮC                                                                                                                                                           |
| 1.2.1    | Màu nền của website là màu tối ?                                                                                                                                  |
| 1.2.2    | Màu nền của website có làm rối người dùng không?                                                                                                                  |
| 1.2.3    | Màu giữa các phần trong website có sự khác biệt rõ ràng và đồng nhất ?                                                                                            |
| 1.2.4    | Màu chữ phần nội dung bình thường đồng nhất hay không?                                                                                                            |
| 1.2.5    | Màu chữ phần nội dung in đậm, in nghiêng, liên kết khác nhau và nổi bật so với màu của phần nội dung bình thường ?                                                |
| 1.2.6    | Màu chữ khi visit vào liên kết có đổi màu hay không ? (Link: cuối trang)                                                                                          |
| 1.2.7    | Màu chữ khi hover vào phần nội dung liên kết có đổi màu ?                                                                                                         |
| 1.2.8    | Màu chữ khi nhập liệu trong textbox có đồng nhất hay không ?                                                                                                      |
| 1.2.9    | Màu nền của các nhóm button đồng nhất với nhau hay không?                                                                                                         |
| 1.2.10   | Màu chữ phần nội dung trên button có đồng nhất hay không?                                                                                                         |
| 1.2.11   | Màu các vùng nhập liệu disable có đồng nhất và khác với các vùng nhập liệu khác hay không?                                                                        |
| 1.3      | NỘI DUNG                                                                                                                                                          |
| 1.3.1    | Font sử dụng trong website có nhất quán theo từng thành phần (button, textbox, nội dung, tiêu đề, liên kết…) không?                                               |
| 1.3.2    | Kích thước font chữ phần nội dung đúng theo chuẩn cơ bản không?                                                                                                   |
| 1.3.3    | Kích thước font chữ phần button và textbox hiển thị hợp lý hay không?                                                                                             |
| 1.3.4    | Kích thước font tiêu đề có làm nổi bật hơn so với phần nội dung không?                                                                                            |
| 1.3.5    | Logo website có để góc trên trái ?                                                                                                                                |
| 1.3.6    | Tất cả nội dung chữ có được canh lề đúng không?                                                                                                                   |
| 1.3.7    | Tất cả các tiêu đề đều được canh lề đúng không?                                                                                                                   |
| 1.3.8    | Website có bố cục rõ ràng, hợp lý ?                                                                                                                               |
| 1.3.9    | Mỗi trang web có tiêu đề rõ ràng không?                                                                                                                           |
| 1.3.10   | Phần tìm kiếm được hiển thị nổi bật và rõ ràng? (Ghi chú: phần search hiện ở filter -> Dễ nhầm lẫn)                                                               |
| 1.3.11   | Phần thông tin, địa chỉ công ty được cung cấp đầy đủ trong website?                                                                                               |
| 1.3.14   | Chính sách bảo mật có được xác định rõ ràng và có sẵn để người dùng truy cập không?                                                                               |
| 1.3.17   | Tất cả nội dung thông báo lỗi có được viết đúng chính tả trên màn hình này không?                                                                                 |
| 1.3.18   | Tất cả nội dung trợ giúp (tooltip) có được viết đúng chính tả trên màn hình này không?                                                                            |
| 1.3.19   | Nội dung trợ giúp (tooltip) cho mọi trường nhập liệu & button có được bật không?                                                                                  |
| 1.4      | FORM                                                                                                                                                              |
| 1.4.1    | HÌNH THỨC                                                                                                                                                         |
| 1.4.1.1  | Đảm bảo có thông báo cho biết các trường nhập liệu bắt buộc và tuỳ chọn                                                                                           |
| 1.4.1.2  | Kiểm tra có hiển thị hướng dẫn nhập liệu (điều kiện ràng buộc) cho các trường nhập liệu phức tạp                                                                  |
| 1.4.1.3  | Kiểm tra có hiển thị giá trị mặc định cho các trường nhập liệu khi tải / tải lại trang (Cũng phải tắt các điều khoản và điều kiện)                                |
| 1.4.1.4  | Kiểm tra tất cả các phần của một bảng (table) hoặc biểu mẫu (form) hiển thị đúng không? Bạn có thể xác nhận rằng các nội dung đã chọn nằm trong "đúng chỗ không?" |
| 1.4.1.5  | Chỉ được chọn 1 trong 1 nhóm radio button (Không có radio button)                                                                                                 |
| 1.4.1.6  | Người dùng có thể chọn một hoặc nhiều checkbox                                                                                                                    |
| 1.4.1.7  | Nội dung trong danh sách combo box hoặc list box được sắp xếp theo thứ tự hợp lý (alphabetical)                                                                   |
| 1.4.2    | KIỂM TRA TRƯỜNG DỮ LIỆU SỐ                                                                                                                                        |
| 1.4.2.1  | Có cho phép nhập kí tự chữ hay không? (Không có trường dữ liệu số)                                                                                                |
| 1.4.2.2  | Có cho phép nhập kí tự đặc biệt hay không?                                                                                                                        |
| 1.4.2.3  | Cho phép null hay không?                                                                                                                                          |
| 1.4.2.4  | Có xử lý phép chia cho 0 hay không? (Không có thực hiện tính toán)                                                                                                |
| 1.4.3    | KIỂM TRA TRƯỜNG DỮ LIỆU CHỮ SỐ                                                                                                                                    |
| 1.4.3.1  | Có phân biệt hoa, thường hay không?                                                                                                                               |
| 1.4.3.2  | Cho phép null hay không?                                                                                                                                          |
| 1.4.3.3  | Có kiểm tra độ dài tối đa hay không?                                                                                                                              |
| 1.4.3.4  | Có giới hạn độ dài chuỗi nhập hay không?                                                                                                                          |
| 1.4.3.5  | Có cho phép nhập kí tự đặc biệt hay không?                                                                                                                        |
| 1.4.3.6  | Có cho phép nhập khoảng trắng ở đầu ký tự không?                                                                                                                  |
| 1.4.3.7  | Có cho phép nhập khoảng trắng ở cuối ký tự không?                                                                                                                 |
| 1.4.3.8  | Khi nhập ô email có kiểm tra format của email hay không? (Không có ô email)                                                                                       |
| 1.4.3.9  | Có cho nhập chữ vào số điện thoại hay không? (Không có ô SĐT)                                                                                                     |
| 1.4.3.10 | Khi nhập vào ô password có ẩn thông tin hay không? (Không có ô password)                                                                                          |
| 2        | TÍNH ĐIỀU HƯỚNG (NAVIGATION)                                                                                                                                      |
| 2.1.1    | Có một liên kết đến trang chủ trên mỗi trang không?                                                                                                               |
| 2.1.2    | Người dùng có biết được mình đang ở đâu trong website không?                                                                                                      |
| 2.1.3    | Tất cả các trang web/cửa sổ điều có thể truy cập từ menu?                                                                                                         |
| 2.1.4    | Chức năng tìm kiếm có được đặt ở đúng vị trí không?                                                                                                               |
| 2.1.5    | Thanh cuộn có xuất hiện nếu được yêu cầu không?                                                                                                                   |
| 2.1.6    | Kiểm tra tất cả các field read-only đều không có thứ tự tab hay không?                                                                                            |
| 3        | TÍNH TƯƠNG THÍCH                                                                                                                                                  |
| 3.1      | TƯƠNG THÍCH TRÌNH DUYỆT                                                                                                                                           |
| 3.1.1    | Phiên bản HTML được sử dụng có tương thích với các phiên bản trình duyệt thích hợp không?                                                                         |
| 3.1.2    | Hình ảnh có hiển thị chính xác với các trình duyệt đang được kiểm tra không?                                                                                      |
| 3.1.3    | Xác minh phông chữ có thể sử dụng được trên bất kỳ trình duyệt nào                                                                                                |
| 3.1.4    | Mã JavaScript có thể sử dụng được bởi các trình duyệt đang được thử nghiệm không?                                                                                 |
| 3.1.5    | Vị trí, kích thuế của các thành phần trong trang web có hiển thị đúng với các trình duyệt đang được kiểm tra không?                                               |
| 3.2      | TƯƠNG THÍCH THIẾT BỊ                                                                                                                                              |
| 3.2.1    | Độ phân giải màn hình (kiểm tra văn bản và liên kết đồ họa vẫn hoạt động, phông chữ có thể đọc được, v.v.) như 1024 x 768, 600x800, 640 x 480 pixel               |
| 3.2.2    | Độ sâu màu (256, 16-bit, 32-bit)                                                                                                                                  |
| 3.3      | TƯƠNG THÍCH MÁY IN                                                                                                                                                |
| 3.3.1    | Căn chỉnh văn bản và hình ảnh                                                                                                                                     |
| 3.3.2    | Màu sắc của văn bản, hình ảnh và nền                                                                                                                              |
| 3.3.3    | Khả năng mở rộng phù hợp với khổ giấy (Phần menu được tinh chỉnh tùy khổ giấy)                                                                                    |
| 3.3.4    | Bảng và đường viền                                                                                                                                                |
| 3.3.5    | Các trang có in rõ ràng không cắt bỏ nội dung không?                                                                                                              |


## 2. Quy trình chung kiểm thử GUI

Trong quá trình kiểm thử thực tế, tại một vị trí màn hình, ta có thể kiểm tra nhiều mục trong checklist, do đó số lượng ảnh chụp màn hình sẽ không nhiều như số lượng checklist. 

Các screenshots trong báo cáo này sẽ tập trung vào quy trình chung, cũng như các bug reports nếu có.

Để thực hiện kiểm thử, có 2 cách chính như sau: 

#### Cách 1: Sử dụng BrowserStack/LambdaTest để kiểm thử trên nhiều trình duyệt và hệ điều hành khác nhau. 

- Các công cụ này thuận lợi trong việc kiểm thử hơn do có hỗ trợ tốt về bộ công cụ cũng như môi trường kiểm thử. Tuy nhiên, các công này là công cụ trả phí (phí khá cao, gói miễn phí ngắt session sau 1 phút -> Không dùng được), do đó em KHÔNG sử dụng công cụ này trong quá trình kiểm thử thực tế.
- Làm thử trên công cụ LambdaTest:  
  - Đầu tiên, khởi tạo môi trường test. LambdaTest hỗ trợ nhiều môi trường hệ điều hành (1), trình duyệt (2), phiên bản trình duyệt (3) và độ phân giải (4) khác nhau phù hợp cho nhiều mục đích kiểm thử.
    ![alt text](image.png)
  - Sau khi trình duyệt ảo được khởi tạo, ta sẽ thấy giao diện như sau:
    ![alt text](lambda_test.png)
    - Trong đó: Mục (1) là thanh công cụ hỗ trợ, bao gồm: Chụp ảnh màn hình, quay video, giả lập cảm ứng, kiểm tra mạng, v.v...
    - Mục (2) là giao diện trình duyệt ảo, ta sẽ thao tác trên đây để kiểm thử GUI.
  - Sau khi khởi tạo, tiền hành kiểm tra theo checklist
- Tuy nhiên:
  - Do công cụ này và cả BrowserStack là trả phí, với free tier rất hạn chế (bị ngắt sau 1-2 phút/phiên), nên khó để sử dụng trong toàn bộ yêu cầu này. Do đó, ta đi đến cách 2.

#### Cách 2: Kiểm thử thủ công trên các trình duyệt phổ biến

- Trong cách này, ta sẽ sử dụng các trình duyệt phổ biến hiện nay như: Chrome, Firefox, Edge, Safari (nếu có máy Mac) để kiểm thử thủ công.
- Quy trình kiểm thử thủ công là:
  - Mở trình duyệt
  - Truy cập vào ứng dụng web
  - Điều khiển bằng tay và kiểm tra theo checklist.

## 3. Các bug tìm thấy

### 3.1. GUI Recruitment list

**1.2.6. Màu chữ khi visit vào liên kết có đổi màu hay không ?**

- Kết quả mong đợi: Màu chữ của liên kết khi visit sẽ đổi màu
- Kết quả thực tế: Màu chữ của liên kết khi visit không đổi màu

- Edge screenshot:
![alt text](link.png)
- Firefox screenshot:
![alt text](image-4.png)
- Chrome screenshot:
![alt text](image-17.png)

**1.2.7. Màu chữ khi hover vào phần nội dung liên kết có đổi màu ?**

- Kết quả mong đợi: Màu chữ của liên kết khi hover sẽ đổi màu
- Kết quả thực tế: Màu chữ của liên kết khi hover không đổi màu

- Edge screenshot:
![alt text](image-1.png)
- Firefox screenshot:
![alt text](image-5.png)
- Chrome screenshot:
![alt text](image-17.png)

**1.4.3.3. Có kiểm tra độ dài tối đa hay không?**
- Kết quả mong đợi: Khi nhập vượt quá độ dài tối đa, hệ thống sẽ hiển thị thông báo lỗi.
- Kết quả thực tế: Khi nhập vượt quá độ dài tối đa, hệ thống không hiển thị thông báo lỗi.

**1.4.3.4. Có giới hạn độ dài chuỗi nhập hay không?**
- Kết quả mong đợi: Hệ thống sẽ giới hạn độ dài chuỗi nhập
- Kết quả thực tế: Hệ thống không giới hạn độ dài chuỗi nhập

- Edge:
![alt text](image-3.png)
- Firefox:
![alt text](image-18.png)
- Chrome:
![alt text](image-19.png)

Chuỗi đã nhập (539 ký tự): "sadsadsadassadsadsadassadsadsadassadsadsadassadsadsadassadsadsadassadsadsadassadsadsadassadsadsadassadsadsadassadsadsadassadsadsadassadsadsadassadsadsadassadsadsadassadsadsadassadsadsadassadsadsadassadsadsadassadsadsadassadsadsadassadsadsadassadsadsadassadsadsadassadsadsadassadsadsadassadsadsadassadsadsadassadsadsadassadsadsadassadsadsadassadsadsadassadsadsadassadsadsadassadsadsadassadsadsadassadsadsadassadsadsadassadsadsadassadsadsadassadsadsadassadsadsadassadsadsadassadsadsadassadsadsadassadsadsadassadsadsadassadsadsadassadsadsadas" 

Việc không giới hạn độ dài chuỗi và không kiểm tra có thể gây nguy hiểm trong việc bị tấn công buffer overflow -> Xem đây là bug.


### 3.2. GUI Recruitment detail

**1.2.6. Màu chữ khi visit vào liên kết có đổi màu hay không ?**

- Kết quả mong đợi: Màu chữ của liên kết khi visit sẽ đổi màu
- Kết quả thực tế: Màu chữ của liên kết khi visit không đổi màu

- Edge screenshot:
![alt text](image-7.png)
- Firefox screenshot:
![alt text](image-6.png)

**1.2.7. Màu chữ khi hover vào phần nội dung liên kết có đổi màu ?**

- Kết quả mong đợi: Màu chữ của liên kết khi hover sẽ đổi màu
- Kết quả thực tế: Màu chữ của liên kết khi hover không đổi màu

- Edge screenshot:
![alt text](image-7.png)
- Firefox screenshot:
![alt text](image-6.png)
- Chrome screenshot:
![alt text](image-7.png)

**1.4.1.1. Đảm bảo có thông báo cho biết các trường nhập liệu bắt buộc và tuỳ chọn**

- Kết quả mong đợi: Các trường bắt buộc sẽ có dấu * và được bôi đỏ để làm nổi bật
- Kết quả thực tế: Có dấu sao nhưng đồng màu chữ, không rõ ràng là field required.
- Edge screenshot:
  ![alt text](image-9.png)
- Firefox screenshot:
  ![alt text](image-8.png)
- Chrome screenshot:
  ![alt text](image-16.png)

**1.4.2.2. Có cho phép nhập kí tự đặc biệt hay không?**

- Kết quả mong đợi: Không cho phép nhập ký tự đặc biệt trong trường tên.
- Kết quả thực tế: Cho phép nhập ký tự đặc biệt trong trường tên.
- Edge screenshot:
  ![alt text](image-10.png)
- Firefox screenshot:
  ![alt text](image-12.png)
- Chrome screenshot:
  ![alt text](image-13.png)

**1.4.3.8. Khi nhập ô email có kiểm tra format của email hay không?**

- Kết quả mong đợi: Kiểm tra định dạng email khi nhập.
- Kết quả thực tế: Không kiểm tra định dạng email khi nhập.
- Edge screenshot:
  ![alt text](image-11.png)
- Firefox screenshot:
  ![alt text](image-15.png)
- Chrome screenshot:
  ![alt text](image-14.png)

## 4. Screenshots khác (success case)

### 4.1. GUI Recruitment list

#### Edge 

- Màu sắc của chữ, button, nội dung đồng nhất trên các thành phần. Bố cục hợp lí.
  ![alt text](image-2.png)

- Tương thích thiết bị: (3 màn hình: 1024x768, 600x800, 640x480)
  ![3.2.1.1](3.2.1.1.png)
  ![3.2.1.2](3.2.1.2.png)
  ![3.2.1.3](3.2.1.3.png)

- Tương thích máy in: Nhận thấy các phần như căn chỉnh văn bản, màu sắc, bảng và đường viền đều in rõ ràng, không bị cắt bỏ nội dung, có thể thấy rằng trang được điều chỉnh theo máy in.
  ![3.3.3.1](3.3.3.1.png)
  ![3.3.3.2](3.3.3.2.png)

#### Chrome

- Màu sắc của chữ, button, nội dung đồng nhất trên các thành phần. Bố cục hợp lí.
  ![alt text](image-25.png)

- Tương thích thiết bị: (3 màn hình: 1024x768, 600x800, 640x480)
  ![alt text](image-26.png)
  ![alt text](image-27.png)
  ![3.2.1.3](3.2.1.3.png)

- Tương thích máy in: Nhận thấy các phần như căn chỉnh văn bản, màu sắc, bảng và đường viền đều in rõ ràng, không bị cắt bỏ nội dung, có thể thấy rằng trang được điều chỉnh theo máy in.
  ![alt text](image-29.png)
  ![alt text](image-28.png)

#### Firefox

- Màu sắc của chữ, button, nội dung đồng nhất trên các thành phần. Bố cục hợp lí.
  ![alt text](image-2.png)

- Tương thích thiết bị: (3 màn hình: 1024x768, 600x800, 640x480)
  ![alt text](image-20.png)
  ![alt text](image-21.png)
  ![alt text](image-22.png)

- Tương thích máy in: Nhận thấy các phần như căn chỉnh văn bản, màu sắc, bảng và đường viền đều in rõ ràng, không bị cắt bỏ nội dung, có thể thấy rằng trang được điều chỉnh theo máy in.
  ![alt text](image-23.png)
  ![alt text](image-24.png)

