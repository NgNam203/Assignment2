import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
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

# 1.Thêm một sản phẩm vào giỏ hàng 
def test_add_single_product_to_cart(driver):
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

    # Chờ giỏ hàng cập nhật
    time.sleep(5)

    # Kiểm tra giỏ hàng có cập nhật hay không
    cart_status = driver.find_element(By.CSS_SELECTOR, 'button.btn-lg.btn-inverse.btn-block.dropdown-toggle').text
    assert "1 item(s)" in cart_status, f"Số lượng sản phẩm trong giỏ hàng không đúng: {cart_status}"
    print(f"Thêm sản phẩm '{selected_product}' vào giỏ hàng thành công.")

# 2.Thêm nhiều sản phẩm khác nhau vào giỏ hàng
def test_add_multiple_products_to_cart(driver):
    # Mở trang OpenCart
    driver.get("https://demo.opencart.com/")
    time.sleep(7)
    driver.refresh() 
    time.sleep(7)
    driver.refresh()
    time.sleep(10)

    # Danh sách sản phẩm có sẵn
    products = ['HTC Touch HD', 'iPhone', 'Nikon D300', 'iPod Classic', 'MacBook', 'MacBook Air', 'iMac', 'Sony VAIO']

    # Thực hiện random từ 2 đến 8 để lấy ra số lượng sản phẩm cần thêm
    num_products_to_add = random.randint(2, 8)

    # Thực hiện random để chọn những sản phẩm cần mua
    selected_products = random.sample(products, num_products_to_add)

    # Thêm từng sản phẩm vào giỏ hàng
    for product_name in selected_products:
        # Tìm thanh tìm kiếm và nhập tên sản phẩm
        search_input = driver.find_element(By.XPATH, '//*[@id="search"]/input')
        # Cuộn đến thanh tìm kiếm
        driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", search_input)
        search_input.clear()
        search_input.send_keys(product_name)

        # Bấm nút tìm kiếm
        search_button = driver.find_element(By.XPATH, '/html/body/header/div/div/div[2]/div/button')

        time.sleep(3)
        # Dùng ActionChains để bấm nút tìm kiếm
        actions = ActionChains(driver)
        actions.move_to_element(search_button).click().perform()
        time.sleep(3)

        # Lấy danh sách sản phẩm tìm được
        product_list = driver.find_elements(By.XPATH, '//*[@id="product-list"]/div[@class="col mb-3"]')

        # Tìm sản phẩm khớp với tên đã chọn và bấm "Add to Cart"
        for index, product in enumerate(product_list, start=1):
            product_name_element = product.find_element(By.XPATH, './/div[@class="description"]/h4/a')
            found_product_name = product_name_element.text
            if product_name in found_product_name:
                # Cuộn đến phần tử "Add to Cart"
                add_to_cart_button = product.find_element(By.XPATH, f'//*[@id="product-list"]/div[{index}]/div/div[2]/form/div/button[1]')
                driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", add_to_cart_button)

                # Chờ phần tử có thể bấm được
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="product-list"]/div[{index}]/div/div[2]/form/div/button[1]')))
                
                # Dùng ActionChains để bấm vào nút
                actions = ActionChains(driver)
                actions.move_to_element(add_to_cart_button).click().perform()
                time.sleep(5)
                break

    # Mở trang giỏ hàng
    cart_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'route=checkout/cart')]"))
    )
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", cart_link)
    actions.move_to_element(cart_link).click().perform()
    time.sleep(5)

    # Lấy danh sách sản phẩm trong giỏ hàng
    cart_items = driver.find_elements(By.XPATH, '//*[@id="shopping-cart"]//tbody/tr')

    # Kiểm tra các sản phẩm đã thêm có trong giỏ hàng không
    cart_product_names = [item.find_element(By.XPATH, './td[@class="text-start text-wrap"]/a').text for item in cart_items]

    # Thực hiện assert để kiểm tra
    for product in selected_products:
        assert product in cart_product_names, f"Sản phẩm '{product}' không có trong giỏ hàng"

    print(f"Đã thêm thành công {num_products_to_add} sản phẩm vào giỏ hàng: {selected_products}")

