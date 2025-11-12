# **Kịch Bản Video Demo DbFit (Thời lượng: 15-20 phút)**

**(Bắt đầu Video)**

---

## **Phần 1: Giới thiệu về DbFit (0:00 - 4:00)**

**Lồng tiếng:**

"Xin chào tất cả mọi người, chào mừng các bạn đã quay trở lại với seminar của chúng tôi. Trong video này, chúng ta sẽ cùng nhau tìm hiểu về DbFit - một công cụ mạnh trợ hỗ Test-Driven Development for Databases."

"Nói qua về DbFit:
- Cho phép chúng ta viết các test case cho stored procedure, function, và các câu lệnh SQL bằng một định dạng bảng rất dễ đọc, dễ hiểu
- Các developer, tester, hay BA (Business Analyst) có thể cùng nhau hợp tác để định nghĩa và kiểm thử các quy tắc nghiệp vụ của hệ thống."

`[VISUAL: Hiển thị trang chủ của DbFit hoặc một slide có logo DbFit và các gạch đầu dòng: "Test-Driven Development for DB", "Human-readable tests", "Collaboration between Dev, QA, BA"]`

"Để bắt đầu với DbFit, bạn chỉ cần tải file zip từ trang chủ của nó, giải nén và chạy một file script. DbFit được xây dựng trên nền tảng FitNesse, một framework kiểm thử tự động. Giao diện của nó hoàn toàn trên nền web."

`[VISUAL: Lướt qua thư mục đã giải nén của DbFit, chỉ vào file start.sh hoặc start.bat. Sau đó chuyển sang trình duyệt web đang mở giao diện DbFit.]`

"Đây là giao diện chính của DbFit. Trên thanh công cụ, chúng ta có các nút chức năng quan trọng như **Edit** để sửa nội dung trang, **Test** để chạy test, **Properties** để thay đổi thuộc tính trang, và **Add** để thêm các trang con."

`[VISUAL: Di chuột và chỉ vào các nút Edit, Test, Properties, Add trên giao diện DbFit.]`

"Trong DbFit, chúng ta có 3 loại trang chính:"
1.  "**Static Page**: Dùng để viết tài liệu, hướng dẫn, không có chức năng kiểm thử."
2.  "**Suite Page**: Là một bộ (suite) chứa các test case liên quan. Khi bạn chạy test ở trang Suite, tất cả các test case con bên trong sẽ được thực thi."
3.  "**Test Page**: Đây là nơi chúng ta viết các kịch bản kiểm thử cụ thể."

`[VISUAL: Tạo hoặc chỉ vào một cấu trúc cây thư mục mẫu trong DbFit, ví dụ: MyProject (Suite) -> Scenario1 (Suite) -> SuccessCase (Test).]`

---

## **Phần 2: Viết Test Case Đầu Tiên với DbFit (4:00 - 9:00)**

**Lồng tiếng:**

"Bây giờ, chúng ta sẽ đi vào phần thú vị nhất: viết một test case hoàn chỉnh. Trong demo này, tôi sử dụng một cơ sở dữ liệu PostgreSQL đơn giản cho hệ thống e-commerce, bao gồm các bảng `Users`, `Products`, `Orders` và `OrderItems`."

`[VISUAL: Hiển thị file db_schema_init.sql và lướt qua cấu trúc các bảng.]`

"Một test case trong DbFit thường tuân theo cấu trúc **Given-When-Then**:"
*   "**Given (Thiết lập)**: Chúng ta chuẩn bị dữ liệu ban đầu."
*   "**When (Hành động)**: Chúng ta thực thi đối tượng cần test (ví dụ: một function)."
*   "**Then (Kết quả)**: Chúng ta kiểm tra xem kết quả có đúng như mong đợi không."

"Hãy bắt đầu với kịch bản đầu tiên và cùng xem file test `scenario_1_success.md` mà chúng ta đã chuẩn bị."

`[VISUAL: Mở file scenario_1_success.md trong VS Code.]`

---
### Suite Page - SetUp - TearDown
#### 1. Suite Page

`[Scence 1 - Tạo Suite và Test Page: scence1.webm]`

"Để phục vụ cho việc demo, mình sẽ tạo một Suit Page tên là dbfit-demo và trong đó có một Test Page tên là Scenario 1: Complete Order - Success Case."

`[VISUAL: Tạo trang Suite và Test trong DbFit.]`

```
!1 Test suite ${PAGE_NAME}
!contents -R2 -g -p -f -h
```

"Đoạn mã trên sẽ tạo mục lục tự động cho trang suite của chúng ta."

`[VISUAL: Quay trở lại file scenario_1_success.md trong VS Code.]`

