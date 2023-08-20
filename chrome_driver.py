from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import urllib.parse

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

def get_driver(html):
    driver = webdriver.Chrome(options=chrome_options)
    encoded_html = "data:text/html;charset=utf-8," + urllib.parse.quote(html)

    driver.get(encoded_html)
    
    def find_element_by_tag_name(tag_name):
        try:
            element = driver.find_element(By.TAG_NAME, tag_name)
            return element
        except NoSuchElementException:
            return None
    
    def find_elements_by_tag_name(tag_name):
        return driver.find_elements(By.TAG_NAME, tag_name)
    
    def find_element_by_class_name(class_name):
        try:
            element = driver.find_element(By.CLASS_NAME, class_name)
            return element
        except NoSuchElementException:
            return None

    def find_elements_by_class_name(class_name):
        return driver.find_elements(By.CLASS_NAME, class_name)
    
    def find_element_by_id(id):
        try:
            element = driver.find_element(By.ID, id)
            return element
        except NoSuchElementException:
            return None
    
    def find_element_by_css_selector(css_selector):
        try:
            element = driver.find_element(By.CSS_SELECTOR, css_selector)
            return element
        except NoSuchElementException:
            return None

    def find_elements_by_css_selector(css_selector):
        return driver.find_elements(By.CSS_SELECTOR, css_selector)
    
    def find_element_by_name(element_name):
        try:
            element = driver.find_element(By.NAME, element_name)
            return element
        except NoSuchElementException:
            return None
    
    def find_elements_by_name(element_name):
        return driver.find_elements(By.NAME, element_name)
    
    def get_computed_style(element, css_property: str):
        js_command = f"return window.getComputedStyle(arguments[0]).getPropertyValue('{css_property}');"
        return  driver.execute_script(js_command, element)
    
    driver.find_element_by_tag_name = find_element_by_tag_name
    driver.find_elements_by_tag_name = find_elements_by_tag_name 
    driver.find_element_by_class_name = find_element_by_class_name 
    driver.find_elements_by_class_name = find_elements_by_class_name 
    driver.find_element_by_id = find_element_by_id 
    driver.find_element_by_css_selector = find_element_by_css_selector 
    driver.find_elements_by_css_selector = find_elements_by_css_selector 
    driver.find_element_by_name = find_element_by_name 
    driver.find_elements_by_name = find_elements_by_name 
    driver.get_computed_style = get_computed_style 

    return driver



