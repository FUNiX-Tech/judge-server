## Tạo image judge

Chạy lệnh `make funix`.

Lệnh này sẽ tạo image judge tier 3 của dmoj và thêm:

- Các packages: 
    - `selenium`, `google-chrome-stable`, `beautifulsoup4`: để chấm các bài html, css.

- Các files: 
    - `HTML.py`: executor cho các bài html, css (thực ra chỉ là python executor) 
    - `chrome_driver.py`, `css_parser.py`: các utils để chấm bài html, css
    - `_cptbox.pyx`: dùng để override file gốc để fix lỗi cython. 

---

## Tạo container judge

Nguồn: https://docs.dmoj.ca/#/judge/setting_up_a_judge

Ví dụ: 

```shell copy
sudo docker run \
    --name jd2 \
    -p "$(ip addr show dev ens5 | perl -ne 'm@inet (.*)/.*@ and print$1 and exit')":9997:9997 \
    -v /projects/site/problems:/problems \
    --cap-add=SYS_PTRACE \
    -d \
    --restart=always \
    judge:latest \
    run -p "9999" -c /problems/judge.yml \
    "$(ip addr show dev ens5 | perl -ne 'm@inet (.*)/.*@ and print$1 and exit')" "jd2" "5cwKWowy5LGziKUf5JracyiayYY+Ty+N8VAo/cxL8HhLUZBRyu3PbOcAO4FNdjRmVrrKv9TK664PG1QgoRedIJYc7om8j+NyjgTP"
```

## Hướng dẫn cách viết file chấm html:

1 html/css problem gồm:

- `init.yml`
- file `.py` là file checker
- file `.zip` chứa các file chứa nội dung tiêu chí (criteria)

Ví dụ problem có code `problem01`:

- Criteria 1: "Thẻ h1 có nội dung 'Hello world'"
- Criteria 2: "Thẻ h2 có nội dung 'Cat'"
- Criteria 3: "Đặt color cho thẻ h2 màu đỏ bằng cách thêm property 'color: red' cho selector 'h2' trong thẻ 'style'"

HTML mẫu:

```html
<html>
  <head>
    <style>
      h2 {
        width: 200px;
      }
    </style>
  </head>
</html>
```

## Cách tạo problem trên:

### 1. Tạo folder có tên `problem01`

### 2. Trong folder vừa tạo, tạo file `init.yml` có nội dung như sau:

```yml
checker: problem01.py # tên file checker
archive: problem01.zip # tên file zip sẽ chứa các file criteria
test_cases:
  - { in: problem01.1.in, points: 10 } # file problem01.1.in nằm trong file zip chứa nội dung criteria 1
  - { in: problem01.2.in, points: 50 } # tương tự
  - { in: problem01.3.in, points: 80 } # tương tự
```

### 3. Tạo file chứa nội dung criteria:

- `problem01.1.in` với nội dung `Thẻ h1 có nội dung 'Hello world'`
- `problem01.2.in` với nội dung `Thẻ h2 có nội dung 'Cat'`
- `problem01.3.in` với nội dung `Đặt color cho thẻ h2 màu đỏ bằng cách thêm property 'color: red' cho selector 'h2' trong thẻ 'style'`

Nén 2 file trên dưới dạng đuôi `.zip`: `problem01.zip`.

### 4. Viết file checker:

Tạo file `problem01.py` với nội dung như sau:

```python
from bs4 import BeautifulSoup
from dmoj.result import CheckerResult
from dmoj.utils.unicode import utf8text
from dmoj.utils.css_parser import parse_css

# Với mỗi criteria, judge sẽ chạy file này 1 lần với các arguments tương ứng với criteria đó
# Có 2 criteria
def check(process_output, judge_output, judge_input, point_value, submission_source, **kwargs):

    input = judge_input.decode('utf-8').strip() # Nội dung criteria lấy từ file problem01.<number>.in

    source = submission_source.decode('utf-8').strip() # source code của học viên

    soup = BeautifulSoup(source, 'html.parser')

    # criteria 1
    if input == "Thẻ h1 có nội dung 'Hello world'":

        h1 = soup.find('h1')

        if not h1:
            return CheckerResult(False, 0, "Thiếu thẻ h1")

        if h1.text == 'Hello world':
            return CheckerResult(True, point_value, "") # point_value = 10
        else:
            return CheckerResult(False, 0, "Nội dung thẻ h1 phải là Hello world")

    # criteria 2
    if input == "Thẻ h2 có nội dung 'Cat'":
        h2 = soup.find('h2')

        if not h2:
            return CheckerResult(False, 0, "Thiếu thẻ h2")

        if h2.text == 'Hello world':
            return CheckerResult(True, point_value, "") # point_value = 50
        else:
            return CheckerResult(False, 0, "Nội dung thẻ h2 phải là Cat")

    # criteria 3
    if input == "Đặt color cho thẻ h2 màu đỏ bằng cách thêm property 'color: red' cho selector 'h2' trong thẻ 'style'":

        css = parse_css(soup)

        css_h2 = css.get("h2")

        if not css_h2:
            return CheckerResult(False, 0, "Không có h2 block trong thẻ style")

        color = css_h2.get("color")

        if not color:
            return CheckerResult(False, 0, "h2 selector không có color")

        if color == 'red':
            return CheckerResult(True, point_value, "")
        else:
            return CheckerResult(False, 0, "color phải là 'red'")

    # không matches if-else -> kiểm tra xem lỗi typo, dấu cách, \n,...
    return CheckerResult(True, point_value, "Lỗi checker")
```

Có thể check kỹ hơn.

`CheckerResult` có 3 tham số:

- Tham số thứ nhất: True là đúng, False là sai
- Tham số thứ 2: Điểm số thí sinh.
- Tham số thú 3: Nhận xét

### 5. Hoàn tất

Copy vào thư mục `problem01` vào thư mục chứa problem data `problems`.
Vào path `/problem/problem01` click `Upate problem data (beta)` để cập nhật nội dung criteria cho problem.
Restart lại Judge nếu cần.


