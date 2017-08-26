#encoding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import time
from flask import Flask, request,make_response
import hashlib
import xml.etree.ElementTree as ET
'''
import sys
sys.path.append("utils")
'''
from utils import timehelper
from utils import travelhelper


app = Flask(__name__)
app.debug=True
@app.route('/',methods=['GET','POST'])


def wechat_auth():
    if request.method == 'GET':
        token='weixintest'
        data = request.args
        print "Get data:",data
        signature = data.get('signature','')
        timestamp = data.get('timestamp','')
        nonce = data.get('nonce','')
        echostr = data.get('echostr','')
        s = [timestamp,nonce,token]
        s.sort()
        s = ''.join(s)
        if (hashlib.sha1(s).hexdigest() == signature):
            return make_response(echostr)
        else: 
            return make_response(echostr)    
    else:
        rec = request.stream.read()
        print "Post data:",rec
        xml_rec = ET.fromstring(rec)
        msgType=xml_rec.find("MsgType").text
        tou = xml_rec.find('ToUserName').text
        fromu = xml_rec.find('FromUserName').text
        content = xml_rec.find('Content').text.strip()
        content = get_response(msgType,xml_rec,content)
        xml_rep = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[%s]]></Content><FuncFlag>0</FuncFlag></xml>"
        response = make_response(xml_rep % (fromu,tou,str(int(time.time())),content))
        response.content_type='application/xml'
        return response

def get_response(msgType,xml_rec,content):
    #try:
    if msgType == 'image':
        picurl = xml_rec.find('PicUrl').text
        content = "图片地址是："+picurl
    else:
        print content
        if content == "1": #旅游
            t = travelhelper.TravelHelper()
            content = t.GetZhuhaiHuWai()
        elif content == '2':
            content = '未开发'
        else:
            content = "收到的内容是："+ content+"<br/>参考1.旅游"
    '''except Exception,e:
        content =  'Error:'+e.message
    finally:'''
    return content
