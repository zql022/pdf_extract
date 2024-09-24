import key_2_English
import json
from table_parsingCH import *
def json_table_find(file_path):
    with open(file_path,'r',encoding='utf-8') as file:
        xiangban_PDF = json.load(file)
    dicc={}

    for line in range(len(xiangban_PDF['data'])):
        for k,v in xiangban_PDF['data'][line].items():
            key=k
            value = v
            if k=='（本人版）':
                content = xiangban_PDF['data'][line]['（本人版）']#['content'][0]
                for i,u in content.items():#键和值
                    if i=='content':
                        lis=u
                        dicc['（本人版）']=table2json_short(lis[0])
                    elif i =='section':
                        if len(content['section'])>1:
                            for linea in range(len(content['section'])):
                                for l,s in content['section'][linea].items():
                                    if l=='其他证件信息':
                                        if len(content['section'][linea][l]['content']) > 0:
                                            lis=content['section'][linea][l]['content'][0]
                                            dicc['（本人版）'][l] = zhengjian_message(lis,l)
                                        else:
                                            print("此处ocr提取可能未提取上，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(l,s))
                                    elif l =='防欺诈警示':
                                        if len(content['section'][linea][l]['content']) > 0:
                                            lis = content['section'][linea][l]['content'][0]
                                            dicc['（本人版）'][l] = table2json_short(lis)
                                        else:
                                            print("此处ocr提取可能未提取上，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(l,s))
                                    elif l =='异议信息提示':
                                        if len(content['section'][linea][l]['content'])>0:
                                            lis = content['section'][linea][l]['content'][0]
                                            dicc['（本人版）'][l] = table2json_short(lis)
                                        else:
                                            dicc['（本人版）'][l] ={}
                                            print("此处ocr提取可能未提取上，请检查该表格提取的ocr信息：\n键：{},\n提取到的键值:{}\n".format(l,s))
                        else:
                            continue
            elif k=='个人基本信息':
                dicc['一 个人基本信息']=[]
                content = xiangban_PDF['data'][line]['个人基本信息']  # ['content'][0]
                for i, u in content.items():  # 键和值
                    if i == 'content':
                        if len(u)==0:
                            continue
                        else:
                            print("此处按照ocr应该没有输出值，否则请检查此处表格提取的信息\n表格：{},\n键值:{}\n".format(content,u))
                    elif i == 'section':
                        if len(content['section']) > 1:
                            for linea in range(len(content['section'])):
                                for l, s in content['section'][linea].items():
                                    if l == '（一）身份信息':
                                        tep={}
                                        if len(content['section'][linea][l]['content'])>0:
                                            lis = content['section'][linea][l]['content'][0]
                                            tep[l]=table2json_long(lis)#####需要修改
                                            dicc['一 个人基本信息'].append(tep.copy())
                                        else:
                                            print("此处ocr提取可能未提取上，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(l,s))
                                    elif l == '（二）配偶信息':
                                        tep={}
                                        if len(content['section'][linea][l]['content']) > 0:
                                            lis = content['section'][linea][l]['content'][0]
                                            tep[l]=peiou_message(lis)
                                            dicc['一 个人基本信息'].append(tep.copy())
                                        else:
                                            print("此处ocr提取可能未提取上，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(l,s))
                                    elif l == '（三）居住信息':
                                        if len(content['section'][linea][l]['content']) > 0:
                                            lis = content['section'][linea][l]['content'][0]
                                            dicc['一 个人基本信息'].append(biaohao_message(lis,'编号',l))
                                        else:
                                            print("此处ocr提取可能未提取上，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(l,s))
                                    elif l == '（四）职业信息':
                                        tep={}
                                        if len(content['section'][linea][l]['content']) > 0:
                                            lis = content['section'][linea][l]['content'][0]
                                            dicc['一 个人基本信息'].append(biaohao_message(lis,'编号',l))
                                        else:
                                            print("此处ocr提取可能未提取上，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(l,s))
                                    else:
                                        continue
            elif k=='二信息概要':
                dicc['二 信息概要'] = []
                content = xiangban_PDF['data'][line]['二信息概要']  # ['content'][0]
                for i, u in content.items():  # 键和值
                    if i == 'content':
                        if len(u)==0:
                            print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n表格：{},\n键值:{}\n".format(content,u))
                        else:
                            if len(content['content'])>0:
                                tep={}
                                lis = content['content'][0]
                                tep['（一）信贷交易信息提示']=v9_message(lis,'业务类型',['贷款','信用卡','其他','合计'])
                                dicc['二 信息概要'].append(tep.copy())
                            else:
                                print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值{}".format(i, u))
                    elif i == 'section':
                        if len(content['section']) > 1:
                            for ll in range(len(content['section'])):
                                for l, s in content['section'][ll].items():
                                    if l == '（二）信贷交易违约信息概要':
                                        line=0
                                        tep={}
                                        tep[l] = []
                                        sec = {}###########ocr识别错误的测试
                                        sec['（三）信贷交易授信及负债信息概要（未结清/未销户）'] = []##########ocr识别错误的测试
                                        for m in  content['section'][0][l]['section']:
                                            for u,v in m.items():
                                                if u=='被追偿信息汇总':
                                                    if len(content['section'][0][l]['section'][line][u]['content'])>0:
                                                        lis = content['section'][0][l]['section'][line][u]['content'][0]
                                                        tep[l].append(title_heji_table(lis,u))
                                                    else:
                                                        print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(u, v))
                                                elif u=='呆账信息汇总':
                                                    if len(content['section'][0][l]['section'][line][u]['content']) > 0:
                                                        lis = content['section'][0][l]['section'][line][u]['content'][0]
                                                        tep[l].append(little_title_table(lis,u,'账户数'))#lis：输入list表格   title表格横行标题    biaoti表格第一个框内字
                                                    else:
                                                        print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(u, v))
                                                elif u=='逾期（透支）信息汇总':
                                                    if len(content['section'][0][l]['section'][line][u]['content']) > 0:
                                                        lis = content['section'][0][l]['section'][line][u]['content'][0]
                                                        tep[l].append(little_title_table(lis,u,'账户类型'))
                                                    else:
                                                        print(
                                                            "此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(
                                                                u, v))
                                                #########ocr识别错误，先进行测试
                                                elif u == '非循环贷账户信息汇总':
                                                    if len(content['section'][0][l]['section'][line][u]['content']) > 0:
                                                        lis = content['section'][0][l]['section'][line][u]['content'][0]
                                                        sec['（三）信贷交易授信及负债信息概要（未结清/未销户）'].append(little_title_table(lis, u,
                                                                                         '管理机构数'))  # lis：输入list表格   title表格横行标题    biaoti表格第一个框内字
                                                    else:
                                                        print(
                                                            "此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(
                                                                u, v))
                                                elif u == '循环贷账户一信息汇总':
                                                    if len(content['section'][0][l]['section'][line][u]['content']) > 0:
                                                        lis = content['section'][0][l]['section'][line][u]['content'][0]
                                                        sec['（三）信贷交易授信及负债信息概要（未结清/未销户）'].append(little_title_table(lis, u,
                                                                                         '管理机构数'))  # lis：输入list表格   title表格横行标题    biaoti表格第一个框内字
                                                    else:
                                                        print(
                                                            "此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(
                                                                u, v))
                                                elif u == '循环贷账户二信息汇总':
                                                    if len(content['section'][0][l]['section'][line][u]['content']) > 0:
                                                        lis = content['section'][0][l]['section'][line][u]['content'][0]
                                                        sec['（三）信贷交易授信及负债信息概要（未结清/未销户）'].append(little_title_table(lis, u, '管理机构数'))
                                                    else:
                                                        print(
                                                            "此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(
                                                                u, v))
                                                elif u == '贷记卡账户信息汇总':
                                                    if len(content['section'][0][l]['section'][line][u]['content']) > 0:
                                                        lis = content['section'][0][l]['section'][line][u]['content'][0]
                                                        sec['（三）信贷交易授信及负债信息概要（未结清/未销户）'].append(little_title_table(lis, u, '发卡机构数'))
                                                    else:
                                                        print(
                                                            "此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(
                                                                u, v))
                                                elif u == '准贷记卡账户信息汇总':
                                                    if len(content['section'][0][l]['section'][line][u]['content']) > 0:
                                                        lis = content['section'][0][l]['section'][line][u]['content'][0]
                                                        sec['（三）信贷交易授信及负债信息概要（未结清/未销户）'].append(little_title_table(lis, u, '发卡机构数'))
                                                    else:
                                                        print(
                                                            "此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(
                                                                u, v))
                                                elif u == '相关还款责任信息汇总':
                                                    if len(content['section'][0][l]['section'][line][u]['content']) > 0:
                                                        lis = content['section'][0][l]['section'][line][u]['content'][0]
                                                        sec['（三）信贷交易授信及负债信息概要（未结清/未销户）'].append(v18_message(lis, u))
                                                    else:
                                                        print(
                                                            "此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(
                                                                u, v))
                                                ###################正常
                                                else:
                                                    continue
                                                line+=1
                                        dicc['二 信息概要'].append(tep.copy())
                                        dicc['二 信息概要'].append(sec.copy())
                                        del tep
                                        del sec
                                    elif '（三）信贷交易授信及负债信息概要' in l:#（三）信贷交易授信及负债信息概要（未结清/未销户）
                                        line=0
                                        tep={}
                                        tep[l] = []
                                        for m in  content['section'][1][l]['section']:#未识别到
                                            for u,v in m.items():
                                                if u=='非循环贷账户信息汇总':
                                                    if len(content['section'][1][l]['section'][line][u]['content'])>0:
                                                        lis = content['section'][1][l]['section'][line][u]['content'][0]
                                                        tep[l].append(little_title_table(lis,u,'管理机构数'))#lis：输入list表格   title表格横行标题    biaoti表格第一个框内字
                                                    else:
                                                        print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(u, v))
                                                elif u=='循环贷账户一信息汇总':
                                                    if len(content['section'][1][l]['section'][line][u]['content']) > 0:
                                                        lis = content['section'][1][l]['section'][line][u]['content'][0]
                                                        tep[l].append(little_title_table(lis,u,'管理机构数'))#lis：输入list表格   title表格横行标题    biaoti表格第一个框内字
                                                    else:
                                                        print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(u, v))
                                                elif u=='循环贷账户二信息汇总':
                                                    if len(content['section'][1][l]['section'][line][u]['content']) > 0:
                                                        lis = content['section'][1][l]['section'][line][u]['content'][0]
                                                        tep[l].append(little_title_table(lis,u,'管理机构数'))
                                                    else:
                                                        print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(u, v))
                                                elif u=='贷记卡账户信息汇总':
                                                    if len(content['section'][1][l]['section'][line][u]['content']) > 0:
                                                        lis = content['section'][1][l]['section'][line][u]['content'][0]
                                                        tep[l].append(little_title_table(lis,u,'发卡机构数'))
                                                    else:
                                                        print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(u, v))
                                                elif u=='准贷记卡账户信息汇总':
                                                    if len(content['section'][1][l]['section'][line][u]['content']) > 0:
                                                        lis = content['section'][1][l]['section'][line][u]['content'][0]
                                                        tep[l].append(little_title_table(lis,u,'发卡机构数'))
                                                    else:
                                                        print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(u, v))
                                                elif u=='相关还款责任信息汇总':
                                                    if len(content['section'][1][ l]['section'][line][u]['content']) > 0:
                                                        lis = content['section'][1][l]['section'][line][u]['content'][0]
                                                        tep[l].append(v18_message(lis,u))
                                                    else:
                                                        print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(u, v))
                                                else:
                                                    continue
                                                line+=1
                                        dicc['二 信息概要'].append(tep.copy())
                                    elif l == '（四）非信贷交易信息概要':
                                        line=0
                                        #2,三未识别到  content['section'][2]['（四）非信贷交易信息概要']
                                        for m in content['section'][1]['（四）非信贷交易信息概要']['section']:
                                            for u, v in m.items():
                                                if u == '后付费业务欠费信息汇总':
                                                    if len(content['section'][1][l]['section'][line][u]['content'])>0:
                                                        lis = content['section'][1][l]['section'][line][u]['content'][0]
                                                        dicc['二 信息概要'].append(little_title_table(lis,l+'--'+u,'业务类型'))  # lis：输入list表格   title表格横行标题    biaoti表格第一个框内字
                                                    else:
                                                        print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(u, v))
                                                else:
                                                    continue
                                                line+=1
                                    elif l == '（五）公共信息概要':
                                        line=0
                                        # 3,三未识别到  content['section'][3]['（五）公共信息概要']
                                        for m in content['section'][2][l]['section']:##3,三未识别到
                                            for u, v in m.items():
                                                if u == '公共信息汇总':
                                                    if len(content['section'][2][l]['section'][line][u]['content'])>0:
                                                        lis = content['section'][2][l]['section'][line][u]['content'][0]
                                                        dicc['二 信息概要'].append(little_title_table(lis, l+'--'+u,'信息类型') ) # lis：输入list表格   title表格横行标题    biaoti表格第一个框内字
                                                    else:
                                                        print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(u, v))
                                                else:
                                                    continue
                                                line+=1
                                    elif l == '（六）非金融信用交易信息概要':
                                        for m in range(len(content['section'][3][l]['content'])):#4,三未识别到
                                            u=content['section'][3][l]['content']
                                            if isinstance(u,list):
                                                if len(u)>0:
                                                    lis = content['section'][3][l]['content'][0]
                                                    dicc['二 信息概要'].append(little_title_table(lis,l,'信息类型'))  # lis：输入list表格   title表格横行标题    biaoti表格第一个框内字
                                                else:
                                                    print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(u, m))
                                            else:
                                                continue
                                    elif l == '（七）公开信息概要':
                                        line=0
                                        for m in content['section'][4][l]['section']:  ##5,三未识别到
                                            for u, v in m.items():
                                                if u == '公开信息汇总':
                                                    if len(content['section'][4][l]['section'][line][u]['content'])>0:
                                                        lis = content['section'][4][l]['section'][line][u]['content'][0]
                                                        dicc['二 信息概要'].append(little_title_table(lis,l+'--'+u,'信息类型'))  # lis：输入list表格   title表格横行标题    biaoti表格第一个框内字
                                                    else:
                                                        print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(u, v))
                                                else:
                                                    continue
                                                line+=1
                                    elif l == '（八）查询记录概要':
                                        tep={}
                                        tep[l] = []
                                        for q, g in s.items():
                                            if q=='content':
                                                if len(content['section'][5][l]['content'])>0:##6,三未识别到
                                                    lis = content['section'][5][l]['content'][0]
                                                    tep[l].append(v23_message(lis,'查询记录概要'))
                                                else:
                                                    print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(l, g))
                                            elif q=='section':
                                                if len(content['section'][5][l]['section'][0]['异议及说明信息']['content'])>0:
                                                    lis = content['section'][5][l]['section'][0]['异议及说明信息']['content'][0]
                                                    tep[l].append(little_title_table(lis,'异议及说明信息','异议标注'))
                                                else:
                                                    print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(l, g))
                                        dicc['二 信息概要'].append(tep.copy())
                        else:
                            continue
            elif k=='三信贷交易信息明细':
                dicc['三信贷交易信息明细'] = []
                content = xiangban_PDF['data'][line]['三信贷交易信息明细']  #
                for i, u in content.items():  # 键和值
                    if i == 'content':
                        if len(u)==0:
                            continue
                        else:
                            print("此处按照ocr输出应该没有值，如果有，请检查该表格提取的ocr信息：\n表格：{},\n键值:{}\n".format(content, u))
                    elif i == 'section':
                        if len(content['section']) > 0:
                            for ll in range(len(content['section'])):
                                for l, s in content['section'][ll].items():###########
                                    if l == '（一）被追偿信息':
                                        line=0
                                        tep={}
                                        tep[l] = []
                                        for m in  content['section'][0]['（一）被追偿信息']['section']:
                                            for u,v in m.items():
                                                if '账户1'in u :
                                                    if len(content['section'][0][l]['section'][line][u]['content'])>0:
                                                        lis = content['section'][0][l]['section'][line][u]['content'][0]
                                                        #lis：输入list表格   title表格横行标题
                                                        tep[l].append(v36_message(lis,u))
                                                    else:
                                                        print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(u, v))
                                                elif '账户2'in u:
                                                    if len(content['section'][0][l]['section'][line][u]['content']) > 0:
                                                        lis = content['section'][0][l]['section'][line][u]['content'][0]
                                                        #lis：输入list表格   title表格横行标题
                                                        tep[l].append(v36_message(lis,u))
                                                    else:
                                                        print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(u, v))
                                                else:
                                                    continue
                                                line+=1
                                        dicc['三信贷交易信息明细'].append(tep.copy())
                                    elif l == '（二）非循环贷账户':
                                        line=0
                                        tep={}
                                        tep[l] = []
                                        for m in  content['section'][1][l]['section']:#
                                            for u,v in m.items():
                                                if '账户1'in u or '（授信协议标识：' in u:
                                                    if len(content['section'][1][l]['section'][line][u]['content'])>0:
                                                        lis = content['section'][1][l]['section'][line][u]['content'][0]
                                                        tep[l].append(v36_message(lis,u))#lis：输入list表格
                                                    else:
                                                        print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(u, v))
                                                elif '账户2'in u or '（授信协议标识：' in u:
                                                    if len(content['section'][1][l]['section'][line][u]['content']) > 0:
                                                        lis = content['section'][1][l]['section'][line][u]['content'][0]
                                                        tep[l].append(v36_message(lis,u))#lis：输入list表格
                                                    else:
                                                        print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(u, v))
                                                elif '账户3'in u or '（授信协议标识：' in u:
                                                    if len(content['section'][1][l]['section'][line][u]['content']) > 0:
                                                        lis = content['section'][1][l]['section'][line][u]['content'][0]
                                                        tep[l].append(v36_message(lis,u))
                                                    else:
                                                        print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(
                                                                u, v))
                                                elif '账户4'in u or '（授信协议标识：' in u:
                                                    if len(content['section'][1][l]['section'][line][u]['content']) > 0:
                                                        lis = content['section'][1][l]['section'][line][u]['content'][0]
                                                        tep[l].append(v36_message(lis,u))
                                                    else:
                                                        print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(u, v))
                                                else:
                                                    continue
                                                line+=1
                                        dicc['三信贷交易信息明细'].append(tep.copy())
                                    elif l == '（三）循环贷账户-':
                                        line=0
                                        tep={}
                                        tep[l] = []
                                        for m in content['section'][2]['（三）循环贷账户-']['section']:#
                                            for u, v in m.items():
                                                if '账户1' in u and '（授信协议标识：' in u:
                                                    if len(content['section'][2][l]['section'][line][u]['content'])>0:
                                                        lis = content['section'][2][l]['section'][line][u]['content'][0]
                                                        tep[l].append(v36_message(lis,u)) # lis：输入list表格
                                                    else:
                                                        print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(u, v))
                                                elif '账户2' in u and '（授信协议标识：' in u:
                                                    if len(content['section'][2][l]['section'][line][u]['content']) > 0:
                                                        lis = content['section'][2][l]['section'][line][u]['content'][0]
                                                        tep[l].append(v36_message(lis,u))  # lis：输入list表格
                                                    else:
                                                        print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(u, v))
                                                else:
                                                    continue
                                                line+=1
                                        dicc['三信贷交易信息明细'].append(tep.copy())
                                    elif l == '（四）循环贷账户二':
                                        line=0
                                        tep={}
                                        tep[l] = []
                                        for m in content['section'][3][l]['section']:##
                                            for u, v in m.items():
                                                if '账户1' in u and '（授信协议标识：' in u:
                                                    if len(content['section'][3][l]['section'][line][u]['content'])>0:
                                                        lis = content['section'][3][l]['section'][line][u]['content'][0]
                                                        tep[l].append(v36_message(lis,u))  # lis：输入list表格   title表格横行标题    biaoti表格第一个框内字
                                                    else:
                                                        print( "此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(u, v))
                                                elif '账户2' in u and '（授信协议标识：' in u:
                                                    if len(content['section'][3][l]['section'][line][u]['content'])>0:
                                                        lis = content['section'][3][l]['section'][line][u]['content'][0]
                                                        tep[l].append(v36_message(lis,u))
                                                    else:
                                                        print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(u, v))
                                                else:
                                                    continue
                                                line+=1
                                        dicc['三信贷交易信息明细'].append(tep.copy())
                                    elif l == '（五）贷记卡账户':
                                        line=0
                                        tep={}
                                        tep[l] = []
                                        for m in content['section'][4][l]['section']:#
                                            for u, v in m.items():
                                                if '账户1' in u and '（授信协议标识：' in u:
                                                    if len(content['section'][4][l]['section'][line][u]['content'])>0:
                                                        lis = content['section'][4][l]['section'][line][u]['content'][0]
                                                        tep[l].append(v36_message(lis,u))  # lis：输入list表格   title表格横行标题    biaoti表格第一个框内字
                                                    else:
                                                        print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(u, v))
                                                elif '账户2' in u and '（授信协议标识：' in u:
                                                    if len(content['section'][4][l]['section'][line][u]['content']) > 0:
                                                        lis = content['section'][4][l]['section'][line][u]['content'][0]
                                                        tep[l].append(v36_message(lis,u))
                                                    else:
                                                        print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(u, v))
                                                elif '账户3' in u and '（授信协议标识：' in u:
                                                    if len(content['section'][4][l]['section'][line][u]['content'])>0:
                                                        lis = content['section'][4][l]['section'][line][u]['content'][0]
                                                        tep[l].append(v36_message(lis,u))
                                                    else:
                                                        print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(u, v))
                                                elif '账户4' in u and '（授信协议标识：' in u:
                                                    if len(content['section'][4][l]['section'][line][u]['content'])>0:
                                                        lis = content['section'][4][l]['section'][line][u]['content'][0]
                                                        tep[l].append(v36_message(lis,u))
                                                    else:
                                                        print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(u, v))
                                                else:
                                                    continue
                                                line += 1
                                        dicc['三信贷交易信息明细'].append(tep.copy())
                                    elif l == '（六）准贷记卡账户':
                                        line=0
                                        tep={}
                                        tep[l] = []
                                        for m in content['section'][5][l]['section']:  ##5,三未识别到
                                            for u, v in m.items():
                                                if '账户1' in u or '（授信协议标识：' in u:
                                                    if len(content['section'][5][l]['section'][line][u]['content'])>0:
                                                        lis = content['section'][5][l]['section'][line][u]['content'][0]
                                                        tep[l].append(v36_message(lis,u))  # lis：输入list表格   title表格横行标题    biaoti表格第一个框内字
                                                    else:
                                                        print( "此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(u, v))
                                                elif '账户2' in u or '（授信协议标识：' in u:
                                                    if len(content['section'][5][l]['section'][line][u]['content'])>0:
                                                        lis = content['section'][5][l]['section'][line][u]['content'][0]
                                                        tep[l].append(v36_message(lis,u))
                                                    else:
                                                        print( "此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(u, v))
                                                else:
                                                    continue
                                                line+=1
                                        dicc['三信贷交易信息明细'].append(tep.copy())
                                    elif l == '（七）相关还款责任信息':
                                        line = 0
                                        tep={}
                                        tep[l] = []
                                        for m in content['section'][6][l]['section']:  ##5,三未识别到
                                            for u, v in m.items():
                                                if '账户1' in u :
                                                    if len(content['section'][6][l]['section'][line][u]['content'])>0:
                                                        lis = content['section'][6][l]['section'][line][u]['content'][0]
                                                        tep[l].append(v36_message(lis,u)) # lis：输入list表格
                                                    else:
                                                        print( "此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(u, v))
                                                elif '账户2' in u:
                                                    if len(content['section'][6][l]['section'][line][u]['content'])>0:
                                                        lis = content['section'][6][l]['section'][line][u]['content'][0]
                                                        tep[l].append(v36_message(lis,u))
                                                    else:
                                                        print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(u, v))
                                                else:
                                                    continue
                                                line += 1
                                        dicc['三信贷交易信息明细'].append(tep.copy())
                                    elif l == '（八）授信协议信息':
                                        line = 0
                                        tep={}
                                        tep[l]=[]
                                        for m in content['section'][7][l]['section']:  ##5,三未识别到
                                            for u, v in m.items():
                                                if '授信协议1' in u:
                                                    if len(content['section'][7][l]['section'][line][u]['content'])>0:
                                                        lis = content['section'][7][l]['section'][line][u]['content'][0]
                                                        tep[l].append(v36_message(lis,u)) # lis：输入list表格
                                                    else:
                                                        print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(u, v))
                                                elif '授信协议2' in u:
                                                    if len(content['section'][7][l]['section'][line][u]['content'])>0:
                                                        lis = content['section'][7][l]['section'][line][u]['content'][0]
                                                        tep[l].append(v36_message(lis,u))
                                                    else:
                                                        print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(u, v))
                                                elif '授信协议3' in u:
                                                    if len(content['section'][7][l]['section'][line][u]['content'])>0:
                                                        lis = content['section'][7][l]['section'][line][u]['content'][0]
                                                        tep[l].append(v36_message(lis,u))
                                                    else:
                                                        print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(u, v))
                                                elif '授信协议4' in u:
                                                    if len(content['section'][7][l]['section'][line][u]['content'])>0:
                                                        lis = content['section'][7][l]['section'][line][u]['content'][0]
                                                        tep[l].append(v36_message(lis,u))
                                                    else:
                                                        print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(u, v))
                                                elif '授信协议5' in u:
                                                    if len(content['section'][7][l]['section'][line][u]['content'])>0:
                                                        lis = content['section'][7][l]['section'][line][u]['content'][0]
                                                        tep[l].append(v36_message(lis,u))
                                                    else:
                                                        print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(u, v))
                                                elif '授信协议6' in u:
                                                    if len(content['section'][7][l]['section'][line][u]['content'])>0:
                                                        lis = content['section'][7][l]['section'][line][u]['content'][0]
                                                        tep[l].append(v36_message(lis,u))
                                                    else:
                                                        print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(u, v))
                                                else:
                                                    continue
                                                line += 1
                                        dicc['三信贷交易信息明细'].append(tep.copy())
                        else:
                            continue
            elif k=='四非信贷交易信息明细':
                dicc['四非信贷交易信息明细']= []
                content = xiangban_PDF['data'][line]['四非信贷交易信息明细']  #
                for i, u in content.items():  # 键和值
                    if i == 'content':
                        if len(u)==0:
                            continue
                        else:
                            print("此处按照ocr输出应该没有值，如果有，请检查该表格提取的ocr信息：\n表格：{},\n键值:{}\n".format(content,u))
                    elif i == 'section':
                        if len(content['section']) > 0:
                            tep={}
                            tep['后付费记录']=[]##ocr未识别出，手动加
                            for ll in range(len(content['section'])):
                                for l in range(len(content['section'][ll])):###########
                                    if '账户' in content['section'][ll].keys():
                                        if len(content['section'][ll]['账户']['content'])>0:
                                            lis = content['section'][ll]['账户']['content'][0]
                                            tep['后付费记录'].append(v36_message(lis,'账户'))#lis：输入list表格   title表格横行标题
                                        else:
                                            print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(l, content['section'][ll]))
                            dicc['四非信贷交易信息明细'].append(tep.copy())
                        else:
                            continue
            elif k == '五公共信息明细':
                dicc['五公共信息明细']= []
                content = xiangban_PDF['data'][line]['五公共信息明细']  #
                for i, u in content.items():  # 键和值
                    if i == 'content':
                        if len(u) == 0:
                            continue
                        else:
                            print("此处按照ocr输出应该没有值，如果有，请检查该表格提取的ocr信息：\n表格：{},\n键值{}\n".format(content,u))
                    elif i == 'section':
                        if len(content['section']) > 0:
                            tep = {}
                            for ll in range(len(content['section'])):
                                for l, s in content['section'][ll].items():  ###########
                                    if l == '（一）欠税记录':
                                        if len(content['section'][ll][l]['content']) > 0:
                                            lis = content['section'][ll][l]['content'][0]
                                            dicc['五公共信息明细'].append(biaohao_message(lis,'编号',l) ) # lis：输入list表格
                                        else:
                                            print(
                                                "此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(l, s))
                                    elif l == '（二）民事判决记录':
                                        if len(content['section'][ll][l]['content']) > 0:
                                            lis = content['section'][ll][l]['content'][0]
                                            dicc['五公共信息明细'].append(biaohao_message(lis,'编号',l)) # lis：输入list表格
                                        else:
                                            print(
                                                "此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(l, s))
                                    elif l == '（三）强制执行记录':
                                        if len(content['section'][ll][l]['content']) > 0:
                                            lis = content['section'][ll][l]['content'][0]
                                            dicc['五公共信息明细'].append(biaohao_message(lis,'编号',l))  # lis：输入list表格
                                        else:
                                            print(
                                                "此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(l, s))
                                    elif l == '（四）行政处罚记录':##识别错误
                                        if len(content['section'][ll][l]['content']) > 0:
                                            lis = content['section'][ll][l]['content'][0]
                                            dicc['五公共信息明细'].append(biaohao_message(lis,'编号',l))  # lis：输入list表格   title表格横行标题    biaoti表格第一个框内字
                                        else:
                                            print(
                                                "此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(l, s))
                                    elif l == '（五）住房公积金参缴记录':
                                        ####ocr识别错误，先按照错误的测试程序执行
                                        if len(content['section'][ll][l]['content']) > 0:
                                            lis = content['section'][ll][l]['content'][0]
                                            dicc['五公共信息明细'].append(v36_message(lis,l))#lis为传入列表
                                        else:
                                            print(
                                                "此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(l, s))
                                    elif l == '（六）低保救助记录':
                                        ####ocr识别错误，先按照错误的测试程序执行
                                        if len(content['section'][ll][l]['content']) > 0:
                                            lis = content['section'][ll][l]['content'][0]
                                            dicc['五公共信息明细'].append(v36_message(lis,l))  # lis：输入list表格
                                        else:
                                            print(
                                                "此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(l, s))
                                    elif l == '（七）执业资格记录':
                                        ####ocr识别错误，先按照错误的测试程序执行
                                        if len(content['section'][ll][l]['content']) > 0:
                                            lis = content['section'][ll][l]['content'][0]
                                            dicc['五公共信息明细'].append(biaohao_message(lis,'编号',l))  # lis：输入list表格
                                        else:
                                            print(
                                                "此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(l, s))
                                    elif l == '（八）行政奖励记录':
                                        ####ocr识别错误，先按照错误的测试程序执行
                                        if len(content['section'][ll][l]['content'])>0:
                                            lis = content['section'][ll][l]['content'][0]
                                            dicc['五公共信息明细'].append(biaohao_message(lis,'编号',l))  # lis：输入list表格
                                        else:
                                            print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(l, s))

                        else:
                            continue
            elif k == '六非金融信用交易信息':
                dicc['六非金融信用交易信息']= []
                content = xiangban_PDF['data'][line]['六非金融信用交易信息']  #
                for i, u in content.items():  # 键和值
                    if i == 'content':
                        if len(u) == 0:
                            continue
                        else:
                            print("此处按照ocr输出应该没有值，如果有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(i,u))
                    elif i == 'section':
                        if len(content['section']) > 0:
                            for ll in range(len(content['section'])):
                                for l, s in content['section'][ll].items():  ###########
                                    if l == '记录1':
                                        if len(content['section'][ll][l]['content'])>0:
                                            lis = content['section'][ll][l]['content'][0]
                                            dicc['六非金融信用交易信息'].append(v36_message(lis,l))  # lis：输入list表格
                                        else:
                                            print(
                                                "此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(
                                                    l, s))
                                    elif l == '记录2':
                                        if len(content['section'][ll][l]['content']) > 0:
                                            lis = content['section'][ll][l]['content'][0]
                                            dicc['六非金融信用交易信息'].append(v36_message(lis,l))  # lis：输入list表格
                                        else:
                                            print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(l, s))
                        else:
                            continue
            elif k=='七公开信息':
                dicc['七公开信息'] =[]
                content = xiangban_PDF['data'][line]['七公开信息']  #
                for i, u in content.items():  # 键和值
                    if i == 'content':
                        if len(u)==0:
                            continue
                        else:
                            print("此处按照ocr输出应该没有值，如果有，请检查该表格提取的ocr信息：\n表格：{},\n键:{}\n".format(content,u))
                    elif i == 'section':
                        if len(content['section']) > 0:
                            for ll in range(len(content['section'])):
                                for l, s in content['section'][ll].items():###########
                                    tep = {}
                                    if l == '（一）判决信息':
                                        tep[l]=[]
                                        lines=0
                                        for m in  content['section'][ll][l]['section']:
                                            for u,v in m.items():
                                                if '记录1'in u :
                                                    lis = content['section'][ll][l]['section'][lines][u]['content'][0]
                                                    tep[l].append(v36_message(lis,u))#lis：输入list表格   title表格横行标题    biaoti表格第一个框内字
                                                elif '记录2'in u:
                                                    lis = content['section'][ll][l]['section'][lines][u]['content'][0]
                                                    tep[l].append(v36_message(lis,u))#lis：输入list表格   title表格横行标题    biaoti表格第一个框内字
                                                else:
                                                    print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值{}\n".format(l,u))
                                                lines+=1
                                        dicc['七公开信息'].append(tep.copy())
                                    ####ocr识别错误，（一）判决信息只识别为记录1和记录2
                                    elif l=='记录1':
                                        tep['（一）判决信息'] = []  ####ocr识别错误，（一）判决信息只识别为记录1和记录2
                                        lis = content['section'][ll][l]['content'][0]
                                        tep['（一）判决信息'].append(v36_message(lis, l))  # lis：输入list表格
                                        dicc['七公开信息'].append(tep.copy())
                                    elif l == '记录2':
                                        tep['（一）判决信息'] = []  ####ocr识别错误，（一）判决信息只识别为记录1和记录2
                                        lis = content['section'][ll][l]['content'][0]
                                        tep['（一）判决信息'].append( v36_message(lis, l))  # lis：输入list表格
                                        dicc['七公开信息'].append(tep.copy())
                                    ####正常的
                                    elif l == '（二）执行信息':
                                        ####ocr识别错误，按照错误的先进行测试
                                        tep[l]=[]
                                        lines=0
                                        for m in  content['section'][ll][l]['section']:#
                                            for u,v in m.items():
                                                if '记录1'in u:
                                                    lis = content['section'][ll][l]['section'][lines][u]['content'][0]
                                                    tep[l].append(v36_message(lis,u))#lis：输入list表格
                                                elif '记录2'in u :
                                                    lis = content['section'][ll][l]['section'][lines][u]['content'][0]
                                                    tep[l].append(v36_message(lis,u))#lis：输入list表格
                                                else:
                                                    print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值{}\n".format(l, u))
                                                lines+=1
                                        dicc['七公开信息'].append(tep.copy())
                                    elif l == '（三）认定类信息':
                                        ####ocr识别错误，按照错误的先进行测试
                                        tep[l]=[]
                                        lines=0
                                        for m in content['section'][ll][l]['section']:  #
                                            for u, v in m.items():
                                                if '记录1' in u:
                                                    lis = content['section'][ll][l]['section'][lines][u]['content'][0]
                                                    tep[l].append(v36_message(lis, u))  # lis：输入list表格
                                                elif '记录2' in u:
                                                    lis = content['section'][3][l]['section'][lines][u]['content'][0]
                                                    tep[l].append(v36_message(lis, u))  # lis：输入list表格
                                                else:
                                                    print(
                                                        "此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值{}\n".format(
                                                            l, u))
                                                lines+=1
                                        dicc['七公开信息'].append(tep.copy())
                                    elif l == '（四）惩戒类信息':
                                        ####ocr识别错误，按照错误的先进行测试
                                        tep[l]=[]
                                        lines=0
                                        for m in content['section'][ll][l]['section']:##
                                            for u, v in m.items():
                                                if '记录1' in u:
                                                    lis = content['section'][ll][l]['section'][lines][u]['content'][0]
                                                    tep[l].append(v36_message(lis, u))  # lis：输入list表格
                                                elif '记录2' in u:
                                                    lis = content['section'][ll][l]['section'][lines][u]['content'][0]
                                                    tep[l].append(v36_message(lis, u))  # lis：输入list表格
                                                else:
                                                    print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值{}\n".format(l, u))
                                                lines+=1
                                        dicc['七公开信息'].append(tep.copy())
                                    elif l == '（五）欠缴信息':
                                        ####ocr识别错误，按照错误的先进行测试
                                        tep[l]=[]
                                        lines=0
                                        for m in content['section'][ll][l]['section']:#
                                            for u, v in m.items():
                                                if '记录1' in u :
                                                    lis = content['section'][ll][l]['section'][lines][u]['content'][0]
                                                    tep[l].append(v36_message(lis, u)) # lis：输入list表格
                                                elif '记录2' in u:
                                                    lis = content['section'][ll][l]['section'][lines][u]['content'][0]
                                                    tep[l].append(v36_message(lis, u))
                                                else:
                                                    print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值{}\n".format(l, u))
                                                lines+=1
                                        dicc['七公开信息'].append(tep.copy())
                                    elif l == '（四）其他公开信息':
                                        tep[l]=[]
                                        lines=0
                                        for m in content['section'][ll][l]['section']:
                                            for u, v in m.items():
                                                if '记录1' in u :
                                                    lis = content['section'][ll][l]['section'][lines][u]['content'][0]
                                                    tep[l].append(v36_message(lis,u))  # lis：输入list表格   title表格横行标题    biaoti表格第一个框内字
                                                elif '记录2' in u :
                                                    lis = content['section'][ll][l]['section'][lines][u]['content'][0]
                                                    tep[l].append(v36_message(lis,u))
                                                else:
                                                    print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值{}".format(u, v))
                                                lines+=1
                                        dicc['七公开信息'].append(tep.copy())
                                    del tep
                        else:
                            continue
            elif k == '八 其他非公开信息':
                dicc['八 其他非公开信息']= []
                content = xiangban_PDF['data'][line]['八 其他非公开信息']  #
                for i, u in content.items():  # 键和值
                    if i == 'content':
                        if len(u) == 0:
                            continue
                        else:
                            print("此处按照ocr输出应该没有值，如果有，请检查该表格提取的ocr信息：\n表格：{}\n".format(content))
                    elif i == 'section':
                        if len(content['section']) > 0:
                            for ll in range(len(content['section'])):
                                for l, s in content['section'][ll].items():  ###########
                                    if l == '记录1':
                                        lis = content['section'][ll][l]['content'][0]
                                        dicc['八 其他非公开信息'].append(v36_message(lis,l))  # lis：输入list表格
                                    elif l == '记录2':
                                        lis = content['section'][ll][l]['content'][0]
                                        dicc['八 其他非公开信息'].append(v36_message(lis,l))  # lis：输入list表格
                        else:
                            continue
            elif k == '九本人声明':
                content = xiangban_PDF['data'][line]['九本人声明']  #
                for i, u in content.items():  # 键和值
                    if i == 'content':
                        if len(u) == 0:
                            print( "此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n表格：{}\n".format(content))
                        else:
                            lis = content['content'][0]
                            dicc['九本人声明']=biaohao_message(lis,'编号','本人声明')#lis为传入列表
                    elif i == 'section':
                        if len(u) == 0:
                            continue
                        else:
                            print("此处按照ocr输出应该没有值，如果有，请检查该表格提取的ocr信息：\n表格：{}\n".format(content))
            elif k == '十 异议标注':
                content = xiangban_PDF['data'][line]['十 异议标注']  #
                for i, u in content.items():  # 键和值
                    if i == 'content':
                        if len(u) == 0:
                            print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n表格：{}\n".format(content))
                        else:
                            lis = content['content'][0]
                            dicc['十 异议标注']=biaohao_message(lis,'编号','异议标注')#lis为传入列表
                    elif i == 'section':
                        if len(u) == 0:
                            print("此处按照ocr输出应该没有值，如果有，请检查该表格提取的ocr信息：\n表格：{}\n".format(content))
                        else:#######ocr识别错误，因此按照错误的先进行代码测试
                            #print("此处按照ocr输出应该没有值，如果有，请检查该表格提取的ocr信息：\n键：{},\n键值{}\n".format(i, u))
                            dicc['十一 查询记录'] = []
                            for ll in range(len(content['section'])):
                                for l, s in content['section'][ll].items():  ###########
                                    tep = {}
                                    if '机构查询记录' in l:
                                        tep[l]=[]
                                        lis = content['section'][ll][l]['content'][0]
                                        tep[l].append(biaohao_message(lis,'编号',l))  # lis：输入list表格
                                    elif '本人查询记录' in l:
                                        tep[l] = []
                                        lis = content['section'][ll][l]['content'][0]
                                        tep[l].append(biaohao_message(lis,'编号',l))
                                dicc['十一 查询记录'].append(tep.copy())
                                del tep
            elif k =='十一 查询记录':
                dicc['十一 查询记录']= []
                content = xiangban_PDF['data'][line]['十一 查询记录']  #
                for i, u in content.items():  # 键和值
                    if i == 'content':
                        if len(u) == 0:
                            break
                        else:
                            continue
                    elif i == 'section':
                        if len(u) == 0:
                            print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值{}\n".format(i, u))
                        else:  #######ocr识别错误，未识别到
                            tep = {}
                            for ll in range(len(content['section'])):
                                for l, s in content['section'][ll].items():  ###########
                                    tep[l]=[]
                                    if '机构查询记录' in l:
                                        lis = content['section'][ll][l]['content'][0]
                                        tep[l].append(biaohao_message(lis, '编号', l))  # lis：输入list表格
                                    elif '本人查询记录' in l:
                                        lis = content['section'][ll][l]['content'][0]
                                        tep[l].append(biaohao_message(lis, '编号', l))
                                    dicc['十一 查询记录'].append(tep.copy())
            else:
                continue
    return dicc

file_path = 'F:/浙商nlp项目/征信报告pdf返回结果-最新版.json'
result=json_table_find(file_path)

