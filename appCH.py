from flask import Flask, jsonify #flask库
import key_2_English
import PDF_CHextract
import requests
app = Flask(__name__)  # 创建一个服务，赋值给APP


@app.route('/test', methods=['Get'])  # 指定接口访问的路径，支持什么请求方式get，post
#定义的方法名必须和接口路径相同
#由于路径是'/test'，所以方法名为test()
#浏览器直接访问直接为'Get'方法
def test():
    # input()#输入ocr解析json文件的地址，如'F:/浙商nlp项目/征信报告pdf返回结果-最新版.json'
    ocr_path = 'F:/浙商nlp项目/征信报告详版返回示例V1.json'  # input()#输入ocr解析json文件的地址，如'F:/浙商nlp项目/征信报告pdf返回结果-最新版.json'
    result = PDF_CHextract.json_table_find(ocr_path)
    try:
        # dicen= {}
        # dicen[key_2_English.key_2_English('个人信用报告')]=[]
        # for k,v in result.items():
        #     tep={}
        #     tep[key_2_English.key_2_English(k)]=key_2_English.translate_answer_key(v)
        #     dicen[key_2_English.key_2_English('个人信用报告')].append(tep)
        dicen=key_2_English.translate_answer_key(result)
    except requests.exceptions.JSONDecodeError:
        print("翻译过程中存在连接或网络等问题，请重新运行或者手动在词典中添加英文键值")
    return result#jsonify(dicen)


if __name__ == '__main__':
    #这个host：windows就一个网卡，可以不写，而linux有多个网卡，写成0.0.0.0可以接受任意网卡信息
    #端口号默认5000，可以手动设置
    app.run(host='0.0.0.0', port=5000, debug=True)#host可以指定端口

