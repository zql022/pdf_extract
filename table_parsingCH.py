import key_2_English

def zhengjian_message(lis,l):
    dicc=[]
    contents = [item for item in lis[0] if item and item is not None]  # 第一行做表头
    for i in range(1,int(len(lis[1:]))+1):
        contents0 = [item for item in lis[i] if item and item is not None]  #
        # contents1 = [item for item in lis[2*i] if item and item is not None]  #
        tep0=dict(zip(contents,contents0))
        # tep1 = dict(zip(contents, contents1))  # 第一行作为表头
        # combined_dict = {key: [tep0[key], tep1[key]] for key in tep0.keys()}
        dicc.append(tep0)
    return dicc#key_2_English.translate_answer_key(dicc)
v4 = [[['证件类型', '证件号码'],
  ['护照', 'G30003516'],
  ['军官证', 'M0938981'],
['身份证', '125648'],
['士兵证', 's4541']]]
# print(zhengjian_message(v4[0],'其他证件信息'))
def table2json_long(lis):#不能表格行数少于三行，否则直接跳出循环
    dicc = {}
    for linea in range(int(len(lis)/2-1)):#列竖行对应
        for t,z in enumerate(lis[2*linea]):
            if z == None:#表格合并，无值情况
                continue
            elif '：' in z:#有冒号情况
                str, st = z.split('：')
                dicc[str] = st
            elif len(z) == 0:#‘’情况
                continue
            elif '编号' in z:#横行读情况
                ss = lis[linea*2:]  # 有个问题，要是横行对应的不到表格末端也会有问题
                #transposed = [[row[i] for row in ss] for i in range(len(ss[0]))]#列表转秩
                zilis = []
                tem = {}
                dicc['编号'] = zilis
                for r in range(int(len(ss)-1)):#列
                    for a, b in enumerate(ss[r+1]):#行  第一行做表头
                        if b == None:#表格合并，无值情况
                            continue
                        elif len(b) == 0:#‘’情况
                            continue
                        else:
                            tem[ss[0][a]]=b
                    temp = tem.copy()
                    dicc['编号'].append(temp)
                    tem={}
                return dicc#key_2_English.translate_answer_key(dicc)
            else:
                dicc[z] = lis[2*linea + 1][t]
    return dicc#key_2_English.translate_answer_key(dicc)
def table2json_short(lis):#表格行数较少，不会出现横行对应情况
    dicc = {}
    if len(lis)>2:
        for linea in range(int(len(lis)-1)):#列竖行对应
            for t,z in enumerate(lis[linea]):
                if z == '':#表格合并，无值情况
                    continue
                elif '：' in z : #有冒号情况
                    stri = z.replace('\n','')
                    str, st = stri.split('：')
                    dicc[str] = st
                elif ':' in z:
                    stri = z.replace('\n', ' ')
                    str, st = stri.split(': ')
                    dicc[str] = st
                elif len(z) == 0:#‘’情况
                    continue
                else:
                    dicc[z] = lis[linea + 1][t]
    elif len(lis)<3:#只有两行情况
        valid_contents0 = [item for item in lis[0] if item and item is not None]
        valid_contents1 = [item for item in lis[1] if item and item is not None]
        dicc=dict(zip(valid_contents0,valid_contents1))
    return dicc#key_2_English.translate_answer_key(dicc)  
v2 = [[['信息主体申请设置防欺诈警示，联系电话：01090000000/13900000000。', ''],
       ['生效日期', '截止日期'],
       ['2015年5月29日', '2016年5月28日']]]
# table4 = table2json_short(v2[0])
def peiou_message(lis):#表格行数较少，不会出现横行对应情况
    dicc = {}
    for linea in range(int(len(lis)-1)):#列竖行对应
        valid_contents0 = [item for item in lis[2*linea] if item and item is not None]
        valid_contents1 = [item for item in lis[2*linea+1] if item and item is not None]
        if len(valid_contents0)==1:
            dicc[valid_contents0[0]] = valid_contents1[0].replace('\n','')
            return dicc#key_2_English.translate_answer_key(dicc) 
        else:
            for t,z in enumerate(valid_contents0):
                if '：' in z:#有冒号情况
                    str, st = z.split('：')
                    dicc[str] = st.replace('\n','')
                else:
                    dicc[z] = valid_contents1[t].replace('\n','')
    return dicc#key_2_English.translate_answer_key(dicc) 
v6=[[['姓名', '证件类型', '证件号码', '工作单位', '联系电话'],
  ['李金花', '外国人居留证', '123560000008888', '三星电子北京分公司财务部', '13800003333'],
  ['数据发生机构名称', '', '', '', ''],
  ['工商银\n行', '', '', '', '']]]
