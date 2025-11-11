---
_class: lead
paginate: true
size: 16:9
marp: true
theme: am_blue
footer: 22120252 - 22120368 - 22120370 - 22120371 / Database Testing
---

<!-- _class: cover_ -->
<!-- _paginate: "" -->

<style>
/* Force black for the H1 on the first slide only */
.remark-slide:first-of-type .remark-slide-content h1,
section:first-of-type h1 {
  color: #000 !important;
  -webkit-text-fill-color: #000 !important;
  fill: #000 !important;
  -webkit-text-stroke: 0 !important;
  text-shadow: none !important;
}
</style>

<h1>Database Testing</h1>

#### Nov 13, 2025

Speakers:

- 22120252 - Giang Đức Nhật
- 22120368 - Phan Thanh Tiến
- 22120370 - Nguyễn Bùi Vương Tiễn
- 22120371 - Lý Trọng Tín

---

<!-- _class: toc_a -->
<!-- _footer: "" -->
<!-- _paginate: "" -->

## Table of contents

- [Tổng quan về Database Testing](#tổng-quan)
- [Các loại Kiểm thử Cơ sở dữ liệu](#Các-loại-kiểm-thử)
- [Quy trình Kiểm thử CSDL](#quy-trình-kiểm-thử)
- [Kỹ thuật Kiểm thử CSDL](#kỹ-thuật-kiểm-thử-csdl)
- [Thách thức trong Kiểm thử CSDL](#thách-thức-trong-kiểm-thử-csdl)
- [Công cụ Kiểm thử CSDL](#công-cụ-kiểm-thử)

---

<!-- _class: trans -->
<!-- _paginate: "" -->

# Tổng quan

---

<!-- _class: navbar -->
<!-- _header: \ ***FIT@HCMUS*** **Tổng quan** *Loại kiểm thử* *Quy trình* *Thách thức* *Công cụ* *Kết luận* -->

## Giới thiệu về Kiểm thử Cơ sở dữ liệu

- **Cơ sở dữ liệu (CSDL)**

  - Là một tập hợp dữ liệu có cấu trúc được lưu trữ và quản lý bởi Hệ quản trị cơ sở dữ liệu (DBMS).
  - Ví dụ: MySQL, PostgreSQL, SQL Server, Oracle.

- **Kiểm thử CSDL**
  - Là quá trình verify và validate chất lượng, chức năng, hiệu suất và bảo mật của CSDL.
  - Đảm bảo việc lưu trữ, truy xuất và quản lý dữ liệu hoạt động chính xác, hiệu quả và an toàn.

<!-- Notes:
- What the fuck is "chat luong"
-
 -->

---

<!-- _class: navbar -->
<!-- _header: \ ***FIT@HCMUS*** **Tổng quan** *Loại kiểm thử* *Quy trình* *Thách thức* *Công cụ* *Kết luận* -->

## Mục đích

- **Database Testing** là quá trình verify và validate chất lượng, chức năng, hiệu suất và bảo mật của hệ thống CSDL.
- **So với UI Testing:**
  - UI Testing tập trung vào những gì người dùng thấy (giao diện, bố cục, tương tác).
  - Database Testing tập trung vào dữ liệu (logic xử lí, tính toán), đảm bảo dữ liệu chính xác, toàn vẹn, an toàn.
- **Vai trò trong quy trình phát triển:**
  - Đảm bảo tính toàn vẹn và chính xác của dữ liệu.
  - Ngăn chặn mất mát hoặc hỏng hóc dữ liệu.
  - Tối ưu hiệu suất và khả năng mở rộng thông qua benchmark/profiling.
  - Tăng cường bảo mật qua việc phát hiện lỗ hổng.

---

<!-- _class: cols-2 navbar -->
<!-- _header: \ ***FIT@HCMUS*** **Tổng quan** *Loại kiểm thử* *Quy trình* *Thách thức* *Công cụ* *Kết luận* -->

## Mục tiêu chính của Database Testing

<div class=ldiv>

- **Toàn vẹn & Ánh xạ Dữ liệu:**

  - **Data Integrity:** Xác thực (Verify) tính chính xác, tính nhất quán của dữ liệu qua các ràng buộc (khóa, check, not null) trong DDL.
  - **Data Mapping:** Đảm bảo luồng dữ liệu từ UI → API → DB được ánh xạ chính xác, không sai lệch.

- **Quy tắc Nghiệp vụ:**
  - Xác minh logic trong **Stored Procedures, Triggers** và các hàm có hoạt động đúng theo yêu cầu nghiệp vụ hay không.

</div>

<div class=rdiv>

- **Đảm bảo thuộc tính ACID:**
  - **Atomicity:** Một giao dịch phải được thực hiện hoàn toàn hoặc không gì cả (all or nothing).
  - **Consistency:** Dữ liệu phải luôn ở trạng thái hợp lệ sau mỗi giao dịch.
  - **Isolation:** Các giao dịch đồng thời không ảnh hưởng lẫn nhau.
  - **Durability:** Dữ liệu đã commit phải được lưu trữ bền vững.

</div>

---

<!-- _class: trans -->
<!-- _paginate: "" -->

# Các loại kiểm thử

---

<!-- _class: navbar -->
<!-- _header: \ ***FIT@HCMUS*** *Tổng quan* **Loại kiểm thử** *Quy trình* *Thách thức* *Công cụ* *Kết luận* -->

## Các loại Kiểm thử Cơ sở dữ liệu

- **Structural Testing:** Tập trung vào việc xác thực các thành phần cấu trúc của CSDL đảm bảo đúng thiết kế. Bao gồm schema, tables, columns, keys, indexes, stored procedures và triggers.
- **Functional Testing:** Kiểm tra các chức năng của CSDL từ góc độ người dùng cuối. Bao gồm: các thao tác CRUD, logic nghiệp vụ, ràng buộc dữ liệu, xử lí lỗi (error handling)/
- **Non-functional Testing:** Đánh giá các khía cạnh như hiệu suất, bảo mật và khả năng sử dụng của CSDL.

---

<!-- _class: cols-2 navbar -->
<!-- _header: \ ***FIT@HCMUS*** *Tổng quan* **Loại kiểm thử** *Quy trình* *Thách thức* *Công cụ* *Kết luận* -->

## Kiểm thử Cấu trúc (Structural)

<div class=ldiv>

- **Kiểm thử Schema & Consistency:**

  - Xác thực **Schema** (bảng, cột, kiểu dữ liệu) khớp với đặc tả.
  - Kiểm tra **Schema Consistency** giữa các môi trường (DEV, TEST, PROD).
  - Đảm bảo không có đối tượng DB thừa/thiếu.

- **Kiểm thử Stored Procedure:**

  - Xác minh logic nghiệp vụ, xử lý lỗi.
  - Kiểm tra kết quả trả về với các bộ dữ liệu đầu vào khác nhau (White-box).

</div>
<div class=rdiv>

- **Kiểm thử Keys & Indexes:**

  - **Khóa (Keys):** Xác thực khóa chính/ngoại (tính duy nhất, not-null, toàn vẹn tham chiếu).
  - **Chỉ mục (Indexes):** Đảm bảo index được tạo đúng, sử dụng hiệu quả và không thừa.

- **Kiểm thử Trigger:**
  - Đảm bảo trigger được kích hoạt đúng sự kiện (`INSERT`, `UPDATE`, `DELETE`).
  - Xác thực logic thực thi có đúng và không gây side-effect.

</div>

---

<!-- _class: navbar -->
<!-- _header: \ ***FIT@HCMUS*** *Tổng quan* **Loại kiểm thử** *Quy trình* *Thách thức* *Công cụ* *Kết luận* -->

## Kiểm thử Chức năng (Functional)

#### Black Box Testing

- Tập trung vào verify chức năng từ góc độ người dùng cuối, không cần biết logic bên trong.
- Được thực hiện bởi **testers**.
- Mục tiêu:
  - **Kiểm thử các thao tác CRUD:** Xác minh các thao tác `CREATE`, `READ`, `UPDATE`, `DELETE` từ giao diện/API được phản ánh chính xác trong CSDL.
  - **Kiểm tra giá trị mặc định/ràng buộc:** Đảm bảo dữ liệu nhập vào tuân thủ đúng các ràng buộc (constraints: kiểu, giới hạn, not null...)
  - **Kiểm tra xử lí lỗi:** Đảm bảo CSDL xử lí đúng các tình huống lỗi (ví dụ: vi phạm ràng buộc, dữ liệu không hợp lệ).

---

<!-- _class: navbar -->
<!-- _header: \ ***FIT@HCMUS*** *Tổng quan* **Loại kiểm thử** *Quy trình* *Thách thức* *Công cụ* *Kết luận* -->

## Kiểm thử Chức năng (Functional)

#### White Box Testing

- Tập trung vào validate logic bên trong các đối tượng CSDL.
- Được thực hiện bởi **developers**.
- Mục tiêu:
  - **Validate logic nghiệp vụ:** Kiểm tra các trigger, stored procedure, và view đảm bảo chúng thực thi đúng yêu cầu.
  - **Kiểm tra toàn vẹn dữ liệu:** Đảm bảo các ràng buộc (constraints) và quan hệ (relationships) hoạt động chính xác.

---

<!-- _class: cols-2 navbar -->
<!-- _header: \ ***FIT@HCMUS*** *Tổng quan* **Loại kiểm thử** *Quy trình* *Thách thức* *Công cụ* *Kết luận* -->

## Kiểm thử Phi chức năng (Non-functional)

<div class=ldiv>

- **Hiệu năng (Performance):**

  - **Load test:** Đánh giá hiệu suất CSDL dưới tải trọng dự kiến, đo thời gian phản hồi truy vấn.
  - **Stress test:** Xác định điểm gãy (breaking point) của CSDL bằng cách tạo tải ảo rất lớn vào CSDL.

- **Bảo mật (Security):**
  - Ngăn chặn các lỗ hổng phổ biến như **SQL Injection**.
  - Xác thực quyền truy cập, đảm bảo người dùng chỉ thấy dữ liệu được phép.

</div>
<div class=rdiv>

- **Khả năng Phục hồi (Recovery):**

  - Xác minh việc sao lưu (backup) và phục hồi (restore) dữ liệu hoạt động đúng.
  - Xác minh CSDL có thể được phục hồi thành công từ các bản sao lưu (backups) sau sự cố.

- **Tương thích (Compatibility):**
  - Đảm bảo CSDL hoạt động ổn định trên các phiên bản DBMS, hệ điều hành, và nền tảng được dùng để triển khai.

</div>

---

<!-- _class: bq-red -->

> Bảo mật CSDL cần ưu tiên:
> *Đảm bảo kiểm soát truy cập chặt chẽ.
> *Tránh các lỗi bảo mật cơ bản như SQL Injection
> \*Mã hóa dữ liệu nhạy cảm ở trạng thái nghỉ và khi truyền tải.

<!-- Speaker notes:
em cần giải thích ỏ đây ạ, trạng thái nghỉ là cái éo gì  -->

---

<!-- _class: trans -->
<!-- _paginate: "" -->

# Quy trình kiểm thử

---

## Quy trình Kiểm thử CSDL

<!-- _class: cols-2 navbar -->
<!-- _header: \ ***FIT@HCMUS*** *Tổng quan* *Loại kiểm thử* **Quy trình** *Thách thức* *Công cụ* *Kết luận* -->

<div class=ldiv>

1.  **Phân tích & Thiết kế Test cases**

    - Xác định yêu cầu nghiệp vụ, phạm vi kiểm thử.
    - Thiết kế test case, kịch bản và bộ dữ liệu.

2.  **Chuẩn bị Môi trường & Dữ liệu**

    - Thiết lập môi trường test riêng biệt, đảm bảo cô lập giữa các bộ test.
    - Tạo bộ dữ liệu thử nghiệm (Test Data).

3.  **Thực thi**
    - Chạy các kịch bản kiểm thử. _(auto/manual)_
    - Ghi lại kết quả và các lỗi phát sinh.

</div>

<div class=rdiv>

4.  **Báo cáo**

    - Phân tích kết quả, so sánh với kết quả mong đợi.
    - Ghi nhận lỗi (log bug) và báo cáo cho đội phát triển.

5.  **Kiểm thử Hồi quy và Hoàn tất**
    - Thực hiện lại các bài kiểm thử sau khi lỗi được sửa.
    - Hoàn tất báo cáo.
    - Đóng test cycle.

</div>

---

<!-- _class: trans -->
<!-- _paginate: "" -->

# Thách thức

---

## Thách thức trong Kiểm thử CSDL

<!-- _class: cols2_ul_ci fglass smalltext navbar-->
<!-- _header: \ ***FIT@HCMUS*** *Tổng quan* *Loại kiểm thử* *Quy trình* **Thách thức** *Công cụ* *Kết luận* -->

- **Dữ liệu lớn và phức tạp:** Việc kiểm thử với khối lượng dữ liệu lớn có thể rất khó khăn và tốn thời gian.
- **Quản lý dữ liệu thử nghiệm:** Tạo và quản lý dữ liệu thử nghiệm phù hợp là rất quan trọng nhưng cũng đầy thách thức.
- **Kiến thức về SQL:** Người kiểm thử cần có hiểu biết tốt về SQL và các khái niệm CSDL.
- **Cô lập môi trường thử nghiệm:** Đảm bảo môi trường thử nghiệm được tách biệt hoàn toàn với môi trường sản phẩm.
- **Chi phí và Thời gian:** Kiểm thử CSDL có thể tốn kém và mất nhiều thời gian, đặc biệt với các hệ thống lớn.

---

<!-- _class: trans -->
<!-- _paginate: "" -->

# Công cụ kiểm thử

---

<!-- _class: bq-yellow navbar -->
<!-- _header: \ ***FIT@HCMUS*** *Tổng quan* *Loại kiểm thử* *Quy trình* *Thách thức* **Công cụ** *Kết luận* -->

> ###### - Chọn công cụ phù hợp với mục đích kiểm thử. Không có một công cụ nào có thể phù hợp với tất cả nhu cầu kiểm thử.
>
> ###### - Để kiểm thử một cách toàn diện, cần kết hợp nhiều công cụ khác nhau.

---

<!-- _class: navbar -->
<!-- _header: \ ***FIT@HCMUS*** *Tổng quan* *Loại kiểm thử* *Quy trình* *Thách thức* **Công cụ** *Kết luận* -->

## Phân loại công cụ

Để chọn đúng công cụ, chúng ta cần xem xét chúng qua các khía cạnh sau:

- **Kiểm thử cái gì?** Hiệu năng, chức năng, bảo mật... Phạm vi kiểm thử?
- **Phương pháp tiếp cận?** Black-box hay White-box?
- **Tự động hóa và Khả năng tích hợp?** Khả năng tích hợp vào CI/CD và quản lý dữ liệu test.
- **Tính tương thích?** Hỗ trợ những hệ quản trị CSDL nào? SQL hay NoSQL?
- **Thiết kế và Chức năng?** Giao diện, tính dễ sử dụng, phù hợp với đối tượng nào (dev hay tester chẳng hạn).

---

<!-- _class: cols-2 navbar -->
<!-- _header: \ ***FIT@HCMUS*** *Tổng quan* *Loại kiểm thử* *Quy trình* *Thách thức* **Công cụ** *Kết luận* -->

## I. Phạm vi & Loại hình Kiểm thử

<div class=ldiv>

- **Kiểm thử Hiệu năng (Performance):**

  - Mô phỏng tải lớn, đo lường thời gian phản hồi và tìm breaking point.
  - Công cụ: JMeter, HammerDB, Swingbench.

- **Kiểm thử Chức năng/Unit Test:**

  - Xác minh logic nghiệp vụ và thao tác CRUD.
  - Công cụ: tSQLt (Unit Test), DbFit (Acceptance Test).

- **Kiểm thử Cấu trúc (Structural):**

  - So sánh và xác thực schema, bảng, cột, khóa...
  - Công cụ: Redgate SQL Compare.

</div>
<div class=rdiv>

- **Kiểm thử Dữ liệu và ETL:**

  - So sánh dữ liệu giữa nguồn và đích, đảm bảo tính toàn vẹn.
  - Công cụ: QuerySurge.

- **Kiểm thử Bảo mật (Security):**
  - Phát hiện các lỗ hổng bảo mật, đặc biệt là SQL Injection.
  - Kiểm tra về phân quyền truy cập dữ liệu.
  - Công cụ: SQLMap (SQL Injection), Các công cụ functional testing (dùng query kiểm tra phân quyền).

</div>

---

<!-- _class: navbar -->
<!-- _header: \ ***FIT@HCMUS*** *Tổng quan* *Loại kiểm thử* *Quy trình* *Thách thức* **Công cụ** *Kết luận* -->

## II. Phương pháp tiếp cận

- **Phương pháp tiếp cận:**

  - **White Box Testing:** Kiểm tra trực tiếp logic thực thi bên trong CSDL.
    - _VD:_ _tSQLt_ cho phép viết test bằng T-SQL.
  - **Black Box Testing:** Kiểm tra kết quả cuối cùng từ góc độ người dùng mà không cần biết logic.
    - _VD:_ _DbFit_ dùng bảng để mô tả logic.

- **Tính cô lập (Isolation):**
  - Đảm bảo mỗi test case chạy độc lập, không ảnh hưởng đến CSDL hay các test khác.
    _VD:_
    - _tSQLt_ tự động `ROLLBACK` sau mỗi test.
    - _DBUnit_ dùng `CLEAN_INSERT` để reset dữ liệu.

---

<!-- _class: cols-2 navbar -->
<!-- _header: \ ***FIT@HCMUS*** *Tổng quan* *Loại kiểm thử* *Quy trình* *Thách thức* **Công cụ** *Kết luận* -->

presen

## III. Tự động hóa & khả năng tích hợp

<div class=ldiv>

- **Tích hợp CI/CD:**

  - Khả năng chạy qua dòng lệnh (CLI) và xuất báo cáo để tích hợp vào Jenkins, GitLab CI.
  - Điều này giúp tự động hóa việc kiểm thử trong quy trình phát triển phần mềm.

- **Mocking:**
  - Thay thế các đối tượng phụ thuộc (bảng, procedure) bằng đối tượng giả để cô lập test.
  - Công cụ: _tSQLt_ cung cấp `FakeTable` và `SpyProcedure`.

</div>
<div class=rdiv>

- **Quản lý dữ liệu test:**
  - Hỗ trợ thiết lập dữ liệu mẫu (dataset) trước khi test và dọn dẹp (teardown) sau đó.
  - Công cụ: _DBUnit_, _NoSQLUnit_ sử dụng file XML/JSON để quản lí và xuất báo cáo.
  - Việc hỗ trợ này giúp đội ngũ dễ dàng trong việc quan sát và phân tích kết quả test để nhanh chóng sửa lỗi

</div>

---

<!-- _class: cols-2 navbar -->
<!-- _header: \ ***FIT@HCMUS*** *Tổng quan* *Loại kiểm thử* *Quy trình* *Thách thức* **Công cụ** *Kết luận* -->

## IV. Tương thích

<div class=ldiv>

- **Tính tương thích:** Tùy vào nhu cầu kiểm thử trên DBMS nào mà chọn công cụ phù hợp.

  - Một số công cụ chỉ hỗ trợ một (vài) DBMS cụ thể:
    - MS SQL Server: _tSQLt_, _DBFit_.
    - Oracle DB: _Swingbench_
  - Một số công cụ có thể hỗ trợ đa nền tảng:
    - _JMeter_ (các DBMS có hỗ trợ JDBC)
    - _NoSQLUnit_ (MongoDB, Cassandra...).

</div>
<div class=rdiv>

- **Giao diện và Tính dễ sử dụng:**
  - Kịch bản test có dễ đọc, dễ hiểu không?
  - **Ví dụ:** _DbFit_ dùng bảng, phù hợp cho cả BA, QA.

## </div>

---

<!-- _class: navbar -->
<!-- _header: \ ***FIT@HCMUS*** *Tổng quan* *Loại kiểm thử* *Quy trình* *Thách thức* **Công cụ** *Kết luận* -->

## V. Khả năng thiết kế test case

- **Hỗ trợ Kỹ thuật Thiết kế Test Case:**
  - Hỗ trợ các kỹ thuật như **Data-Driven Testing (DDT)**.
  - **Ví dụ:** _JMeter_ có thể đọc dữ liệu từ file CSV để thực hiện nhiều kịch bản test.

---

<!-- _class: cols-2 navbar -->
<!-- _header: \ ***FIT@HCMUS*** *Tổng quan* *Loại kiểm thử* *Quy trình* *Thách thức* **Công cụ** *Kết luận* -->

## Structural Testing

<div class=ldiv>

- **Redgate SQL Compare**
  - **Là gì:** Công cụ thương mại mạnh mẽ để so sánh schema CSDL.
  - **Chức năng:** Tìm và đồng bộ hóa sự khác biệt về schema (bảng, cột, view...) giữa các môi trường (VD: DEV vs. PROD).
  - **Chi phí:** Trả phí (Thương mại).

</div>

<div class=rdiv>

- **ApexSQL Diff**
  - **Là gì:** Công cụ thương mại tương tự Redgate.
  - **Chức năng:** So sánh, phát hiện sự khác biệt trong cả schema và dữ liệu.
  - **Chi phí:** Trả phí (Thương mại).

</div>

---

<!-- _class: navbar -->
<!-- _header: \ ***FIT@HCMUS*** *Tổng quan* *Loại kiểm thử* *Quy trình* *Thách thức* **Công cụ** *Kết luận* -->

## Functional Testing (Unit test)

- **tSQLt:** Framework mã nguồn mở cho SQL Server để thực hiện Unit Test.
- **DbFit:** Hỗ trợ kiểm thử CSDL qua các bảng quyết định (decision tables), dễ dàng cho cả tester và BA.
- **DbUnit:** Mở rộng của JUnit, chuyên dùng để quản lý trạng thái CSDL giữa các lần chạy test.

---

<!-- _class: cols-2 navbar -->
<!-- _header: \ ***FIT@HCMUS*** *Tổng quan* *Loại kiểm thử* *Quy trình* *Thách thức* **Công cụ** *Kết luận* -->

## Non-functional: Performance & Security

<div class=ldiv>

- **Apache JMeter**

  - Kiểm thử tải và hiệu năng, bằng cách tạo ra lượng lớn truy vấn đồng thời để đo thời gian phản hồi và khả năng chịu tải của CSDL.
  - Open source, miễn phí.

- **HammerDB**
  - Công cụ benchmark và load testing.
  - Chuyên đo lường hiệu suất của nhiều loại CSDL (Oracle, SQL Server, PostgreSQL...) dưới các kịch bản tải khác nhau.
  - Open source, miễn phí.

</div>
<div class=rdiv>

- **SQLMap**
  - Chuyên dò tìm và khai thác lỗ hổng SQL Injection.
  - Tự động hóa việc phát hiện các điểm yếu bảo mật liên quan đến SQL Injection trong ứng dụng.
  - Open source, miễn phí.

</div>

---

<!-- _class: trans -->
<!-- _paginate: "" -->

# Best practices & kết luận

---

<!-- _class: trans -->
<!-- _paginate: "" -->
## Hai công cụ nổi bật

---
<!-- _class: navbar -->
<!-- _header: \ ***@HCMUS*** *Giới thiệu* *Mục tiêu* *Loại kiểm thử* *Quy trình* *Thách thức* **Công cụ** *Kết luận* -->

## tSQLt - Database Unit Testing Framework

### **Giới thiệu**
- **tSQLt** là framework **mã nguồn mở** chuyên về Unit Testing cho **SQL Server**.
- Cho phép viết và thực thi test case trực tiếp bằng **T-SQL**, không cần chuyển đổi giữa các công cụ.
- Tương thích với các phiên bản SQL Server từ **2005 SP2** trở lên.

### **Đặc điểm nổi bật**
- **Quản lý Transaction tự động:** Mỗi test chạy trong một transaction riêng.
- **Tổ chức Test theo Schema:** Nhóm các test theo schema, dễ dàng quản lý và sử dụng chung phương thức setup.
- **Khả năng Cô lập (Isolation):** Hỗ trợ `FakeTable` và `SpyProcedure` để thay thế các đối tượng phụ thuộc.
- **Tích hợp CI/CD:** Xuất kết quả dạng plain text hoặc XML, tích hợp vào Jenkins, GitLab CI,...

---
<!-- _class: cols-2 navbar -->
<!-- _header: \ ***@HCMUS*** *Giới thiệu* *Mục tiêu* *Loại kiểm thử* *Quy trình* *Thách thức* **Công cụ** *Kết luận* -->

## tSQLt - Ưu & Nhược điểm

<div class=ldiv>

### **Ưu điểm**
- **Mã nguồn mở và miễn phí:** Không mất chi phí license.
- **Viết test bằng T-SQL:** Phù hợp với DBA và SQL Developer, không cần học ngôn ngữ mới.
- **Độc lập và Clean-up tự động:** Transaction tự động rollback sau mỗi test.
- **Khả năng mở rộng:** Đã được chứng minh với các dự án lớn (hơn 6000 test cases).
- **Hỗ trợ Mocking mạnh mẽ:** Tạo fake table, spy procedure để cô lập code.

</div>
<div class=rdiv>

### **Nhược điểm**
- **Chỉ hỗ trợ SQL Server:** Không thể sử dụng cho Oracle, MySQL, PostgreSQL...
- **Yêu cầu CLR & TRUSTWORTHY:** Cần bật CLR và đặt thuộc tính `TRUSTWORTHY = ON`, có thể gây lo ngại về bảo mật.
- **Hạn chế với Foreign Key phức tạp:** Chỉ mock được khóa ngoại đơn cột, không hỗ trợ cascading delete.
- **Không mock được Function/Trigger:** Phải test trực tiếp với implementation thật.
- **Vấn đề với Transaction lồng nhau:** Gặp khó khăn khi code có logic commit/rollback.

</div>

---
<!-- _class: navbar -->
<!-- _header: \ ***@HCMUS*** *Giới thiệu* *Mục tiêu* *Loại kiểm thử* *Quy trình* *Thách thức* **Công cụ** *Kết luận* -->

## tSQLt - Ứng dụng thực tế

- **Unit Testing cho Stored Procedures:**
  - Xác thực logic nghiệp vụ phức tạp trong các stored procedure.
  - Kiểm tra xử lý lỗi và các trường hợp biên (edge cases).

- **Test-Driven Development (TDD) cho Database:**
  - Viết test trước, sau đó implement code SQL.
  - Giúp đảm bảo code database luôn đáp ứng yêu cầu nghiệp vụ.

- **Regression Testing:**
  - Phát hiện sớm các lỗi khi thay đổi schema hoặc logic database.
  - Chạy tự động trong CI/CD pipeline để đảm bảo chất lượng.

- **Validation của Business Rules:**
  - Kiểm tra các ràng buộc, trigger và validation logic hoạt động đúng.

---
<!-- _class: navbar -->
<!-- _header: \ ***@HCMUS*** *Giới thiệu* *Mục tiêu* *Loại kiểm thử* *Quy trình* *Thách thức* **Công cụ** *Kết luận* -->

## DbFit - Table-Driven Database Testing

### **Giới thiệu**
- **DbFit** là framework **mã nguồn mở** hỗ trợ **Test-Driven Development** cho database.
- Được xây dựng trên nền tảng **FitNesse**, một framework testing trưởng thành với cộng đồng lớn.
- Hỗ trợ **đa nền tảng:** Oracle, SQL Server, MySQL, DB2, PostgreSQL, HSQLDB, Derby.

### **Đặc điểm nổi bật**
- **Kiểm thử dựa trên Bảng (Table-based):** Test được viết dưới dạng bảng wiki, dễ đọc hơn xUnit.
- **Dễ tiếp cận với Non-technical Users:** BA và QA có thể đọc và hiểu test mà không cần kiến thức SQL sâu.
- **Quản lý Transaction linh hoạt:** Hỗ trợ 2 chế độ (Flow và Standalone), tự động rollback sau mỗi test.
- **Tích hợp đa dạng:** Chạy qua command-line, Java IDE, REST API, hoặc CI tools.
- **Parameterization:** Hỗ trợ tham số hóa để tái sử dụng test với nhiều bộ dữ liệu khác nhau.

---
<!-- _class: cols-2 navbar -->
<!-- _header: \ ***@HCMUS*** *Giới thiệu* *Mục tiêu* *Loại kiểm thử* *Quy trình* *Thách thức* **Công cụ** *Kết luận* -->

## DbFit - Ưu & Nhược điểm

<div class=ldiv>

### **Ưu điểm**
- **Mã nguồn mở (GPL license):** Hoàn toàn miễn phí.
- **Đa nền tảng:** Hỗ trợ nhiều loại CSDL khác nhau (Oracle, SQL Server, MySQL...).
- **Dễ đọc và bảo trì:** Format bảng giúp test dễ hiểu, phù hợp cho cả team kỹ thuật và phi kỹ thuật.
- **Hỗ trợ Acceptance Testing:** Cho phép viết test theo phong cách BDD (Behavior-Driven Development).
- **Tích hợp tốt với CI/CD:** Có thể chạy qua JUnit, Maven, hoặc command line.
- **Test nhiều loại đối tượng DB:** Query, Insert, Update, Stored Procedure, Function...

</div>
<div class=rdiv>

### **Nhược điểm**
- **Yêu cầu nhiều Runtime:** Cần cả Java và .NET 2.0 runtime (tùy cấu hình).
- **Không tích hợp sẵn JDBC Drivers:** Phải tự cài đặt driver cho từng loại database do hạn chế license.
- **Cấu hình phức tạp hơn:** So với tSQLt, việc setup ban đầu có thể khó khăn hơn.
- **Phụ thuộc FitNesse:** Cần hiểu cách hoạt động của FitNesse để sử dụng hiệu quả.
- **Cộng đồng nhỏ hơn:** Ít tài liệu và ví dụ hơn so với các framework phổ biến khác.

</div>

---
<!-- _class: navbar -->
<!-- _header: \ ***@HCMUS*** *Giới thiệu* *Mục tiêu* *Loại kiểm thử* *Quy trình* *Thách thức* **Công cụ** *Kết luận* -->

## DbFit - Ứng dụng thực tế

- **Regression Testing cho Data Warehouse:**
  - So sánh kết quả query trước và sau khi thay đổi.
  - Xác thực tính chính xác của các phép biến đổi dữ liệu (transformations).

- **Data Migration Testing:**
  - Kiểm tra việc di chuyển dữ liệu từ hệ thống cũ sang hệ thống mới.
  - Đảm bảo không có dữ liệu bị mất hoặc sai lệch.

- **ETL Testing:**
  - Xác thực các quy trình Extract-Transform-Load hoạt động đúng.
  - Kiểm tra tính toàn vẹn dữ liệu từ nguồn đến đích.

- **Acceptance Testing cho Database:**
  - Tạo test case dưới dạng bảng để stakeholder có thể review và approve.
  - Làm cầu nối giữa yêu cầu nghiệp vụ và implementation kỹ thuật.

---

<!-- _class: navbar -->
<!-- _header: \ ***FIT@HCMUS*** *Tổng quan* *Loại kiểm thử* *Quy trình* *Thách thức* *Công cụ* **Kết luận** -->

## Best Practices (1/4)

- Document chi tiết, đầy đủ:

  - Test case: input, output, expected result, steps.
  - Test log: kết quả, lỗi, thời gian. Phục vụ cho debug và kiểm tra lại.
  - Test coverage: đảm bảo bao phủ các thành phần quan trọng.

- Kiểm tra dữ liệu & metadata:

  - Xác minh cấu trúc bảng: column, type, default value, constraints, indexes.
  - Kiểm tra giới hạn dữ liệu (length, range, enum), giá trị mặc định và NULL handling.
  - Kiểm tra cả functional data và metadata (migrations, schema versions).

---

<!-- _class: navbar -->
<!-- _header: \ ***FIT@HCMUS*** *Tổng quan* *Loại kiểm thử* *Quy trình* *Thách thức* *Công cụ* **Kết luận** -->

## Best Practicesc (2/4)

- Chú ý ETL operations:

  - Kiểm thử các bước extract/transform/load riêng biệt và toàn bộ quá trình (end‑to‑end).
  - So sánh dữ liệu nguồn và đích (row counts, checksums, sample records).
  - Kiểm tra incremental loads (chỉ thực hiện thay đổi trên dữ liệu mới so với lần chạy trước đó), error handling và idempotency.

- Cô lập môi trường thực thi testcases:

  - Mỗi test chạy độc lập (setup → execute → teardown) để tránh side‑effects.
  - Xác định thời điểm chạy setup/teardown và dùng transaction/rollback hoặc snapshot để reset.
  - Sử dụng môi trường test tách biệt (sandbox) hoặc containerized DB.

<!-- Speaker notes:
- Why ETL? -> In the industry, you don't just have one database. You have multiple databases, and you need to move data between them. So ETL testing is crucial to ensure data integrity during these operations.
 -->

---

<!-- _class: navbar -->
<!-- _header: \ ***FIT@HCMUS*** *Tổng quan* *Loại kiểm thử* *Quy trình* *Thách thức* *Công cụ* **Kết luận** -->

## Best Practices (3/4)

- Sử dụng dữ liệu đầu vào:

  - Validate input test data trước khi chạy.
  - Dùng mock/seed data gần thực tế: generator tools, anonymized production samples.
  - Thực hiện data‑driven tests với bộ dữ liệu đại diện cho các phân vùng và biên.

- Tự động hóa test execution:

  - Nếu khả thi, tự động hóa để hỗ trợ regression và CI.
  - Công cụ gợi ý: DBUnit, tSQLt, SQLTest, DbFit; hoặc scripting (bash/python) cho orchestration.
  - Nếu tự động hóa không khả thi: duy trì checklist, template logs và execution plan.

---

<!-- _class: navbar -->
<!-- _header: \ ***FIT@HCMUS*** *Tổng quan* *Loại kiểm thử* *Quy trình* *Thách thức* *Công cụ* **Kết luận** -->

## Best Practices (4/4)

- Kiểm tra các yếu tố vận hành (operational checks):
  - DB logs: xác nhận logs được ghi và rotate đúng.
  - Cron/jobs: kiểm tra jobs chạy đúng lịch và hoàn thành thành công.
  - Backup: kiểm tra backup tồn tại, validate integrity và thử restore định kỳ.
  - Distributed DB: kiểm tra dữ liệu sync/replication, detect lag/consistency issues.
  - Giám sát Recovery Time Object/Recovery Point Object và tài liệu quy trình khôi phục.

<!-- Speaker notes:
You may forgot this, but in realistic, this test is crucial because we don't know when an issue happens.
Any mistake in the database in this test may cause such a large (thiet hai).
RTO: thời gian cần để hệ thống có thể hoạt động lại sau sự cố. Tức là: Thời gian chấp nhận hệ thống bị gián đoạn.
RPO: lượng data chấp nhận mất khi gặp sự cố. Tức là: Sẽ chấp nhận mất dữ liệu phát sinh trong khoảng thời gian RPO này.
  -->

---

<!-- _class: navbar -->
<!-- _header: \\ ***FIT@HCMUS*** *Tổng quan* *Loại kiểm thử* *Quy trình* *Thách thức* *Công cụ* **Kết luận** -->

## Kết luận

- Database testing giúp phát hiện các vấn đề về **độ tin cậy** (reliability), **tính toàn vẹn** (data integrity) và các vấn đề khác khi **vận hành** CSDL (security, performance, scalability...).
- **Tự động hóa và AI** đang định hình lại tương lai của kiểm thử CSDL, giúp tạo test case thông minh một cách tự động. Tuy nhiên, vai trò của con người vẫn rất quan trọng trong việc thiết kế kịch bản kiểm thử và phân tích kết quả.
- **Kết hợp** các **kỹ thuật** truyền thống với **công cụ** hiện đại sẽ giúp đảm bảo việc kiểm thử trở nên đầy đủ hơn, giúp phát hiện sớm các vấn đề tìm ẩn.

---

<!-- _paginate: "" -->

## Tài liệu tham khảo

- [Divesh Mehta — Database testing: What is it? Why & best practices](https://testsigma.com/blog/database-testing/) [truy cập: Oct. 22, 2025]
- [Indaacademy — Database Testing Tutorial – Hướng dẫn kiểm thử Cơ sở dữ liệu (P2)](https://indaacademy.vn/database-testing/database-testing-tutorial-huong-dan-kiem-thu-co-so-du-lieu-p2/) [truy cập: Oct. 22, 2025]
- [Thomas Hamilton — Database Testing Tutorial (Guru99)](https://www.guru99.com/data-testing.html#structural-database-testing) [truy cập: Oct. 22, 2025]
- [Gunashree RS — Database Tests: Guide to Ensuring Data Integrity and Performance](https://www.devzery.com/post/comprehensive-guide-to-database-tests-strategies-andbest-practices) [truy cập: Oct. 22, 2025]
- [David Ekete — Advanced Test Data Management: Techniques and Best Practices](<https://blog.magicpod.com/advanced-test-data-management-techniques-and-best-practices#:~:text=Test%20data%20management%20(TDM)%20involves,scenarios%20for%20software%20performance%20insights>) [truy cập: Oct. 23, 2025]
- [HammerDB Documentation](https://www.devzery.com/post/comprehensive-guide-to-database-tests-strategies-and-best-practices) [truy cập: Oct. 23, 2025]

---

<!-- _class: lastpage -->
<!-- _footer: "" -->

###### Q&A

---

<!-- _class: trans -->
<!-- _paginate: "" -->

## Các kỹ thuật kiểm thử

---

<!-- _class: navbar -->
<!-- _header: \ ***FIT@HCMUS*** *Tổng quan* *Loại kiểm thử* *Quy trình* **Kỹ thuật** *Thách thức* *Công cụ* *Kết luận* -->

## SQL Queries

- **Mục tiêu:**

  - Đảm bảo các câu lệnh SQL trả về kết quả _chính xác_ và _toàn vẹn_.
  - Kiểm tra _hiệu suất_ của truy vấn.

- **Bao gồm:**
  - **Kiểm tra tính đúng đắn:** So sánh kết quả của truy vấn với dữ liệu mong đợi, đảm bảo rằng dữ liệu khi thay đổi trong database phải chính xác.
  - **Kiểm tra hiệu suất:** Phân tích `Execution Plan` để xác định các truy vấn chậm, thiếu index... Từ những phân tích này, tối ưu hóa câu lệnh SQL để cài thiện hiệu suất.
  - **Kiểm tra với dữ liệu lớn:** Đánh giá thời gian phản hồi khi CSDL có hàng triệu bản ghi.
  - **Kiểm tra bảo mật:** Đảm bảo truy vấn không dễ bị tấn công SQL Injection.

<!-- Speaker notes
- Dữ liệu không chỉ cần đúng. Trong thế giới phần mềm hiện đại, hiệu suất là rất quan trọng. Hiệu suất không chỉ là nhanh chậm, nó còn gây ảnh hưởng đến tính sẵn sàng và khả năng mở rộng của hệ thống. Đặc biệt là ảnh hưởng đến chi phí.
-
 -->

---

<!-- _class: navbar -->
<!-- _header: \\ ***FIT@HCMUS*** *Tổng quan* *Loại kiểm thử* *Quy trình* **Kỹ thuật** *Thách thức* *Công cụ* *Kết luận* -->

## Data-Driven

- **Phân vùng Tương đương (EP):**
  - Chia dữ liệu đầu vào thành các nhóm (lớp) mà hệ thống xử lý tương tự nhau.
  - **Ví dụ:** Với trường `tuổi`, các lớp có thể là:
    - `Âm` (không hợp lệ)
    - `0-17` (trẻ em)
    - `18-60` (người lớn)
    - `> 60` (người cao tuổi)
  - Chỉ cần chọn một giá trị đại diện trong mỗi lớp để kiểm thử.

---

<!-- _class: navbar -->
<!-- _header: \\ ***FIT@HCMUS*** *Tổng quan* *Loại kiểm thử* *Quy trình* **Kỹ thuật** *Thách thức* *Công cụ* *Kết luận* -->

## Kỹ thuật Data-Driven

- **Phân tích Giá trị Biên (BVA):**
  - Tập trung kiểm thử tại các giá trị biên của mỗi phân vùng.
  - **Ví dụ:** Với lớp `18-60`, các giá trị biên cần kiểm thử là:
    - `17` (ngay dưới)
    - `18` (biên dưới)
    - `19` (ngay trên)
    - `59` (ngay dưới)
    - `60` (biên trên)
    - `61` (ngay trên)
  - Giúp phát hiện lỗi logic tại các điểm chuyển tiếp.