# 3. Thêm cùng một sản phẩm nhiều lần vào giỏ hàng và kiểm tra số tiền
def test_add_same_product_multiple_times(driver):
    # Mở trang OpenCart
    driver.get("https://demo.opencart.com/")
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
            
            # Số lần bấm ngẫu nhiên vào nút "Add to Cart"
            random_clicks = random.randint(2, 5)
            print(f"Số lần bấm ngẫu nhiên vào '{product_name}': {random_clicks}")

            # Dùng vòng lặp để bấm ngẫu nhiên số lần vào nút "Add to Cart"
            for _ in range(random_clicks):
                actions.move_to_element(add_to_cart_button).click().perform()
                time.sleep(5)  # Tạm dừng ngắn giữa các lần bấm để mô phỏng tương tác tự nhiên
            break

    # Chờ giỏ hàng cập nhật
    time.sleep(5)

    # Mở trang giỏ hàng
    cart_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'route=checkout/cart')]"))
    )
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", cart_link)
    actions = ActionChains(driver)
    actions.move_to_element(cart_link).click().perform()
    time.sleep(5)

    # Lấy danh sách sản phẩm trong giỏ hàng
    cart_items = driver.find_elements(By.XPATH, '//*[@id="shopping-cart"]//tbody/tr')

    # Tìm sản phẩm đã thêm vào giỏ hàng
    for item in cart_items:
        cart_product_name = item.find_element(By.XPATH, './td[@class="text-start text-wrap"]/a').text
        if selected_product in cart_product_name:
            # Lấy số lượng của sản phẩm trong giỏ hàng
            quantity_element = item.find_element(By.XPATH, './td[@class="text-start"]/form/div/input[@name="quantity"]')
            cart_quantity = int(quantity_element.get_attribute('value'))

            # Lấy đơn giá của sản phẩm
            unit_price_element = item.find_element(By.XPATH, './td[@class="text-end"]')
            unit_price = float(unit_price_element.text.replace('$', '').replace(',', ''))

            # Lấy tổng số tiền của sản phẩm
            total_price_element = item.find_element(By.XPATH, './td[@class="text-end"][last()]')
            total_price = float(total_price_element.text.replace('$', '').replace(',', ''))

            # Kiểm tra số lượng có khớp với số lần bấm ngẫu nhiên
            assert cart_quantity == random_clicks, f"Số lượng trong giỏ hàng không đúng: {cart_quantity}, kỳ vọng: {random_clicks}"

            # Kiểm tra tổng số tiền có đúng (đơn giá * số lượng)
            expected_total_price = unit_price * random_clicks
            assert total_price == expected_total_price, f"Tổng số tiền không đúng: {total_price}, kỳ vọng: {expected_total_price}"

            print(f"Sản phẩm '{selected_product}' có số lượng: {cart_quantity}, tổng số tiền: {total_price} (Kỳ vọng: {expected_total_price})")
            break

