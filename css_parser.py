from bs4 import BeautifulSoup
import re

regex1 = r'\s*@media\s+[^{}]+\{(?:[^{}]+\{[^{}]*\})*\s*\}' # for @media block
regex2 =  r"\s*[^{}]+\{[^{}]+\}" # for normal block

def get_soup(html):
    try:
        soup = BeautifulSoup(html, 'html.parser')
        return soup
    except:
        return None
    
def _get_css_blocks(style_block) -> list:

    striped = "" if style_block.string is None else re.sub(r"[\n\r\t ]+", " ", style_block.string.strip())
    
    return re.findall(regex1 + '|' + regex2, striped, re.IGNORECASE)
    
def _is_media_block(block: str) -> bool:
    return block.strip().startswith("@media")

def _get_normal_css_blocks(parent_block: str) -> list:
    return re.findall(regex2, parent_block, re.IGNORECASE)

def _get_media_selector(media_block: str) -> str:
    return re.findall(r"@media\s+[^{}]+", media_block, re.IGNORECASE)[0].strip()

def _parse_css_block(block: str) -> list:
    
    selectors, attrs = re.sub(r"}", "", block).split('{')
    
    selector_list = list(map(lambda selector: selector.strip(), selectors.split(',')))
    
    props = []
    
    for attr in attrs.split(';'):
        
        if not attr.strip():
            continue
        
        colon_index = attr.index(":")
        
        key = attr[0:colon_index].strip()
        
        value = attr[colon_index + 1:].strip()
        
        props.append({
            "key": key,
            "value": value
        })
    
    return [selector_list, props]
            
def _should_write_css(parent_block: dict, selector: str, key: str, value: str) -> bool:
    return not parent_block[selector].get(key) \
        or parent_block[selector][key].find(" !important") == -1 \
        or value.find(" !important") != -1

def parse_css(soup):
    css_attributes = {}
    
    style_tags = soup.find_all('style')
    
    for style_tag in style_tags:

        blocks = _get_css_blocks(style_tag)

        if not blocks:
            continue

        for match in blocks:
            match = match.strip()
            if _is_media_block(match):
                child_blocks = _get_normal_css_blocks(match)
                
                media = _get_media_selector(match)
                
                if not css_attributes.get(media):
                    css_attributes[media] = {}
                    
                for child_block in child_blocks:
                    
                    selectors, attrs = _parse_css_block(child_block)
                    
                    for s in selectors:
                        
                        if not s:
                            continue
                        
                        if not css_attributes[media].get(s):
                            css_attributes[media][s] = {}
                            
                        for attr in attrs:
                            
                            if _should_write_css(css_attributes[media], s, attr["key"], attr["value"]):

                                css_attributes[media][s][attr["key"]] = attr["value"]
            else:
                selectors, attrs = _parse_css_block(match)
                
                for s in selectors:
                
                    if not css_attributes.get(s):
                        css_attributes[s] = {}
                        
                    for attr in attrs:
                        
                        if _should_write_css(css_attributes, s, attr["key"], attr["value"]):
                                
                            css_attributes[s][attr["key"]] = attr["value"]
    
    return css_attributes

# inline css
def _should_write_inline_css(css_attributes: dict, attr_name: str, attr_val: str) -> bool:
    if not css_attributes.get(attr_name):
        return True

    if css_attributes[attr_name].find("!important") == -1:
        return True

    if attr_val.find("!important") != -1:
        return True

def parse_inline_css(tag):

    css_attributes = {}

    inline_css = tag.get('style')
    
    if inline_css is None:
        return css_attributes

    inline_css = re.sub(r"[\n\r\t ]+", " ", inline_css)
    
    for attr in inline_css.split(';'):
        if not attr.strip():
            continue
        colon_index = attr.index(":")
        attr_name = attr[0:colon_index].strip()
        attr_value = attr[colon_index + 1:].strip()
        
        if _should_write_inline_css(css_attributes, attr_name, attr_value):
            css_attributes[attr_name] = attr_value

    return css_attributes

def get_element_selectors(soup, tag):
    css = parse_css(soup)

    selectors = []
    
    for selector in list(css.keys()):
        if tag in soup.select(selector):
            selectors.append(selector)     

    return selectors

def _calculate_specificity(selector):
    a = selector.count('#')  # ID selectors
    b = selector.count('.') + selector.count('[') + selector.count(':not')  
    c = selector.count(':') - (selector.count('::') * 2) 
    d = selector.count('*') 
    e = len(re.findall(r"\b(\w+)\b(?![.#])", selector))  

    specificity_score = (a, b, c, d, e)
    return specificity_score

def is_important_value(css_value):
    return re.fullmatch(r"^.+\s!important$", css_value)

def get_element_css_value(soup, tag, property):
    
    applied_value = ""
    
    css = parse_css(soup)

    inline_css = parse_inline_css(tag)
    
    selectors = get_element_selectors(soup, tag)
    
    applied_points = (0, 0, 0, 0, 0)

    # get css value in <style> will be applied
    for selector in selectors:
        css_value = css[selector].get(property)

        if css_value is None: 
            continue

        selector_points = _calculate_specificity(selector)
        
        if is_important_value(applied_value) and is_important_value(css_value):
            if selector_points > applied_points:
                applied_points = selector_points
                applied_value = css_value

        if is_important_value(applied_value) and not is_important_value(css_value):
            continue

        if not is_important_value(applied_value) and is_important_value(css_value):
            applied_points = selector_points
            applied_value = css_value

        if not is_important_value(applied_value) and not is_important_value(css_value):
            if selector_points > applied_points:
                applied_points = selector_points
                applied_value = css_value
        
    inline_css_value = inline_css.get(property)    

    if inline_css_value:
        if is_important_value(inline_css_value) or not is_important_value(applied_value):
            applied_value = inline_css_value
    
    return applied_value  
    
def count_element(soup, tag_name):
    return len(soup.find_all(tag_name))