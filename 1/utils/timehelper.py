#encoding=utf-8
import time
import datetime
'''
time.time()
time.localtime()
time.gmtime()
time.mktime(time.localtime())
'''


class TimeHelper(object):
    def __init__(self):
        print 'test'

    def GetCurrentTimeStr(self, fmt='%Y/%m/%d %H:%M:%S'):
        return time.strftime(fmt)

    def AddDate(self,days=0,hours=0,mins=0):
        d = datetime.datetime.now()+datetime.timedelta(days=days,hours=hours,minutes=mins)
        return d

    def GetYearMonths(self,offset):
        #往前或往后多少个月
        yearmonths = []
        now = self.GetNow()
        y = curyear = now.year
        curmonth = now.month
        for i in range(0,abs(offset)):
            if offset > 0 :
                m = (curmonth+i-1)%12+1
            else:
                m =(curmonth-i-1)%12+1
            if i>0 and m==1 and offset > 0 :
                y +=1
            if i>0 and m==12  and offset < 0 :
                y -=1
            yearmonths.append({"year":y,"month":m})
        return yearmonths

    def GetNow(self):
        # year : datetime.datetime.now().year
        return datetime.datetime.now()

def elapsedtimedeco(arg=True):
    if arg:
        def _deco(func):
            def wrapper(*args,**kwargs):
                startTime = time.time()
                func(*args,**kwargs)
                endTime = time.time()
                msecs = (endTime - startTime) * 1000
                print "->elapsed time: %f ms" % msecs
            return wrapper
    else:
        def _deco(func):
            return func
    return _deco

if __name__ == '__main__':
    # 装饰器使用
    @elapsedtimedeco(True)
    def addFunc(a,b,c):
        print 'start'
        time.sleep(0.9)
        print a+b+c
        print 'end'

    addFunc(5,6,8)
