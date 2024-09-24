import json
from table_parsingCH import *
import time
import requests
def json_table_find(file_path):
    start=time.time()
    with open(file_path,'r',encoding='utf-8') as file:
        xiangban_PDF = json.load(file)
    dicc={}

    for line in range(len(xiangban_PDF['data']['个人信用报告']['section'])):#xiangban_PDF['data']['个人信用报告']['section'][line].items()
        for k,v in xiangban_PDF['data']['个人信用报告']['section'][line].items():##新返回txt里添加标题之后的检索方法
            if '本人版' in k:
                content = xiangban_PDF['data']['个人信用报告']['section'][line][k]#'（本人版）'
                for i,u in content.items():#键和值
                    if i=='content':
                        lis=u
                        dicc[k]=table2json_short(lis[0])
                    elif i =='section':
                        if len(content['section'])>1:
                            for linea in range(len(content['section'])):
                                for l,s in content['section'][linea].items():
                                    if '其他证件信息' in l:
                                        if len(content['section'][linea][l]['content']) > 0:
                                            lis=content['section'][linea][l]['content'][0]
                                            dicc[k][l] = zhengjian_message(lis,l)
                                        else:
                                            print("此处ocr提取可能未提取上，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(l,s))
                                    elif '防欺诈警示' in l:
                                        if len(content['section'][linea][l]['content']) > 0:
                                            lis = content['section'][linea][l]['content'][0]
                                            dicc[k][l] = table2json_short(lis)
                                        else:
                                            print("此处ocr提取可能未提取上，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(l,s))
                                    elif '异议信息提示' in l:
                                        if len(content['section'][linea][l]['content'])>0:
                                            lis = content['section'][linea][l]['content'][0]
                                            dicc[k][l] = table2json_short(lis)
                                        else:
                                            dicc[k][l] ={}
                                            print("此处ocr提取可能未提取上，请检查该表格提取的ocr信息：\n键：{},\n提取到的键值:{}\n".format(l,s))
                        else:
                            continue
            elif '个人基本信息' in k:
                dicc[k]=[]#'一 个人基本信息'
                content = xiangban_PDF['data']['个人信用报告']['section'][line][k]  # '个人基本信息'
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
                                    if '身份信息' in l:#（一）身份信息
                                        tep={}
                                        if len(content['section'][linea][l]['content'])>0:
                                            lis = content['section'][linea][l]['content'][0]
                                            tep[l]=table2json_long(lis)#####需要修改
                                            dicc[k].append(tep.copy())
                                        else:
                                            print("此处ocr提取可能未提取上，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(l,s))
                                    elif '配偶信息' in l:#（二）配偶信息
                                        tep={}
                                        if len(content['section'][linea][l]['content']) > 0:
                                            lis = content['section'][linea][l]['content'][0]
                                            tep[l]=peiou_message(lis)
                                            dicc[k].append(tep.copy())
                                        else:
                                            print("此处ocr提取可能未提取上，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(l,s))
                                    elif '居住信息' in l:#'（三）居住信息'
                                        if len(content['section'][linea][l]['content']) > 0:
                                            lis = content['section'][linea][l]['content'][0]
                                            dicc[k].append(biaohao_message(lis,'编号',l))
                                        else:
                                            print("此处ocr提取可能未提取上，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(l,s))
                                    elif '职业信息' in l:#（四）职业信息
                                        tep={}
                                        if len(content['section'][linea][l]['content']) > 0:
                                            lis = content['section'][linea][l]['content'][0]
                                            dicc[k].append(biaohao_message(lis,'编号',l))
                                        else:
                                            print("此处ocr提取可能未提取上，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(l,s))
                                    else:
                                        continue
            elif '信息概要' in k:#二信息概要
                dicc[k] = []
                content = xiangban_PDF['data']['个人信用报告']['section'][line][k]  #
                for i, u in content.items():  # 键和值
                    if i == 'content':
                        if len(u)==0:
                            print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n表格：{},\n键值:{}\n".format(content,u))
                        else:
                            if len(content['content'])>0:
                                tep={}
                                if '信贷交易信息' not in content['content'][0]:
                                    print("此处按照ocr输出应该识别表格标题，但未识别‘信贷交易信息提示’的标题，在此手动加上了\n,章节标题：{}\n表格：{}".format(k,content))
                                    lis = content['content'][0]
                                    tep['信贷交易信息提示']=v9_message(lis,'业务类型',['贷款','信用卡','其他','合计'])
                                    dicc[k].append(tep.copy())
                                else:
                                    lis = content['信贷交易信息提示']['content'][0]
                                    tep['信贷交易信息提示'] = v9_message(lis, '业务类型',  ['贷款', '信用卡', '其他', '合计'])
                                    dicc[k].append(tep.copy())
                            else:
                                print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值{}".format(i, u))
                    elif i == 'section':
                        if len(content['section']) > 1:
                            for ll in range(len(content['section'])):
                                for l, s in content['section'][ll].items():
                                    if '信贷交易违约信息' in l:#（二）信贷交易违约信息概要
                                        line=0
                                        tep={}
                                        tep[l] = []
                                        for m in  content['section'][ll][l]['section']:
                                            for u,v in m.items():
                                                if '被追偿信息' in u:#被追偿信息汇总
                                                    if len(content['section'][ll][l]['section'][line][u]['content'])>0:
                                                        lis = content['section'][ll][l]['section'][line][u]['content'][0]
                                                        tep[l].append(title_heji_table(lis,u))
                                                    else:
                                                        print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(u, v))
                                                elif '呆账信息' in u:#呆账信息汇总
                                                    if len(content['section'][ll][l]['section'][line][u]['content']) > 0:
                                                        lis = content['section'][ll][l]['section'][line][u]['content'][0]
                                                        tep[l].append(little_title_table(lis,u,'账户数'))#lis：输入list表格   title表格横行标题    biaoti表格第一个框内字
                                                    else:
                                                        print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(u, v))
                                                elif '逾期透支信息' in u:#逾期（透支）信息汇总
                                                    if len(content['section'][ll][l]['section'][line][u]['content']) > 0:
                                                        lis = content['section'][ll][l]['section'][line][u]['content'][0]
                                                        tep[l].append(little_title_table(lis,u,'账户类型'))
                                                    else:
                                                        print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(
                                                                u, v))
                                                else:
                                                    print("此处按照ocr输出应该不含其他类型表格，如果有值，可能存在表格粘连情况，请检查该表格提取的ocr信息：\n当前表格名称：{},\n表格内容:{},\n表格大标题:{}\n".format(u, v,k))
                                                line+=1
                                        dicc[k].append(tep.copy())
                                        del tep
                                    elif '信贷交易授信及负债' in l:#（三）信贷交易授信及负债信息概要（未结清/未销户）
                                        line=0
                                        tep={}
                                        tep[l] = []
                                        for m in  content['section'][ll][l]['section']:#未识别到
                                            for u,v in m.items():
                                                if '非循环贷账户信息' in u:#非循环贷账户信息汇总
                                                    if len(content['section'][ll][l]['section'][line][u]['content'])>0:
                                                        lis = content['section'][ll][l]['section'][line][u]['content'][0]
                                                        tep[l].append(little_title_table(lis,u,'管理机构数'))#lis：输入list表格   title表格横行标题    biaoti表格第一个框内字
                                                    else:
                                                        print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(u, v))
                                                elif '循环贷账户一信息' in u:
                                                    if len(content['section'][ll][l]['section'][line][u]['content']) > 0:
                                                        lis = content['section'][ll][l]['section'][line][u]['content'][0]
                                                        tep[l].append(little_title_table(lis,u,'管理机构数'))#lis：输入list表格   title表格横行标题    biaoti表格第一个框内字
                                                    else:
                                                        print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(u, v))
                                                elif '循环贷账户二信息' in u:
                                                    if len(content['section'][ll][l]['section'][line][u]['content']) > 0:
                                                        lis = content['section'][ll][l]['section'][line][u]['content'][0]
                                                        tep[l].append(little_title_table(lis,u,'管理机构数'))
                                                    else:
                                                        print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(u, v))
                                                elif '贷记卡账户信息' in u:
                                                    if len(content['section'][ll][l]['section'][line][u]['content']) > 0:
                                                        lis = content['section'][ll][l]['section'][line][u]['content'][0]
                                                        tep[l].append(little_title_table(lis,u,'发卡机构数'))
                                                    else:
                                                        print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(u, v))
                                                elif '准贷记卡账户信息' in u:
                                                    if len(content['section'][ll][l]['section'][line][u]['content']) > 0:
                                                        lis = content['section'][ll][l]['section'][line][u]['content'][0]
                                                        tep[l].append(little_title_table(lis,u,'发卡机构数'))
                                                    else:
                                                        print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(u, v))
                                                elif '相关还款责任信息' in u:
                                                    if len(content['section'][ll][l]['section'][line][u]['content']) > 0:
                                                        lis = content['section'][ll][l]['section'][line][u]['content'][0]
                                                        tep[l].append(v18_message(lis,u))
                                                    else:
                                                        print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(u, v))
                                                else:
                                                    continue
                                                line+=1
                                        dicc[k].append(tep.copy())
                                    elif '非信贷交易信息' in l:#（四）非信贷交易信息概要
                                        line=0
                                        try:
                                           for m in content['section'][ll][l]['section']:
                                               for u, v in m.items():
                                                   if '后付费业务欠费信息汇总' in u:
                                                       if len(content['section'][ll][l]['section'][line][u]['content'])>0:
                                                           lis = content['section'][ll][l]['section'][line][u]['content'][0]
                                                           dicc[k].append(little_title_table(lis,l+'--'+u,'业务类型'))  # lis：输入list表格
                                                       else:
                                                           print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(u, v))
                                                   else:
                                                       print("此处按照ocr输出应该没有值，如果有，请检查该表格提取的ocr信息：\n当前表格标题：{},\n表格内容:{},\n章节标题:{}\n".format(u, v,k))
                                                   line+=1
                                        except KeyError:
                                            dicc[k].append(l)
                                            print("此处可能存在ocr识别漏标题情况：\n表格：{},\n标题：{}\n".format(content,l))
                                    elif '公共信息概要' in l:#（五）公共信息概要
                                        line=0
                                        try:
                                            for m in content['section'][ll][l]['section']:##
                                                for u, v in m.items():
                                                    if '公共信息汇总' in u:
                                                        if len(content['section'][ll][l]['section'][line][u]['content'])>0:
                                                            lis = content['section'][ll][l]['section'][line][u]['content'][0]
                                                            dicc[k].append(little_title_table(lis, l+'--'+u,'信息类型') ) # lis：输入list表格   title表格横行标题    biaoti表格第一个框内字
                                                        else:
                                                            print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(u, v))
                                                    else:
                                                        print("此处按照ocr输出应该没有值，如果有，请检查该表格提取的ocr信息：\n当前表格标题：{},\n表格内容:{},\n章节标题:{}\n".format(u, v,k))
                                                    line+=1
                                        except KeyError:
                                            dicc[k].append(l)
                                            print("此处可能存在ocr识别漏标题情况：\n表格：{},\n标题：{}\n".format(content,l))
                                    elif '非金融信用交易信息概要' in l:#（六）非金融信用交易信息概要
                                        try:
                                            for m in range(len(content['section'][ll][l]['content'])):#4,三未识别到
                                                u=content['section'][ll][l]['content']
                                                if isinstance(u,list):
                                                    if len(u)>0:
                                                        lis = content['section'][ll][l]['content'][0]
                                                        dicc[k].append(little_title_table(lis,l,'信息类型'))  # lis：输入list表格   title表格横行标题    biaoti表格第一个框内字
                                                    else:
                                                        print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(u, m))
                                                else:
                                                    print("此处按照ocr输出应该没有值，如果有，请检查该表格提取的ocr信息：\n表格内容:{},\n章节标题:{}\n".format(u, k))
                                        except KeyError:
                                            dicc[k].append(l)
                                            print("此处可能存在ocr识别漏标题情况：\n表格：{},\n标题：{}\n".format(content,l))
                                    elif  '公开信息概要' in l:#（七）公开信息概要
                                        line=0
                                        try:
                                            for m in content['section'][ll][l]['section']:  ##5,三未识别到
                                                for u, v in m.items():
                                                    if '公开信息汇总' in u:
                                                        if len(content['section'][ll][l]['section'][line][u]['content'])>0:
                                                            lis = content['section'][ll][l]['section'][line][u]['content'][0]
                                                            dicc[k].append(little_title_table(lis,l+'--'+u,'信息类型'))  # lis：输入list表格   title表格横行标题    biaoti表格第一个框内字
                                                        else:
                                                            print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(u, v))
                                                    else:
                                                        print("此处按照ocr输出应该没有值，如果有，请检查该表格提取的ocr信息：\n当前表格标题：{},\n表格内容:{},\n章节标题:{}\n".format(u, v,k))
                                                    line+=1
                                        except KeyError:
                                            dicc[k].append(l)
                                            print("此处可能存在ocr识别漏标题情况：\n表格：{},\n标题：{}\n".format(content,l))
                                    elif '查询记录概要' in l:#（八）查询记录概要
                                        tep={}
                                        tep[l] = []
                                        for q, g in s.items():
                                            try:
                                                if q=='content':
                                                    if len(content['section'][ll][l]['content'])>0:##6,三未识别到
                                                        lis = content['section'][ll][l]['content'][0]
                                                        tep[l].append(v23_message(lis,'查询记录概要'))
                                                    else:
                                                        print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(l, g))
                                                elif q=='section':
                                                    if len(content['section'][ll][l]['section'][0]['异议及说明信息']['content'])>0:
                                                        lis = content['section'][ll][l]['section'][0]['异议及说明信息']['content'][0]
                                                        tep[l].append(little_title_table(lis,'异议及说明信息','异议标注'))
                                                    else:
                                                        print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(l, g))
                                            except IndexError:
                                                print("此处可能存在ocr识别漏标题情况：\n表格：{},\n标题：{}\n".format(content, l))
                                            else:
                                                print(
                                                    "此处按照ocr输出应该没有值，如果有，请检查该表格提取的ocr信息：\n当前表格标题：{},\n表格内容:{},\n章节标题:{}\n".format(l, g, k))
                                        dicc[k].append(tep.copy())
                        else:
                            print("此处按照ocr输出应该没有值，如果有，请检查该表格提取的ocr信息：\n章节标题：{},\n表格内容:{}\n".format( k,content))

            elif '非信贷交易' in k:#四非信贷交易信息明细
                dicc[k]= []
                content = xiangban_PDF['data']['个人信用报告']['section'][line][k]  #
                for i, u in content.items():  # 键和值
                    if i == 'content':
                        if len(u)==0:
                            continue
                        else:
                            print("此处按照ocr输出应该没有值，如果有，请检查该表格提取的ocr信息：\n表格：{},\n键值:{}\n".format(content,u))
                    elif i == 'section':
                        if len(content['section']) > 0:
                            tep={}
                            ##ocr未识别出'后付费记录'
                            for ll in range(len(content['section'])):
                                for q,g in content['section'][ll].items():###########
                                    if '后付费' in q :
                                        tep[q]=[]
                                        line=0
                                        try:
                                            for m in content['section'][ll][q]['section']:  ##未识别到
                                                for l, s in m.items():
                                                    if '账户' in u:
                                                        if len(content['section'][ll][l]['section'][line][u]['content'])>0:
                                                            lis = content['section'][ll][l]['section'][line][u]['content'][0]
                                                            tep[q].append(v36_message(lis,u))#lis：输入list表格   title表格横行标题
                                                        else:
                                                            print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(l, content['section'][ll]))
                                                    line+=1
                                                dicc[k].append(tep.copy())
                                        except KeyError:
                                            print("此处可能存在ocr识别漏标题情况：\n表格：{},\n标题：{}\n".format(content,k))
                                    elif '账户' in q:#ocr识别错误的情况
                                        print("ocr未识别到表格标题，请检查此处表格ocr识别结果\n章节标题：{}，\n表格标题：{}，\n提取内容{}\n".format(k,q,content))
                                        tep[q] = []
                                        if len(content['section'][ll][q]['content']) > 0:
                                            lis = content['section'][ll][q]['content'][0]
                                             # lis：输入list表格   title表格横行标题
                                            tep[q].append(v36_message(lis, '账户'))
                                        else:
                                            print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(l, content['section'][ll]))

                                    else:
                                        print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(
                                                    l, content['section'][ll]))
                                    dicc[k].append(tep.copy())
                                    tep={}
                        else:
                            print("此处按照ocr输出应该没有值，如果有,可能存在表格粘连问题，请检查该表格提取的ocr信息：\n表格标题：{},\n表格内容:{}\n".format(
                                    k, content))
            elif '信贷交易' in k:#三信贷交易信息明细
                dicc[k] = []
                content = xiangban_PDF['data']['个人信用报告']['section'][line][k]  #
                for i, u in content.items():  # 键和值
                    if 'content' in i:
                        if len(u)==0:
                            continue
                        else:
                            print("此处按照ocr输出应该没有值，如果有，请检查该表格提取的ocr信息：\n表格：{},\n键值:{}\n".format(content, u))
                    elif 'section' in i:
                        if len(content['section']) > 0:
                            for ll in range(len(content['section'])):
                                for l, s in content['section'][ll].items():###########
                                    if '被追偿' in l:#（一）被追偿信息
                                        line=0
                                        tep={}
                                        tep[l] = []
                                        for m in  content['section'][ll][l]['section']:
                                            for u,v in m.items():
                                                if '账户1' in u :
                                                    if len(content['section'][ll][l]['section'][line][u]['content'])>0:
                                                        lis = content['section'][ll][l]['section'][line][u]['content'][0]
                                                        #lis：输入list表格   title表格横行标题
                                                        tep[l].append(v36_message(lis,u))
                                                    else:
                                                        print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(u, v))
                                                elif '账户2' in u:
                                                    if len(content['section'][ll][l]['section'][line][u]['content']) > 0:
                                                        lis = content['section'][ll][l]['section'][line][u]['content'][0]
                                                        #lis：输入list表格   title表格横行标题
                                                        tep[l].append(v36_message(lis,u))
                                                    else:
                                                        print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(u, v))
                                                else:
                                                    continue
                                                line+=1
                                        dicc[k].append(tep.copy())
                                    elif '非循环贷账户' in l:#（二）非循环贷账户
                                        line=0
                                        tep={}
                                        tep[l] = []
                                        try:
                                            for m in  content['section'][ll][l]['section']:#
                                                for u,v in m.items():
                                                    if '账户1'in u or '（授信协议标识：' in u:
                                                        if len(content['section'][ll][l]['section'][line][u]['content'])>0:
                                                            lis = content['section'][ll][l]['section'][line][u]['content'][0]
                                                            tep[l].append(v36_message(lis,u))#lis：输入list表格
                                                        else:
                                                            print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(u, v))
                                                    elif '账户2'in u or '（授信协议标识：' in u:
                                                        if len(content['section'][ll][l]['section'][line][u]['content']) > 0:
                                                            lis = content['section'][ll][l]['section'][line][u]['content'][0]
                                                            tep[l].append(v36_message(lis,u))#lis：输入list表格
                                                        else:
                                                            print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(u, v))
                                                    elif '账户3'in u or '（授信协议标识：' in u:
                                                        if len(content['section'][ll][l]['section'][line][u]['content']) > 0:
                                                            lis = content['section'][ll][l]['section'][line][u]['content'][0]
                                                            tep[l].append(v36_message(lis,u))
                                                        else:
                                                            print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(
                                                                    u, v))
                                                    elif '账户4'in u or '（授信协议标识：' in u:
                                                        if len(content['section'][ll][l]['section'][line][u]['content']) > 0:
                                                            lis = content['section'][ll][l]['section'][line][u]['content'][0]
                                                            tep[l].append(v36_message(lis,u))
                                                        else:
                                                            print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(u, v))
                                                    else:
                                                        continue
                                                    line+=1
                                        except KeyError:
                                            print("此处可能存在ocr识别漏标题情况：\n表格：{},\n标题：{}\n".format(content,l))
                                        dicc[k].append(tep.copy())
                                    elif '循环贷账户' in l:#（三）循环贷账户-
                                        line=0
                                        tep={}
                                        tep[l] = []
                                        for m in content['section'][ll][l]['section']:#
                                            for u, v in m.items():
                                                if '账户1' in u and '（授信协议标识：' in u:
                                                    if len(content['section'][ll][l]['section'][line][u]['content'])>0:
                                                        lis = content['section'][ll][l]['section'][line][u]['content'][0]
                                                        tep[l].append(v36_message(lis,u)) # lis：输入list表格
                                                    else:
                                                        print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(u, v))
                                                elif '账户2' in u and '（授信协议标识：' in u:
                                                    if len(content['section'][ll][l]['section'][line][u]['content']) > 0:
                                                        lis = content['section'][ll][l]['section'][line][u]['content'][0]
                                                        tep[l].append(v36_message(lis,u))  # lis：输入list表格
                                                    else:
                                                        print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(u, v))
                                                else:
                                                    continue
                                                line+=1
                                        dicc[k].append(tep.copy())
                                    elif '循环贷账户二' in l:#（四）循环贷账户二
                                        line=0
                                        tep={}
                                        tep[l] = []
                                        for m in content['section'][ll][l]['section']:##
                                            for u, v in m.items():
                                                if '账户1' in u and '（授信协议标识：' in u:
                                                    if len(content['section'][ll][l]['section'][line][u]['content'])>0:
                                                        lis = content['section'][ll][l]['section'][line][u]['content'][0]
                                                        tep[l].append(v36_message(lis,u))  # lis：输入list表格   title表格横行标题    biaoti表格第一个框内字
                                                    else:
                                                        print( "此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(u, v))
                                                elif '账户2' in u and '（授信协议标识：' in u:
                                                    if len(content['section'][ll][l]['section'][line][u]['content'])>0:
                                                        lis = content['section'][ll][l]['section'][line][u]['content'][0]
                                                        tep[l].append(v36_message(lis,u))
                                                    else:
                                                        print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(u, v))
                                                else:
                                                    continue
                                                line+=1
                                        dicc[k].append(tep.copy())
                                    elif '贷记卡账户' in l:#（五）贷记卡账户
                                        line=0
                                        tep={}
                                        tep[l] = []
                                        for m in content['section'][ll][l]['section']:#
                                            for u, v in m.items():
                                                if '账户1' in u or '（授信协议标识：' in u:
                                                    if len(content['section'][ll][l]['section'][line][u]['content'])>0:
                                                        lis = content['section'][ll][l]['section'][line][u]['content'][0]
                                                        tep[l].append(v36_message(lis,u))  # lis：输入list表格   title表格横行标题    biaoti表格第一个框内字
                                                    else:
                                                        print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(u, v))
                                                elif '账户2' in u or '（授信协议标识：' in u:
                                                    if len(content['section'][ll][l]['section'][line][u]['content']) > 0:
                                                        lis = content['section'][ll][l]['section'][line][u]['content'][0]
                                                        tep[l].append(v36_message(lis,u))
                                                    else:
                                                        print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(u, v))
                                                elif '账户3' in u or '（授信协议标识：' in u:
                                                    if len(content['section'][ll][l]['section'][line][u]['content'])>0:
                                                        lis = content['section'][ll][l]['section'][line][u]['content'][0]
                                                        tep[l].append(v36_message(lis,u))
                                                    else:
                                                        print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(u, v))
                                                elif '账户4' in u or '（授信协议标识：' in u:
                                                    if len(content['section'][ll][l]['section'][line][u]['content'])>0:
                                                        lis = content['section'][ll][l]['section'][line][u]['content'][0]
                                                        tep[l].append(v36_message(lis,u))
                                                    else:
                                                        print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(u, v))
                                                else:
                                                    continue
                                                line += 1
                                        dicc[k].append(tep.copy())
                                    elif '准贷记卡' in l:#（六）准贷记卡账户
                                        line=0
                                        tep={}
                                        tep[l] = []
                                        for m in content['section'][ll][l]['section']:  ##5,三未识别到
                                            for u, v in m.items():
                                                if '账户1' in u or '（授信协议标识：' in u:
                                                    if len(content['section'][ll][l]['section'][line][u]['content'])>0:
                                                        lis = content['section'][ll][l]['section'][line][u]['content'][0]
                                                        tep[l].append(v36_message(lis,u))  # lis：输入list表格   title表格横行标题    biaoti表格第一个框内字
                                                    else:
                                                        print( "此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(u, v))
                                                elif '账户2' in u or '（授信协议标识：' in u:
                                                    if len(content['section'][ll][l]['section'][line][u]['content'])>0:
                                                        lis = content['section'][ll][l]['section'][line][u]['content'][0]
                                                        tep[l].append(v36_message(lis,u))
                                                    else:
                                                        print( "此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(u, v))
                                                else:
                                                    continue
                                                line+=1
                                        dicc[k].append(tep.copy())
                                    elif '相关还款责任' in l:#（七）相关还款责任信息
                                        line = 0
                                        tep={}
                                        tep[l] = []
                                        for m in content['section'][ll][l]['section']:  ##5,三未识别到
                                            for u, v in m.items():
                                                if '账户1' in u :
                                                    if len(content['section'][ll][l]['section'][line][u]['content'])>0:
                                                        lis = content['section'][ll][l]['section'][line][u]['content'][0]
                                                        tep[l].append(v36_message(lis,u)) # lis：输入list表格
                                                    else:
                                                        print( "此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(u, v))
                                                elif '账户2' in u:
                                                    if len(content['section'][ll][l]['section'][line][u]['content'])>0:
                                                        lis = content['section'][ll][l]['section'][line][u]['content'][0]
                                                        tep[l].append(v36_message(lis,u))
                                                    else:
                                                        print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(u, v))
                                                else:
                                                    continue
                                                line += 1
                                        dicc[k].append(tep.copy())
                                    elif '授信协议' in l:#（八）授信协议信息
                                        line = 0
                                        tep={}
                                        tep[l]=[]
                                        for m in content['section'][ll][l]['section']:  ##5,三未识别到
                                            for u, v in m.items():
                                                if '授信协议1' in u:
                                                    if len(content['section'][ll][l]['section'][line][u]['content'])>0:
                                                        lis = content['section'][ll][l]['section'][line][u]['content'][0]
                                                        tep[l].append(v36_message(lis,u)) # lis：输入list表格
                                                    else:
                                                        print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(u, v))
                                                elif '授信协议2' in u:
                                                    if len(content['section'][ll][l]['section'][line][u]['content'])>0:
                                                        lis = content['section'][ll][l]['section'][line][u]['content'][0]
                                                        tep[l].append(v36_message(lis,u))
                                                    else:
                                                        print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(u, v))
                                                elif '授信协议3' in u:
                                                    if len(content['section'][ll][l]['section'][line][u]['content'])>0:
                                                        lis = content['section'][ll][l]['section'][line][u]['content'][0]
                                                        tep[l].append(v36_message(lis,u))
                                                    else:
                                                        print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(u, v))
                                                elif '授信协议4' in u:
                                                    if len(content['section'][ll][l]['section'][line][u]['content'])>0:
                                                        lis = content['section'][ll][l]['section'][line][u]['content'][0]
                                                        tep[l].append(v36_message(lis,u))
                                                    else:
                                                        print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(u, v))
                                                elif '授信协议5' in u:
                                                    if len(content['section'][ll][l]['section'][line][u]['content'])>0:
                                                        lis = content['section'][ll][l]['section'][line][u]['content'][0]
                                                        tep[l].append(v36_message(lis,u))
                                                    else:
                                                        print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(u, v))
                                                elif '授信协议6' in u:
                                                    if len(content['section'][ll][l]['section'][line][u]['content'])>0:
                                                        lis = content['section'][ll][l]['section'][line][u]['content'][0]
                                                        tep[l].append(v36_message(lis,u))
                                                    else:
                                                        print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(u, v))
                                                else:
                                                    continue
                                                line += 1
                                        dicc[k].append(tep.copy())
                        else:
                            print("此处按照ocr输出应该没有值，如果有,可能存在表格粘连问题，请检查该表格提取的ocr信息：\n表格标题：{},\n表格内容:{}\n".format(
                                    k, content))
            elif '公共信息明细' in k:#五公共信息明细
                dicc[k]= []
                content = xiangban_PDF['data']['个人信用报告']['section'][line][k]  #
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
                                    if '欠税记录' in l:#（一）欠税记录
                                        if len(content['section'][ll][l]['content']) > 0:
                                            lis = content['section'][ll][l]['content'][0]
                                            dicc[k].append(biaohao_message(lis,'编号',l) ) # lis：输入list表格
                                        else:
                                            print(
                                                "此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(l, s))
                                    elif '民事判决' in l:#（二）民事判决记录
                                        if len(content['section'][ll][l]['content']) > 0:
                                            lis = content['section'][ll][l]['content'][0]
                                            dicc[k].append(biaohao_message(lis,'编号',l)) # lis：输入list表格
                                        else:
                                            print(
                                                "此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(l, s))
                                    elif '强制执行' in l:#（三）强制执行记录
                                        if len(content['section'][ll][l]['content']) > 0:
                                            lis = content['section'][ll][l]['content'][0]
                                            dicc[k].append(biaohao_message(lis,'编号',l))  # lis：输入list表格
                                        else:
                                            print(
                                                "此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(l, s))
                                    elif '行政处罚' in l:##（四）行政处罚记录 识别错误
                                        if len(content['section'][ll][l]['content']) > 0:
                                            lis = content['section'][ll][l]['content'][0]
                                            dicc[k].append(biaohao_message(lis,'编号',l))  # lis：输入list表格   title表格横行标题    biaoti表格第一个框内字
                                        else:
                                            print(
                                                "此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(l, s))
                                    elif '住房公积金参缴' in l:#（五）住房公积金参缴记录
                                        if len(content['section'][ll][l]['content']) > 0:
                                            lis = content['section'][ll][l]['content'][0]
                                            dicc[k].append(v36_message(lis,l))#lis为传入列表
                                        else:
                                            print(
                                                "此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(l, s))
                                    elif '低保救助' in l:#（六）低保救助记录
                                        if len(content['section'][ll][l]['content']) > 0:
                                            lis = content['section'][ll][l]['content'][0]
                                            dicc[k].append(v36_message(lis,l))  # lis：输入list表格
                                        else:
                                            print(
                                                "此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(l, s))
                                    elif  '执业资格' in l:#（七）执业资格记录
                                        if len(content['section'][ll][l]['content']) > 0:
                                            lis = content['section'][ll][l]['content'][0]
                                            dicc[k].append(biaohao_message(lis,'编号',l))  # lis：输入list表格
                                        else:
                                            print(
                                                "此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(l, s))
                                    elif '行政奖励' in l:#（八）行政奖励记录
                                        if len(content['section'][ll][l]['content'])>0:
                                            lis = content['section'][ll][l]['content'][0]
                                            dicc[k].append(biaohao_message(lis,'编号',l))  # lis：输入list表格
                                        else:
                                            print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(l, s))

                        else:
                            print("此处按照ocr输出应该没有值，如果有,可能存在表格粘连问题，请检查该表格提取的ocr信息：\n表格标题：{},\n表格内容:{}\n".format(
                                    k, content))
            elif '非金融信用交易' in k:#六非金融信用交易信息
                dicc[k]= []
                content = xiangban_PDF['data']['个人信用报告']['section'][line][k]  #
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
                                    if '记录1' in l:
                                        if len(content['section'][ll][l]['content'])>0:
                                            lis = content['section'][ll][l]['content'][0]
                                            dicc[k].append(v36_message(lis,l))  # lis：输入list表格
                                        else:
                                            print(
                                                "此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(
                                                    l, s))
                                    elif '记录2' in l:
                                        if len(content['section'][ll][l]['content']) > 0:
                                            lis = content['section'][ll][l]['content'][0]
                                            dicc[k].append(v36_message(lis,l))  # lis：输入list表格
                                        else:
                                            print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值:{}\n".format(l, s))
                                    else:
                                        print("此处按照ocr输出应该有没值，如果有，请检查该表格提取的ocr信息：\n键：{},\n键值:{},\n章节标题:{}\n".format(l, s,k))
                        else:
                            print("此处按照ocr输出应该没有值，如果有,可能存在表格粘连问题，请检查该表格提取的ocr信息：\n表格标题：{},\n表格内容:{}\n".format(
                                    k, content))

            elif '其他非公开信息' in k:#八 其他非公开信息
                dicc[k]= []
                content = xiangban_PDF['data']['个人信用报告']['section'][line][k]  #
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
                                        dicc[k].append(v36_message(lis,l))  # lis：输入list表格
                                    elif l == '记录2':
                                        lis = content['section'][ll][l]['content'][0]
                                        dicc[k].append(v36_message(lis,l))  # lis：输入list表格
                        else:
                            print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n表格标题：{},\n表格内容{}\n".format(k,content))
            elif '公开信息' in k: #七公开信息
                dicc[k] =[]
                content = xiangban_PDF['data']['个人信用报告']['section'][line][k]  #
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
                                    if '判决' in l:#（一）判决信息  未识别出
                                        tep[l]=[]
                                        lines=0
                                        for m in  content['section'][ll][l]['section']:
                                            for u,v in m.items():
                                                if '记录1' in u :
                                                    lis = content['section'][ll][l]['section'][lines][u]['content'][0]
                                                    tep[l].append(v36_message(lis,u))#lis：输入list表格   title表格横行标题    biaoti表格第一个框内字
                                                elif '记录2' in u:
                                                    lis = content['section'][ll][l]['section'][lines][u]['content'][0]
                                                    tep[l].append(v36_message(lis,u))#lis：输入list表格   title表格横行标题    biaoti表格第一个框内字
                                                else:
                                                    print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n键：{},\n键值{}\n".format(l,u))
                                                lines+=1
                                        dicc[k].append(tep.copy())
                                    elif '记录' in l:
                                        print("表格ocr识别中可能存在表格识别小标题未识别到的情况，请检查该表格\n表格：{},\n表格标题：{},\n表格名称：{}\n".format(content,k,l))
                                    elif  '执行' in l:#（二）执行信息
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
                                        dicc[k].append(tep.copy())
                                    elif '认定类' in l:#（三）认定类信息
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
                                        dicc[k].append(tep.copy())
                                    elif '惩戒类' in l:#（四）惩戒类信息
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
                                        dicc[k].append(tep.copy())
                                    elif '欠缴' in l:#（五）欠缴信息
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
                                        dicc[k].append(tep.copy())
                                    elif '其他公开' in l:#（四）其他公开信息
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
                                        dicc[k].append(tep.copy())
                                    del tep
                        else:
                            print("此处按照ocr输出应该没有值，如果有,可能存在表格粘连问题，请检查该表格提取的ocr信息：\n表格标题：{},\n表格内容:{}\n".format(
                                    k, content))
            elif '本人声明' in k:#九本人声明
                content = xiangban_PDF['data']['个人信用报告']['section'][line][k]  #
                for i, u in content.items():  # 键和值
                    if i == 'content':
                        if len(u) == 0:
                            print( "此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n表格：{}\n".format(content))
                        else:
                            lis = content['content'][0]
                            dicc[k]=biaohao_message(lis,'编号','本人声明')#lis为传入列表
                    elif i == 'section':
                        if len(u) == 0:
                            continue
                        else:
                            print("此处按照ocr输出应该没有值，如果有，请检查该表格提取的ocr信息：\n表格：{}\n".format(content))
                    else:
                        print("此处按照ocr输出应该没有值，如果有,可能存在表格粘连问题，请检查该表格提取的ocr信息：\n表格标题：{},\n表格内容:{}\n".format(
                                k, content))
            elif '异议标注' in k:#十 异议标注
                content = xiangban_PDF['data']['个人信用报告']['section'][line][k]  #
                for i, u in content.items():  # 键和值
                    if i == 'content':
                        if len(u) == 0:
                            print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n表格：{}\n".format(content))
                        else:
                            lis = content['content'][0]
                            dicc[k]=biaohao_message(lis,'编号','异议标注')#lis为传入列表
                    elif i == 'section':
                        if len(u) == 0:
                            continue
                        else:
                            print("此处按照ocr输出应该没有值，如果有，请检查该表格提取的ocr信息：\n表格标题：{},\n键值{}\n".format(k, u))
                    else:
                        print( "此处按照ocr输出应该没有值，如果有,可能存在表格粘连问题，请检查该表格提取的ocr信息：\n表格标题：{},\n表格内容:{}\n".format(
                                k, content))
            elif '查询记录' in k:#十一 查询记录
                dicc[k]= []
                content = xiangban_PDF['data']['个人信用报告']['section'][line][k]  #
                for i, u in content.items():  # 键和值
                    if i == 'content':
                        if len(u) == 0:
                            break
                        else:
                            continue
                    elif i == 'section':
                        if len(u) == 0:
                            print("此处按照ocr输出应该有值，如果没有，请检查该表格提取的ocr信息：\n标题：{},\n键值{}\n".format(k, u))
                        elif len(u)>0:
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
                                    dicc[k].append(tep.copy())
                        else:
                            print("此处按照ocr输出应该没有值，如果有,可能存在表格粘连问题，请检查该表格提取的ocr信息：\n表格标题：{},\n表格内容:{}\n".format(
                                    k, content))
            else:
                continue

    # try:
    #     dicen= {}
    #     dicen[key_2_English.key_2_English('个人信用报告')]=[]
    #     for k,v in dicc.items():
    #         tep={}
    #         tep[key_2_English.key_2_English(k)]=key_2_English.translate_answer_key(v)
    #         dicen[key_2_English.key_2_English('个人信用报告')].append(tep)
    #
    # except requests.exceptions.JSONDecodeError:
    #     print("翻译过程中存在连接或网址等问题，请重新运行或者手动在词典中添加英文键值")
    end = time.time()
    process_time=end-start
    print(process_time)
    return dicc#key_2_English.translate_answer_key(dicc)

file_path = 'F:/浙商nlp项目/征信报告详版返回示例V1.json'
result=json_table_find(file_path)
print(result)
