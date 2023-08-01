import json
import requests
import cv2
headers = {'Content-Type':'application/json'}
url='https://www.pushplus.plus/api/common/openApi/getAccessKey'
def get_AccessKey(data):
    res=requests.post(url=url,data=data,headers=headers).text
    res_list=res.split(',')
    res_code=res_list[0].split(':')[-1]
    if int(res_code)==200:
        accessKey=res_list[2].split('"')[-2]
    return accessKey
def get_QRcode_url(headers,topicId):
    get_QRcode_url=requests.get('https://www.pushplus.plus/api/open/topic/qrCode?topicId={a}&forever=0'.format(a=topicId),headers=headers) 
    QRcode_url0=get_QRcode_url.text.split(',')[2]
    QRcode_url1=QRcode_url0.split('"')[-2]
    return QRcode_url1
import time
def log(AK):
    with open('log.txt','a',encoding='utf-8') as f:
        txt=time.asctime()+AK
        f.write(txt)
def login(): 
    with open('logintime.txt','w',encoding='utf-8') as ff:
        ff.write(str(int(time.time())))
    return True
def refresh_AK():
    nt=int(time.time())
    fff=open('logintime.txt',encoding='utf-8')
    lt=int(fff.read())
    if nt>lt+7200:
        return False
    else:
        return True
def delete(data,headers):
    r=requests.post('https://www.pushplus.plus/api/open/topicUser/subscriberList',data=data,headers=headers)
    get_idlist_1=r.text.split(',')
    idlist1_len = len(get_idlist_1)
    index_list = []
    idlist=[]
    if  idlist1_len >8:
        for i in range(0, idlist1_len):
            if get_idlist_1[i] == get_idlist_1[11]:
                index_list.append(i-5)
        for i in index_list:
            id_1=get_idlist_1[i].split(':')[-1]
            id_2=int(id_1)
            idlist.append(id_2)
        delete_count=0 
        for i in idlist:
            data_0={'topicRelationId':int(i)}
            body_0=json.dumps(data_0).encode(encoding='utf-8')
            delete=requests.post('https://www.pushplus.plus/api/open/topicUser/deleteTopicUser?topicRelationId=1',headers=headers,data=body_0)
            response_code0=int(delete.text.split(',')[0].split(':')[-1])
            if response_code0==200:
                delete_count=+1
        print(f'已清除{delete_count}个账户')
def get_QRcode(url):
    cv2.namedWindow('photo',1)   #0窗口大小可以任意拖动，1自适应
    cv2.resizeWindow('photo',640,480)
    cap=cv2.VideoCapture(url)
    ret=cap.isOpened()
    while (ret):
        ret,img=cap.read()
        if not ret:break
        cv2.imshow('photo', img)
        cv2.waitKey(0)
    cap.release()
    return True
import requests
def call(token,message):
    url='http://www.pushplus.plus/send'
    body={
        "token":token,
        "title":"叫号",
        'content':message,
        "topic":"114514",
        'template':"markdown"
        
    }
    data=json.dumps(body).encode(encoding='utf-8')
    requests.post(url=url,data=data)
import time
def check():
    f=open('config.ini',encoding='utf-8')
    a=f.readlines()
    if len(a)==4:
        return True
    else:
        return False
def check_password(password):
    user_password=int(input("请输入管理员密码进行关机操作:"))
    if user_password==password:
        return True
    else:
        return False