# table6 = peiou_message(v6[0])
def v9_message(lis,title,biao):#lis为输入列表形式表格,title为该表名称，biao为需要横行对应的表头列表
    dicc = {}
    text=[]#把title切分出来
    for linea in range(len(lis) - 1):  # 列竖行对应
        if title in lis[linea]:
            text.append(lis[0][1:])
            text[0].insert(0, None)
            for g in lis[1:]:
                text.append(g)
    line = 1
    sanji = {}
    erji = {}
    danxiang = []#横行切分矩阵
    for biaotou  in biao:
        #数组处理只分两个情况，1：表头为行第一个值且为第一行时，表头为行第一个值但不是第一行时，其余的行第一个值为None，会进行判断
        for t,z in enumerate([item for item in text[line] if item and item is not None]):
            if biaotou == z and line==1:#仅当第一行时
                danxiang.append(text[0][1:])#账户数，月份
                danxiang.append(text[line][1:])  # 贷款、信用卡行信息
                line += 1
            elif line+1 == len(text):#最后一行  合计
                danxiang.append(text[0][1:])  # 账户数，月份
                danxiang.append(text[line][1:])  # 贷款、信用卡行信息
                break
            elif biaotou == z and biaotou =="其他":#/其他类
                danxiang.append(text[0][1:])  # 账户数，月份
                danxiang.append(text[line][1:])  # 贷款、信用卡行信息
                line += 1
                break
            elif biaotou == z and biaotou=="信用卡":#信用卡
                danxiang.append(text[0][1:])  # 账户数，月份
                danxiang.append(text[line][1:])  # 贷款、信用卡行信息
                line += 1
            elif text[line][0]==None or text[line][0]== '':
                danxiang.append(text[line][1:])
                line += 1
        tem = {}
        if len(danxiang[1:])>1 :#单项内含有子项情况
            for r in range(len(danxiang[1:])):#行
                for j in range(len(danxiang[0][1:])):
                    tem[danxiang[0][j+1]]=danxiang[r+1][j+1]# j+1  第一行做表头
                sanji[danxiang[r+1][0]]=tem.copy()
                tem={}
        elif "合计" == z:#合计不具有子项的情况
            for j in range(1,3):
                tem[danxiang[0][j]] = danxiang[1][j]
            sanji= tem.copy()
            tem = {}
        elif "其他" == z:
            for j in range(1,3):
                tem[danxiang[0][j]] = danxiang[1][j]
            sanji["--"] = tem.copy()
            tem = {}

        erji[biaotou]=sanji.copy()
        sanji={}
        danxiang = []
    dicc[title] = erji
    return dicc#key_2_English.translate_answer_key(dicc) 
v9 = [[['业务类型', '', '账户数', '首笔业务发放月份'],
       ['贷款', '个人住房贷款', '2', '2007.09'],
       ['', '个人商用房贷款（包括商住两用房）', '1', '2007.09'],
       ['', '其他类贷款', '2', '2007.09'],
       ['信用卡', '贷记卡', '2', '2007.09'],
       ['', '准贷记卡', '1', '2007.09'],
       ['其他', '', '3', '2007.09'],
       ['合计', '', '11', '--']]]
# table9 = v9_message(v9[0],'业务类型',['贷款','信用卡','其他','合计'])
def title_heji_table(lis,title):#lis：输入list表格   title表格横行标题    biaoti表格第一个框内字
    dicc = {}
    for linea in range(int(len(lis)-1)):#列竖行对应
        valid_contents0 = [item for item in lis[linea] if item and item is not None]
        if len(valid_contents0)==1:
            dicc[title]= []
        else:
            dicc[title] = []
            tem = {}
            line=0
            for r in range(1,len(lis)):#行
                v = lis[r][0]
                if "合计" == lis[r][0]:#有合计的情况
                    dic={}
                    dic["合计"]=[]
                    for a in range(1,len(lis[r])):#列  第一行做表头
                        tem[lis[0][a]]=lis[r][a]#第一行做表头
                    dic["合计"].append(tem)
                    dicc[title].append(dic.copy())
                    tem = {}
                    return dicc#key_2_English.translate_answer_key(dicc) 
                elif line < len(lis)-1:#无合计的情况
                    for a, b in enumerate(lis[line + 1]):  # 列  第一行做表头
                        tem[lis[0][a]] = b  # 第一行做表头
                    dicc[title].append(tem.copy())
                    tem={}
                    line += 1
        return dicc# key_2_English.translate_answer_key(dicc)#key_2_English.translate_answer_key(dicc)
v10 = [[['业务类型', '账户数', '余额'],
        ['资产处置业务', '', '10,000'], ['垫款业务', '', '20,000'],['合计', '2', '30,000']]]
# table10=title_heji_table(v10[0],'被追偿信息汇总')
def biaohao_message(lis, sst, biaotou):  # lis为传入列表,title为列表名称，sst默认为编号，所有为编号列表可用此函数处理
    dicc = {}
    text = []  # 切分文本
    xuhao = []  # 标题序号
    tem = []  # 拼接
    tex = []  # 行标题
    for i in range(len(lis)):
        valid_contents = lis[i]#[item for item in lis[i] if item and item is not None]
        if sst in lis[i]:
            xuhao.append(i)
    xuhao.append(len(lis))

    for t in range(len(xuhao) - 1):
        tex.append(lis[xuhao[t]])  # 行标题
        text.append(lis[xuhao[t]:xuhao[t + 1]])  # 行内容

    # 将不同的列进行拼接
    if len(text) == 3:
        for i in range(len(text[0])):
            s = text[0][i]#[item for item in text[0][i] if item and item is not None]
            u = text[1][i]#[item for item in text[1][i] if item and item is not None]
            v = text[2][i]#[item for item in text[2][i] if item and item is not None]
            tem.append(s + u[1:] + v[1:])  # 拼接标题
    elif len(text) == 2:
        for i in range(len(text[0])):
            s = text[0][i]#[item for item in text[0][i] if item and item is not None]
            u = text[1][i]#[item for item in text[1][i] if item and item is not None]
            tem.append(s + u[1:])  # 拼接
    elif len(text) == 1:
        for i in range(len(text[0])):
            s = text[0][i]#[item for item in text[0][i] if item and item is not None]
            tem.append(s)

    first = tem[0]
    if first[0] == sst:
        temp = {}
        dicc[biaotou]=[]
        for linea in range(1, len(tem)):  # 行
            for t, z in enumerate(tem[linea]):  # 列 第一行做表头
                temp[first[t]] = z.replace('\n','')  # 第一行做表头
            try:
                del temp['']
            except KeyError:
                pass
            dicc[biaotou].append(temp.copy())
            temp = {}
    return dicc#key_2_English.translate_answer_key(dicc)
