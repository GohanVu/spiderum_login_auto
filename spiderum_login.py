from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
import time
import random
import getpass

def instagram_login():
    # Thiết lập trình điều khiển Chrome với các tùy chọn
    # Options cho phép bạn tùy chỉnh cách Chrome hoạt động
    chrome_options = Options()
    # Bỏ comment dòng dưới đây để chạy Chrome ở chế độ headless (không hiển thị giao diện)
    # chrome_options.add_argument("--headless")
    # Tùy chọn no-sandbox giúp Chrome hoạt động ổn định hơn trong môi trường tự động hóa
    chrome_options.add_argument("--no-sandbox")
    # Tùy chọn disable-dev-shm-usage giúp tránh lỗi khi chạy trên hệ thống có ít bộ nhớ
    chrome_options.add_argument("--disable-dev-shm-usage")
    # Thêm user-agent như người dùng thật
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    try:
        # Khởi tạo trình duyệt Chrome với các tùy chọn đã cấu hình
        driver = webdriver.Chrome(options=chrome_options)
        driver.maximize_window()  # Mở cửa sổ toàn màn hình như người dùng thực
        
        # Mở trang đăng nhập Spiderum
        driver.get("https://auth.spiderum.com/sso")
        # Chờ ngẫu nhiên từ 1-3 giây như người dùng đang xem trang
        random_sleep(1, 3)

        # Tìm các trường đăng nhập
        inputs_username = driver.find_elements(By.XPATH, "//input[@id='name']")
        inputs_password = driver.find_elements(By.XPATH, "//input[@id='password']")

        # Lấy ô nhập tên đăng nhập và mật khẩu
        username_input = inputs_username[0]
        password_input = inputs_password[0]
        
        # Thông tin đăng nhập cố định
        username = "hoangdz1811@gmail.com"
        password = "Hoang@123"

        # Mô phỏng người dùng di chuyển chuột đến ô username
        action = ActionChains(driver)
        action.move_to_element(username_input).perform()
        random_sleep(0.5, 1.5)
        
        # Điền tên đăng nhập với tốc độ ngẫu nhiên
        type_like_human(username_input, username)
        
        # Di chuyển đến ô mật khẩu như người dùng thực
        action.move_to_element(password_input).perform()
        random_sleep(0.5, 1.5)
        
        # Điền mật khẩu với tốc độ ngẫu nhiên
        type_like_human(password_input, password)
        
        # Tạm dừng ngẫu nhiên trước khi nhấn đăng nhập
        random_sleep(0.8, 2)
        
        # Tìm và nhấp vào nút đăng nhập
        login_button = driver.find_element(By.XPATH, "//input[@id='submit-btn']")
        
        # Di chuyển chuột đến nút đăng nhập
        action.move_to_element(login_button).perform()
        random_sleep(0.3, 1)
        
        login_button.click()

        # Chờ đợi phần tử xác nhận đã đăng nhập thành công
        username_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a[href='/logout']"))
        )
        random_sleep(1, 2.5)
        
        # Tìm nút tiếp tục và nhấp vào
        login_continue_list = driver.find_elements(By.XPATH, "//a[@href='https://spiderum.com']")
        login_continue_button = login_continue_list[1]
        
        # Di chuyển chuột đến nút tiếp tục
        action.move_to_element(login_continue_button).perform() 
        random_sleep(0.5, 1.5)
        
        login_continue_button.click()
        random_sleep(1.5, 3)
        
        # Đóng dialog nếu xuất hiện
        close_dialog_button = driver.find_element(By.XPATH, "//div[@id='dialog']//i[contains(@class, 'close-button')]")
        action.move_to_element(close_dialog_button).perform()
        random_sleep(0.3, 1)
        close_dialog_button.click()
        random_sleep(1, 2)
        
        # Nhấp lại nút đăng nhập
        reclick_button = driver.find_element(By.XPATH, "//span[contains(text(), 'Đăng nhập')]/parent::a")
        action.move_to_element(reclick_button).perform()
        random_sleep(0.5, 1.5)
        reclick_button.click()
        
        # Thêm thời gian chờ ở đây (sửa lỗi thiếu time.sleep())
        random_sleep(1, 2)
        
        # Bỏ qua hướng dẫn
        skip_list = driver.find_elements(By.XPATH, "//button[contains(@class, 'button-secondary') and contains(text(), 'Bỏ qua hướng dẫn')] ")
        skip_button = skip_list[0]
        action.move_to_element(skip_button).perform()
        random_sleep(0.5, 1.5)
        skip_button.click()
        
        # Chờ đợi trang tải xong
        random_sleep(2, 5)
        
        # Cuộn trang một chút như người dùng thực
        driver.execute_script("window.scrollBy(0, 300);")
        random_sleep(2, 4)
        driver.execute_script("window.scrollBy(0, 300);")
        random_sleep(1, 3)

    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")
    
    finally:
        # Hỏi người dùng có muốn giữ trình duyệt mở không
        keep_open = input("Bạn có muốn giữ trình duyệt mở không? (y/n): ").lower()
        
        if keep_open != 'y':
            # Đóng trình duyệt và giải phóng tài nguyên
            driver.quit()
            print("Đã đóng trình duyệt")
        else:
            print("Trình duyệt vẫn đang mở. Hãy đóng thủ công khi hoàn tất.")
            input("Nhấn Enter để thoát chương trình...")

def random_sleep(min_time, max_time):
    """Tạm dừng với thời gian ngẫu nhiên trong khoảng cho trước"""
    time.sleep(random.uniform(min_time, max_time))

def type_like_human(element, text):
    """Gõ văn bản với tốc độ ngẫu nhiên như người thật"""
    for char in text:
        element.send_keys(char)
        # Tạm dừng ngẫu nhiên giữa các ký tự 0.05-0.2s
        time.sleep(random.uniform(0.05, 0.2))

if __name__ == "__main__":
    print("Ví dụ Tự động đăng nhập Spiderum")
    print("----------------------------------")
    instagram_login() 