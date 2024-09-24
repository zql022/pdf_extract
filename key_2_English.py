from translate import Translator
import os
import re
import json

trans_dict_path = "./data/key2en.json"
translator = Translator(from_lang="ZH",to_lang="EN")

def key_2_English(key, translator=translator, 
                  trans_dict_path=trans_dict_path, 
                  force_translate=False, update_trans_dict_file=True):
    '''
    用translate包将key转换成英文
    并维护一个中转英的dict
    可以人为修改对应英文

    key: 一个要翻译的字符串
    translator: Translator(from_lang="ZH",to_lang="EN")
    trans_dict_path: 存储中英字符对应翻译

    force_translate: 强制重新翻译，也会更新表格
    update_trans_dict_file：是否更新存储的dict
    '''
    ## 检查是否含有中文
    contains_ZH = False
    for char in key:
        if '\u4e00' <= char <= '\u9fff':
            contains_ZH = True
            break
    if not contains_ZH:
        return key
        
    need_updating = False  ## flag for 是否需要更新字典

    ## 载入已有dict, 或创立新dict
    if not os.path.exists(trans_dict_path):
        need_updating = True
        trans_dict = {}
    else:
        with open(trans_dict_path, 'r',encoding='utf-8') as file:
            trans_dict = json.load(file)

    key_en = trans_dict.get(key)
    if force_translate:
        key_en = None
    if not key_en:
        need_updating = True
        key_en = translator.translate(key)

        matches = re.findall(">(.*?)<", key_en)  ## 有时会有<bold>..<>修饰
        if matches:
            key_en = matches[0].strip(":")

        ## 原有下划线为标题分级
        key_en = re.sub(r'\_', '\_\_', key_en)  
        ## 转小写
        ## 删除非英文字母非空格的字符
        key_en = re.sub(r'[^a-zA-Z0-9\_\s]', '', key_en.lower())  
        ## 下划线连接
        key_en = '_'.join(key_en.split())
        
        ## 更新dict
        trans_dict[key] = key_en
        if update_trans_dict_file:
            with open(trans_dict_path, 'w',encoding='utf-8') as file:
                json.dump(trans_dict, file)

    return key_en

def update_trans_dict(key, key_en, trans_dict_path=trans_dict_path):
    '''
    手动修改英文翻译
    '''
    need_updating = False

    ## 载入已有dict, 或创立新dict
    if not os.path.exists(trans_dict_path):
        need_updating = True
        trans_dict = {}
    else:
        with open(trans_dict_path, 'r',encoding='utf-8') as file:
            trans_dict = json.load(file)

    ## 更新dict
    trans_dict[key] = key_en
    with open(trans_dict_path, 'w',encoding='utf-8') as file:
        json.dump(trans_dict, file,indent=2)

def key_list_2_English(keys):
    return [key_2_English(k) for k in keys]


def translate_answer_key(answer):#, translator, trans_dict_path
    """
    递归地处理字典和列表中的字典，翻译所有键。
    """
    if isinstance(answer, dict):
        # 创建一个新的字典来存储修改后的键值对
        new_dict = {}
        for key, value in answer.items():
            # 翻译当前键
            new_key = key_2_English(key, translator, trans_dict_path)
            # 递归处理值
            new_dict[new_key] = translate_answer_key(value)
        return new_dict
    elif isinstance(answer, list):
        # 处理列表中元素的键
        return [translate_answer_key(item) for item in answer]
    else:
        # 如果不是字典也不是列表，则直接返回原值
        return answer
# dic ={'本人版': {'报告编号': '201506010000332123', '报告时间': '2015.06.01 10:05:15', '被查询者姓名': '张十五', '被查询者证件类型': '身份证', '被查询者证件号码': '110108******181X', '查询机构': '中国人民银行营业管理部', '查询原因': '本人查询（临柜）', '其他证件信息': [{'证件类型': '护照', '证件号码': 'G30003516'}, {'证件类型': '军官证', '证件号码': 'M0938981'}], '防欺诈警示': {'信息主体申请设置防欺诈警示，联系电话': '01090000000/13900000000。', '生效日期': '2015年5月29日', '截止日期': '2016年5月28日'}, '异议信息提示': {}}}
# dicc= {}
# for u,v in dic.items():
#     dicc[key_2_English(u)]=translate_answer_key(v)
# print(dicc)
## key用英文显示
# title=['相关还款责任信息汇总']
# print(key_list_2_English(title)[0])
# print({key_2_English(k):v for k,v in dic.items()})
# update_trans_dict('十 异议标注', ' 10_objection_annotation', trans_dict_path=trans_dict_path)
