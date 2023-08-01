import function
f=open('config.ini',encoding='utf-8')
data1=f.readline()
data2=f.readline() 
topicId=f.readline()
token=f.readline()
f.close()
function.login()
AK=function.get_AccessKey(data1)
headers_after_get_AK={'Content-Type':'application/json','access-key':AK}
url=function.get_QRcode_url(headers_after_get_AK,topicId)
q = [0] * 1000    #足够大的队列
name_list=[0]*1000
head = 0          #表示队头
tail = 0          #表示队尾
num = 1           #表示准备取号的号码
if function.check():
    password=int(input('请设置管理员6位数字密码：'))
    if password>99999 and password<1000000:
        if function.refresh_AK():
            print("1.新到顾客（取号）")
            print("2.下一个顾客（叫号）")
            print("3.程序结束")
            print("请输入具体的操作编号：")
            x = int(input())
            while x != 3 :
                if x == 1:
                    if   tail==head+10          :            #当前排队人数达到10人
                        print("当前排队人数已达上限，请稍后再来，谢谢。")
                    else:
                        print('请输入您的名字,并扫码登记')
                        name_1=input('请输入您的名字:')                     
                        function.get_QRcode(url)
                        q[tail]=num                     #把新顾客取号放入队列
                        name_list[tail]=name_1
                        print(f"您当前的号码为：A{num}, "  
                        f"当前准备叫号A{  q[head]  }, "  
                        f"要等待的人数为{  tail-head  }。")
                        tail+=1                  #队尾往后移一位
                        num+=1                 #下次取号加一
                if x == 2:
                    if     head==tail          :          #没有人在队列
                        print("对不起，没有等待的客户。")
                        '''
                        清除叫号服务用户组
                        '''
                        function.delete(data2,headers_after_get_AK)
                    else:
                        message=f"请A{  q[head]  }号顾客{name_list[head]}就餐，祝您用餐愉快。"
                        print(message)
                        function.call(token,message)
                        head=head+1                   #下一人作为队首
                x = int(input("请输入操作编号："))
        else:
            AK=function.get_AccessKey(data1)
            headers_after_get_AK={'Content-Type':'application/json','access-key':AK}
            url=function.get_QRcode_url(headers_after_get_AK,topicId)
        if function.check_password(password):
            function.delete(data2,headers_after_get_AK)
            print('正在关机')
        else:
            print('密码错误')
    else:
        print('您设置的密码有误,系统即将关机')

else:
    print('检测到config.ini文件不完整,请补全')