def little_title_table(lis, title, biaoti):  # lis：输入list表格   title表格横行标题    biaoti表格第一个框内字
    dicc = {}
    for linea in range(int(len(lis) - 1)):  # 列竖行对应
        valid_contents0 = [item.replace('\n','') for item in lis[linea] if item and item is not None]
        if len(valid_contents0) == 1:
            dicc[title] = {}
            # dicc[key_2_English.key_list_2_English([title])[0]] = {}
        else:
            for t, z in enumerate(valid_contents0):
                if biaoti in z:  # 横行读情况
                    ss = lis[linea:]  # 有个问题，要是横行对应的不到表格末端也会有问题
                    zilis = []
                    tem = {}
                    for r in range(len(ss) - 1):  # 行
                        valid_contents1 = ss[r + 1]#[item for item in ss[r + 1] if item and item is not None]
                        for a, b in enumerate(valid_contents1):  # 列  第一行做表头
                            tem[ss[0][a]] = b.replace('\n','')#tem[[item for item in ss[0] if item and item is not None][a]] = b.replace('\n','') # 第一行做表头
                        temp = tem.copy()
                        zilis.append(temp)
                        try:
                            del temp['']
                        except KeyError:
                            pass
                        dicc[title]=zilis
                        # dicc[key_2_English.key_list_2_English([title])[0]] = key_2_English.translate_answer_key(zilis)
                        tem = {}
                    return dicc#key_2_English.translate_answer_key(dicc) 

    return dicc#key_2_English.translate_answer_key(dicc)
v12=[[['账户类型', '账户数', '月份数', '单月最高逾期/透支总额', '最长逾期/透支月数'],
      ['非循环贷账户', '3', '6', '5,500', '2'],
      ['循环贷账户一', '1', '3', '2,500', '1'],
      ['循环贷账户二', '2', '6', '5,500', '2'],
      ['贷记卡账户', '2', '4', '5,500', '4'],
      ['准贷记卡账户', '', '', '', '']]]
# table12=little_title_table(v12[0],'逾期（透支）信息汇总','账户类型')#little_title_table修改了valid_contents1，检查是否影响其他表格对该函数的使用
def v23_message(lis,biao_title):
    #横行多列分割表格形式
    dicc = {}
    text = []
    dicc[biao_title]=[]
    start=0
    for s,t in enumerate(lis[0]):
        v = len(lis[0])
        if  s< v-1 and t=='' and lis[0][s+1]!='':
            for z in range(len(lis)):
                text.append([item for item in lis[z][start:s+1] if item and item is not None])
        elif t=='' and s==v-1:#最后一列
            for z in range(len(lis)):
                text.append([item for item in lis[z][start:s+1] if item and item is not None])#lis[z][start:s+1]
        else:
            continue
        inner_dict = little_title_table(text,text[0][0],text[1][0])##lis：输入list表格   title表格横行标题    biaoti表格第一个框内字
        text=[]
        start=s+1
        dicc[biao_title].append(inner_dict)
    return dicc#key_2_English.translate_answer_key(dicc)
v23 =[['最近1个月内的查询机构数', None, '最近1个月内的查询次数', None, None, '最近2年内的查询次数', None, None],
      ['贷款审批', '信用卡审批', '贷款审批', '信用卡审批', '本人查询', '贷后管理', '担保资格\n审查', '特约商户\n实名审查'],
      ['0', '0', '0', '0', '3', '7', '1', '1']]
v18_2=[['担保责任', '', '', '其他相关还款责任', '', ''],
      ['账户数', '担保金额', '余额', '账户数', '还款责任金额', '余额'],
      ['1', '200,000', '100,000', '3', '900,000', '500,000']]
# table23=v23_message(v18_2,'查询记录概要')
def v18_message(lis,title):
    dicc={}
    text = []
    dicc[title]=[]
    start = 1
    for i in range(len(lis)):
        countent = [item for item in lis[i] if item and item is not None]
        if countent[0]=="为个人":
            for s in range(3):
                text.append(lis[start+s])
            dicc[title].append(v23_message(text, "为个人"))
            text=[]
        elif countent[0]=="为企业":
            for s in range(3):
                text.append(lis[start+s])
            dicc[title].append(v23_message(text, "为企业"))
            text = []
        else:
            continue

    return dicc#key_2_English.translate_answer_key(dicc)
