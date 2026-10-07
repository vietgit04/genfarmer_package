# GenFarmer Automation Guide

Tài liệu hướng dẫn tự động hoá **Facebook, Instagram, TikTok**, dựng lại từ 3 file PDF "Hướng dẫn sử dụng tự động hoá" theo đúng giao diện của GenFarmer Support Center.

- **File để gửi / deploy:** `dist/genfarmer-automation-guide.html`. Đây là một file HTML duy nhất, đã nhúng sẵn toàn bộ ảnh, mở trực tiếp hoặc kéo thả lên Netlify là chạy.
- **4 ngôn ngữ:** English (mặc định), Tiếng Việt, Español, 日本語. Đổi bằng nút 🌐 trên header; lựa chọn được lưu lại cho lần sau.
- **22 trang × 4 ngôn ngữ**, 30 chức năng, 172 ảnh chụp màn hình (đã bỏ ảnh trùng, nén 1400px / JPEG q82).

## Đường dẫn

Mỗi trang có link riêng, có thể kèm ngôn ngữ và mục:

```
#/fb-trust                 trang, theo ngôn ngữ đang chọn
#/vi/fb-trust              trang, ép tiếng Việt
#/ja/tt-boost/seed_live    nhảy thẳng tới một chức năng
```

## Cấu trúc

```
content/
  common.py      giao diện, câu dùng chung, thư viện trường cấu hình (Device threads, API key VILAO, ...)
  platforms.py   dữ liệu từng nền tảng: link APK, package, chức năng, trường, ảnh của từng bước
  pages.py       chữ của từng trang: tiêu đề, mô tả, nội dung
template/
  style.css      CSS lấy nguyên từ Support Center
  icons.svg      bộ icon SVG của Support Center
  app.js         router đa ngôn ngữ, tìm kiếm, mục lục, đổi giao diện sáng/tối
images/          ảnh chụp màn hình, đặt tên theo mã hash của ảnh gốc trong PDF
images/brand/    logo, biểu tượng, ảnh bìa lấy từ Support Center
build.py         ghép tất cả thành dist/genfarmer-automation-guide.html
```

Mọi đoạn chữ đều nằm trong `content/*.py`, dạng `L(en, vi, es, ja)`, nên sửa một câu thì sửa đủ 4 ngôn ngữ ở cùng một chỗ.

## Build lại

Cần Python 3 và Pillow (`pip install pillow`).

```
python3 build.py
```

## Những chỗ khác với PDF

- Phần **Thêm tài khoản vào Account Manager** giống nhau ở cả 3 PDF nên được gộp thành một trang dùng chung. Dạng tài khoản TikTok dùng Hotmail/Outlook cũng nằm trong trang này.
- Phần **tải package** (bước 1–2 lặp lại 3 lần trong PDF) được gộp: mở Store một lần, sau đó làm bước 3–4 cho từng package.
- **Tên mục trong menu RUN** lấy theo ảnh chụp app, không theo chữ trong PDF. Ví dụ PDF ghi chức năng *Join group* của Facebook chọn "SEEDING, FOLLOW USER", nhưng ảnh chụp cho thấy mục đúng là `Join group`.
- Sửa lỗi chính tả và lỗi chép nhầm giữa các bản: "trân thực" → "chân thực"; trường ảnh đại diện Instagram ghi "tiktok"; trường Topic của *Post Video* TikTok ghi "phiên livestream"; *Post group* ghi "bình luận mẫu" thay vì "bài viết mẫu"; một số bước tham chiếu sai số bước.
- Thêm 3 trang tra cứu sinh tự động từ dữ liệu: bảng tra chức năng, các trường cấu hình (kèm chức năng nào dùng), và cách chuẩn bị file text.
