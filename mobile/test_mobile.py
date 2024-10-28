import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait,Select
import time
import random


@pytest.fixture
def driver():
    # Cấu hình Chrome ở chế độ mô phỏng thiết bị di động (iPhone X)
    mobile_emulation = { "deviceName": "iPhone X" }
    chrome_options = Options()
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    
    driver = webdriver.Chrome(options=chrome_options)
    yield driver
    driver.quit()

# 1. Kiểm tra đăng nhập trên điện thoại
def test_mobile_login(driver):
    # Truy cập trang chủ
    driver.get("https://demo.opencart.com/")
    #Đợi load trang và xác minh
    time.sleep(10)
    driver.refresh() 
    time.sleep(10)
    driver.refresh()
    time.sleep(10)

    icon_account = driver.find_element(By.XPATH,'/html/body/nav/div/div[2]/ul/li[2]/div/a')
    icon_account.click()
    time.sleep(3)

    login_link = driver.find_element(By.XPATH,'/html/body/nav/div/div[2]/ul/li[2]/div/ul/li[2]/a')
    login_link.click()
    time.sleep(3)

    email_input = driver.find_element(By.ID,'input-email')
    email_input.send_keys('nom@gmail.com')

    password_input = driver.find_element(By.ID, 'input-password')
    password_input.send_keys('password123')

    login_btn = driver.find_element(By.XPATH,'/html/body/main/div[2]/div/div/div/div[2]/div/form/div[3]/button')
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", login_btn)
    time.sleep(3)
    login_btn.click()

    # Chờ và kiểm tra chuyển hướng đến trang tài khoản
    try:
        time.sleep(3)
        current_url = driver.current_url
        assert "route=account/account" in current_url, \
            f"Chuyển hướng đến trang tài khoản thất bại, URL hiện tại là: {current_url}"
        print("Đăng nhập thành công và đã chuyển hướng đến trang tài khoản trên điện thoại.")
    except Exception as e:
        print(f"Đăng nhập thất bại hoặc không có chuyển hướng: {e}")
        assert False, "Đăng nhập thất bại hoặc không có chuyển hướng trên điện thoại."

# 2. Kiểm thử tìm kiếm thành công trên điện thoại
def test_mobile_search_valid_keyword(driver):
    driver.get("https://demo.opencart.com/")
    
    #Đợi load trang và xác minh
    time.sleep(10)
    driver.refresh() 
    time.sleep(10)
    driver.refresh()
    time.sleep(10)

    # Lấy danh sách các sản phẩm từ Featured
    product_names = ['HTC Touch HD', 'iPhone', 'Nikon D300', 'iPod Classic', 'MacBook Air', 'iMac', 'Sony VAIO']

    # Chọn ngẫu nhiên một sản phẩm từ danh sách
    random_product = random.choice(product_names)

    # Bấm vào nút tìm kiếm
    search_button = driver.find_element(By.XPATH, "//button[@class='btn btn-light btn-lg']")
    search_button.click()

    # Nhập từ khóa tìm kiếm
    search_input = driver.find_element(By.ID, "input-search")
    search_input.send_keys(random_product)

    # Nhấn nút "Search"
    driver.find_element(By.ID, "button-search").click()

    time.sleep(3)
    # Kiểm tra kết quả
    try:
        product_list = driver.find_element(By.ID, "product-list")
        assert product_list is not None
        print("Tìm kiếm thành công với từ khóa hợp lệ.")
    except Exception as e:
        print(f"Tìm kiếm thất bại: {e}")
        assert False

