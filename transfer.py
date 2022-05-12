import re
import json
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer


def generate_raw(input_file, output_file):
    output = dict()
    current_idx = ''
    for page_layout in extract_pages(input_file):
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                print(element.get_text())
                for basic_char in re.findall(r'(\d{3})\s+([\u4e00-\u9fff])+', element.get_text()):
                    print(basic_char)
                    current_idx = int(basic_char[0])
                    output[current_idx] = dict(name=basic_char[1])
                if '華 語' in element.get_text():
                    meaning = re.findall(r'華 語\s+([\u4e00-\u9fff、]{2,5})', element.get_text())
                    print(meaning)
                    output[current_idx]['meaning'] = meaning
                if '詞 彙' in element.get_text():
                    voc = re.findall(r'([\u4e00-\u9fff]{2,5})', element.get_text())
                    print(voc)
                    output[current_idx]['vocabulary'] = voc

    print(output)
    with open(output_file, 'w') as f:
        json.dump(output, f)
    # https://regex101.com/
    # https://hts.ithuan.tw/%E6%96%87%E6%9C%AC%E7%9B%B4%E6%8E%A5%E5%90%88%E6%88%90?%E6%9F%A5%E8%A9%A2%E8%85%94%E5%8F%A3=%E5%8F%B0%E8%AA%9E&%E6%9F%A5%E8%A9%A2%E8%AA%9E%E5%8F%A5=ak-hue
    # https://language.moe.gov.tw/upload/download/jts/02%E8%AA%9E%E8%A9%9E1(%E9%9F%B3%E6%AA%94)/0201_014_A.mp3

def generate_markdown(raw_file):
    with open('taigi_vocabularies.md', 'w') as f_md:
        with open(raw_file) as f:
            vocabularies = json.load(f)
            f_md.writelines([f'# Taigi Vocabularies 504\n'])
            for voc_no, detail in vocabularies.items():
                # print(detail)
                name = detail.get('name')
                voc_no_idx = f'{int(voc_no):03d}'
                vocabulary_items = detail.get("vocabulary")
                meaning = detail.get("meaning")
                v = ','.join(vocabulary_items) if vocabulary_items else None
                m = meaning[0] if meaning else None
                f_md.writelines([f'## {voc_no_idx} [{name}](https://itaigi.tw/k/{name})\n'])
                f_md.writelines([f'- {m}\n'])
                f_md.writelines([f'- {v}\n'])
                f_md.writelines([f'- [pronunciation](https://language.moe.gov.tw/upload/download/jts/02%E8%AA%9E%E8%A9%9E1(%E9%9F%B3%E6%AA%94)/0201_{voc_no_idx}_A.mp3)\n'])
                f_md.writelines(['\n'])

if __name__=='__main__':
    input_file = 'source.pdf'
    raw_file = 'raw.json'
    # generate_raw(input_file, raw_file)
    generate_markdown(raw_file)