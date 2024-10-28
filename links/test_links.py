import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import time

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

# 1. Kiểm tra tất cả các link ở footer
def test_specific_links(driver):
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
    
    # Đợi trang tải đầy đủ
    time.sleep(8)

    # Lấy các phần tử <div> chứa liên kết cụ thể
    divs = driver.find_elements(By.XPATH, "/html/body/footer/div/div")

    # Biến đếm số lượng liên kết hợp lệ và liên kết lỗi
    valid_links_count = 0
    broken_links_count = 0

    # Duyệt qua từng <div> để tìm liên kết bên trong
    for div in divs:
        links = div.find_elements(By.TAG_NAME, "a")
        print(f"Kiểm tra {len(links)} liên kết trong div: {div.get_attribute('innerHTML')[:30]}...")

        # Duyệt qua các liên kết trong mỗi <div>
        for link in links:
            url = link.get_attribute("href")
            print(f"Kiểm tra: {url}")

            # Kiểm tra nếu URL rỗng hoặc không hợp lệ
            if url is None or url == "":
                print("URL không được cấu hình cho thẻ anchor hoặc rỗng")
                continue

            # Chỉ kiểm tra các liên kết thuộc miền demo.opencart.com
            if not url.startswith("https://demo.opencart.com"):
                print(f"URL thuộc về domain khác, bỏ qua: {url}")
                continue

            try:
                time.sleep(3)
                # Gửi yêu cầu HTTP HEAD để kiểm tra liên kết
                response = requests.head(url, allow_redirects=True)
                
                if response.status_code >= 400:
                    print(f"{url} là liên kết lỗi (status code: {response.status_code})")
                    broken_links_count += 1
                else:
                    print(f"{url} là liên kết hợp lệ")
                    valid_links_count += 1
            
            except requests.exceptions.RequestException as e:
                print(f"Lỗi khi kiểm tra {url}: {e}")

    # In kết quả tổng số liên kết hợp lệ và lỗi
    print(f"Tổng số liên kết hợp lệ: {valid_links_count}")
    print(f"Tổng số liên kết lỗi: {broken_links_count}")

    # Kiểm tra nếu có bất kỳ liên kết nào bị lỗi, thực hiện assert False
    assert broken_links_count == 0, f"Có {broken_links_count} liên kết lỗi, kiểm thử thất bại."

# 2. Kiểm tra tất cả các link ở thanh Category
def test_category_links(driver):
    driver.get("https://demo.opencart.com/")
    
    # Đợi trang tải đầy đủ
    time.sleep(10)
    driver.refresh()
    time.sleep(10)
    driver.refresh()
    time.sleep(10)
    # Lấy các phần tử <div> chứa danh mục sản phẩm
    navbar_menu = driver.find_element(By.ID, "narbar-menu")
    
    # Lấy tất cả các liên kết <a> bên trong phần tử menu
    links = navbar_menu.find_elements(By.TAG_NAME, "a")
    print(f"Tổng số liên kết tìm thấy trong menu: {len(links)}")

    # Biến đếm số lượng liên kết hợp lệ và liên kết lỗi
    valid_links_count = 0
    broken_links_count = 0

    # Duyệt qua các liên kết và kiểm tra tính hợp lệ của chúng
    for link in links:
        url = link.get_attribute("href")
        print(f"Kiểm tra: {url}")

        # Kiểm tra nếu URL rỗng hoặc không hợp lệ
        if url is None or url == "":
            print("URL không được cấu hình cho thẻ anchor hoặc rỗng")
            continue

        # Chỉ kiểm tra các liên kết thuộc miền demo.opencart.com
        if not url.startswith("https://demo.opencart.com"):
            print(f"URL thuộc về domain khác, bỏ qua: {url}")
            continue

        try:
            time.sleep(3)
            # Gửi yêu cầu HTTP HEAD để kiểm tra liên kết
            response = requests.head(url, allow_redirects=True)
            
            if response.status_code >= 400:
                print(f"{url} là liên kết lỗi (status code: {response.status_code})")
                broken_links_count += 1
            else:
                print(f"{url} là liên kết hợp lệ")
                valid_links_count += 1
        
        except requests.exceptions.RequestException as e:
            print(f"Lỗi khi kiểm tra {url}: {e}")
            broken_links_count += 1

    # In kết quả tổng số liên kết hợp lệ và lỗi
    print(f"Tổng số liên kết hợp lệ: {valid_links_count}")
    print(f"Tổng số liên kết lỗi: {broken_links_count}")

    # Kiểm tra nếu có bất kỳ liên kết nào bị lỗi, thực hiện assert False
    assert broken_links_count == 0, f"Có {broken_links_count} liên kết lỗi, kiểm thử thất bại."