# 3.Thêm sản phẩm vào giỏ hàng trên điện thoại
def test_mobile_add_single_product_to_cart(driver):
    # Mở trang OpenCart
    driver.get("https://demo.opencart.com/")
    # Đợi load trang và xác minh
    time.sleep(7)
    driver.refresh() 
    time.sleep(7)
    driver.refresh()
    time.sleep(10)

    # Danh sách sản phẩm
    products = ['HTC Touch HD', 'iPhone', 'Nikon D300', 'iPod Classic', 'MacBook', 'MacBook Air', 'iMac', 'Sony VAIO']
    
    # Chọn ngẫu nhiên một sản phẩm từ danh sách
    selected_product = random.choice(products)

    # Tìm thanh tìm kiếm và nhập tên sản phẩm
    search_input = driver.find_element(By.XPATH, '//*[@id="search"]/input')
    search_input.clear()
    search_input.send_keys(selected_product)
    
    # Tìm và bấm nút tìm kiếm
    search_button = driver.find_element(By.XPATH, '/html/body/header/div/div/div[2]/div/button')
    search_button.click()

    time.sleep(5)

    # Lấy danh sách sản phẩm tìm được
    product_list = driver.find_elements(By.XPATH, '//*[@id="product-list"]/div[@class="col mb-3"]')
    
    # Tìm sản phẩm khớp với tên đã chọn
    for index, product in enumerate(product_list, start=1):
        product_name_element = product.find_element(By.XPATH, f'.//div[@class="description"]/h4/a')
        product_name = product_name_element.text
        if selected_product in product_name:
            # Cuộn đến phần tử "Add to Cart"
            add_to_cart_button = product.find_element(By.XPATH, f'//*[@id="product-list"]/div[{index}]/div/div[2]/form/div/button[1]')
            driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", add_to_cart_button)
            # Chờ phần tử có thể bấm
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="product-list"]/div[{index}]/div/div[2]/form/div/button[1]')))
            # Dùng ActionChains để bấm vào nút
            actions = ActionChains(driver)
            actions.move_to_element(add_to_cart_button).click().perform()
            break

    driver.execute_script("window.scrollTo(0, 0);")

    # Chờ giỏ hàng cập nhật
    time.sleep(5)
    # Kiểm tra giỏ hàng có cập nhật hay không
    cart_status = driver.find_element(By.CSS_SELECTOR, 'button.btn-lg.btn-inverse.btn-block.dropdown-toggle').text
    assert "1 item(s)" in cart_status, f"Số lượng sản phẩm trong giỏ hàng không đúng: {cart_status}"
    print(f"Thêm sản phẩm '{selected_product}' vào giỏ hàng thành công.")


