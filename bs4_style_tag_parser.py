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
    
def get_css_blocks(style_block: str) -> list:
    
    striped = re.sub(r"[\n ]+", " ", style_block.string.strip())
    
    return re.findall(regex1 + '|' + regex2, striped, re.IGNORECASE)
    
def is_media_block(block: str) -> bool:
    return block.strip().startswith("@media")

def get_normal_css_blocks(parent_block: str) -> list:
    return re.findall(regex2, parent_block, re.IGNORECASE)

def get_media_selector(media_block: str) -> str:
    return re.findall(r"@media\s+[^{}]+", media_block, re.IGNORECASE)[0].strip()

def parse_css_block(block: str) -> list:
    
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
            
def should_write_css(parent_block: dict, selector: str, key: str, value: str) -> bool:
    return not parent_block[selector].get(key) \
        or parent_block[selector][key].find("!important") == -1 \
        or value.find("!important") != -1


def main(soup):
    css_attributes = {}
    
    style_tags = soup.find_all('style')
    
    for style_tag in style_tags:

        blocks = get_css_blocks(style_tag)

        if not blocks:
            continue

        for match in blocks:
            match = match.strip()
            if is_media_block(match):
                child_blocks = get_normal_css_blocks(match)
                
                media = get_media_selector(match)
                
                if not css_attributes.get(media):
                    css_attributes[media] = {}
                    
                for child_block in child_blocks:
                    
                    selectors, attrs = parse_css_block(child_block)
                    
                    for s in selectors:
                        
                        if not s:
                            continue
                        
                        if not css_attributes[media].get(s):
                            css_attributes[media][s] = {}
                            
                        for attr in attrs:
                            
                            if should_write_css(css_attributes[media], s, attr["key"], attr["value"]):

                                css_attributes[media][s][attr["key"]] = attr["value"]
            else:
                selectors, attrs = parse_css_block(match)
                
                for s in selectors:
                
                    if not css_attributes.get(s):
                        css_attributes[s] = {}
                        
                    for attr in attrs:
                        
                        if should_write_css(css_attributes, s, attr["key"], attr["value"]):
                                
                            css_attributes[s][attr["key"]] = attr["value"]
    
    return css_attributes

file = open("draft.html", "r")
html = file.read()
soup = get_soup(html)
result = main(soup)

for css in result:
    print(css, result[css])
