from bs4 import BeautifulSoup
from dmoj.result import CheckerResult
from dmoj.utils.unicode import utf8text

def check(process_output, judge_output, judge_input, point_value, submission_source, **kwargs):
    input = judge_input.decode('utf-8').strip()
    source = submission_source.decode('utf-8').strip()

    soup = BeautifulSoup(source, 'html.parser')
    forms = soup.find_all('form')
    if not forms:
        return CheckerResult(False, 0, "Quá nhiều form")
    
    if len(forms) > 1:
        return CheckerResult(False, 0, "Không có form nào")
    
    form = forms[0]
    
    input1 = soup.find("input", id="indoor", type="radio")
    if not input1:
        return CheckerResult(False, 0, "Thiếu thẻ input mẫu")
        
    label1 = input1.parent
    if label1.name != 'label':
        return CheckerResult(False, 0, "Input mẫu phải ở trong label")
    
    print("--------------")
    print(label1.text)
    if label1.text != "Indoor":
        return CheckerResult(False, 0, "Nội dung thẻ label mẫu phải là Indoor")
    
    input2 = soup.find("input", id="outdoor", type="radio")
    if not input2:
        return CheckerResult(False, 0, "Thiếu input với id outdoor, type radio")
    
    label2 = input2.parent
    if label2.name != 'label':
        return CheckerResult(False, 0, "Input được tạo phải có thẻ cha là label")
    
    if label2.text != "Outdoor":
        return CheckerResult(False, 0, "Thẻ label được tạo phải có nội dung Outdoor")

    if label1.find_next_sibling('label') != label2:
        return CheckerResult(False, 0, "Thẻ label được tạo phải nằm sau thẻ label mẫu")
        
        
    return CheckerResult(True, point_value, "Chính xác")