---
#### 2. SetUp
"Đầu tiên, chúng ta cần khai báo driver và kết nối tới database. Mình sẽ tạo một static page tên là DbFitSetup để chứa phần cấu hình này."

`[VISUAL: Chỉ vào các dòng sau trong file test]`
```
!path lib/*.jar
!|dbfit.PostgresTest|
!|Connect|localhost:5544|myuser|mypassword|mydatabase|
```
"Dòng `!path` chỉ định đường dẫn đến file JDBC driver. Tiếp theo, chúng ta dùng lệnh `Connect` để kết nối tới database PostgreSQL đang chạy trên Docker."

---
#### 3. TearDown
"Ở cuối mỗi test case, chúng ta nên ngắt kết nối với database để tránh rò rỉ tài nguyên. Điều này có thể được thực hiện bằng cách sử dụng lệnh `Close` trong phần TearDown của test suite hoặc test case."
```
!|Close|
```

#### 4. Test connection

"Mình sẽ test thử 1 câu lệnh query đơn giản để lấy dữ liệu từ bảng Products."

`[VISUAL: Chỉ vào lệnh Query trong file test]`

```
!|Query|SELECT productname, stockquantity FROM products ORDER BY productname|
|productname|stockquantity|
|Laptop Dell XPS|10|
|Mouse Logitech|50|
```

---

### Thực hiện Scenario 1: Success Case - Complete a pending order

`[Scence 2 - Viết Test Case Scenario 1: scence2.webm]`

#### 1. Given - Thiết lập trạng thái ban đầu


"**Bước 1: Given - Thiết lập trạng thái ban đầu.**"\
"Thay vì chèn dữ liệu thủ công bằng nhiều lệnh, DbFit cho phép chúng ta chạy một file SQL để setup toàn bộ dữ liệu. Đây là một cách làm rất hiệu quả và sạch sẽ."

`[VISUAL: Chỉ vào lệnh Execute File và các bảng Query kiểm tra dữ liệu ban đầu.]`
```
!|Execute File|sql_queries/scenario_1.sql|

!|Query|SELECT productname, stockquantity FROM products ...|
...
```
"Lệnh `Execute File` sẽ chạy file `scenario_1.sql` của chúng ta. File này chứa các hàm PL/pgSQL và script để tạo một đơn hàng đang ở trạng thái 'Pending'."

"**Bước 2: When - Thực thi hành động.**"
"Bây giờ, chúng ta sẽ gọi hàm chính `fn_complete_order` để xử lý đơn hàng này."

`[VISUAL: Chỉ vào lệnh Execute.]`
```
!|Execute|SELECT fn_complete_order(1)|
|fn_complete_order?|
|Order completed successfully|
```
"Lệnh `Execute` sẽ thực thi câu lệnh SELECT và chúng ta kiểm tra kết quả trả về của hàm. Dấu `?` ở cuối tên cột `fn_complete_order?` báo cho DbFit biết rằng đây là một giá trị cần kiểm tra (assertion)."

"**Bước 3: Then - Kiểm tra kết quả cuối cùng.**"
"Sau khi hàm được thực thi, chúng ta cần xác minh rằng dữ liệu trong database đã thay đổi đúng như mong đợi."

`[VISUAL: Chỉ vào các bảng Query kiểm tra dữ liệu cuối cùng.]`
```
!|Query|SELECT productname, stockquantity FROM products ...|
|productname|stockquantity?|
|Laptop Dell XPS|8|
|Mouse Logitech|47|

!|Query|SELECT orderid, status, totalamount FROM orders ...|
|orderid|status?|totalamount?|
|1|Completed|2475.00|
```
"Chúng ta dùng lệnh `Query` để kiểm tra lại số lượng tồn kho của sản phẩm đã bị trừ đi, và trạng thái của đơn hàng đã được cập nhật thành 'Completed' cùng với tổng số tiền."

---


## **Phần 3: Demo Thực Tế và Phân Tích Kết Quả (9:00 - 18:00)**

**Lồng tiếng:**

"Bây giờ, hãy chạy thử test case này trên giao diện DbFit."

`[VISUAL: Chuyển sang trình duyệt, vào trang test case của Scenario 1, nhấn nút "Test". Kết quả sẽ hiển thị màu xanh lá cây.]`

"Tuyệt vời! Toàn bộ test case đã chuyển sang màu xanh, nghĩa là mọi thứ đều đúng như kỳ vọng. DbFit đã thực hiện kết nối, chạy file SQL, thực thi hàm, và tất cả các kiểm tra của chúng ta đều khớp với kết quả thực tế."

"Tiếp theo, chúng ta sẽ thử nghiệm kịch bản thứ hai: **Không đủ hàng trong kho (Insufficient Stock)**."

