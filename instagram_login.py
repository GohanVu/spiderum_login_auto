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
import pyotp

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
        
        # Mở trang đăng nhập Instagram
        driver.get("https://www.instagram.com/")
        
        # Tạo mã OTP từ mã 2FA trước khi bắt đầu quá trình đăng nhập
        totp = pyotp.TOTP("43S6NNTF4FCDCN3NDSV4JBCZ5SZDYYCQ")
        six_digit_code = totp.now()

        # Thông tin đăng nhập
        username = "itein0rqtnrfnye539"
        password = "AUcVIt3f1232"

        # Tìm và điền thông tin đăng nhập
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@name='username'] | //input[@type='text']"))
        )
        # Tìm các trường input
        inputs_username = driver.find_elements(By.XPATH, "//input[@name='username'] | //input[@type='text']")
        inputs_password = driver.find_elements(By.XPATH, "//input[@name='password'] | //input[@type='password']")
        
        # Lấy ô nhập tên đăng nhập và mật khẩu
        username_input = inputs_username[0]
        password_input = inputs_password[0]
        random_sleep(0.5, 1.5)
        # Điền thông tin đăng nhập
        type_like_human(username_input, username)
        random_sleep(0.5, 1.5)
        type_like_human(password_input, password)
        
        # Nhấn nút đăng nhập
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
        )
        random_sleep(0.5, 1.5)
        login_button.click()
        
        # Chờ và điền mã xác thực
        verification_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@name='verificationCode']"))
        )
        random_sleep(0.5, 1.5)
        type_like_human(verification_input, six_digit_code)
        
        # Nhấn nút xác nhận
        confirm_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Confirm')]"))
        )
        random_sleep(0.5, 1.5)
        confirm_button.click()
        
        # Chờ đăng nhập thành công
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@style, 'transform: translateX(0px)')]"))
            )
            print("Đăng nhập thành công!")
        except:
            print("Đăng nhập không thành công!")
            
        # Chờ đợi trang tải xong
        random_sleep(2, 3)
        
        #Tìm thanh tìm kiếm và nhập từ khóa tìm kiếm
        search_input = driver.find_element(By.XPATH, "//div[@class='x1iyjqo2 xh8yej3']/div[2]")
        random_sleep(0.5, 1)
        search_input.click()
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='text']"))
        )
        search_input = driver.find_element(By.XPATH, "//input[@type='text']")
        random_sleep(0.5, 1)
        type_like_human(search_input, "ufc")
        random_sleep(0.5, 1)
        
        # Chờ đợi kết quả tìm kiếm xuất hiện
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'x6s0dn4')]"))
        )
        random_sleep(1, 2)
        search_output_lists = driver.find_elements(By.XPATH, "//div[contains(@class, 'x6s0dn4')]//div[contains(@class, 'x9f619')]//a | //div[contains(@class, 'x6s0dn4')]/div[contains(@class, 'x9f619') and contains(@class, 'x78zum5')]/a[@role='link']")
        random_sleep(0.5, 1)
        target_search_output = search_output_lists[0]
        random_sleep(0.5, 1)
        target_search_output.click()
        random_sleep(0.5, 1)
        
        # Cuộn xuống 3 lần
        for i in range(3):
            # Cuộn xuống 1000px mỗi lần
            driver.execute_script("window.scrollBy(0, 1000);")
            random_sleep(0.8, 1.5)
            
        # Cuộn lên 3 lần
        for i in range(3):
            # Cuộn lên 1000px mỗi lần 
            driver.execute_script("window.scrollBy(0, -1000);")
            random_sleep(0.8, 1.5)
        
            
        
        
        
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
        time.sleep(random.uniform(0.05, 0.15))  # Giảm thời gian chờ giữa các ký tự

if __name__ == "__main__":
    print("Ví dụ Tự động đăng nhập Instagram")
    print("----------------------------------")
    instagram_login()