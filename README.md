# judge-server

- Copy file `HTML.py` vào thư mục `docker:/judge/dmoj/executors`.
- Cài bs4 cho docker: `(DMOJ) pip install beautifulsoup4`
- `\_cptbox.pyx` là để fix tạm thời lỗi cài đặt judge-server nếu có lỗi xảy ra liên quan `cython`.
- Copy file `css_parser.py` vào `docker:/judge/dmoj/utils`

# Hướng dẫn cách viết file chấm html:

1 html/css problem gồm:

- init.yml
- file .py là file checker
- file .zip chứa các file chứa nội dung tiêu chí (criteria)

Ví dụ 1 problem, có code là `problem01`:

- Criteria 1: "Thẻ h1 có nội dung 'Hello world'"
- Criteria 2: "Thẻ h2 có nội dung 'Cat'"

## Cách tạo problem trên:

### 1. Tạo folder có tên `problem01`

### 2. Trong folder vừa tạo, tạo file init.yml có nội dung như sau:

```yml
checker: problem01.py # tên file checker
archive: problem01.zip # tên file zip sẽ chứa các file criteria
test_cases:
  - { in: problem01.1.in, points: 10 } # file problem01.1.in nằm trong file zip chứa nội dung criteria 1
  - { in: problem01.2.in, points: 50 } # tương tự
```

### 3. Tạo file chứa nội dung criteria:

- `problem01.1.in` với nội dung `Thẻ h1 có nội dung 'Hello world'`
- `problem01.2.in` với nội dung `Thẻ h2 có nội dung 'Cat'`

Nén 2 file trên dưới dạng đuôi `.zip`: `problem01.zip`.

### 4. Viết file checker:

Tạo file problem01.py với nội dung như sau:

```python
from bs4 import BeautifulSoup
from dmoj.result import CheckerResult
from dmoj.utils.unicode import utf8text

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
Vào path `/problem/problem01` click `Upate problem data (beta)` để cập nhật nội dung criterias cho problem.
Restart lại Judge nếu cần.
