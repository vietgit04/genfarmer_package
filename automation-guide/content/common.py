"""Shared strings for the automation guide, in every language.

Each text is a dict keyed by language code. Use L(en, vi, es, ja) to build one.
Placeholders in braces ({p}, {pkg}, {label}, {x}, {f}, {n}) are filled by build.py.
Inline markup allowed: <strong>, <em>, <code>, <a>.
"""

LANGS = ["en", "vi", "es", "ja"]
DEFAULT_LANG = "en"
LANG_NAMES = {"en": "English", "vi": "Tiếng Việt", "es": "Español", "ja": "日本語"}
HTML_LANG = {"en": "en", "vi": "vi", "es": "es", "ja": "ja"}

VERSION = "1.0"
UPDATED = {"en": "Last updated 10/2026", "vi": "Cập nhật lần cuối 10/2026",
           "es": "Última actualización 10/2026", "ja": "最終更新 2026/10"}

SUPPORT_URL = "https://radiant-dieffenbachia-91a57d.netlify.app/#/home"


def L(en, vi, es, ja):
    return {"en": en, "vi": vi, "es": es, "ja": ja}


# ---------------------------------------------------------------- interface

UI = {
    "brand_sub": L("Automation Guide", "Hướng dẫn tự động hoá", "Guía de automatización", "自動化ガイド"),
    "search": L("Search...", "Tìm kiếm...", "Buscar...", "検索..."),
    "search_ph": L("Search the automation guide...", "Tìm trong tài liệu...", "Buscar en la guía...", "ガイド内を検索..."),
    "no_result": L("No result for", "Không có kết quả cho", "Sin resultados para", "該当なし："),
    "support": L("Support Center", "Trung tâm hỗ trợ", "Centro de soporte", "サポートセンター"),
    "on_page": L("On this page", "Trong trang này", "En esta página", "このページの内容"),
    "prev": L("Previous", "Trang trước", "Anterior", "前へ"),
    "next": L("Next", "Trang sau", "Siguiente", "次へ"),
    "theme": L("Switch theme", "Đổi giao diện sáng/tối", "Cambiar tema", "テーマを切り替え"),
    "lang": L("Language", "Ngôn ngữ", "Idioma", "言語"),
    "menu": L("Open navigation", "Mở menu", "Abrir navegación", "メニューを開く"),
    "version": L("Version {v} · 10/2026", "Phiên bản {v} · 10/2026", "Versión {v} · 10/2026", "バージョン {v} · 2026/10"),
    "doc_title": L("GenFarmer Automation Guide", "Hướng dẫn tự động hoá GenFarmer",
                   "Guía de automatización GenFarmer", "GenFarmer 自動化ガイド"),
    "col_field": L("Field", "Trường", "Campo", "項目"),
    "col_enter": L("What to enter", "Nhập gì", "Qué introducir", "入力内容"),
    "col_page": L("Page", "Trang", "Página", "ページ"),
    "col_covers": L("What it covers", "Nội dung", "Qué cubre", "内容"),
    "col_value": L("Value", "Giá trị", "Valor", "値"),
    "col_meaning": L("Meaning", "Ý nghĩa", "Significado", "意味"),
    "col_package": L("Package", "Package", "Paquete", "パッケージ"),
    "col_function": L("Function", "Chức năng", "Función", "機能"),
    "col_menu": L("Item in the RUN menu", "Mục trong menu RUN", "Opción del menú RUN", "RUN メニューの項目"),
    "col_does": L("What it does", "Làm gì", "Qué hace", "内容"),
    "col_used_by": L("Used by", "Dùng ở", "Lo usan", "使用する機能"),
    "col_platform": L("Platform", "Nền tảng", "Plataforma", "プラットフォーム"),
    "features": L("What the script does", "Tính năng của script", "Qué hace el script", "スクリプトの機能"),
    "notes": L("Important notes", "Lưu ý quan trọng", "Notas importantes", "重要な注意事項"),
    "open_pkg": L("Open the package", "Mở package", "Abrir el paquete", "パッケージを開く"),
    "functions": L("{n} functions", "{n} chức năng", "{n} funciones", "{n} 個の機能"),
    "fn_label": L("Function {n}", "Chức năng {n}", "Función {n}", "機能 {n}"),
    "optional": L("Optional.", "Có thể bỏ trống.", "Opcional.", "省略可。"),
}

TABS = {
    "start": L("Start here", "Bắt đầu", "Empezar", "はじめに"),
    "fb": L("Facebook", "Facebook", "Facebook", "Facebook"),
    "ig": L("Instagram", "Instagram", "Instagram", "Instagram"),
    "tt": L("TikTok", "TikTok", "TikTok", "TikTok"),
    "ref": L("Reference", "Tra cứu", "Referencia", "リファレンス"),
}

# ---------------------------------------------------------------- phrases used by many pages