v18=[[['为个人', '', '', '', '', ''],
      ['担保责任', '', '', '其他相关还款责任', '', ''],
      ['账户数', '担保金额', '余额', '账户数', '还款责任金额', '余额'],
      ['1', '200,000', '100,000', '3', '900,000', '500,000'],
      ['为企业', '', '', '', '', ''],
      ['担保责任', '', '', '其他相关还款责任', '', ''],
      ['账户数', '担保金额', '余额', '账户数', '还款责任金额', '余额'],
      ['1', '200,000', '100,000', '3', '900,000', '500,000']]]
# table18=v18_message(v18[0],'相关还款责任信息汇总')
# print(table4)

def v36_heng(lis):
    ##v36表格中“月的还款记录”中横行读处理部分
    dicc= {}
    text=lis[1:]
    month= lis[0][1:]
    for i in range(0,int(len(text)-1),2):#两行一次循环，定位年份
        dicc[text[i][0]]=[]
        contents0 = text[i][1:]
        contents1 = text[i + 1][1:]
        tep0 = dict(zip(month, contents0))#月份作为表头
        tep1 = dict(zip(month, contents1))#月份作为表头
        combined_dict = {key: [tep0[key], tep1[key]] for key in tep0.keys()}
        del combined_dict['']#None
        dicc[text[i][0]].append(combined_dict.copy())
        del tep0
        del tep1
    return dicc #key_2_English.translate_answer_key(dicc)
def v50jiaofei_heng(lis):
    ##v50表格中“月的缴费记录”中横行读处理部分
    dicc= {}
    text=lis[1:]
    month= lis[0][1:]
    for i in range(int(len(text))):#两行一次循环，定位年份
        dicc[text[i][0]]=[]
        contents0 = text[i][1:]
        tep0 = dict(zip(month, contents0))#月份作为表头
        del tep0['']#None
        dicc[text[i][0]].append(tep0.copy())
        del tep0
    return dicc #key_2_English.translate_answer_key(dicc)
def v36_message(lis,title):
    #v36表格类型中的表格处理方式，按照横行项目进行判断，键值对应，首先进行了表格切分，根据切分的节点进行各个子表格处理
    start=[]
    end = []
    dicc = []
    tep={}
    for i in range(len(lis)):#表格按标题切分
        contents = [item for item in lis[i] if item and item is not None]
        if len(contents) == 1 and contents[0].find('截至') != -1:
            if i==0:
                start = []
            else:
                end.append(i)
            start.append(i)
        elif len(contents) == 0:
            print("表格ocr识别中可能存在表格识别小标题未识别到的情况，请检查该表格\n表格：{},\n表格名称：{}\n".format(lis,title))
        elif len(contents) == 1 and contents[0].find('大额专项分期') != -1:
            end.append(i)
            start.append(i)
        elif len(contents) == 1 and contents[0].find('日以后的最新还款') != -1:
            end.append(i)
            start.append(i)
        elif len(contents) == 1 and contents[0].find('月的还款') != -1 or contents[0].find('还款记录') != -1:
            end.append(i)
            start.append(i)
        elif len(contents) == 1 and contents[0].find('月的缴费记录') != -1 or contents[0].find('月的缴费') != -1:
            end.append(i)
            start.append(i)
        elif len(contents) == 1 and contents[0].find('特殊事件') != -1:
            end.append(i)
            start.append(i)
        elif '特殊交易' in contents[0]:
            end.append(i)
            start.append(i)
        elif '机构说明' in contents:
            end.append(i )
            start.append(i)
        elif '本人声明' in contents:
            end.append(i)
            start.append(i)
        elif '异议标注' in contents:
            end.append(i)
            start.append(i)
        else:
            if i==0:
                start.append(i)
            continue

    end.append(len(lis))
    for t,z in enumerate(start):
        contents = [item for item in lis[z] if item and item is not None]
        if len(contents)==1 and contents[0].find('截至') != -1:
            text = list(lis[z:end[t]])
            tep = v36_message(text[1:], contents[0])
            dicc.append(tep.copy())
            del text
        elif len(contents)==1 and contents[0].find('大额专项分期信息') != -1:
            text = list(lis[z:end[t]])
            tep = v36_message(text[1:],contents[0])
            dicc.append(tep[0])
            del text
        elif len(contents)==1 and contents[0].find('日以后的最新还款') != -1:
            text = list(lis[z:end[t]])
            tep = v36_message(text[1:],contents[0])
            try:
                dicc.append(tep[0])
            except IndexError:
                print("表格提取可能存在表格切分问题，请检查该表格的ocr提取结果\n表格：{}，\n表格名称：{}\n".format(lis, title))
            del text
        elif len(contents)==1 and contents[0].find('月的缴费记录') != -1 :#or contents[0].find('月的缴费') != -1
            text = list(lis[z:end[t]])
            tep[contents[0]] = v50jiaofei_heng(text[1:])
            dicc.append(tep.copy())#dicc.append(key_2_English.translate_answer_key(tep))
            del text
        elif len(contents)==1 and contents[0].find('月的还款') != -1 or contents[0].find('还款记录') != -1:
            text = list(lis[z:end[t]])
            tep[contents[0]] = v36_heng(text[1:])
            dicc.append(tep.copy())#dicc.append(key_2_English.translate_answer_key(tep))
            del text
        elif len(contents)==1 and contents[0].find('特殊事件') != -1:
            text = list(lis[z:end[t]])
            contents0 = [item for item in text[0] ]#if item and item is not None
            contents1 = [item for item in text[1] ]
            tep = dict(zip(contents0, contents1))
            if tep.get('') == '':
                del tep['']
            dicc.append(tep.copy())#dicc.append(key_2_English.translate_answer_key(tep))
            del text
        elif '特殊交易' in contents[0]:
            text = list(lis[z:end[t]])
            contents0 = [item for item in text[0] ]#if item and item is not None
            contents1 = [item for item in text[1] ]
            tep = dict(zip(contents0, contents1))
            if tep.get('') == '':
                del tep['']
            dicc.append(tep.copy())#dicc.append(key_2_English.translate_answer_key(tep))
        elif '机构说明' in contents:
            text = list(lis[z:end[t]])
            contents0 = [item for item in text[0] ]#if item and item is not None
            contents1 = [item for item in text[1] ]
            tep=dict(zip(contents0,contents1))
            if tep.get('') == '':
                del tep['']
            dicc.append(tep.copy())#dicc.append(key_2_English.translate_answer_key(tep))
        elif '本人声明' in contents:
            text = list(lis[z:end[t]])
            contents0 = [item for item in text[0] ]#if item and item is not None
            contents1 = [item for item in text[1] ]#if item and item is not None
            tep = dict(zip(contents0, contents1))
            if tep.get('') == '':
                del tep['']
            dicc.append(tep.copy())#dicc.append(key_2_English.translate_answer_key(tep))
        elif '异议标注' in contents:
            text = list(lis[z:end[t]])
            contents0 = [item for item in text[0] ]#if item and item is not None
            contents1 = [item for item in text[1] ]#if item and item is not None
            tep = dict(zip(contents0, contents1))
            if tep.get('') == '':
                del tep['']
            dicc.append(tep.copy())  #dicc.append(key_2_English.translate_answer_key(tep))
        else:
            tex = lis[z:end[t]]#
            for linea in range(int(len(tex)/2)):  # 列竖行对应
                contents0 = [item.replace('\n','') for item in tex[2*linea] ]#if item and item is not None
                contents1 = [item.replace('\n','') for item in tex[2*linea+1] ]#if item and item is not None
                if len(contents0)!=len(contents1):
                    print("此处可能存在表格上下信息识别不全的情况，请检查此处表格的ocr识别结果：\n表格识别结果：{},\n表格标题：{}\n".format(lis,title))
                tep[title]=dict(zip(contents0, contents1))
                if tep[title].get('') == '':
                    del tep[title]['']
                dicc.append(tep.copy())#dicc.append(key_2_English.translate_answer_key(tep))
        tep={}
    return  dicc#list(key_2_English.translate_answer_key([i])for i in dicc ) #--EN #dicc --CH #

