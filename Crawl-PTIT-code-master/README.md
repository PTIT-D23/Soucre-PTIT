# Cào Cốt trên Cốt Pờ Tít (Code PTIT)

Cào cốt đã AC trên <a href="https://code.ptit.edu.vn/">Code PTIT <img style="height: 64px;" src="https://code.ptit.edu.vn/2020/images/logo_ptit.png"></a>

Ví dụ: https://github.com/KiyoGami/Python-PTIT

Chương trình sẽ cào cốt tốt nhất của bạn (theo thời gian, bộ nhớ)

**Note:** Mình làm cái này vì mục đích giúp ae khoá sau sẽ bớt trải nghiệm đau khổ khi gặp mấy bài oái oăm vc =)). Lưu ý là mình chỉ làm trên windows, chưa test trên các hđh khác

## Yêu cầu 
- git
- python 3.6.5+
- pip
- virtualenv

## Cài đặt
1. Tạo một môi trường ảo cho project.
```
virtualenv venv
```

2. Clone mã nguồn.
```
git clone https://github.com/KiyoGami/Crawl-PTIT-code app
```

3. Activate môi trường.
```
./venv/Scripts/activate
```

4. Cài các package cần thiết.
```
(venv) cd app/
(venv) pip install -r requirements.txt
```

5. Tạo các biến môi trường để chương trình có thể lấy được data từ site.

Tạo file '.env' trong thư mục gốc
Và thêm dữ liệu theo cấu trúc dưới đây (Ví dụ: PTIT_username=B20DCCN546, timesleep=60)

```
PTIT_username=<Tên tài khoản của bạn>
PTIT_password=<Mật khẩu>
course=<mã của môn, lấy trong file data.txt nhé>
storage_path=<Path đến folder lưu trữ>
timesleep=<thời gian đợi, mặc định là 60>
timedelay=<khuyên là 1>
timeperten=<tuỳ>
```
**timesleep:** thường khi ta gửi request quá nhiều sẽ bị web cho vào thời gian chờ

6. Chỉnh setting tuỳ chỉnh trong custom_settings.py.
```
CACHE=True/False
```
bật True thì những bài cào rồi sẽ k cào lại nữa

7. Run.
```
(venv) python main.py
```

**Note:** Nếu sleep liên tục thì bạn nên tạm dừng chương trình (Ctrl+C), rồi đợi lúc sau cào tiếp. 

## Nyagami