# 4. Kiểm thử checkout (chế độ khách hàng không đăng nhập) trên điện thoại
def test_guest_checkout(driver):
    # Truy cập trang chủ
    driver.get("https://demo.opencart.com/")
    #Đợi load trang và xác minh
    time.sleep(10)
    driver.refresh() 
    time.sleep(10)
    driver.refresh()
    time.sleep(10)

    # Danh sách sản phẩm
    products = ['HTC Touch HD', 'iPhone', 'Nikon D300', 'iPod Classic', 'MacBook Air', 'iMac', 'Sony VAIO']
    
    # Chọn ngẫu nhiên một sản phẩm từ danh sách
    selected_product = random.choice(products)

    time.sleep(3)
    # Tìm thanh tìm kiếm và nhập tên sản phẩm
    search_input = driver.find_element(By.XPATH, '//*[@id="search"]/input')
    search_input.clear()
    search_input.send_keys(selected_product)
    
    # Tìm và bấm nút tìm kiếm
    search_button = driver.find_element(By.XPATH, '/html/body/header/div/div/div[2]/div/button')
    search_button.click()

    time.sleep(3)

    # Lấy danh sách sản phẩm tìm được
    product_list = driver.find_elements(By.XPATH, '//*[@id="product-list"]/div[@class="col mb-3"]')
    
    # Tìm sản phẩm khớp với tên đã chọn
    for index, product in enumerate(product_list, start=1):
        product_name_element = product.find_element(By.XPATH, f'.//div[@class="description"]/h4/a')
        product_name = product_name_element.text
        if selected_product in product_name:
            # Cuộn đến phần tử "Add to Cart"
            add_to_cart_button = product.find_element(By.XPATH, f'//*[@id="product-list"]/div[{index}]/div/div[2]/form/div/button[1]')
            driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", add_to_cart_button)
            # Chờ phần tử có thể bấm
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="product-list"]/div[{index}]/div/div[2]/form/div/button[1]')))
            # Dùng ActionChains để bấm vào nút
            actions = ActionChains(driver)
            actions.move_to_element(add_to_cart_button).click().perform()
            break
    
    driver.execute_script("window.scrollTo(0, 0);")
    # Chờ giỏ hàng cập nhật
    time.sleep(5)

    # Mở trang checkout
    # Dùng ActionChains để bấm vào nút
    actions = ActionChains(driver)
    checkout_link = driver.find_element(By.XPATH, '/html/body/nav/div/div[2]/ul/li[5]/a')
    actions.move_to_element(checkout_link).click().perform()
    
    # Chờ trang checkout tải xong
    time.sleep(3)

    # ChọnGuest Checkout
    form_register = driver.find_element(By.ID,'form-register')

    radio_input_guest = form_register.find_element(By.ID,'input-guest')
    radio_input_guest.click()

    # Điền các thồng tin cần thiết
    first_name = form_register.find_element(By.ID, 'input-firstname')
    first_name.send_keys('test')

    last_name = form_register.find_element(By.ID,'input-lastname')
    last_name.send_keys('test')

    email_in = form_register.find_element(By.ID,'input-email')
    email_in.send_keys('test@gmail.com')

    address_1 = form_register.find_element(By.ID,'input-shipping-address-1')
    address_1.send_keys('test')

    city_in = form_register.find_element(By.ID,'input-shipping-city')
    city_in.send_keys('test')

    post_code_in = form_register.find_element(By.ID,'input-shipping-postcode')
    post_code_in.send_keys('test')

    region_select = form_register.find_element(By.ID,'input-shipping-zone')
    Select(region_select).select_by_index(1)

    time.sleep(3)

    # Bám tiếp tục
    continue_register = form_register.find_element(By.ID,'button-register')
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", continue_register)
    continue_register.click()
    time.sleep(10)
    # Chọn phương thức giao hàng
    shipping_method_button = driver.find_element(By.ID, 'button-shipping-methods')
    # Dùng ActionChains để bấm vào nút
    actions = ActionChains(driver)
    actions.move_to_element(shipping_method_button).click().perform()

    time.sleep(3)

    # Tìm form và bấm nút "Continue"
    shipping_form = driver.find_element(By.ID, 'form-shipping-method')
    radio_shipping_method = shipping_form.find_element(By.ID, 'input-shipping-method-flat-flat')
    radio_shipping_method.click()
    continue_button_shipping = shipping_form.find_element(By.ID, 'button-shipping-method')
    continue_button_shipping.click()

    time.sleep(2)

    # Chọn phương thức thanh toán
    payment_method_button = driver.find_element(By.ID, 'button-payment-methods')
    payment_method_button.click()
    time.sleep(2)

    # Tìm form và bấm nút "Continue"
    payment_form = driver.find_element(By.ID, 'form-payment-method')
    radio_payment_method = payment_form.find_element(By.ID,'input-payment-method-cod-cod')
    radio_payment_method.click()
    continue_button_payment = payment_form.find_element(By.ID, 'button-payment-method')
    continue_button_payment.click()


    time.sleep(2)

    # Bấm nút "Confirm Order"
    confirm_order_button = driver.find_element(By.ID, 'button-confirm')
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", confirm_order_button)
    time.sleep(3)
    confirm_order_button.click()

    # Chờ trang xác nhận hoàn tất
    time.sleep(5)

    # Kiểm tra URL của trang xác nhận thành công
    current_url = driver.current_url
    assert current_url == "https://demo.opencart.com/en-gb?route=checkout/success", f"URL không đúng: {current_url}"

    print("Checkout thành công với chế độ khách hàng không đăng nhập.")
   

# Results: PS C:\Users\ADMIN\OneDrive\Desktop\Daihoc\HK I 24 - 25\Testing\assignment2_2\mobile> pytest -s .\test_mobile.py
# ========================================================================================================== short test summary info ========================================================================================================== 
# FAILED test_mobile.py::test_guest_checkout - selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element: {"method":"css selector","selector":"[id="form-register"]"}
# ================================================================================================== 1 failed, 3 passed in 206.62s (0:03:26) ==================================================================================================