P = {
    # checks every script asks for
    "chk_net": L("Check the internet connection before running the script.",
                 "Kiểm tra kết nối internet trước khi chạy script.",
                 "Comprueba la conexión a internet antes de ejecutar el script.",
                 "スクリプトを実行する前に、インターネット接続を確認してください。"),
    "chk_acc": L("Make sure the {p} accounts work normally, to avoid errors.",
                 "Đảm bảo tài khoản {p} hoạt động bình thường để tránh lỗi.",
                 "Asegúrate de que las cuentas de {p} funcionan con normalidad para evitar errores.",
                 "エラーを防ぐため、{p} アカウントが正常に使える状態か確認してください。"),
    "chk_proxy": L("Check the proxy and the time on each device, so that both are accurate.",
                   "Kiểm tra proxy và thời gian trên thiết bị để đảm bảo tính chính xác.",
                   "Comprueba el proxy y la hora de cada dispositivo para que ambos sean correctos.",
                   "各端末のプロキシと時刻が正しいか確認してください。"),
    "chk_lang": L("Make sure the {p} app language is set to English.",
                  "Đảm bảo ngôn ngữ của {p} đã được chuyển sang tiếng Anh.",
                  "Asegúrate de que el idioma de la app de {p} está en inglés.",
                  "{p} アプリの表示言語が英語になっていることを確認してください。"),
    "one_acc": L("<strong>When you are starting out, log in one account per device.</strong> Only log the next account into a device once the system runs stably.",
                 "<strong>Mới đầu sử dụng, bạn nên đăng nhập mỗi thiết bị một tài khoản.</strong> Sau khi hệ thống chạy ổn định mới đăng nhập tài khoản tiếp theo vào thiết bị.",
                 "<strong>Al empezar, inicia sesión con una sola cuenta por dispositivo.</strong> Añade la siguiente cuenta a un dispositivo solo cuando el sistema funcione de forma estable.",
                 "<strong>使い始めは、1 台の端末に 1 アカウントだけログインしてください。</strong>システムが安定して動くようになってから、次のアカウントを端末にログインさせます。"),

    # opening of every script
    "s_am": L("Choose <strong>ACCOUNT MANAGER</strong>.", "Chọn mục <strong>ACCOUNT MANAGER</strong>.",
              "Elige <strong>ACCOUNT MANAGER</strong>.", "<strong>ACCOUNT MANAGER</strong> を選びます。"),
    "s_table": L("Choose your {p} account table.", "Chọn bảng tài khoản {p} tương ứng.",
                 "Elige tu tabla de cuentas de {p}.", "{p} アカウントのテーブルを選びます。"),
    "s_setup": L("Choose <strong>SETUP AUTOMATION</strong>.", "Chọn mục <strong>SETUP AUTOMATION</strong>.",
                 "Elige <strong>SETUP AUTOMATION</strong>.", "<strong>SETUP AUTOMATION</strong> を選びます。"),
    "s_select": L("Choose <strong>{pkg}</strong>, then click <strong>Select</strong>.",
                  "Chọn chức năng <strong>{pkg}</strong>, tiếp theo chọn <strong>Select</strong>.",
                  "Elige <strong>{pkg}</strong> y haz clic en <strong>Select</strong>.",
                  "<strong>{pkg}</strong> を選び、<strong>Select</strong> をクリックします。"),
    "s_config": L("Choose <strong>Config app</strong> to configure the data.",
                  "Chọn mục <strong>Config app</strong> để cấu hình dữ liệu.",
                  "Elige <strong>Config app</strong> para configurar los datos.",
                  "<strong>Config app</strong> を選んでデータを設定します。"),

    # body of every function
    "s_fill": L("Enter the data for the system", "Nhập dữ liệu cho hệ thống",
                "Introduce los datos para el sistema", "システムにデータを入力します"),
    "s_save": L("Click <strong>SAVE</strong>.", "Chọn <strong>SAVE</strong>.",
                "Haz clic en <strong>SAVE</strong>.", "<strong>SAVE</strong> をクリックします。"),
    "s_rows": L("Click the row numbers in the table to select the devices.",
                "Chọn vào ô thứ tự trong bảng để chọn các thiết bị.",
                "Haz clic en los números de fila de la tabla para seleccionar los dispositivos.",
                "テーブルの行番号をクリックして、実行する端末を選択します。"),
    "s_run": L("Hover over <strong>RUN</strong>, then choose <code>{label}</code>.",
               "Di chuột vào mục <strong>RUN</strong>, sau đó chọn <code>{label}</code>.",
               "Pasa el ratón por <strong>RUN</strong> y elige <code>{label}</code>.",
               "<strong>RUN</strong> にマウスを合わせ、<code>{label}</code> を選びます。"),
    "s_watch": L("Now go back to the <strong>CONTROL CENTER</strong> screen of the GenFarmer app to watch the function run.",
                 "Bây giờ, quay trở về màn hình <strong>CONTROL CENTER</strong> của app GenFarmer để xem chức năng hoạt động.",
                 "Ahora vuelve a la pantalla <strong>CONTROL CENTER</strong> de la app GenFarmer para ver la función en marcha.",
                 "GenFarmer アプリの <strong>CONTROL CENTER</strong> 画面に戻り、機能が動いている様子を確認します。"),

    # Facebook custom-column steps
    "s_gear": L("Click the <strong>settings icon</strong>, then choose <strong>New Field</strong>.",
                "Chọn <strong>biểu tượng cài đặt</strong>, tiếp theo chọn <strong>New Field</strong>.",
                "Haz clic en el <strong>icono de ajustes</strong> y elige <strong>New Field</strong>.",
                "<strong>設定アイコン</strong>をクリックし、<strong>New Field</strong> を選びます。"),
    "s_addf": L("Add the field <code>{f}</code> if it is not there yet, then click <strong>Confirm</strong>.",
                "Thêm trường <code>{f}</code> nếu chưa có, sau đó nhấn <strong>Confirm</strong>.",
                "Añade el campo <code>{f}</code> si todavía no existe y haz clic en <strong>Confirm</strong>.",
                "<code>{f}</code> 項目がまだなければ追加し、<strong>Confirm</strong> をクリックします。"),
    "w_addf": L("The field name must be exactly <code>{f}</code>.",
                "Phải thêm đúng tên trường: <code>{f}</code>.",
                "El nombre del campo debe ser exactamente <code>{f}</code>.",
                "項目名は必ず <code>{f}</code> と正確に入力してください。"),
    "s_copy_img": L("Copy the path of an image, or of the folder holding your images.",
                    "Copy đường dẫn ảnh hoặc folder chứa các hình ảnh của bạn.",
                    "Copia la ruta de una imagen o de la carpeta que contiene tus imágenes.",
                    "画像、または画像を入れたフォルダーのパスをコピーします。"),
    "s_copy_name": L("Copy the names you prepared.", "Copy các name mà bạn đã chuẩn bị sẵn.",
                     "Copia los nombres que preparaste.", "用意しておいた名前をコピーします。"),
    "s_paste": L("Find the <code>{f}</code> column you added in step 4, then paste what you copied into it.",
                 "Tìm cột <code>{f}</code> vừa thêm ở bước 4, sau đó paste dữ liệu vừa copy vào cột này.",
                 "Busca la columna <code>{f}</code> que añadiste en el paso 4 y pega en ella lo que copiaste.",
                 "手順 4 で追加した <code>{f}</code> 列を探し、コピーした内容を貼り付けます。"),
}

