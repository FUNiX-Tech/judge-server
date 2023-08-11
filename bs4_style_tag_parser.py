from bs4 import BeautifulSoup
import re


def get_soup(html):
    try:
        soup = BeautifulSoup(html, 'html.parser')
        return soup
    except:
        return None

def main(soup):
    css_attributes = {}
    regex1 = r'\s*@media\s+[^{}]+\{(?:[^{}]+\{[^{}]*\})*\s*\}' # for @media block
    regex2 =  r"\s*[^{}]+\{[^{}]+\}" # for normal block
    
    style_tags = soup.find_all('style')
    for style_tag in style_tags:
        
        css_text = re.sub(r"[\n ]+", " ", style_tag.string.strip())

        matches = re.findall(regex1 + '|' + regex2, css_text, re.IGNORECASE)

        if not matches:
            continue

        for match in matches:
            if match.strip().startswith("@media"):
                inner_media_matches = re.findall(regex2, match.strip(), re.IGNORECASE)
                
                media_key = re.findall(r"@media\s+[^{}]+", match.strip(), re.IGNORECASE)[0].strip()
                if not css_attributes.get(media_key):
                    css_attributes[media_key] = {}
                    
                for inner_media_match in inner_media_matches:
                    inner_media_match = re.sub(r"}", "", inner_media_match)
                    
                    selectors, attrs = inner_media_match.split('{')
                    selector_list = selectors.split(',')
                    for selector in selector_list:
                        selector = selector.strip()
                        if not selector:
                            continue
                        if not css_attributes[media_key].get(selector):
                            css_attributes[media_key][selector] = {}
                        attr_list = attrs.split(';')
                        for attr in attr_list:
                            if not attr.strip():
                                continue
                            attr = attr
                            colon_index = attr.index(":")
                            attr_name = attr[0:colon_index].strip()
                            attr_value = attr[colon_index + 1:].strip()
                            if not css_attributes[media_key][selector].get(attr_name) or css_attributes[media_key][selector].get(attr_name).find("!important") != -1:
                                css_attributes[media_key][selector][attr_name] = attr_value
            else:
                match = re.sub(r"}", "", match)
                selectors, attrs = match.split('{')
                selector_list = selectors.split(',')
                for selector in selector_list:
                    selector = selector.strip()
                    if not selector:
                        continue
                    if not css_attributes.get(selector):
                        css_attributes[selector] = {}
                    attr_list = attrs.split(';')
                    for attr in attr_list:
                        if not attr.strip():
                            continue
                        attr = attr
                        colon_index = attr.index(":")
                        attr_name = attr[0:colon_index].strip()
                        attr_value = attr[colon_index + 1:].strip()
                        if not css_attributes[selector].get(attr_name) or css_attributes[selector].get(attr_name).find("!important") != -1:
                            css_attributes[selector][attr_name] = attr_value
    
    return css_attributes
