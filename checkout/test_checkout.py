import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import random

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


# 1. Kiểm thử checkout khi người dùng đã đăng nhập
def test_checkout_with_logged_in_user(driver):
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

    # Chờ giỏ hàng cập nhật
    time.sleep(5)

    # Mở trang checkout
    checkout_link = driver.find_element(By.XPATH, '/html/body/nav/div/div[2]/ul/li[5]/a')
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", checkout_link)
    time.sleep(2)
    checkout_link.click()

     # Chờ trang checkout tải xong
    time.sleep(5)

    # Ở phần "Shipping Address" tích chọn 'I want to use an existing address'
    existing_address_radio = driver.find_element(By.ID, 'input-shipping-existing')
    existing_address_radio.click()
    
    # Chọn địa chỉ giao hàng từ danh sách có sẵn
    shipping_address_select = driver.find_element(By.ID, 'input-shipping-address')
    Select(shipping_address_select).select_by_index(1)  # Chọn địa chỉ có sẵn đầu tiên

    time.sleep(2)

    # Chọn phương thức giao hàng
    shipping_method_button = driver.find_element(By.ID, 'button-shipping-methods')
    shipping_method_button.click()
    time.sleep(2)

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

    print("Checkout thành công với người dùng đã đăng nhập.")


# 2. Kiểm thử checkout với chế độ khách hàng không đăng nhập
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

    # Chờ giỏ hàng cập nhật
    time.sleep(5)

    # Mở trang checkout
    checkout_link = driver.find_element(By.XPATH, '/html/body/nav/div/div[2]/ul/li[5]/a')
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", checkout_link)
    time.sleep(2)
    checkout_link.click()

    # Chờ trang checkout tải xong
    time.sleep(5)

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

    time.sleep(2)

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
   


# 3. Kiểm thử checkout với việc thêm địa chỉ giao hàng mới
def test_checkout_with_new_shipping_address(driver):
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

    # Chờ giỏ hàng cập nhật
    time.sleep(5)

    # Mở trang checkout
    checkout_link = driver.find_element(By.XPATH, '/html/body/nav/div/div[2]/ul/li[5]/a')
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", checkout_link)
    time.sleep(2)
    checkout_link.click()

     # Chờ trang checkout tải xong
    time.sleep(5)

    # Ở phần "Shipping Address" tích chọn 'I want to use a new address'
    existing_address_radio = driver.find_element(By.ID, 'input-shipping-new')
    existing_address_radio.click()

    time.sleep(2)

    first_name = driver.find_element(By.ID, 'input-shipping-firstname')
    first_name.send_keys('test')

    last_name = driver.find_element(By.ID, 'input-shipping-lastname')
    last_name.send_keys('test')

    address_1 = driver.find_element(By.ID, 'input-shipping-address-1')
    address_1.send_keys('test')

    city = driver.find_element(By.ID,'input-shipping-city')
    city.send_keys('test')

    post_code = driver.find_element(By.ID, 'input-shipping-postcode')
    post_code.send_keys('test')

    region_select = driver.find_element(By.ID,'input-shipping-zone')
    Select(region_select).select_by_index(1)


    time.sleep(2)

    # Bám tiếp tục
    continue_register = driver.find_element(By.ID,'button-shipping-address')
    continue_register.click()

    time.sleep(2)

    # Chọn phương thức giao hàng
    shipping_method_button = driver.find_element(By.ID, 'button-shipping-methods')
    shipping_method_button.click()
    time.sleep(2)

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

    print("Checkout thành công với người dùng đã đăng nhập.")

# 4. Kiểm thử checkout thanh toán không hợp lệ khi bỏ trống phương thức thanh toán, giao hàng
def test_checkout_with_invalid_payment_information(driver):
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

    # Chờ giỏ hàng cập nhật
    time.sleep(5)

    # Mở trang checkout
    checkout_link = driver.find_element(By.XPATH, '/html/body/nav/div/div[2]/ul/li[5]/a')
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", checkout_link)
    time.sleep(2)
    checkout_link.click()

    # Chờ trang checkout tải xong
    time.sleep(5)

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
    time.sleep(3)

    # Bấm nút "Confirm Order"
    confirm_order_button = driver.find_element(By.XPATH, '/html/body/main/div[2]/div/div/div/div[2]/div[3]/div[2]/div/button')
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", confirm_order_button)
    is_disabled = confirm_order_button.get_attribute("disabled")
    time.sleep(3)
     
    assert is_disabled is not None,"Confirm Order không bị disabled."

    print("Nút Confirm Order bị disabled")
   

# Results: PS C:\Users\ADMIN\OneDrive\Desktop\Daihoc\HK I 24 - 25\Testing\assignment2_2\checkout> pytest -s .\test_checkout.py
# ============================================================================================================ test session starts ============================================================================================================
# platform win32 -- Python 3.12.6, pytest-8.3.3, pluggy-1.5.0
# rootdir: C:\Users\ADMIN\OneDrive\Desktop\Daihoc\HK I 24 - 25\Testing\assignment2_2\checkout
# plugins: anyio-4.6.2.post1
# collected 4 items

# test_checkout.py
# DevTools listening on ws://127.0.0.1:64804/devtools/browser/119332eb-4bc1-4d47-bf26-b8400dc51883
# Created TensorFlow Lite XNNPACK delegate for CPU.
# Attempting to use a delegate that only supports static-sized tensors with a graph that has dynamic-sized tensors (tensor#58 is a dynamic-sized tensor).
# Checkout thành công với người dùng đã đăng nhập.
# .
# DevTools listening on ws://127.0.0.1:64950/devtools/browser/dd1c8117-b796-4412-8c52-82d921078d62
# Created TensorFlow Lite XNNPACK delegate for CPU.
# Attempting to use a delegate that only supports static-sized tensors with a graph that has dynamic-sized tensors (tensor#58 is a dynamic-sized tensor).
# Checkout thành công với chế độ khách hàng không đăng nhập.
# .
# DevTools listening on ws://127.0.0.1:65097/devtools/browser/f8be4b83-0985-402c-b7d4-e4e37c768b44
# Created TensorFlow Lite XNNPACK delegate for CPU.
# Attempting to use a delegate that only supports static-sized tensors with a graph that has dynamic-sized tensors (tensor#58 is a dynamic-sized tensor).
# Checkout thành công với người dùng đã đăng nhập.
# .
# DevTools listening on ws://127.0.0.1:65364/devtools/browser/acb64529-74c2-4f52-88a9-ce863fb15323
# Created TensorFlow Lite XNNPACK delegate for CPU.
# Attempting to use a delegate that only supports static-sized tensors with a graph that has dynamic-sized tensors (tensor#58 is a dynamic-sized tensor).
# Nút Confirm Order bị disabled
# .

# ======================================================================================================= 4 passed in 347.97s (0:05:47) ======================================================================================================= 