# Results: PS C:\Users\ADMIN\OneDrive\Desktop\Daihoc\HK I 24 - 25\Testing\assignment2_2\links> pytest -s .\test_links.py
# ============================================================================================================ test session starts ============================================================================================================
# platform win32 -- Python 3.12.6, pytest-8.3.3, pluggy-1.5.0
# rootdir: C:\Users\ADMIN\OneDrive\Desktop\Daihoc\HK I 24 - 25\Testing\assignment2_2\links
# plugins: anyio-4.6.2.post1
# collected 2 items

# test_links.py
# DevTools listening on ws://127.0.0.1:52721/devtools/browser/c9bb8fed-f674-45f9-be61-95d336b8dd2c
# Created TensorFlow Lite XNNPACK delegate for CPU.
# Attempting to use a delegate that only supports static-sized tensors with a graph that has dynamic-sized tensors (tensor#58 is a dynamic-sized tensor).
# Kiểm tra 15 liên kết trong div: 
#       <div class="col-sm-3">
# ...
# Kiểm tra: https://demo.opencart.com/en-gb/information/terms
# https://demo.opencart.com/en-gb/information/terms là liên kết hợp lệ
# Kiểm tra: https://demo.opencart.com/en-gb/information/delivery
# https://demo.opencart.com/en-gb/information/delivery là liên kết hợp lệ
# Kiểm tra: https://demo.opencart.com/en-gb/information/about-us
# https://demo.opencart.com/en-gb/information/about-us là liên kết hợp lệ
# Kiểm tra: https://demo.opencart.com/en-gb/information/privacy
# https://demo.opencart.com/en-gb/information/privacy là liên kết hợp lệ
# Kiểm tra: https://demo.opencart.com/en-gb?route=information/contact
# https://demo.opencart.com/en-gb?route=information/contact là liên kết hợp lệ
# Kiểm tra: https://demo.opencart.com/en-gb?route=account/returns.add
# https://demo.opencart.com/en-gb?route=account/returns.add là liên kết hợp lệ
# Kiểm tra: https://demo.opencart.com/en-gb?route=information/sitemap
# https://demo.opencart.com/en-gb?route=information/sitemap là liên kết hợp lệ
# Kiểm tra: https://demo.opencart.com/en-gb/brands
# https://demo.opencart.com/en-gb/brands là liên kết hợp lệ
# Kiểm tra: https://demo.opencart.com/en-gb?route=checkout/voucher
# https://demo.opencart.com/en-gb?route=checkout/voucher là liên kết hợp lệ
# Kiểm tra: https://demo.opencart.com/en-gb?route=account/affiliate&customer_token=772486c1c28897214ae3f28aac
# https://demo.opencart.com/en-gb?route=account/affiliate&customer_token=772486c1c28897214ae3f28aac là liên kết hợp lệ
# Kiểm tra: https://demo.opencart.com/en-gb?route=product/special&customer_token=772486c1c28897214ae3f28aac
# https://demo.opencart.com/en-gb?route=product/special&customer_token=772486c1c28897214ae3f28aac là liên kết hợp lệ
# Kiểm tra: https://demo.opencart.com/en-gb?route=account/account&customer_token=772486c1c28897214ae3f28aac
# https://demo.opencart.com/en-gb?route=account/account&customer_token=772486c1c28897214ae3f28aac là liên kết hợp lệ
# Kiểm tra: https://demo.opencart.com/en-gb?route=account/order&customer_token=772486c1c28897214ae3f28aac
# https://demo.opencart.com/en-gb?route=account/order&customer_token=772486c1c28897214ae3f28aac là liên kết hợp lệ
# Kiểm tra: https://demo.opencart.com/en-gb?route=account/wishlist&customer_token=772486c1c28897214ae3f28aac
# https://demo.opencart.com/en-gb?route=account/wishlist&customer_token=772486c1c28897214ae3f28aac là liên kết hợp lệ
# Kiểm tra: https://demo.opencart.com/en-gb?route=account/newsletter&customer_token=772486c1c28897214ae3f28aac
# https://demo.opencart.com/en-gb?route=account/newsletter&customer_token=772486c1c28897214ae3f28aac là liên kết hợp lệ
# Tổng số liên kết hợp lệ: 15
# Tổng số liên kết lỗi: 0
# .
# DevTools listening on ws://127.0.0.1:52980/devtools/browser/2f9ca8e4-0e9d-4a87-98c9-1a34c664e743
# Tổng số liên kết tìm thấy trong menu: 39
# Kiểm tra: https://demo.opencart.com/en-gb/catalog/desktops
# Created TensorFlow Lite XNNPACK delegate for CPU.
# https://demo.opencart.com/en-gb/catalog/desktops là liên kết hợp lệ
# Kiểm tra: https://demo.opencart.com/en-gb/catalog/desktops/pc
# https://demo.opencart.com/en-gb/catalog/desktops/pc là liên kết hợp lệ
# Kiểm tra: https://demo.opencart.com/en-gb/catalog/desktops/mac
# https://demo.opencart.com/en-gb/catalog/desktops/mac là liên kết hợp lệ
# Kiểm tra: https://demo.opencart.com/en-gb/catalog/desktops
# https://demo.opencart.com/en-gb/catalog/desktops là liên kết hợp lệ
# Kiểm tra: https://demo.opencart.com/en-gb/catalog/laptop-notebook
# Attempting to use a delegate that only supports static-sized tensors with a graph that has dynamic-sized tensors (tensor#58 is a dynamic-sized tensor).
# https://demo.opencart.com/en-gb/catalog/laptop-notebook là liên kết hợp lệ
# Kiểm tra: https://demo.opencart.com/en-gb/catalog/laptop-notebook/macs
# https://demo.opencart.com/en-gb/catalog/laptop-notebook/macs là liên kết hợp lệ
# Kiểm tra: https://demo.opencart.com/en-gb/catalog/laptop-notebook/windows
# https://demo.opencart.com/en-gb/catalog/laptop-notebook/windows là liên kết hợp lệ
# Kiểm tra: https://demo.opencart.com/en-gb/catalog/laptop-notebook
# https://demo.opencart.com/en-gb/catalog/laptop-notebook là liên kết hợp lệ
# Kiểm tra: https://demo.opencart.com/en-gb/catalog/component
# https://demo.opencart.com/en-gb/catalog/component là liên kết hợp lệ
# Kiểm tra: https://demo.opencart.com/en-gb/catalog/component/mouse
# https://demo.opencart.com/en-gb/catalog/component/mouse là liên kết hợp lệ
# Kiểm tra: https://demo.opencart.com/en-gb/catalog/component/monitor
# https://demo.opencart.com/en-gb/catalog/component/monitor là liên kết hợp lệ
# Kiểm tra: https://demo.opencart.com/en-gb/catalog/component/printers
# https://demo.opencart.com/en-gb/catalog/component/printers là liên kết hợp lệ
# Kiểm tra: https://demo.opencart.com/en-gb/catalog/component/scanner
# https://demo.opencart.com/en-gb/catalog/component/scanner là liên kết hợp lệ
# Kiểm tra: https://demo.opencart.com/en-gb/catalog/component/web-camera
# https://demo.opencart.com/en-gb/catalog/component/web-camera là liên kết hợp lệ
# Kiểm tra: https://demo.opencart.com/en-gb/catalog/component
# https://demo.opencart.com/en-gb/catalog/component là liên kết hợp lệ
# Kiểm tra: https://demo.opencart.com/en-gb/catalog/tablet
# https://demo.opencart.com/en-gb/catalog/tablet là liên kết hợp lệ
# Kiểm tra: https://demo.opencart.com/en-gb/catalog/software
# https://demo.opencart.com/en-gb/catalog/software là liên kết hợp lệ
# Kiểm tra: https://demo.opencart.com/en-gb/catalog/smartphone
# https://demo.opencart.com/en-gb/catalog/smartphone là liên kết hợp lệ
# Kiểm tra: https://demo.opencart.com/en-gb/catalog/cameras
# https://demo.opencart.com/en-gb/catalog/cameras là liên kết hợp lệ
# Kiểm tra: https://demo.opencart.com/en-gb/catalog/mp3-players
# https://demo.opencart.com/en-gb/catalog/mp3-players là liên kết hợp lệ
# Kiểm tra: https://demo.opencart.com/en-gb/catalog/mp3-players/test-11
# https://demo.opencart.com/en-gb/catalog/mp3-players/test-11 là liên kết hợp lệ
# Kiểm tra: https://demo.opencart.com/en-gb/catalog/mp3-players/test-12
# https://demo.opencart.com/en-gb/catalog/mp3-players/test-12 là liên kết hợp lệ
# Kiểm tra: https://demo.opencart.com/en-gb/catalog/mp3-players/test-15
# https://demo.opencart.com/en-gb/catalog/mp3-players/test-15 là liên kết hợp lệ
# Kiểm tra: https://demo.opencart.com/en-gb/catalog/mp3-players/test-16
# https://demo.opencart.com/en-gb/catalog/mp3-players/test-16 là liên kết hợp lệ
# Kiểm tra: https://demo.opencart.com/en-gb/catalog/mp3-players/test-17
# https://demo.opencart.com/en-gb/catalog/mp3-players/test-17 là liên kết hợp lệ
# Kiểm tra: https://demo.opencart.com/en-gb/catalog/mp3-players/test-18
# https://demo.opencart.com/en-gb/catalog/mp3-players/test-18 là liên kết hợp lệ
# Kiểm tra: https://demo.opencart.com/en-gb/catalog/mp3-players/test-19
# https://demo.opencart.com/en-gb/catalog/mp3-players/test-19 là liên kết hợp lệ
# Kiểm tra: https://demo.opencart.com/en-gb/catalog/mp3-players/test-20
# https://demo.opencart.com/en-gb/catalog/mp3-players/test-20 là liên kết hợp lệ
# Kiểm tra: https://demo.opencart.com/en-gb/catalog/mp3-players/test-21
# https://demo.opencart.com/en-gb/catalog/mp3-players/test-21 là liên kết hợp lệ
# Kiểm tra: https://demo.opencart.com/en-gb/catalog/mp3-players/test-22
# https://demo.opencart.com/en-gb/catalog/mp3-players/test-22 là liên kết hợp lệ
# Kiểm tra: https://demo.opencart.com/en-gb/catalog/mp3-players/test-23
# https://demo.opencart.com/en-gb/catalog/mp3-players/test-23 là liên kết hợp lệ
# Kiểm tra: https://demo.opencart.com/en-gb/catalog/mp3-players/test-24
# https://demo.opencart.com/en-gb/catalog/mp3-players/test-24 là liên kết hợp lệ
# Kiểm tra: https://demo.opencart.com/en-gb/catalog/mp3-players/test-4
# https://demo.opencart.com/en-gb/catalog/mp3-players/test-4 là liên kết hợp lệ
# Kiểm tra: https://demo.opencart.com/en-gb/catalog/mp3-players/test-5
# https://demo.opencart.com/en-gb/catalog/mp3-players/test-5 là liên kết hợp lệ
# Kiểm tra: https://demo.opencart.com/en-gb/catalog/mp3-players/test-6
# https://demo.opencart.com/en-gb/catalog/mp3-players/test-6 là liên kết hợp lệ
# Kiểm tra: https://demo.opencart.com/en-gb/catalog/mp3-players/test-7
# https://demo.opencart.com/en-gb/catalog/mp3-players/test-7 là liên kết hợp lệ
# Kiểm tra: https://demo.opencart.com/en-gb/catalog/mp3-players/test-8
# https://demo.opencart.com/en-gb/catalog/mp3-players/test-8 là liên kết hợp lệ
# Kiểm tra: https://demo.opencart.com/en-gb/catalog/mp3-players/test-9
# https://demo.opencart.com/en-gb/catalog/mp3-players/test-9 là liên kết hợp lệ
# Kiểm tra: https://demo.opencart.com/en-gb/catalog/mp3-players
# https://demo.opencart.com/en-gb/catalog/mp3-players là liên kết hợp lệ
# Tổng số liên kết hợp lệ: 39
# Tổng số liên kết lỗi: 0
# .

# ======================================================================================================= 2 passed in 422.31s (0:07:02) =======================================================================================================