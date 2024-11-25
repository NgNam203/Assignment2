Environment Setup:
+ Programming Language: Python 3.12.6
+ IDE: Visual Studio Code
+ Selenium WebDriver: Install and configure Selenium WebDriver.
+ Browser: Chrome 130.0.6723.70
+ Dependencies: pip 24.2 , pytest 8.3.3
+ Version Control: Git

Web kiểm thử:
OpenCart (https://demo.opencart.com/)
![image](https://github.com/user-attachments/assets/a345dc62-9efa-43dd-bdf6-4b90754f57c1)


Cách chạy kiểm thử:
+ Sau khi setup Enviroment
+ Chạy lệnh trong terminal : git clone https://github.com/NgNam203/Assignment2.git
+ Cách chạy một chức năng cụ thể:
  cd .\login_logout\
  pytest -s .\test_login.py 
  pytest -s .\test_logout.py

Tóm tắt các chức năng kiểm thử (thư mục kiểm thử của chức năng):
+ Đăng xuất, đăng nhập (login_logout)
+ Đăng ký (register)
+ Link chuyển hướng trang (links)
+ Tìm kiếm sản phẩm (search)
+ Thêm sản phẩm vào giỏ hàng (cart)
+ Thanh toán (checkout)
+ Thiết kế phản hồi đối với điện thoại (mobile)



Các Test Case - tên hàm:

 Đăng xuất/ Đăng nhập.
 
- TC001: Kiểm thử đăng nhập với dữ liệu hợp lệ - test_valid_login.
- TC002: Kiểm thử đăng nhập với dữ liệu không hợp lệ - test_invalid_login.
- TC003: Kiểm thử đăng nhập sai quá số lần - test_exceeded_attempts.
- TC004: Kiểm thử đăng xuất - test_logout.

Đăng ký.

- TC005: Kiểm thử đăng ký thành công - test_register_success.
- TC006: Kiểm thử đăng ký với thiếu trường bắt buộc (cụ thể là Last Name) - test_register_missing_fields.
- TC007: Kiểm thử với dữ liệu không hợp lệ (email sai định dạng) - test_register_invalid_email.
- TC008: Kiểm thử với email đã tồn tại - test_register_existing_email.
- TC009: Kiểm thử đăng ký khi không tích Privacy Policy - test_register_without_privacy_policy.

Tìm kiếm sản phẩm.

- TC010: Kiểm thử tìm kiếm thành công với từ khóa hợp lệ - test_search_valid_keyword.
- TC011: Kiểm thử tìm kiếm thất bại với từ khóa không hợp lệ - test_search_invalid_keyword.
- TC012: Kiểm thử tìm kiếm với tùy chọn tìm kiếm trong mô tả sản phẩm - test_search_in_description.
- TC013: Kiểm thử tìm kiếm trong một danh mục cụ thể - test_search_in_specific_category.

Thêm sản phẩm vào giỏ hàng.

- TC014: Kiểm thử thêm một sản phẩm vào giỏ hàng - test_add_single_product_to_cart.
- TC015: Kiểm thử thêm nhiều sản phẩm khác nhau vào giỏ hàng - test_add_multiple_products_to_cart
- TC016: Kiểm thử thêm cùng một sản phẩm nhiều lần (số lượng) vào giỏ hàng và kiểm tra số tiền - test_add_same_product_multiple_times
- TC017: Kiểm thử thêm các sản phẩm với số lượng cụ thể vào giỏ hàng và kiểm tra tổng số tiền - test_add_products_with_quantity

Thanh toán

- TC018: Kiểm thử checkout khi người dùng đã đăng nhập - test_checkout_with_logged_in_user
- TC019: Kiểm thử checkout với chế độ khách hàng không đăng nhập - test_guest_checkout
- TC020: Kiểm thử checkout với việc thêm địa chỉ giao hàng mới - test_checkout_with_new_shipping_address
- TC021: Kiểm thử checkout thanh toán không hợp lệ khi bỏ trống phương thức thanh toán, giao hàng - test_checkout_with_invalid_payment_information

Link chuyển hướng trang

- TC022: Kiểm tra tất cả các link ở footer - test_specific_links
- TC023: Kiểm tra tất cả các link ở thanh Category - test_category_links

Thiết kế phản hồi đối với điện thoại

- TC024: Kiểm thử đăng nhập trên điện thoại - test_mobile_login
- TC025: Kiểm thử tìm kiếm thành công trên điện thoại - test_mobile_search_valid_keyword
- TC026: Kiểm thử thêm sản phẩm vào giỏ hàng trên điện thoại - test_mobile_add_single_product_to_cart
- TC027: Kiểm thử checkout (chế độ khách hàng không đăng nhập) trên điện thoại - test_guest_checkout


