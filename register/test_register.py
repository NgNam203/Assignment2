import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import string

# Hàm tạo email ngẫu nhiên
def generate_random_email():
    random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"{random_string}@example.com"


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()
    
# 1. Kiểm thử đăng ký thành công
def test_register_success(driver):
    # Truy cập trang chủ
    driver.get("https://demo.opencart.com/")
    #Đợi load trang và xác minh
    time.sleep(10)
    driver.refresh() 
    time.sleep(10)
    driver.refresh()
    time.sleep(10)
    # Bấm vào "My Account"
    my_account = driver.find_element(By.XPATH, "//a[contains(@class, 'dropdown-toggle') and contains(., 'My Account')]")
    my_account.click()

    time.sleep(3)
    # Chọn "Register" từ menu thả xuống
    login_link = driver.find_element(By.XPATH, "//a[contains(@href, 'account/register') and contains(text(), 'Register')]")
    login_link.click()

    time.sleep(5)

    # Tạo email ngẫu nhiên
    random_email = generate_random_email()

    # Điền vào các trường bắt buộc
    driver.find_element(By.ID, "input-firstname").send_keys("test")
    driver.find_element(By.ID, "input-lastname").send_keys("test")
    driver.find_element(By.ID, "input-email").send_keys(random_email)  # email ngẫu nhiên
    driver.find_element(By.ID, "input-password").send_keys("password123")
    driver.find_element(By.NAME, "agree").click()  # Chấp nhận điều khoản và chính sách

    # Nhấn nút "Continue" để đăng ký
    driver.find_element(By.XPATH, "//button[@type='submit' and contains(text(), 'Continue')]").click()

    # Chờ và kiểm tra chuyển hướng đến trang đăng ký thành công
    time.sleep(5)
    try: 
        current_url = driver.current_url
        assert "route=account/success" in current_url
        print("Đăng ký thành công và đã chuyển hướng đến trang đăng ký thành công.")
    except Exception as e:
        print(f"Đăng ký thất bại hoặc không có chuyển hướng: {e}")
        assert False
        
# 2. Kiểm thử đăng ký với thiếu trường bắt buộc (cụ thể là Last Name)
def test_register_missing_fields(driver): 
    # Truy cập trang chủ
    driver.get("https://demo.opencart.com/")
    #Đợi load trang và xác minh
    time.sleep(10)
    driver.refresh() 
    time.sleep(10)
    driver.refresh()
    time.sleep(10)
    # Bấm vào "My Account"
    my_account = driver.find_element(By.XPATH, "//a[contains(@class, 'dropdown-toggle') and contains(., 'My Account')]")
    my_account.click()

    time.sleep(3)
    # Chọn "Register" từ menu thả xuống
    login_link = driver.find_element(By.XPATH, "//a[contains(@href, 'account/register') and contains(text(), 'Register')]")
    login_link.click()

    time.sleep(3)

    # Tạo email ngẫu nhiên
    random_email = generate_random_email()
    # Điền thiếu một số trường bắt buộc (không điền họ)
    driver.find_element(By.ID, "input-firstname").send_keys("test")

    driver.find_element(By.ID, "input-email").send_keys(random_email)  # email ngẫu nhiên
    driver.find_element(By.ID, "input-password").send_keys("password123")
    driver.find_element(By.NAME, "agree").click()  # Chấp nhận điều khoản và chính sách
    # Nhấn nút "Continue" để đăng ký
    driver.find_element(By.XPATH, "//button[@type='submit' and contains(text(), 'Continue')]").click()
    time.sleep(5)
    # Kiểm tra thông báo lỗi
    try:
        error_message = driver.find_element(By.ID, "error-lastname").text
        assert "Last Name must be between 1 and 32 characters!" in error_message
        print("Thông báo lỗi xuất hiện đúng khi thiếu trường Last Name.")
    except Exception as e:
        print(f"Kiểm tra thất bại: {e}")
        assert False

