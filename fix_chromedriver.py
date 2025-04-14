import os
import re
import urllib.request
import zipfile
import subprocess
import sys

def get_chrome_version():
    """Tìm phiên bản Chrome đang cài đặt trên Windows"""
    try:
        # Đường dẫn thông thường đến Chrome trên Windows
        paths = [
            r'C:\Program Files\Google\Chrome\Application\chrome.exe',
            r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
            os.path.expanduser(r'~\AppData\Local\Google\Chrome\Application\chrome.exe')
        ]
        
        for path in paths:
            if os.path.exists(path):
                # Sử dụng PowerShell để lấy thông tin phiên bản
                output = subprocess.check_output(
                    f'powershell -command "(Get-Item \'{path}\').VersionInfo.FileVersion"',
                    shell=True
                )
                version = output.decode('utf-8').strip()
                # Lấy phần major version (vd: 115.0.5790.171 -> 115)
                major_version = version.split('.')[0]
                return version, major_version
                
        print("Không tìm thấy Chrome. Vui lòng cài đặt Chrome trước.")
        return None, None
        
    except Exception as e:
        print(f"Lỗi khi xác định phiên bản Chrome: {e}")
        return None, None

def download_chromedriver(major_version):
    """Tải ChromeDriver tương ứng với phiên bản Chrome"""
    try:
        base_url = "https://chromedriver.storage.googleapis.com"
        
        # Tạo thư mục drivers nếu chưa tồn tại
        os.makedirs("drivers", exist_ok=True)
        
        # Lấy danh sách các phiên bản ChromeDriver có sẵn
        version_url = f"{base_url}/LATEST_RELEASE_{major_version}"
        response = urllib.request.urlopen(version_url)
        driver_version = response.read().decode('utf-8').strip()
        
        print(f"Đang tải ChromeDriver phiên bản {driver_version}...")
        
        # Tải ChromeDriver cho Windows
        download_url = f"{base_url}/{driver_version}/chromedriver_win32.zip"
        zip_path = os.path.join("drivers", "chromedriver.zip")
        urllib.request.urlretrieve(download_url, zip_path)
        
        # Giải nén file
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall("drivers")
        
        # Xóa file zip
        os.remove(zip_path)
        
        chromedriver_path = os.path.join("drivers", "chromedriver.exe")
        print(f"ChromeDriver đã được tải xuống tại: {os.path.abspath(chromedriver_path)}")
        return True
        
    except Exception as e:
        print(f"Lỗi khi tải ChromeDriver: {e}")
        return False

def main():
    print("Công cụ sửa lỗi ChromeDriver")
    print("============================")
    
    chrome_version, major_version = get_chrome_version()
    
    if chrome_version:
        print(f"Phiên bản Chrome đã phát hiện: {chrome_version}")
        print(f"Major version: {major_version}")
        
        if download_chromedriver(major_version):
            print("\nHƯỚNG DẪN:")
            print("1. Đã tải ChromeDriver phù hợp với Chrome của bạn")
            print("2. Bây giờ bạn có thể chạy 'python instagram_login.py'")
            print("3. Script sẽ sử dụng ChromeDriver từ thư mục 'drivers'")
    else:
        print("Không thể tiếp tục. Vui lòng cài đặt Chrome trước.")

if __name__ == "__main__":
    main() 