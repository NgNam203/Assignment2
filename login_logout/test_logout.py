import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()
# Kiểm thử đăng xuất
def test_logout(driver):
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

    time.sleep(2)

    # Bấm vào "My Account"
    my_account = driver.find_element(By.XPATH, "//a[contains(@class, 'dropdown-toggle') and contains(., 'My Account')]")
    my_account.click()

    time.sleep(2)

    # Tìm và bấm vào "Logout" từ menu thả xuống
    logout_link = driver.find_element(By.XPATH, "//a[contains(@href, 'account/logout') and contains(text(), 'Logout')]")
    logout_link.click()

    time.sleep(2)

    # Kiểm tra chuyển hướng đến trang logout
    try:
        current_url = driver.current_url
        assert current_url == "https://demo.opencart.com/en-gb?route=account/logout", \
            f"Chuyển hướng đến trang logout thất bại, URL hiện tại là: {current_url}"
        print("Logout thành công và đã chuyển hướng đến trang logout.")
    except Exception as e:
        print(f"Logout thất bại hoặc không chuyển hướng đúng: {e}")
        assert False, "Logout thất bại hoặc không chuyển hướng đúng."


# Results: PS C:\Users\ADMIN\OneDrive\Desktop\Daihoc\HK I 24 - 25\Testing\assignment2_2\login_logout> pytest -s .\test_logout.py  
# ============================================================================================================ test session starts ============================================================================================================ 
# platform win32 -- Python 3.12.6, pytest-8.3.3, pluggy-1.5.0                                                                                                                                                                                   
# rootdir: C:\Users\ADMIN\OneDrive\Desktop\Daihoc\HK I 24 - 25\Testing\assignment2_2\login_logout                                                                                                                                               
# plugins: anyio-4.6.2.post1
# collected 1 item

# test_logout.py
# DevTools listening on ws://127.0.0.1:61017/devtools/browser/456865b3-b415-42d1-b0b5-71f493fecd5b
# Created TensorFlow Lite XNNPACK delegate for CPU.
# Attempting to use a delegate that only supports static-sized tensors with a graph that has dynamic-sized tensors (tensor#58 is a dynamic-sized tensor).
# Logout thành công và đã chuyển hướng đến trang logout.
# .

# ============================================================================================================ 1 passed in 54.19s =============================================================================================================