# ---------------------------------------------------------------- configuration fields
# name: label shown in the Config app form (same in every language) or a dict per language.
# Placeholders: {p} platform, {x} the data being updated (name, bio, username).

X_WORD = {
    # singular, plural
    "name": {"en": ("name", "names"), "vi": ("name", "name"), "es": ("nombre", "nombres"), "ja": ("名前", "名前")},
    "bio": {"en": ("bio", "bios"), "vi": ("bi-o", "bi-o"), "es": ("biografía", "biografías"), "ja": ("自己紹介（bio）", "自己紹介（bio）")},
    "username": {"en": ("username", "usernames"), "vi": ("username", "username"),
                 "es": ("nombre de usuario", "nombres de usuario"), "ja": ("ユーザー名", "ユーザー名")},
}

FIELDS = {
    "threads": {
        "name": "Device threads",
        "d": L("The number of devices you want to use.", "Số thiết bị bạn muốn sử dụng.",
               "El número de dispositivos que quieres usar.", "使用する端末の台数。")},
    "apikey": {
        "name": "API key VILAO",
        "d": L("The API the AI uses to generate data for the system, such as topics and comments. Without an API key, the system uses its default data.",
               "API mà AI dùng để tạo dữ liệu cho hệ thống như chủ đề, bình luận… Nếu không có API key, hệ thống sẽ dùng các dữ liệu mặc định.",
               "La API que usa la IA para generar datos para el sistema, como temas y comentarios. Sin API key, el sistema usa sus datos predeterminados.",
               "AI がトピックやコメントなどのデータを生成するための API。API キーがない場合は、既定のデータが使われます。")},
    "apikey_caption": {
        "name": "API key VILAO",
        "d": L("The API the AI uses to generate data for the system, such as topics, comments and captions. Without an API key, the system uses its default data.",
               "API mà AI dùng để tạo dữ liệu cho hệ thống như chủ đề, bình luận, caption… Nếu không có API key, hệ thống sẽ dùng các dữ liệu mặc định.",
               "La API que usa la IA para generar datos para el sistema, como temas, comentarios y textos de publicación. Sin API key, el sistema usa sus datos predeterminados.",
               "AI がトピック、コメント、キャプションなどのデータを生成するための API。API キーがない場合は、既定のデータが使われます。")},
    "language": {
        "name": "Language",
        "d": L("The language of the content you want the AI to generate.", "Ngôn ngữ của dữ liệu mà bạn muốn AI tạo ra.",
               "El idioma del contenido que quieres que genere la IA.", "AI に生成させるデータの言語。")},
    "topic_nurture": {
        "name": "Topic",
        "d": L("The topics you want to warm the accounts up on. Separate topics with <code>|</code>.",
               "Chủ đề mà bạn muốn nuôi các tài khoản. Mỗi chủ đề cách nhau bằng dấu <code>|</code>.",
               "Los temas sobre los que quieres calentar las cuentas. Separa los temas con <code>|</code>.",
               "アカウントを育成したいトピック。複数ある場合は <code>|</code> で区切ります。")},
    "aiguide": {
        "name": "AI-Guided Comment",
        "d": L("Guide comments that show the AI what kind of comments to write, so that interactions look more natural. Without an API key, the system uses these comments at random. Separate comments with <code>|</code>.",
               "Các bình luận định hướng để AI nhận biết và tạo ra bình luận trông chân thực hơn trong quá trình tương tác. Nếu không dùng API key, hệ thống sẽ dùng ngẫu nhiên các bình luận định hướng này. Mỗi bình luận cách nhau bằng dấu <code>|</code>.",
               "Comentarios guía que muestran a la IA qué tipo de comentarios escribir, para que las interacciones parezcan más naturales. Sin API key, el sistema usa estos comentarios al azar. Separa los comentarios con <code>|</code>.",
               "AI にどんなコメントを書かせたいかを示すガイド用コメント。やり取りをより自然に見せるために使われます。API キーがない場合は、これらのコメントがランダムに使われます。コメントは <code>|</code> で区切ります。")},
    "action_rate": {
        "name": "Action Rate",
        "d": L("Sets the random rate of each action during interaction: heart, comment, share and save.",
               "Tuỳ chỉnh tỉ lệ ngẫu nhiên của các hành động trong quá trình tương tác: thả tim, bình luận, chia sẻ, lưu.",
               "Ajusta la probabilidad aleatoria de cada acción durante la interacción: corazón, comentario, compartir y guardar.",
               "やり取り中の各アクション（ハート、コメント、シェア、保存）のランダムな実行率を設定します。")},
    "topic_related": {
        "name": "Topic",
        "d": L("Topics related to your videos, posts or profile. The AI uses them to generate more realistic data.",
               "Chủ đề liên quan tới các video, bài viết hoặc trang cá nhân của bạn. AI dựa vào các chủ đề này để tạo ra dữ liệu chân thực hơn.",
               "Temas relacionados con tus vídeos, publicaciones o perfil. La IA los usa para generar datos más realistas.",
               "あなたの動画・投稿・プロフィールに関連するトピック。AI はこれを基に、より自然なデータを生成します。")},
    "topic_interest": {
        "name": "Topic",
        "d": L("The topics you are interested in. The AI uses them to generate more realistic data.",
               "Chủ đề mà bạn đang quan tâm. AI dựa vào dữ liệu này để tạo ra các dữ liệu chân thực hơn.",
               "Los temas que te interesan. La IA los usa para generar datos más realistas.",
               "関心のあるトピック。AI はこれを基に、より自然なデータを生成します。")},
    "topic_ai": {
        "name": "Topic",
        "d": L("The topics you want the AI to generate data about. Separate topics with <code>|</code>.",
               "Chủ đề mà bạn muốn AI tạo ra các dữ liệu. Mỗi chủ đề cách nhau bằng dấu <code>|</code>.",
               "Los temas sobre los que quieres que la IA genere datos. Separa los temas con <code>|</code>.",
               "AI にデータを生成させたいトピック。複数ある場合は <code>|</code> で区切ります。")},
    "topic_reup": {
        "name": "Topic",
        "d": L("The topics the accounts search to find related videos to re-upload. Separate topics with <code>|</code>.",
               "Chủ đề mà bạn muốn các tài khoản tìm kiếm các video liên quan để reup. Mỗi chủ đề cách nhau bằng dấu <code>|</code>.",
               "Los temas que las cuentas buscan para encontrar vídeos relacionados que volver a subir. Separa los temas con <code>|</code>.",
               "アカウントが再投稿用の関連動画を探すためのトピック。複数ある場合は <code>|</code> で区切ります。")},
    "topic_msg": {
        "name": "Topic",
        "d": L("Topics related to the content of your message. The AI uses them to generate more realistic data.",
               "Chủ đề liên quan tới nội dung tin nhắn của bạn. AI dựa vào các chủ đề này để tạo ra dữ liệu chân thực hơn.",
               "Temas relacionados con el contenido de tu mensaje. La IA los usa para generar datos más realistas.",
               "メッセージの内容に関連するトピック。AI はこれを基に、より自然なデータを生成します。")},
    "topic_media": {
        "name": "Topic",
        "d": L("Topics related to the videos and images you want to post. The AI uses them to generate more realistic data.",
               "Chủ đề liên quan tới nội dung video, hình ảnh muốn đăng của bạn. AI dựa vào các chủ đề này để tạo ra dữ liệu chân thực hơn.",
               "Temas relacionados con los vídeos e imágenes que quieres publicar. La IA los usa para generar datos más realistas.",
               "投稿したい動画・画像の内容に関連するトピック。AI はこれを基に、より自然なデータを生成します。")},
    "topic_live": {
        "name": "Topic",
        "d": L("Topics related to the content of your livestream. The AI uses them to generate more realistic data.",
               "Chủ đề liên quan tới nội dung phiên livestream của bạn. AI dựa vào các chủ đề này để tạo ra dữ liệu chân thực hơn.",
               "Temas relacionados con el contenido de tu directo. La IA los usa para generar datos más realistas.",
               "ライブ配信の内容に関連するトピック。AI はこれを基に、より自然なデータを生成します。")},
    "topic_videos": {
        "name": "Topic",
        "d": L("Topics related to the videos you post. The AI uses them to generate more realistic data.",
               "Chủ đề liên quan tới nội dung các video bạn đăng. AI dựa vào các chủ đề này để tạo ra dữ liệu chân thực hơn.",
               "Temas relacionados con los vídeos que publicas. La IA los usa para generar datos más realistas.",
               "投稿する動画に関連するトピック。AI はこれを基に、より自然なデータを生成します。")},
    "links_posts": {
        "name": L("Post links", "Link bài viết", "Enlaces de publicaciones", "投稿リンク"),
        "d": L("The links of the videos or posts to interact with. Enter only video or post links, no other kind of link. You can enter several, one link per line.",
               "Link các video / bài viết muốn tương tác. Chỉ nhập link video / bài viết, không nhập các loại link khác. Có thể nhập nhiều link, mỗi link một dòng.",
               "Los enlaces de los vídeos o publicaciones con los que interactuar. Introduce solo enlaces de vídeos o publicaciones, ningún otro tipo. Puedes introducir varios, uno por línea.",
               "やり取りしたい動画・投稿のリンク。動画・投稿以外のリンクは入力しないでください。1 行に 1 リンクで、複数入力できます。")},
    "links_profiles": {
        "name": L("Profile links", "Link trang cá nhân", "Enlaces de perfiles", "プロフィールリンク"),
        "d": L("The links of the profiles to interact with. Enter only profile links, no other kind of link. One link per line.",
               "Link các trang cá nhân muốn tương tác. Chỉ nhập link profile, không nhập các loại link khác. Mỗi link một dòng.",
               "Los enlaces de los perfiles con los que interactuar. Introduce solo enlaces de perfiles, ningún otro tipo. Un enlace por línea.",
               "やり取りしたいプロフィールのリンク。プロフィール以外のリンクは入力しないでください。1 行に 1 リンクです。")},
    "live_link": {
        "name": L("Livestream link", "Link livestream", "Enlace del directo", "ライブ配信リンク"),
        "d": L("The link of the livestream to interact with. Enter only a livestream link, and only one.",
               "Link livestream bạn muốn tương tác. Chỉ nhập link livestream, nhập duy nhất một link.",
               "El enlace del directo con el que interactuar. Introduce solo un enlace de directo, y solo uno.",
               "やり取りしたいライブ配信のリンク。ライブ配信のリンクを 1 つだけ入力します。")},
    "views_per": {
        "name": L("Views per link", "Số view mỗi link", "Visualizaciones por enlace", "リンクあたりの再生数"),
        "d": L("The number of views each account (one phone) adds to each link.",
               "Số view bạn muốn một tài khoản (một điện thoại) tăng cho một link.",
               "El número de visualizaciones que cada cuenta (un teléfono) añade a cada enlace.",
               "1 アカウント（1 台の端末）が 1 つのリンクに加える再生数。")},
    "views_per_opt": {
        "name": L("Views per link", "Số view mỗi link", "Visualizaciones por enlace", "リンクあたりの再生数"),
        "d": L("The number of views each account (one phone) adds to each link. Optional.",
               "Số view bạn muốn một tài khoản (một điện thoại) tăng cho một link. Có thể nhập hoặc không.",
               "El número de visualizaciones que cada cuenta (un teléfono) añade a cada enlace. Opcional.",
               "1 アカウント（1 台の端末）が 1 つのリンクに加える再生数。省略可。")},
    "goal": {
        "name": L("Goal", "Mục tiêu", "Objetivo", "目標"),
        "d": L("The goal of the interaction for your videos, posts or profile. The AI uses it to generate more realistic data.",
               "Mục tiêu mà bạn muốn tương tác liên quan tới các video, bài viết hoặc trang cá nhân của bạn. AI dựa vào đây để tạo ra dữ liệu chân thực hơn.",
               "El objetivo de la interacción con tus vídeos, publicaciones o perfil. La IA lo usa para generar datos más realistas.",
               "動画・投稿・プロフィールに対するやり取りの目標。AI はこれを基に、より自然なデータを生成します。")},
    "goal_live": {
        "name": L("Goal", "Mục tiêu", "Objetivo", "目標"),
        "d": L("The goal of the interaction for your livestream. The AI uses it to generate more realistic data.",
               "Mục tiêu mà bạn muốn tương tác liên quan tới nội dung phiên live của bạn. AI dựa vào đây để tạo ra dữ liệu chân thực hơn.",
               "El objetivo de la interacción con tu directo. La IA lo usa para generar datos más realistas.",
               "ライブ配信に対するやり取りの目標。AI はこれを基に、より自然なデータを生成します。")},
    "goal_msg": {
        "name": L("Goal", "Mục tiêu", "Objetivo", "目標"),
        "d": L("The goal related to the content of your message. The AI uses it to generate more realistic data.",
               "Mục tiêu liên quan tới nội dung tin nhắn của bạn. AI dựa vào đây để tạo ra dữ liệu chân thực hơn.",
               "El objetivo relacionado con el contenido de tu mensaje. La IA lo usa para generar datos más realistas.",
               "メッセージの内容に関連する目標。AI はこれを基に、より自然なデータを生成します。")},
    "goal_media": {
        "name": L("Goal", "Mục tiêu", "Objetivo", "目標"),
        "d": L("The goal related to the videos and images you want to post. The AI uses it to generate more realistic data.",
               "Mục tiêu liên quan tới nội dung video, hình ảnh muốn đăng của bạn. AI dựa vào đây để tạo ra dữ liệu chân thực hơn.",
               "El objetivo relacionado con los vídeos e imágenes que quieres publicar. La IA lo usa para generar datos más realistas.",
               "投稿したい動画・画像に関連する目標。AI はこれを基に、より自然なデータを生成します。")},
    "video_goals": {
        "name": "Video goals",
        "d": L("The goal of the interaction for your videos, posts or profile. The AI uses it to generate more realistic data.",
               "Mục tiêu mà bạn muốn tương tác liên quan tới các video, bài viết hoặc trang cá nhân của bạn. AI dựa vào đây để tạo ra dữ liệu chân thực hơn.",
               "El objetivo de la interacción con tus vídeos, publicaciones o perfil. La IA lo usa para generar datos más realistas.",
               "動画・投稿・プロフィールに対するやり取りの目標。AI はこれを基に、より自然なデータを生成します。")},
    "video_goals_live": {
        "name": "Video goals",
        "d": L("The goal of the interaction for your livestream. The AI uses it to generate more realistic data.",
               "Mục tiêu mà bạn muốn tương tác liên quan tới các phiên livestream của bạn. AI dựa vào đây để tạo ra dữ liệu chân thực hơn.",
               "El objetivo de la interacción con tu directo. La IA lo usa para generar datos más realistas.",
               "ライブ配信に対するやり取りの目標。AI はこれを基に、より自然なデータを生成します。")},
    "portrait": {
        "name": "Portrait of viewer",
        "d": L("A portrait of the customers you want to engage with your videos, posts or profile. The AI uses it to generate more realistic data.",
               "Chân dung các khách hàng bạn muốn tương tác liên quan tới các video, bài viết hoặc trang cá nhân của bạn. AI dựa vào đây để tạo ra dữ liệu chân thực hơn.",
               "Un retrato de los clientes con los que quieres interactuar a través de tus vídeos, publicaciones o perfil. La IA lo usa para generar datos más realistas.",
               "動画・投稿・プロフィールで関わりたい顧客像。AI はこれを基に、より自然なデータを生成します。")},
    "portrait_live": {
        "name": "Portrait of viewer",
        "d": L("A portrait of the customers you want to engage with your livestream. The AI uses it to generate more realistic data.",
               "Chân dung các khách hàng bạn muốn tương tác liên quan tới phiên livestream của bạn. AI dựa vào đây để tạo ra dữ liệu chân thực hơn.",
               "Un retrato de los clientes con los que quieres interactuar en tu directo. La IA lo usa para generar datos más realistas.",
               "ライブ配信で関わりたい顧客像。AI はこれを基に、より自然なデータを生成します。")},
    "file_comment": {
        "name": "File comment",
        "d": L("A text document holding the default comments you prepared, one comment per line. Without an API key, the system uses the comments in this file. <a href=\"#/ref-files\">How to set up the file</a>",
               "File text document chứa các bình luận mặc định bạn đã chuẩn bị sẵn, mỗi bình luận một dòng. Nếu không dùng API key, hệ thống sẽ dùng các bình luận trong file này. <a href=\"#/ref-files\">Hướng dẫn setup file</a>",
               "Un documento de texto con los comentarios predeterminados que preparaste, uno por línea. Sin API key, el sistema usa los comentarios de este archivo. <a href=\"#/ref-files\">Cómo preparar el archivo</a>",
               "あらかじめ用意した既定のコメントを 1 行に 1 つずつ書いたテキストファイル。API キーがない場合は、このファイルのコメントが使われます。<a href=\"#/ref-files\">ファイルの準備方法</a>")},
    "post_sample": {
        "name": L("Sample post", "Bài viết mẫu", "Publicación de ejemplo", "投稿のサンプル"),
        "d": L("The content of a sample post. The AI writes a new post around it and posts that. Without AI, this sample is posted as it is.",
               "Nội dung một bài viết mẫu bạn muốn dùng để đăng. AI sẽ dựa vào nội dung này để tạo ra một bài viết khác xoay quanh nội dung mẫu để đăng. Nếu không dùng AI, hệ thống dùng luôn bài viết mẫu này.",
               "El contenido de una publicación de ejemplo. La IA escribe una nueva publicación a partir de ella y la publica. Sin IA, se publica el ejemplo tal cual.",
               "投稿のサンプル本文。AI はこれを基に別の投稿を作成して投稿します。AI を使わない場合は、このサンプルがそのまま投稿されます。")},
    "comment_sample": {
        "name": L("Sample comment", "Bình luận mẫu", "Comentario de ejemplo", "コメントのサンプル"),
        "d": L("The content of a sample comment for seeding. The AI writes new comments around it. Without AI, this sample is used as it is.",
               "Nội dung một bình luận mẫu bạn muốn dùng để seeding. AI sẽ dựa vào nội dung này để tạo ra bình luận khác xoay quanh nội dung mẫu. Nếu không dùng AI, hệ thống dùng luôn bình luận mẫu này.",
               "El contenido de un comentario de ejemplo para el seeding. La IA escribe nuevos comentarios a partir de él. Sin IA, se usa el ejemplo tal cual.",
               "シーディング用のコメントのサンプル。AI はこれを基に別のコメントを作成します。AI を使わない場合は、このサンプルがそのまま使われます。")},
    "folder_images_opt": {
        "name": L("Image folder", "Folder ảnh", "Carpeta de imágenes", "画像フォルダー"),
        "d": L("The path of a folder holding the images you want to attach to the content, if needed. Optional.",
               "Đường dẫn của folder chứa những hình ảnh bạn muốn đăng kèm theo nội dung (nếu cần). Có thể không nhập.",
               "La ruta de una carpeta con las imágenes que quieres adjuntar al contenido, si hace falta. Opcional.",
               "必要に応じて、内容に添付したい画像を入れたフォルダーのパス。省略可。")},
    "img_pick": {
        "name": L("Image order", "Cách dùng ảnh", "Orden de las imágenes", "画像の使い方"),
        "d": L("How the images are used. <em>Random</em> takes images from your folder at random; <em>Sorted</em> (Sắp xếp) gives each account its own image.",
               "Tuỳ chọn cách sử dụng ảnh. Chọn <em>Ngẫu nhiên</em>, hệ thống lấy ngẫu nhiên các hình ảnh trong folder; chọn <em>Sắp xếp</em>, hệ thống lấy cho mỗi tài khoản một ảnh riêng.",
               "Cómo se usan las imágenes. <em>Aleatorio</em> toma imágenes de tu carpeta al azar; <em>Ordenado</em> (Sắp xếp) da a cada cuenta su propia imagen.",
               "画像の使い方。<em>ランダム</em>ではフォルダー内の画像をランダムに使い、<em>順番</em>（Sắp xếp）では各アカウントに別々の画像を割り当てます。")},
    "folder_avatar": {
        "name": L("Image folder", "Folder ảnh", "Carpeta de imágenes", "画像フォルダー"),
        "d": L("The folder on your computer holding the images to use as profile pictures for the {p} accounts.",
               "Folder chứa các hình ảnh trên máy tính của bạn, dùng làm ảnh đại diện cho các tài khoản {p}.",
               "La carpeta de tu ordenador con las imágenes que se usarán como foto de perfil de las cuentas de {p}.",
               "{p} アカウントのプロフィール画像に使う画像を入れた、パソコン上のフォルダー。")},
    "file_or_ai": {
        "name": "File or AI",
        "d": L("Where the {x} comes from. <em>AI</em>: the system uses AI to generate {xs} around your topic. <em>File</em>: the system uses the {xs} you prepared in a text document.",
               "Tuỳ chọn cách lấy dữ liệu {x}. Chọn <em>AI</em>, hệ thống dùng AI tạo ra các {x} xoay quanh chủ đề của bạn để cập nhật. Chọn <em>File</em>, hệ thống dùng dữ liệu bạn chuẩn bị sẵn trong file text document.",
               "De dónde salen los datos ({xs}). <em>AI</em>: el sistema usa IA para generar {xs} sobre tu tema. <em>File</em>: el sistema usa lo que preparaste en un documento de texto.",
               "{x}の取得方法。<em>AI</em> を選ぶと、AI がトピックに沿った{x}を生成します。<em>File</em> を選ぶと、テキストファイルに用意した{x}が使われます。")},
    "x_pick": {
        "name": L("Order", "Cách dùng", "Orden", "使い方"),
        "d": L("How the {xs} are used. <em>Random</em> takes {xs} from your file at random; <em>Sorted</em> (Sắp xếp) gives each account its own {x}.",
               "Tuỳ chọn cách sử dụng {x}. Chọn <em>Ngẫu nhiên</em>, hệ thống lấy ngẫu nhiên các {x} trong file; chọn <em>Sắp xếp</em>, hệ thống lấy cho mỗi tài khoản một {x} riêng.",
               "Cómo se usan los datos ({xs}). <em>Aleatorio</em> toma líneas de tu archivo al azar; <em>Ordenado</em> (Sắp xếp) da a cada cuenta una línea distinta.",
               "{x}の使い方。<em>ランダム</em>ではファイル内の{x}をランダムに使い、<em>順番</em>（Sắp xếp）では各アカウントに別々の{x}を割り当てます。")},
    "x_file": {
        "name": L("File path", "Đường dẫn file", "Ruta del archivo", "ファイルのパス"),
        "d": L("The path to the text document on your computer that holds your {xs}, one per line. <a href=\"#/ref-files\">How to set up the file</a>",
               "Đường dẫn tới file text document chứa các {x} của bạn trên máy tính, mỗi thông tin một dòng. <a href=\"#/ref-files\">Hướng dẫn setup file</a>",
               "La ruta al documento de texto de tu ordenador que contiene tus {xs}, uno por línea. <a href=\"#/ref-files\">Cómo preparar el archivo</a>",
               "{x}を 1 行に 1 つずつ書いた、パソコン上のテキストファイルのパス。<a href=\"#/ref-files\">ファイルの準備方法</a>")},
    "msg_template": {
        "name": L("Message template", "Tin nhắn mẫu", "Plantilla de mensaje", "メッセージのテンプレート"),
        "d": L("The message you want the accounts to send to the profile links you entered. With an API key, the system writes other messages around this template and sends those.",
               "Mẫu tin nhắn mà bạn muốn các tài khoản gửi tới các link profile đã nhập. Nếu dùng API key, hệ thống sẽ tạo ra các tin nhắn khác xoay quanh tin nhắn mẫu để gửi.",
               "El mensaje que quieres que las cuentas envíen a los enlaces de perfil que introdujiste. Con API key, el sistema escribe otros mensajes a partir de esta plantilla y los envía.",
               "入力したプロフィールにアカウントから送りたいメッセージ。API キーがある場合は、このテンプレートを基に別のメッセージを作成して送ります。")},
    "share_story": {
        "name": L("Share to story", "Chia sẻ lên story", "Compartir en la historia", "ストーリーズに共有"),
        "d": L("Whether to also share the post to the story.", "Tuỳ chọn có share bài đăng lên story luôn hay không.",
               "Si compartir también la publicación en la historia.", "投稿をストーリーズにも共有するかどうか。")},
    "folder_media": {
        "name": L("Media folder", "Folder video / ảnh", "Carpeta de contenido", "メディアフォルダー"),
        "d": L("The path to the folder on your computer holding the videos or images you want to post.",
               "Đường dẫn tới folder chứa các video / hình ảnh mà bạn muốn đăng ở trong máy tính.",
               "La ruta a la carpeta de tu ordenador con los vídeos o imágenes que quieres publicar.",
               "投稿したい動画・画像を入れた、パソコン上のフォルダーのパス。")},
    "folder_videos": {
        "name": L("Video folder", "Folder video", "Carpeta de vídeos", "動画フォルダー"),
        "d": L("The path to the folder on your computer holding the videos you want to post.",
               "Đường dẫn tới folder chứa các video mà bạn muốn đăng ở trong máy tính.",
               "La ruta a la carpeta de tu ordenador con los vídeos que quieres publicar.",
               "投稿したい動画を入れた、パソコン上のフォルダーのパス。")},
    "video_count": {
        "name": L("Number of videos", "Số video", "Número de vídeos", "動画の本数"),
        "d": L("The number of videos you want to post.", "Số video mà bạn muốn đăng.",
               "El número de vídeos que quieres publicar.", "投稿したい動画の本数。")},
    "ai_video": {
        "name": L("AI video", "Video AI", "Vídeo con IA", "AI 動画"),
        "d": L("Whether the AI creates the videos automatically, or the videos already in the folder are used.",
               "Tuỳ chọn AI tự động tạo video hoặc dùng sẵn các video có trong folder.",
               "Si la IA crea los vídeos automáticamente o se usan los vídeos que ya están en la carpeta.",
               "AI が動画を自動で作るか、フォルダー内の既存の動画を使うかの選択。")},
    "delete_after": {
        "name": L("Delete after posting", "Xoá sau khi đăng", "Borrar tras publicar", "投稿後に削除"),
        "d": L("Whether to delete a video from the folder on your computer once it has been picked for posting.",
               "Tuỳ chọn xoá hoặc không xoá video khỏi folder trong máy tính sau khi video vừa được chọn để đăng.",
               "Si borrar un vídeo de la carpeta de tu ordenador una vez elegido para publicarlo.",
               "投稿用に選ばれた動画を、パソコンのフォルダーから削除するかどうか。")},
    "hashtags": {
        "name": "Hashtags",
        "d": L("Extra hashtags to add when posting. Optional.", "Các hashtag thêm vào khi đăng video. Có thể nhập hoặc không.",
               "Hashtags adicionales que se añaden al publicar. Opcional.", "投稿時に追加するハッシュタグ。省略可。")},
    "caption_tpl": {
        "name": L("Caption", "Caption", "Texto de la publicación", "キャプション"),
        "d": L("A sample caption for the videos or images. With AI, the system writes captions around your topic and this sample. Without AI, the sample is used as the caption.",
               "Mẫu caption bạn muốn dùng khi đăng video / ảnh. Nếu chọn AI, hệ thống dùng AI tạo ra các caption xoay quanh chủ đề và nội dung caption mẫu. Nếu không dùng AI, hệ thống dùng luôn caption mẫu.",
               "Un texto de ejemplo para los vídeos o imágenes. Con IA, el sistema escribe textos a partir de tu tema y este ejemplo. Sin IA, se usa el ejemplo como texto.",
               "動画・画像に付けるキャプションのサンプル。AI を使う場合は、トピックとこのサンプルを基にキャプションを作成します。使わない場合は、サンプルがそのままキャプションになります。")},
    "caption_mode": {
        "name": L("Caption", "Caption", "Texto de la publicación", "キャプション"),
        "d": L("How captions are created. With AI, the system writes captions around your topic and each video's file name. Without AI, the video's file name is used as the caption.",
               "Tuỳ chọn cách tạo caption khi đăng video. Nếu chọn AI, hệ thống dùng AI tạo ra các caption xoay quanh chủ đề và tên file của video. Nếu không dùng AI, hệ thống dùng luôn tên file video làm caption.",
               "Cómo se crean los textos. Con IA, el sistema los escribe a partir de tu tema y del nombre de archivo de cada vídeo. Sin IA, el nombre de archivo del vídeo se usa como texto.",
               "キャプションの作り方。AI を使う場合は、トピックと各動画のファイル名を基にキャプションを作成します。使わない場合は、動画のファイル名がそのままキャプションになります。")},
    "captcha": {
        "name": L("Captcha API key", "API giải captcha", "API key de captcha", "キャプチャ API キー"),
        "d": L("The captcha-solving API key from <a href=\"https://omocaptcha.com/vi/welcome\" target=\"_blank\" rel=\"noopener\">OMOCAPTCHA</a>. <a href=\"https://drive.google.com/file/d/17h_9ImGF4x8n4QQ7mp-xLA8r8NYAGhtc/view?usp=sharing\" target=\"_blank\" rel=\"noopener\">Video guide</a>",
               "API giải captcha của <a href=\"https://omocaptcha.com/vi/welcome\" target=\"_blank\" rel=\"noopener\">OMOCAPTCHA</a>. <a href=\"https://drive.google.com/file/d/17h_9ImGF4x8n4QQ7mp-xLA8r8NYAGhtc/view?usp=sharing\" target=\"_blank\" rel=\"noopener\">Video hướng dẫn</a>",
               "La API key para resolver captchas de <a href=\"https://omocaptcha.com/vi/welcome\" target=\"_blank\" rel=\"noopener\">OMOCAPTCHA</a>. <a href=\"https://drive.google.com/file/d/17h_9ImGF4x8n4QQ7mp-xLA8r8NYAGhtc/view?usp=sharing\" target=\"_blank\" rel=\"noopener\">Vídeo de ayuda</a>",
               "<a href=\"https://omocaptcha.com/vi/welcome\" target=\"_blank\" rel=\"noopener\">OMOCAPTCHA</a> のキャプチャ解決用 API キー。<a href=\"https://drive.google.com/file/d/17h_9ImGF4x8n4QQ7mp-xLA8r8NYAGhtc/view?usp=sharing\" target=\"_blank\" rel=\"noopener\">解説動画</a>")},
}
