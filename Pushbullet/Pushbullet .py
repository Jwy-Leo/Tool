def trainfinish(title,message="Finish"):
    import pycurl as pyc
    try:
        # python 3
        from urllib.parse import urlencode
    except ImportError:
        # python 2
        from urllib import urlencode
    c = pyc.Curl()
    c.setopt(pyc.URL, 'https://api.pushbullet.com/v2/pushes')
    post={  "type":"note",
            "title":title+"Training Finish",
            "body":message}
    #head=['Access-Token: Your Access']
    head=['Access-Token: ']
    post = urlencode(post)
    c.setopt(pyc.HTTPHEADER,head)
    c.setopt(pyc.POSTFIELDS, post)
    c.perform()
    c.close()
def Predict_time(nowepoch,use_time,Epoch):
    import time
    dif=Epoch-nowepoch
    title='Epoch:\t%d/%d'%(nowepoch,Epoch)

    S = time.strftime("%Y_%m_%d_%H_%M", time.localtime())
    S_list = str.split(S, '_')
    #print(S)
    y, m, d, h, min = calender_time(int(S_list[0]),
                                    int(S_list[1]),
                                    int(S_list[2]),
                                    int(S_list[3]),
                                    int(S_list[4]), use_time*dif)
    predict='%d/%02d/%02d,\t%d:%d' % (y, m, d, h, min)

    message = 'Now\t%s\n%s will Finish trainging.' % (S,predict)
    trainfinish(title=title,message=message)
def calender_time(year,month,day,hour,miunte,Addsecond):
    Addsecond=(Addsecond -Addsecond % 60)//60
    miunte += Addsecond % 60
    nextstep=miunte//60
    miunte =miunte % 60

    temp=(Addsecond-Addsecond % 60)//60

    hour=hour+nextstep+temp%24
    nextstep = hour // 24
    hour=hour%24

    temp = (temp-temp%24) // 24

    day = day + nextstep + temp % 30
    nextstep = day // 30
    day=(day%30)

    temp = (temp - temp % 30) // 30

    month = month + nextstep + temp % 12
    nextstep = month // 12
    month = month % 12

    temp = (temp - temp % 12) // 12
    year = year + nextstep + temp

    return year,month,day,hour,miunte
if __name__=='__main__':
    '''
        # import example
        import sys
        # Need to append system path
        sys.path.append('../Pushbullet')
        from Pushbullet import trainfinish
    '''
    #trainfinish('Test')