v36=[[['发卡机构', '', '账户标识', '', '', '', '', '', '开立日期', '', '', '', '', '账户授信额度', '', '', '', '', '共享授信额度', '', '', '', '', '币种', '', '', '', '业务种类', '', '', '', '', '担保方式', ''],
      ['工商银行\n信用卡中心', '', 'AAAOO3', '', '', '', '', '', '2009.05.22', '', '', '', '', '16,000', '', '', '', '', '160,000', '', '', '', '', '人民币', '', '', '', '贷记卡', '', '', '', '', '信用/免担保', ''],
      ['截至2015年04月12日', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
      ['账户状态', '', '', '余额', '', '', '', '', '', '', '已用额度', '', '', '', '', '', '未出单的大额\n专项分期余额', '', '', '', '', '剩余分期期数', '', '', '', '', '最近6个月\n平均使用额度', '', '', '', '', '最大使用额度', '', ''],
      ['正常', '', '', '255,500', '', '', '', '', '', '', '135,500', '', '', '', '', '', '110,000', '', '', '', '', '11', '', '', '', '', '90,000', '', '', '', '', '150,000', '', ''],
      ['账单日', '', '', '', '', '', '本月应还款', '', '', '', '', '', '本月实还款', '', '', '', '', '', '最近一次还款日期', '', '', '', '', '', '前逾期期数', '', '', '', '', '当前逾期总额', '', '', '', ''],
      ['2015.04.12', '', '', '', '', '', '24,500', '', '', '', '', '', '0', '', '', '', '', '', '2015.03.10\n1', '', '', '', '', '', '', '', '', '', '', '24,550', '', '', '', ''],
      ['大额专项分期信息', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
      ['大额专项分期额度', '', '', '', '', '', '', '', '分期额度生效日期', '', '', '', '', '', '', '', '', '', '分期额度到期日期', '', '', '', '', '', '', '', '', '已用分期金额', '', '', '', '', '', ''],
      ['120,000', '', '', '', '', '', '', '', '2015.09.12', '', '', '', '', '', '', '', '', '', '2016.09.11', '', '', '', '', '', '', '', '', '120,000', '', '', '', '', '', ''],
      ['2015年04月12日以后的最新还款记录', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
      ['余额', '', '', '', '', '', '', '', '还款日期', '', '', '', '', '', '', '', '', '', '还款金额', '', '', '', '', '', '', '', '', '当前还款状态', '', '', '', '', '', ''],
      ['230,950', '', '', '', '', '', '', '', '2015.04.25', '', '', '', '', '', '', '', '', '', '24,550', '', '', '', '', '', '', '', '', 'N', '', '', '', '', '', ''],
      ['2010年07月-2015年04月的还款', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
      ['', '1', '', '', '', '2', '', '3', '', '', '', '4', '', '', '5', '', '', '6', '', '', '7', '', '8', '', '', '9', '', '', '10', '', '11', '', '', '12'],
      ['2015', 'N', '', '', '', 'N', '', 'N', '', '', '', 'N', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
      ['', '0', '', '', '', '0', '', '0', '', '', '', '0', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
      ['2014', 'N', '', '', '', 'N', '', 'N', '', '', '', 'N', '', '', 'N', '', '', 'N', '', '', 'N', '', 'N', '', '', 'N', '', '', 'N', '', 'N', '', '', 'N'],
      ['', '0', '', '', '', '0', '', '0', '', '', '', '0', '', '', '0', '', '', '0', '', '', '0', '', '0', '', '', '0', '', '', '0', '', '0', '', '', '0'],
      ['2013', 'N', '', '', '', 'N', '', 'N', '', '', '', 'N', '', '', 'N', '', '', 'N', '', '', 'N', '', 'N', '', '', 'N', '', '', 'N', '', 'N', '', '', 'N'],
      ['', '0', '', '', '', '0', '', '0', '', '', '', '0', '', '', '0', '', '', '0', '', '', '0', '', '0', '', '', '0', '', '', '0', '', '0', '', '', '0'],
      ['2012', 'N', '', '', '', 'N', '', 'N', '', '', '', 'N', '', '', 'N', '', '', 'N', '', '', 'N', '', 'N', '', '', 'N', '', '', 'N', '', 'N', '', '', 'N'],
      ['', '0', '', '', '', '0', '', '0', '', '', '', '0', '', '', '0', '', '', '0', '', '', '0', '', '0', '', '', '0', '', '', '0', '', '0', '', '', '0'],
      ['2011', '#', '', '', '', '#', '', '#', '', '', '', '#', '', '', '#', '', '', '#', '', '', '#', '', '#', '', '', '#', '', '', '#', '', 'N', '', '', 'N'],
      ['', '--', '', '', '', '', '', '--', '', '', '', '--', '', '', '--', '', '', '--', '', '', 'R--', '', '--', '', '', '--', '', '', '--', '', '0', '', '', '0'],
      ['2010', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'N', '', 'N', '', '', 'N', '', '', 'N', '', 'N', '', '', 'N'],
      ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '0', '', '0', '', '', '0', '', '', '0', '', '0', '', '', '0'],
      ['特殊事件说明', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
      ['该账户"2015年05月不出单。', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
      ['特殊交易类型', '', '', '', '发生日期', '', '', '', '', '变更月数', '', '', '', '', '', '发生金额', '', '', '', '明细记录', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
      ['个性化分期', '', '', '', '2012.07', '', '', '', '', '5', '', '', '', '', '', '10,000', '', '', '', '--', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
      ['机构说明', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '添加日期', '', '', '', ''],
      ['该卡逾期情况极为严\n重。', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '2012.12.15', '', '', '', ''],
      ['本人声明', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '添加日期', '', '', '', ''],
      ['本人因出国无法及时还款，导致当前逾期，非恶意违约。', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '2013.07.02', '', '', '', ''],
      ['异议标注', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '添加日期', '', '', '', ''],
      ['该笔业务正处\n异议处理中。', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '2013.07.22', '', '', '', '']]]
v28=[[['管理机构', '', '', '', '', '账户标识', '', '', '', '', '', '开立日期', '', '', '', '', '', '到期日期', '', '', '', '', '借款金额', '', '', '', '', '账户币种', '', ''],
      ['中国银行北京分行', '', '', '', '', 'BOCBJ00100', '', '', '', '', '', '2010.09.22', '', '', '', '', '', '2025.09.21', '', '', '', '', '500,000', '', '', '', '', '美元', '', ''],
      ['业务种类', '', '', '', '', '担保方式', '', '', '', '', '', '还款期数', '', '', '', '', '', '还款频率', '', '', '', '', '还款方式', '', '', '', '', '共同借款标志', '', ''],
      ['个人商业住房贷款', '', '', '', '', '抵押', '', '', '', '', '', '180', '', '', '', '', '', '月', '', '', '', '', '分期等额本金', '', '', '', '', '无', '', ''],
      ['截至2015年05月05日', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
      ['账户状态', '', '五级分类', '', '', '', '', '', '余额', '', '', '', '剩余还款期数', '', '', '', '', '本月应还款\n应还款日', '', '', '', '', '', '', '最近一次\n本月实还款\n还款日期', '', '', '', '', ''],
      ['逾期', '', '次级', '', '', '', '', '', '400,000', '', '', '', '125', '', '', '', '', '5,000', '', '', '', '2015.05.05', '', '', '0\n2015.03.05', '', '', '', '', ''],
      ['当前逾期期数', '', '', '', '', '当前逾期总额', '', '', '', '', '', '逾期31--60天\n未还本金', '', '', '', '', '', '逾期61-90天\n未还本金', '', '', '', '', '逾期91-180天\n未还本金', '', '', '', '', '逾期180天以上\n未还本金', '', ''],
      ['2', '', '', '', '', '6,100', '', '', '', '', '', '1,000', '', '', '', '', '', '0', '', '', '', '', '0', '', '', '', '', '0', '', ''],
      ['2015年05月05日以后的最新还款记录', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
      ['五级分类', '', '', '', '', '', '余额', '', '', '', '', '', '', '', '还款日期', '', '', '', '', '还款金额', '', '', '', '', '', '', '当前还款状态', '', '', ''],
      ['正常\n394,000\n2015.05.31\n6,100\nN\n2010年09月-2015年05月的还款记录', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
      ['', '1', '', '', '2', '', '', '3', '', '', '4', '', '', '5', '', '', '6', '', '7', '', '8', '', '', '9', '', '10', '', '', '11', '12'],
      ['2015', 'N', '', '', 'N', '', '', 'N', '', '', '1', '', '', '2', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
      ['', '0', '', '', '0', '', '', '0', '', '', '3,000', '', '', '6,100', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
      ['2014', 'N', '', '', 'N', '', '', 'N', '', '', 'N', '', '', 'N', '', '', 'N', '', 'D', '', 'N', '', '', 'N', '', 'N', '', '', 'N', 'N'],
      ['', '0', '', '', '0', '', '', '0', '', '', '0', '', '', '0', '', '', '0', '', '0', '', '0', '', '', '0', '', '0', '', '', '0', '0'],
      ['2013', 'N', '', '', '', '', '', 'N', '', '', 'N', '', '', 'N', '', '', 'N', '', 'N', '', 'N', '', '', 'N', '', 'N', '', '', 'N', 'N'],
      ['', '0', '', '', '0', '', '', '0', '', '', '0', '', '', '0', '', '', '0', '', '0', '', '0', '', '', '0', '', '0', '', '', '0', '0'],
      ['2012', 'N', '', '', 'N', '', '', 'N', '', '', 'N', '', '', 'N', '', '', 'N', '', 'N', '', 'N', '', '', 'N', '', 'N', '', '', 'N', 'N'],
      ['', '0', '', '', '0', '', '', '0', '', '', '0', '', '', '0', '', '', '0', '', '0', '', '0', '', '', '0', '', '0', '', '', '0', '0'],
      ['2011', 'N', '', '', 'N', '', '', 'N', '', '', 'N', '', '', 'N', '', '', 'N', '', 'N', '', 'N', '', '', 'N', '', 'N', '', '', 'N', 'N'],
      ['', '0', '', '', '0', '', '', '0', '', '', '0', '', '', '0', '', '', '0', '', '0', '', '0', '', '', '0', '', '0', '', '', '0', '0'],
      ['2010', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'N', '', 'N', '', '', 'N', 'N'],
      ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '0', '', '0', '', '', '0', '0'],
      ['特殊交易类型', '', '', '发生日期', '', '', '', '', '', '变更月数', '', '', '', '', '', '发生金额', '', '', '明细记录', '', '', '', '', '', '', '', '', '', '', ''],
      ['担保人（第三', '', '', '2014.07.05', '', '', '', '', '', '0', '', '', '', '', '', '20,000', '', '', '该贷款由XX公司代偿20,000元。', '', '', '', '', '', '', '', '', '', '', ''],
      ['方）代偿', ''],
      ['机构说明', '添加日期'],
      ['该客户委托XX公司偿还贷款，\n因公司不按时还款导致出现多次逾期。', '2014.08.12'], ['本人声明', '添加日期'],
      ['本人因出国未能按时还款，非恶意拖欠。', '2014.09.12'],
      ['异议标注', '添加日期'],
      ['该笔业务正处于异议处理中。', '2013.10.10'],
      ['特殊标注', '添加日期'], ['异议信息确实有误,\n但因技术原因暂时无法更正。', '2013.10.25']]]
v30=[[['管理机构', '', '', '账户标识', '', '', '', '开立日期', '', '', '到期日期', '', '', '', '借款金额', '', '', '账户币种', '', ''],
      ['邮储银行北京分行', '', '', 'PSBOC00005', '', '', '', '2011.09.29', '', '', '一', '', '', '', '10,000', '', '', '人民币', '', ''], ['业务种类', '', '', '担保方式', '', '', '', '还款期数', '', '', '还款频率', '', '', '', '还款方式', '', '', '共同借款标志', '', ''], ['商业助学贷款', '', '', '信用/免担保', '', '', '', '', '', '', '不定期', '', '', '', '到期一次\n还本付息', '', '', '无', '', ''], ['截至2015年05月15日', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''], ['账户状态', '', '', '', '', '', '', '', '', '', '账户关闭日期', '', '', '', '', '', '', '', '', ''], ['结清', '', '', '', '', '', '', '', '', '', '2015.05.15', '', '', '', '', '', '', '', '', ''], ['2011年09月-2015年05月的还款记录', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''], ['', '1', '2', '', '3', '', '4', '', '5', '6', '', '', '7', '8', '', '9', '10', '', '11', '12'], ['2015', 'N', 'N', '', 'N', '', 'N', '', 'C', '', '', '', '', '', '', '', '', '', '', ''], ['', '0', '0', '', '0', '', '0', '', '0', '', '', '', '', '', '', '', '', '', '', ''], ['2014', 'B', 'B', '', 'B', '', 'N', '', 'N', 'N', '', '', 'N', 'N', '', 'N', 'N', '', 'N', 'N'], ['', '900', '1,000', '', '1,100', '', '0', '', '0', '0', '', '', '0', '0', '', '0', '0', '', '0', '0'], ['2013', 'N', 'N', '', 'N', '', 'N', '', '1', '2', '', '', '3', '4', '', '5', '6', '', 'B', 'B'], ['', '0', '0', '', '0', '', '0', '', '100', '200', '', '', '300', '400', '', '500', '600', '', '700', '800'], ['2012', 'N', '1', '', 'N', '', 'N', '', 'N', 'N', '', '', 'N', 'N', '', 'N', 'N', '', 'N', 'N'], ['', '0', '100', '', '0', '', '0', '', '0', '0', '', '', '0', '0', '', '0', '0', '', '0', '0'], ['2011', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'N', 'N', '', 'N', 'N'], ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '0', '0', '', '0', '0'], ['特殊交易类型', '', '发生日期', '', '', '变更月数', '', '', '发生金额', '', '', '明细记录', '', '', '', '', '', '', '', ''], ['提前结清', '', '2015.05.15', '', '', '7', '', '', '500', '', '', '', '', '', '', '', '', '', '', '']]]
v50=[[['机构名称', '', '', '业务类型', '', '', '业务开通日期', '', '', '当前缴费状态', '', '', '当前欠费金额', '', '', '记账年月', '', ''],
      ['中国铁通甘肃分公司', '', '', '固定电话后付费', '', '', '2009.08.17', '', '', '欠费', '', '', '10,000', '', '', '2015.05', '', ''], ['2013年06月-2015年05月的缴费记录', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''], ['', '1', '2', '', '3', '4', '', '5', '6', '', '7', '8', '', '9', '10', '', '11', '12'], ['2015', 'N', 'N', '', 'N', '1', '', '2', '', '', '', '', '', '', '', '', '', ''], ['2014', 'N', 'N', '', 'N', 'N', '', 'N', 'N', '', 'N', 'N', '', 'N', 'N', '', 'N', 'N'], ['2013', '', '', '', '', '', '', '', 'N', '', 'N', 'N', '', 'N', 'N', '', 'N', 'N']]]
v54=[[['编号', '立案法院\n一', '案由', '', '', '立案日期', '', '结案方式'],
      ['1', '北京市宣武区人民法院', '--', '', '', '2011.09.11', '', '判决'], ['2', '北京市东城区人民法院', '', '', '', '2009.05.09', '', '判决'], ['编号', '判决/调解结果', '', '判决/调解生效日期', '诉讼标的', '', '诉讼标的金额', ''], ['1', '被告张十五赔偿原告李四人民币500,000元', '', '2011.07.09', '房屋买卖纠纷', '', '500,000', ''], ['2', '被告张十五赔偿原告王五人民币200,000元', '', '2010.10.11', '房屋买卖纠纷', '', '200,000', '']]]
v57=[[['参缴地', '参缴日期', '初缴月份', '缴至月份', '缴费状态', '月缴存额', '个人缴存比例', '单位缴存比例'],
      ['内蒙古自治区通辽市', '2007.01.01', '2007.01', '2008.12', '缴交', '1,000', '12%', '12%'], ['缴费单位', '', '', '', '', '', '', '信息更新日期'], ['科左中旗努日木苏木经管站', '', '', '', '', '', '', '2013.07'], ['', '', '', '', '', '', '', ''], ['参缴地', '参缴日期', '初缴月份', '缴至月份', '缴费状态', '月缴存额', '个人缴存比例', '单位缴存比例'], ['北京市', '2006.07.01', '2006.01', '2006.12', '缴交', '1,000', '12%', '12%'], ['缴费单位', '', '', '', '', '', '', '信息更新日期'], ['北京银行', '', '', '', '', '', '', '2014.07']]]
v55=[['编号', '执行法院', '', '', '', '执行案由', '', '', '', '', '立案日期', '', '', '', '结案方式'],
     ['1', '北京市西城区人民法院\n--', '', '', '', '', '', '', '', '', '2012.09.11', '', '', '', '执行结案'], ['2', '北京市宣武区人民法院', '', '', '', '', '', '', '', '', '2011.05.09', '', '', '', '执行结案'], ['编号', '案件状态', '结案日期', '', '申请执行标的', '', '申请执行标的价值', '', '', '已执行标的', '', '', '已执行标的金额', '', ''], ['1', '执行完毕', '2012.09.15', '', '房屋', '', '420,000', '', '', '房屋买卖纠纷', '', '', '420,000', '', ''], ['2', '执行完毕', '2011.10.11', '', '房屋', '', '220,000', '', '', '房屋买卖纠纷', '', '', '220,000', '', ''], ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''], ['编号', '处罚机构', '', '处罚内容', '', '', '', '处罚金额', '生效日期', '', '', '截止日期', '', '行政复议结果', ''], ['1', '青海省西宁市地方\n税务局', '', '责令限期改正、没收违法所得', '', '', '', '400', '2012.08', '', '', '2015.07', '', '--', ''], ['2', '湖南省建设管理服务\n中心', '', '暂扣或者吊销许可证、暂扣\n或者吊销执照', '', '', '', '--', '2010.07', '', '', '2013.07', '', '', '']]

# print(biaohao_message(v54[0],'编号','强制执行记录 '))
# table28=v36_message(v36[0],"防欺诈警示")
# print(table28)
# for i in table28:
#     print(key_2_English.translate_answer_key([i]))