# 4. Thêm các sản phẩm với số lượng cụ thể vào giỏ hàng và kiểm tra tổng số tiền
def test_add_products_with_quantity(driver):

    # Mở trang OpenCart
    driver.get("https://demo.opencart.com/")
    time.sleep(7)
    driver.refresh() 
    time.sleep(7)
    driver.refresh()
    time.sleep(10)

    # Danh sách sản phẩm và số lượng cần thêm
    products_with_quantity = {
        'MacBook': 2,
        'iPhone': 3,
        'Nikon D300': 1
    }

    # Thêm từng sản phẩm với số lượng cụ thể vào giỏ hàng
    for product_name, quantity in products_with_quantity.items():
        # Tìm thanh tìm kiếm và nhập tên sản phẩm
        search_input = driver.find_element(By.XPATH, '//*[@id="search"]/input')
       # Cuộn đến thanh tìm kiếm
        driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", search_input)
        search_input.clear()
        search_input.send_keys(product_name)

        # Bấm nút tìm kiếm
        search_button = driver.find_element(By.XPATH, '/html/body/header/div/div/div[2]/div/button')
        driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", search_button)
        actions = ActionChains(driver)
        actions.move_to_element(search_button).click().perform()

        time.sleep(5)

        # Lấy danh sách sản phẩm tìm được
        product_list = driver.find_elements(By.XPATH, '//*[@id="product-list"]/div[@class="col mb-3"]')

        # Tìm sản phẩm khớp với tên đã chọn
        for index, product in enumerate(product_list, start=1):
            product_name_element = product.find_element(By.XPATH, f'.//div[@class="description"]/h4/a')
            found_product_name = product_name_element.text
            if product_name in found_product_name:
                # Cuộn đến phần tử "Add to Cart"
                add_to_cart_button = product.find_element(By.XPATH, f'//*[@id="product-list"]/div[{index}]/div/div[2]/form/div/button[1]')
                driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", add_to_cart_button)

                # Chờ phần tử có thể bấm được
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="product-list"]/div[{index}]/div/div[2]/form/div/button[1]')))
                # Dùng ActionChains để bấm vào nút
                actions = ActionChains(driver)
                # Thêm sản phẩm với số lượng cụ thể vào giỏ hàng
                for _ in range(quantity):
                    actions.move_to_element(add_to_cart_button).click().perform()
                    time.sleep(2)  # Tạm dừng giữa các lần bấm để mô phỏng tương tác tự nhiên
                break

    # Chờ giỏ hàng cập nhật
    time.sleep(5)

    # Mở trang giỏ hàng
    cart_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'route=checkout/cart')]"))
    )
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", cart_link)
    actions.move_to_element(cart_link).click().perform()
    time.sleep(5)

    # Lấy danh sách sản phẩm trong giỏ hàng
    cart_items = driver.find_elements(By.XPATH, '//*[@id="shopping-cart"]//tbody/tr')

    total_calculated = 0  # Tổng số tiền tính toán dựa trên sản phẩm đã thêm

    # Kiểm tra các sản phẩm đã thêm có trong giỏ hàng và tính tổng số tiền
    for item in cart_items:
        cart_product_name = item.find_element(By.XPATH, './td[@class="text-start text-wrap"]/a').text

        # Tìm sản phẩm trong giỏ hàng
        for product_name, quantity in products_with_quantity.items():
            if product_name in cart_product_name:
                # Lấy số lượng của sản phẩm trong giỏ hàng
                quantity_element = item.find_element(By.XPATH, './td[@class="text-start"]/form/div/input[@name="quantity"]')
                cart_quantity = int(quantity_element.get_attribute('value'))

                # Lấy đơn giá của sản phẩm
                unit_price_element = item.find_element(By.XPATH, './td[@class="text-end"]')
                unit_price = float(unit_price_element.text.replace('$', '').replace(',', ''))

                # Lấy tổng số tiền của sản phẩm
                total_price_element = item.find_element(By.XPATH, './td[@class="text-end"][last()]')
                total_price = float(total_price_element.text.replace('$', '').replace(',', ''))

                # Kiểm tra số lượng có khớp với số lượng đã chọn
                assert cart_quantity == quantity, f"Số lượng trong giỏ hàng không đúng: {cart_quantity}, kỳ vọng: {quantity}"

                # Kiểm tra tổng số tiền có đúng (đơn giá * số lượng)
                expected_total_price = unit_price * quantity
                assert total_price == expected_total_price, f"Tổng số tiền không đúng: {total_price}, kỳ vọng: {expected_total_price}"

                total_calculated += total_price
                print(f"Sản phẩm '{product_name}' có số lượng: {cart_quantity}, tổng số tiền: {total_price} (Kỳ vọng: {expected_total_price})")
                break

    # Kiểm tra tổng số tiền tính toán với tổng số tiền hiển thị
    total_displayed_element = driver.find_element(By.XPATH, '//*[@id="checkout-total"]/tr[last()]/td[@class="text-end"]')
    total_displayed = float(total_displayed_element.text.replace('$', '').replace(',', ''))
    assert total_calculated == total_displayed, f"Tổng số tiền tính toán: {total_calculated}, hiển thị: {total_displayed}"

    print(f"Tổng số tiền trong giỏ hàng chính xác: {total_displayed}")



# ========================================================================================================== short test summary info ==========================================================================================================
# FAILED test_add_to_cart.py::test_add_same_product_multiple_times - AssertionError: Tổng số tiền không đúng: 4802.0, kỳ vọng: 4808.0
# FAILED test_add_to_cart.py::test_add_products_with_quantity - AssertionError: Tổng số tiền không đúng: 1202.0, kỳ vọng: 1204.0
# ================================================================================================== 2 failed, 2 passed in 250.39s (0:04:10) ================================================================================================== 

