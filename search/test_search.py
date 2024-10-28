import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random



@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

#Lấy danh sách tên sản phẩm từ Featured.
def get_product_names(driver):
    product_names = []
    try:
        # Đợi cho đến khi các phần tử sản phẩm xuất hiện
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@class='description']/h4/a"))
        )
        # Lấy tất cả các phần tử tên sản phẩm
        product_elements = driver.find_elements(By.XPATH, "//div[@class='description']/h4/a")
        
        # Duyệt qua các phần tử và thêm tên sản phẩm vào danh sách
        for product in product_elements:
            product_names.append(product.text)
    except Exception as e:
        print(f"Lỗi khi lấy tên sản phẩm: {e}")
    
    return product_names
#Lấy danh sách các mô tả sản phẩm từ Featured
def get_product_descriptions(driver):
    product_descriptions = []
    try:
        # Đợi cho đến khi các phần tử mô tả sản phẩm xuất hiện
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@class='description']/p"))
        )
        # Lấy tất cả các phần tử mô tả sản phẩm
        description_elements = driver.find_elements(By.XPATH, "//div[@class='description']/p")
        
        # Duyệt qua các phần tử và thêm tối đa 6 từ từ mỗi mô tả vào danh sách
        for description in description_elements:
            full_text = description.text
            # Chia mô tả thành các từ và chỉ lấy tối đa 5 từ
            words = full_text.split()
            truncated_text = ' '.join(words[:5])  # Lấy tối đa 5 từ
            product_descriptions.append(truncated_text)
    except Exception as e:
        print(f"Lỗi khi lấy mô tả sản phẩm: {e}")
    
    return product_descriptions

# 1. Kiểm thử tìm kiếm thành công với từ khóa hợp lệ
def test_search_valid_keyword(driver):
    driver.get("https://demo.opencart.com/")
    
    #Đợi load trang và xác minh
    time.sleep(10)
    driver.refresh() 
    time.sleep(10)
    driver.refresh()
    time.sleep(10)

    # Lấy danh sách các sản phẩm từ Featured
    product_names = get_product_names(driver)

    # Kiểm tra nếu danh sách sản phẩm không trống
    assert len(product_names) > 0

    # Chọn ngẫu nhiên một sản phẩm từ danh sách
    random_product = random.choice(product_names)

    # Bấm vào nút tìm kiếm
    search_button = driver.find_element(By.XPATH, "//button[@class='btn btn-light btn-lg']")
    search_button.click()

    time.sleep(3)
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

# 2. Kiểm thử tìm kiếm thất bại với từ khóa không hợp lệ
def test_search_invalid_keyword(driver):
    driver.get("https://demo.opencart.com/")

    #Đợi load trang và xác minh
    time.sleep(10)
    driver.refresh() 
    time.sleep(10)
    driver.refresh()
    time.sleep(10)
    
    # Bấm vào nút tìm kiếm
    search_button = driver.find_element(By.XPATH, "//button[@class='btn btn-light btn-lg']")
    search_button.click()

    time.sleep(3)
    # Nhập từ khóa tìm kiếm
    search_input = driver.find_element(By.ID, "input-search")
    search_input.send_keys("@$%*-")

    # Nhấn nút "Search"
    driver.find_element(By.ID, "button-search").click()

    time.sleep(3)
    # Kiểm tra kết quả
    try:
        no_product_message = driver.find_element(By.XPATH, "/html/body/main/div[2]/div/div/p")
        assert "There is no product that matches the search criteria." in no_product_message.text
        print("Thông báo hiển thị đúng khi không tìm thấy sản phẩm.")
    except Exception as e:
        print(f"Tìm kiếm thất bại: {e}")
        assert False

# 3. Tìm kiếm với tùy chọn tìm kiếm trong mô tả sản phẩm
def test_search_in_description(driver):
    driver.get("https://demo.opencart.com/")
    
    #Đợi load trang và xác minh
    time.sleep(10)
    driver.refresh() 
    time.sleep(10)
    driver.refresh()
    time.sleep(10)

    # Lấy danh sách mô tả sản phẩm từ trang HTML
    product_descriptions = get_product_descriptions(driver)

    # Kiểm tra nếu danh sách mô tả sản phẩm không trống
    assert len(product_descriptions) > 0

    # Chọn ngẫu nhiên một mô tả từ danh sách
    random_description = random.choice(product_descriptions)

    # Bấm vào nút tìm kiếm
    search_button = driver.find_element(By.XPATH, "//button[@class='btn btn-light btn-lg']")
    search_button.click()

    # Nhập từ khóa tìm kiếm
    search_input = driver.find_element(By.ID, "input-search")
    search_input.send_keys(random_description )

    # Tích chọn vào ô "Search in product descriptions"
    description_checkbox = driver.find_element(By.ID, "input-description")
    description_checkbox.click()

    # Nhấn nút "Search"
    driver.find_element(By.ID, "button-search").click()
    time.sleep(5)
    # Kiểm tra kết quả
    try:
        # Chờ đợi kết quả xuất hiện
        product_list = driver.find_element(By.ID, "product-list")
        assert product_list is not None
        print("Tìm kiếm với mô tả sản phẩm thành công.")
    except Exception as e:
        print(f"Tìm kiếm với mô tả sản phẩm thất bại: {e}")
        assert False, "Không tìm thấy sản phẩm trong mô tả."

