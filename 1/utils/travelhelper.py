#encoding=utf-8
import timehelper
from pyquery import PyQuery as pq
import sys
sys.path.append("..")
import pandas as pd

class TravelHelper(object):
    def __init__(self):
        self.huodong="http://www.zhuhaihuwai.com/plugin.php?id=zzzai_ecal&month=%s"

    def HandleResult(self,result):
        df = pd.DataFrame(result)
        now = timehelper.TimeHelper().GetNow()
        curdate = "%04d%02d%02d" % (now.year,now.month,now.day)
        df = df[df.date>curdate]
        # 中文过滤需要转换字符集才能匹配成功,其实下面的过滤不成功
        df = df[-df.title.str.contains('徒步')]
        #nicodeDecodeError: 'gb2312' codec can't decode bytes in position 2-3: illegal multibyte sequence
        #df= df[-df.name.str.contains(unicode('徒步','gb2312'))]
        content = ''
        for name,group in df.groupby('name'):
            content += "%s<br/>%s" % (name , pd.Series(group["title"]).str.cat(sep=','))
        return content

    def SaveResult(self,ymon,day,seq,name,title,url):
        #return {"year":ymon["year"],"month":ymon["month"],"Seq":seq,"Name":name,"title":title,"href":url}
        date = "%04d%02d%02d" % (ymon["year"],ymon["month"],day)
        return {"date":date,"seq":seq,"name":name,"title":"<a href='%s'>%s</a>" % (url,title)}

    def ZhuhaiHuWai(self,ymon):
        url = self.huodong % ("%d%02d" % (ymon["year"],ymon["month"]))
        print url
        d=pq(url=url)
        td = d("#z_tb_ecal tr td")
        #div = d("#z_tb_ecal tr td div")
        cnt = td.length
        result = []

        for i in range(0,cnt):
            day = td.eq(i).find('div').text()
            tda =  td.eq(i).find('p a')
            tdacnt = tda.length
            for j in range(0,tdacnt):
                name = tda.eq(j).text()
                href = tda.eq(j).attr.href
                title = tda.eq(j).attr.title
                result.append(self.SaveResult(ymon,int(day),j,name,title,href))
        return result

    def GetZhuhaiHuWai(self):
        #获取当前月份开始的1年
        t = timehelper.TimeHelper()
        ymons = t.GetYearMonths(12)
        result=[]
        for ymon in ymons:
            #curmonth=timehelper.TimeHelper().GetCurrentTimeStr(fmt='%Y%m')
            result = result + self.ZhuhaiHuWai(ymon)
        content = self.HandleResult(result)
        return content
        #return result