`[VISUAL: Tạo một trang test mới trong DbFit tên là "InsufficientStock". Copy nội dung từ test success, nhưng sửa đổi file setup SQL hoặc dùng lệnh `Update` của DbFit để thay đổi số lượng tồn kho của 'Laptop Dell XPS' thành 1.]`

**Lồng tiếng:**
"Trong kịch bản này, khách hàng muốn mua 2 laptop nhưng trong kho chỉ còn 1. Chúng ta sẽ tạo một file SQL setup riêng hoặc dùng lệnh `Update` của DbFit để cập nhật số lượng tồn kho."

"Đây là test case cho kịch bản không đủ hàng:"
`[VISUAL: Hiển thị nội dung test case "Insufficient Stock".]`
1.  "**Given**: `Products` table có `StockQuantity` của Laptop là 1."
2.  "**When**: Vẫn gọi `fn_complete_order(1)`."
3.  "**Then**:
    *   Kết quả trả về của hàm phải là 'Insufficient stock...'.
    *   Bảng `Products` không thay đổi số lượng.
    *   Bảng `Orders` vẫn ở trạng thái 'Pending'."

`[VISUAL: Chạy test case "Insufficient Stock". Kết quả sẽ màu xanh. Giải thích tại sao nó pass.]`

"Như các bạn thấy, test case này cũng đã pass. Điều này xác nhận rằng logic xử lý của chúng ta đã ngăn chặn việc hoàn thành đơn hàng khi không đủ tồn kho, và dữ liệu được giữ nguyên."

"Nếu kết quả sai thì sao? Giả sử chúng ta kỳ vọng `TotalAmount` là 2475.00 nhưng thực tế nó là 0.00."

`[VISUAL: Sửa test case "Insufficient Stock", thay đổi expected `TotalAmount` thành 2475.00 và chạy lại. Kết quả sẽ có ô màu đỏ.]`

"DbFit sẽ báo lỗi ngay lập tức bằng cách tô đỏ ô chứa giá trị sai. Nó hiển thị rõ ràng: `expected [2475.00] but was [0.00]`. Đây chính là điểm mạnh của DbFit, giúp chúng ta xác định lỗi một cách cực kỳ nhanh chóng."

"Tương tự, chúng ta có thể dễ dàng tạo các test case cho **Scenario 2 (Querying and Formatting)**, nơi chúng ta dùng lệnh `Query` hoặc `Ordered Query` để kiểm tra kết quả trả về của một hàm SELECT có đúng định dạng và thứ tự hay không."

`[VISUAL: Lướt nhanh qua một test case đã chuẩn bị cho Scenario 2, tập trung vào việc so sánh kết quả của một bảng.]`

"Và với **Scenario 3 & 4 (Testing Constraints)**, chúng ta có thể viết các test case cố tình vi phạm các ràng buộc của database (như `CHECK` constraint hoặc `UNIQUE` constraint) và dùng lệnh `Execute` để kiểm tra xem nó có trả về đúng thông báo lỗi từ database hay không."

`[VISUAL: Lướt nhanh qua một test case cho Scenario 4, trong đó có một lệnh `Execute` cố gắng INSERT một giá trị âm vào `StockQuantity` và kiểm tra thông báo lỗi.]`

---

## **Phần 4: Tổng kết (18:00 - 20:00)**

**Lồng tiếng:**

"Qua các ví dụ vừa rồi, chúng ta có thể thấy DbFit là một công cụ rất trực quan và hiệu quả để kiểm thử cơ sở dữ liệu."

"Hãy cùng tổng kết lại những ưu điểm chính:"
*   "**Dễ đọc, dễ viết**: Các test case được viết dưới dạng bảng, rất gần với ngôn ngữ tự nhiên."
*   "**Tách biệt dữ liệu và logic**: Dữ liệu test được quản lý trong các file SQL hoặc ngay trong các bảng, giúp test case tập trung vào hành vi."
*   "**Tái sử dụng**: Dễ dàng tạo các bộ test (Suite) và chạy lại chúng một cách tự động, tích hợp vào quy trình CI/CD."
*   "**Hỗ trợ nhiều loại database**: DbFit hoạt động với hầu hết các hệ quản trị cơ sở dữ liệu phổ biến như SQL Server, Oracle, PostgreSQL, MySQL."

"Mặc dù có một chút đường cong học tập ban đầu về cú pháp, nhưng những lợi ích mà DbFit mang lại cho việc đảm bảo chất lượng của các logic nghiệp vụ trong database là rất lớn."

"Phần demo của tôi đến đây là kết thúc. Cảm ơn các bạn đã chú ý lắng nghe. Nếu có bất kỳ câu hỏi nào, đừng ngần ngại đặt câu hỏi trong phần thảo luận."

**(Kết thúc Video)**