# # 4. Tìm kiếm trong một danh mục cụ thể
def test_search_in_specific_category(driver):
    driver.get("https://demo.opencart.com/")
    
    #Đợi load trang và xác minh
    time.sleep(10)
    driver.refresh() 
    time.sleep(10)
    driver.refresh()
    time.sleep(10)

    # Bấm vào nút tìm kiếm
    search_button = driver.find_element(By.XPATH, "//button[@class='btn btn-light btn-lg']")
    search_button.click()


    # Nhập từ khóa tìm kiếm
    search_input = driver.find_element(By.ID, "input-search")
    search_input.send_keys("a")

    # Chọn danh mục từ menu thả xuống
    category_dropdown = driver.find_element(By.ID, "input-category")
    for option in category_dropdown.find_elements(By.TAG_NAME, 'option'):
        if option.text.strip() == "Desktops":
            option.click()
            break

    # Nhấn nút "Search"
    driver.find_element(By.ID, "button-search").click()

    time.sleep(3)
    # Kiểm tra kết quả
    try:
        # Chờ đợi kết quả xuất hiện
        product_list = driver.find_element(By.ID, "product-list")
        assert product_list is not None
        print("Tìm kiếm trong danh mục 'Desktops' thành công.")
    except Exception as e:
        print(f"Tìm kiếm trong danh mục 'Desktops' thất bại: {e}")
        assert False


# Results: PS C:\Users\ADMIN\OneDrive\Desktop\Daihoc\HK I 24 - 25\Testing\assignment2_2\search> pytest -s .\test_search.py
# ============================================================================================================ test session starts ============================================================================================================
# platform win32 -- Python 3.12.6, pytest-8.3.3, pluggy-1.5.0
# rootdir: C:\Users\ADMIN\OneDrive\Desktop\Daihoc\HK I 24 - 25\Testing\assignment2_2\search
# plugins: anyio-4.6.2.post1
# collected 4 items

# test_search.py
# DevTools listening on ws://127.0.0.1:56247/devtools/browser/77667538-abe3-459f-b915-a87fee471f03
# Created TensorFlow Lite XNNPACK delegate for CPU.
# Attempting to use a delegate that only supports static-sized tensors with a graph that has dynamic-sized tensors (tensor#58 is a dynamic-sized tensor).
# Tìm kiếm thành công với từ khóa hợp lệ.
# .
# DevTools listening on ws://127.0.0.1:56336/devtools/browser/1295fe31-8696-458a-8f37-70b4634a7fca
# Created TensorFlow Lite XNNPACK delegate for CPU.
# Attempting to use a delegate that only supports static-sized tensors with a graph that has dynamic-sized tensors (tensor#58 is a dynamic-sized tensor).
# Thông báo hiển thị đúng khi không tìm thấy sản phẩm.
# .
# DevTools listening on ws://127.0.0.1:56422/devtools/browser/f1a06451-ec36-4ba6-bc3c-e52691dd3533
# Created TensorFlow Lite XNNPACK delegate for CPU.
# Attempting to use a delegate that only supports static-sized tensors with a graph that has dynamic-sized tensors (tensor#58 is a dynamic-sized tensor).
# Tìm kiếm với mô tả sản phẩm thành công.
# .
# DevTools listening on ws://127.0.0.1:56504/devtools/browser/6fa00e6a-7319-4eb9-8d80-303dc0c77411
# Created TensorFlow Lite XNNPACK delegate for CPU.
# Attempting to use a delegate that only supports static-sized tensors with a graph that has dynamic-sized tensors (tensor#58 is a dynamic-sized tensor).
# Tìm kiếm trong danh mục 'Desktops' thành công.
# .

# ======================================================================================================= 4 passed in 189.47s (0:03:09) ======================================================================================================= 