# 3. Kiểm thử với dữ liệu không hợp lệ (email sai định dạng)
def test_register_invalid_email(driver):
    # Truy cập trang chủ
    driver.get("https://demo.opencart.com/")
    #Đợi load trang và xác minh
    time.sleep(10)
    driver.refresh() 
    time.sleep(10)
    driver.refresh()
    time.sleep(8)
    # Bấm vào "My Account"
    my_account = driver.find_element(By.XPATH, "//a[contains(@class, 'dropdown-toggle') and contains(., 'My Account')]")
    my_account.click()

    time.sleep(3)
    # Chọn "Register" từ menu thả xuống
    login_link = driver.find_element(By.XPATH, "//a[contains(@href, 'account/register') and contains(text(), 'Register')]")
    login_link.click()

    time.sleep(3)

    # Điền vào các trường với email sai định dạng
    driver.find_element(By.ID, "input-firstname").send_keys("test")
    driver.find_element(By.ID, "input-lastname").send_keys("test")
    driver.find_element(By.ID, "input-email").send_keys("test@com")  # Email không hợp lệ
    driver.find_element(By.ID, "input-password").send_keys("password123")
    driver.find_element(By.NAME, "agree").click()

    # Nhấn nút "Continue" để đăng ký
    driver.find_element(By.XPATH, "//button[@type='submit' and contains(text(), 'Continue')]").click()
    time.sleep(3)
    # Kiểm tra thông báo lỗi email
    try:
        error_message = driver.find_element(By.ID, "error-email").text
        assert "E-Mail Address does not appear to be valid!" in error_message
        print("Thông báo lỗi xuất hiện đúng khi email không hợp lệ.")
    except Exception as e:
        print(f"Kiểm tra thất bại: {e}")
        assert False

# # 4. Kiểm thử với email đã tồn tại
def test_register_existing_email(driver):
    # Truy cập trang chủ
    driver.get("https://demo.opencart.com/")
    #Đợi load trang và xác minh
    time.sleep(10)
    driver.refresh() 
    time.sleep(10)
    driver.refresh()
    time.sleep(8)
    # Bấm vào "My Account"
    my_account = driver.find_element(By.XPATH, "//a[contains(@class, 'dropdown-toggle') and contains(., 'My Account')]")
    my_account.click()

    time.sleep(3)
    # Chọn "Register" từ menu thả xuống
    login_link = driver.find_element(By.XPATH, "//a[contains(@href, 'account/register') and contains(text(), 'Register')]")
    login_link.click()

    time.sleep(3)

    # Điền vào các trường với email đã tồn tại
    driver.find_element(By.ID, "input-firstname").send_keys("John")
    driver.find_element(By.ID, "input-lastname").send_keys("Doe")
    driver.find_element(By.ID, "input-email").send_keys("nom1@gmail.com")  # Giả sử email này đã được đăng ký
    driver.find_element(By.ID, "input-password").send_keys("password123")
    driver.find_element(By.NAME, "agree").click()

    # Nhấn nút "Continue" để đăng ký
    driver.find_element(By.XPATH, "//button[@type='submit' and contains(text(), 'Continue')]").click()

    time.sleep(3)
    # Kiểm tra thông báo lỗi email đã tồn tại
    try:
        error_message_element = driver.find_element(By.CSS_SELECTOR, "dirv.alert.alert-danger")
        error_message = error_message_element.text
        assert "Warning: E-Mail Address is already registered!" in error_message
        print("Thông báo lỗi xuất hiện đúng khi email đã tồn tại.")
    except Exception as e:
        print(f"Kiểm tra thất bại: {e}")
        assert False

