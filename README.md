# MemriseRobot

MemriseRobot là một chương trình python giúp bổ sung **audio** và **pronunciation** cho các khóa học từ vựng trên Memrise.

## 1. Hướng dẫn sử dụng

Bước 1: Thêm người dùng **memrise.robot** là cộng tác viên của khóa học. 

![them cong tac vien](./assets/cvt.png)

Bước 2: Tải và cài đặt chương trình.

Tải chương trình:
```
git clone https://github.com/hieubkset/MemriseRobot.git
```

Cài đặt các thư viện phụ thuộc:
```
pip install requirements.txt
```

Bước 3: Tải chương trình chromedriver

_Từ phiên bản selenium v4.6.0 không cần tải đã tích hợp sẵn chromedriver, do đó nếu dùng selenium >= 4.6.0 không cần thực hiện bước này._

Truy cập trang web https://chromedriver.chromium.org/downloads, tải **ChromeDriver** phiên bản mới nhất tương ứng với hệ điều hành. 

![chromedriver](./assets/chromedriver.png)

Sau đó, lưu **ChromeDriver** vào thư mục trong dự án. Cụ thể:
+ chrome/linux: cho hệ điều hành linux
+ chrome/macos: cho hệ điều hành macos
+ chrome/windows: cho hệ điều hành windows

Bước 4: Thay đổi các giá trị cấu hình
```
if __name__ == "__main__":
    start_page = 1
    language_code = 'en-US'
    url = "https://app.memrise.com/course/6235501/pmp/edit/database/7281972/"
    memrise_upload(url, start_page, language_code)
```
Trong đó:
+ start_page: thiết lập giá trị này để bỏ qua các page đã có audio để rút ngắn thời gian xử lý, giá trị mặc định là 1.
+ language_code: chọn một trong hai giá trị _en-US_ (Anh Mỹ) hoặc _en-BE_ (Anh Anh).
+ url: đường dẫn tới khóa học, lưu ý phải có chữ _database_ trong đường dẫn mới đúng.

