import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

#https://demo.opencart.com/

# 1. Đăng nhập với dữ liệu hợp lệ
def test_valid_login(driver):
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
    # Chọn "Login" từ menu thả xuống
    login_link = driver.find_element(By.XPATH, "//a[contains(@href, 'account/login') and contains(text(), 'Login')]")
    login_link.click()

    # Chờ trang login tải xong
    time.sleep(5)

    # Điền email
    email_input = driver.find_element(By.ID, "input-email")
    email_input.clear()
    email_input.send_keys("nom@gmail.com")  # Thay bằng email hợp lệ

    # Điền mật khẩu
    password_input = driver.find_element(By.ID, "input-password")
    password_input.clear()
    password_input.send_keys("password123")  # Thay bằng mật khẩu hợp lệ

    # Click nút đăng nhập
    login_button = driver.find_element(By.XPATH, "//button[@type='submit' and contains(@class, 'btn-primary')]")
    login_button.click()

    # Chờ và kiểm tra chuyển hướng đến trang tài khoản
    try:
        time.sleep(5)
        current_url = driver.current_url
        assert "route=account/account" in current_url, \
            f"Chuyển hướng đến trang tài khoản thất bại, URL hiện tại là: {current_url}"
        print("Đăng nhập thành công và đã chuyển hướng đến trang tài khoản.")
    except Exception as e:
        print(f"Đăng nhập thất bại hoặc không có chuyển hướng: {e}")
        assert False, "Đăng nhập thất bại hoặc không có chuyển hướng."

# 2. Đăng nhập với dữ liệu không hợp lệ
def test_invalid_login(driver):
    # Truy cập trang chủ
    driver.get("https://demo.opencart.com/")
    
    time.sleep(10)
    driver.refresh() #Đợi load trang ho xác minh
    time.sleep(10)
    driver.refresh()
    time.sleep(10)

    # Bấm vào "My Account"
    my_account = driver.find_element(By.XPATH, "//a[contains(@class, 'dropdown-toggle') and contains(., 'My Account')]")
    my_account.click()

    time.sleep(3)
    # Chọn "Login" từ menu thả xuống
    login_link = driver.find_element(By.XPATH, "//a[contains(@href, 'account/login') and contains(text(), 'Login')]")
    login_link.click()

    time.sleep(3)

    # Locate and fill in the email field
    email_input = driver.find_element(By.ID, "input-email")
    email_input.clear()
    email_input.send_keys("invalid@aexample.com")

    # Locate and fill in the password field
    password_input = driver.find_element(By.ID, "input-password")
    password_input.clear()
    password_input.send_keys("wrongpassword")

    # Locate and click the login button
    login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    login_button.click()

    time.sleep(2)

    # Chờ và lấy nội dung của thông báo lỗi
    try:

        error_message_element = driver.find_element(By.CSS_SELECTOR, "dirv.alert.alert-danger")
        error_message = error_message_element.text

        # Kiểm tra và in ra nội dung thông báo lỗi
        assert "Warning: No match for E-Mail Address and/or Password." in error_message, \
            f"Thông báo lỗi không đúng, thông báo nhận được là: {error_message}"
        print(f"Đăng nhập thất bại và xuất hiện thông báo lỗi: {error_message}")
    except Exception as e:
        print(f"Lỗi không xuất hiện hoặc có vấn đề khác: {e}")
        assert False, "Không có thông báo lỗi xuất hiện khi đăng nhập thất bại."

# 3. Đăng nhập sai quá số lần
def test_exceeded_attempts(driver):
    # Truy cập trang chủ
    driver.get("https://demo.opencart.com/")
    
    time.sleep(10)
    driver.refresh() #Đợi load trang ho xác minh
    time.sleep(10)
    driver.refresh()
    time.sleep(10)

    # Bấm vào "My Account"
    my_account = driver.find_element(By.XPATH, "//a[contains(@class, 'dropdown-toggle') and contains(., 'My Account')]")
    my_account.click()

    time.sleep(2)
    # Chọn "Login" từ menu thả xuống
    login_link = driver.find_element(By.XPATH, "//a[contains(@href, 'account/login') and contains(text(), 'Login')]")
    login_link.click()

    time.sleep(2)
    
    for _ in range(5):  # Simulate exceeding the number of allowed attempts
        email_input = driver.find_element(By.ID, "input-email")
        email_input.clear()
        email_input.send_keys("nom1@gmail.com")

        password_input = driver.find_element(By.ID, "input-password")
        password_input.clear()
        password_input.send_keys("wrongpassword")

        login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        login_button.click()

    password_input = driver.find_element(By.ID, "input-password")
    password_input.clear()
    password_input.send_keys("password123")  # Thay bằng mật khẩu hợp lệ

    login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    login_button.click()
    time.sleep(2)
    try:
        error_message_element = driver.find_element(By.CSS_SELECTOR, "dirv.alert.alert-danger")
        error_message = error_message_element.text

        # Kiểm tra và in ra nội dung thông báo lỗi
        assert "Warning: Your account has exceeded allowed number of login attempts. Please try again in 1 hour." in error_message, \
            f"Thông báo lỗi không đúng, thông báo nhận được là: {error_message}"
        print(f"Đăng nhập thất bại và xuất hiện thông báo lỗi quá số lần: {error_message}")
    except Exception as e:
        print(f"Lỗi không xuất hiện hoặc có vấn đề khác: {e}")
        assert False, "Không có thông báo lỗi xuất hiện khi đăng nhập thất bại."


# Results: PS C:\Users\ADMIN\OneDrive\Desktop\Daihoc\HK I 24 - 25\Testing\assignment2_2\login_logout> pytest -s .\test_login.py
# ============================================================================================================ test session starts ============================================================================================================
# platform win32 -- Python 3.12.6, pytest-8.3.3, pluggy-1.5.0
# rootdir: C:\Users\ADMIN\OneDrive\Desktop\Daihoc\HK I 24 - 25\Testing\assignment2_2\login_logout
# plugins: anyio-4.6.2.post1
# collected 3 items

# test_login.py
# DevTools listening on ws://127.0.0.1:60574/devtools/browser/27d120d1-c442-4bfb-939c-9beadfa03571
# Created TensorFlow Lite XNNPACK delegate for CPU.
# Attempting to use a delegate that only supports static-sized tensors with a graph that has dynamic-sized tensors (tensor#58 is a dynamic-sized tensor).
# Đăng nhập thành công và đã chuyển hướng đến trang tài khoản.
# .
# DevTools listening on ws://127.0.0.1:60667/devtools/browser/9405e1cc-cabf-4ee2-b6aa-fa4c44ed1e61
# Created TensorFlow Lite XNNPACK delegate for CPU.
# Attempting to use a delegate that only supports static-sized tensors with a graph that has dynamic-sized tensors (tensor#58 is a dynamic-sized tensor).
# Đăng nhập thất bại và xuất hiện thông báo lỗi: Warning: No match for E-Mail Address and/or Password.
# .
# DevTools listening on ws://127.0.0.1:60746/devtools/browser/3a0371ec-3580-4672-ac30-df5e7b9a75a3
# Created TensorFlow Lite XNNPACK delegate for CPU.
# Attempting to use a delegate that only supports static-sized tensors with a graph that has dynamic-sized tensors (tensor#58 is a dynamic-sized tensor).
# Đăng nhập thất bại và xuất hiện thông báo lỗi quá số lần: Warning: Your account has exceeded allowed number of login attempts. Please try again in 1 hour.
# .

# ======================================================================================================= 3 passed in 158.30s (0:02:38) =======================================================================================================