# 5. Kiểm thử đăng ký khi không tích Privacy Policy 
def test_register_without_privacy_policy(driver):
    # Truy cập trang chủ
    driver.get("https://demo.opencart.com/")
    
    # Đợi load trang và xác minh
    time.sleep(10)
    driver.refresh()
    time.sleep(10)
    driver.refresh()
    time.sleep(8)

    # Bấm vào "My Account"
    my_account = driver.find_element(By.XPATH, "//a[contains(@class, 'dropdown-toggle') and contains(., 'My Account')]")
    my_account.click()

    time.sleep(3)
    # Chọn "Register" từ menu thả xuống
    register_link = driver.find_element(By.XPATH, "//a[contains(@href, 'account/register') and contains(text(), 'Register')]")
    register_link.click()

    time.sleep(3)

    # Điền vào các trường bắt buộc (trừ tích chọn Privacy Policy)
    driver.find_element(By.ID, "input-firstname").send_keys("John")
    driver.find_element(By.ID, "input-lastname").send_keys("Doe")
    driver.find_element(By.ID, "input-email").send_keys("test_privacy@example.com")  # Sử dụng email ngẫu nhiên
    driver.find_element(By.ID, "input-password").send_keys("password123")
    # Không tích vào ô "Privacy Policy"

    # Nhấn nút "Continue" để đăng ký
    driver.find_element(By.XPATH, "//button[@type='submit' and contains(text(), 'Continue')]").click()

    time.sleep(3)

    # Kiểm tra thông báo lỗi về Privacy Policy
    try:
        error_message_element = driver.find_element(By.CSS_SELECTOR, "dirv.alert.alert-danger")
        error_message = error_message_element.text
        assert "Warning: You must agree to the Privacy Policy!" in error_message
        print("Thông báo lỗi xuất hiện đúng khi không tích vào Privacy Policy.")
    except Exception as e:
        print(f"Kiểm tra thất bại: {e}")
        assert False

# Results: PS C:\Users\ADMIN\OneDrive\Desktop\Daihoc\HK I 24 - 25\Testing\assignment2_2\register> pytest -s .\test_register.py
# ============================================================================================================ test session starts ============================================================================================================
# platform win32 -- Python 3.12.6, pytest-8.3.3, pluggy-1.5.0
# rootdir: C:\Users\ADMIN\OneDrive\Desktop\Daihoc\HK I 24 - 25\Testing\assignment2_2\register
# plugins: anyio-4.6.2.post1
# collected 5 items

# test_register.py
# DevTools listening on ws://127.0.0.1:62411/devtools/browser/816f72af-fe57-4526-992d-b3e64cdd764c
# Created TensorFlow Lite XNNPACK delegate for CPU.
# Attempting to use a delegate that only supports static-sized tensors with a graph that has dynamic-sized tensors (tensor#58 is a dynamic-sized tensor).
# Đăng ký thành công và đã chuyển hướng đến trang đăng ký thành công.
# .
# DevTools listening on ws://127.0.0.1:62494/devtools/browser/e44e6233-2f8e-41bf-8f25-6b940da2577f
# Created TensorFlow Lite XNNPACK delegate for CPU.
# Attempting to use a delegate that only supports static-sized tensors with a graph that has dynamic-sized tensors (tensor#58 is a dynamic-sized tensor).
# Thông báo lỗi xuất hiện đúng khi thiếu trường Last Name.
# .
# DevTools listening on ws://127.0.0.1:62614/devtools/browser/2f532b02-c25f-4fbe-aa48-3b91f13c62e4
# Created TensorFlow Lite XNNPACK delegate for CPU.
# Attempting to use a delegate that only supports static-sized tensors with a graph that has dynamic-sized tensors (tensor#58 is a dynamic-sized tensor).
# Thông báo lỗi xuất hiện đúng khi email không hợp lệ.
# .
# DevTools listening on ws://127.0.0.1:62693/devtools/browser/170d5dc2-ef64-4f86-861d-70b5190e6742
# Created TensorFlow Lite XNNPACK delegate for CPU.
# Attempting to use a delegate that only supports static-sized tensors with a graph that has dynamic-sized tensors (tensor#58 is a dynamic-sized tensor).
# Thông báo lỗi xuất hiện đúng khi email đã tồn tại.
# .
# DevTools listening on ws://127.0.0.1:62773/devtools/browser/94ca2633-f22a-41d5-97e7-73157333d8cb
# Created TensorFlow Lite XNNPACK delegate for CPU.
# Attempting to use a delegate that only supports static-sized tensors with a graph that has dynamic-sized tensors (tensor#58 is a dynamic-sized tensor).
# Thông báo lỗi xuất hiện đúng khi không tích vào Privacy Policy.
# .

# ======================================================================================================= 5 passed in 258.72s (0:04:18) =======================================================================================================