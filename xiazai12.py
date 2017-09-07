# -*- coding:utf-8 -*-
#2016年8月15日，软件可以实现http软件可以实现http://www.zngirls.com/g/XXXXX/1.html'的某个图片编号范围的图片批量下载到各自名字下的文件夹
#2016年8月16日，软件完善到self.user
#8月16日，部分网址导入后报错，'gbk' codec can't encode character u'\ubc15' in position 4: illegal multibyte sequence
#部分字符从utf-8解析为unicode后无法被gkb编码，需要进行处理decode('utf-8','ignore').encode('gbk','ignore')
#2016年8月30日试图完善timeout报错问题,已经解决，并试图完成模块化处理
#dfff
#2017年7月2日女神录域名改为nvshens,如果使用zngirls
import re
import os  
import urllib
import urllib2
import socket
import string

class xiazai:
	#初始化方法，定义一些变量
    def __init__(self):
        self.url = 'http://www.zngirls.com/g/'
        cookie='Hm_lvt_1bb490b9b92efa278bd96f00d3d8ebb4=1495864233,1495875134,1496497139,1496580279; gallery_22961=1; records=%5B%7B%22id%22%3A%2221363%22%2C%22name%22%3A%22%u718A%u4F73%22%7D%2C%7B%22id%22%3A%2218071%22%2C%22name%22%3A%22%u5289%u5955%u5BE7%22%7D%2C%7B%22id%22%3A%2218723%22%2C%22name%22%3A%22%u738B%u8273%u5353%22%7D%2C%7B%22id%22%3A%2219400%22%2C%22name%22%3A%22%u738B%u66FC%u59AE%22%7D%2C%7B%22id%22%3A%2221501%22%2C%22name%22%3A%22%u590F%u7F8E%u9171%22%7D%5D; gallery_22955=1; gallery_22930=1; gallery_22959=1; gallery_22934=1; Hm_lvt_f378865b660846b55ba91d29e1c4c04d=1496497135,1496580267,1496997767,1496999204; Hm_lpvt_f378865b660846b55ba91d29e1c4c04d=1497000069'
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'
        self.referer=self.url[:]
        self.headers = { 'User-Agent' : self.user_agent,
                         'Connection':'keep-alive',
                         'Cookie':cookie,
                         'Cache-Control': 'max-age=0',
                         'Referer':self.referer }
        #存放程序是否继续运行的变量
        self.enable = True


    #对传入网址或图片进行解析，为避免被ban,加入headers进行申请
    def getPage(self, url):
        try:
            request1 = urllib2.Request(url, headers=self.headers)
            response1 = urllib2.urlopen(request1, timeout=1)
            # 将页面转化为UTF-8编码
            pageCode = response1.read()
            return pageCode
        #遇到报错超时后重启
        except socket.timeout, e:
            print 'onece start'
            return self.getPage(url)
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print u"连接失败,错误原因", e.reason, 'error'
                if hasattr(e, 'code'):
                    if e.code.real == 404:
                        self.enable = False
                        return None
                            # 将超时的错误原因输出为str格式，方便进行循环比较。
                error = e.reason.message  # str格式，timed out
                if (error == 'timed out'):
                    print 'restart once again'
                    return self.getPage(url)
       # except urllib2.HTTPError:
       #      return self.getPage(url)


    #获取传入页面图片地址里列表
    def getPhoto_url(self,url):
        pageCode=self.getPage(url)
        if not pageCode:
            print "页面加载失败...."
            return None
        pattern = re.compile('''<div class="photos">.*?<img src='(.*?).jpg' alt='.*?'>''',re.S)
        items = re.findall(pattern,pageCode)
        if len(items)>0:
            print items[0]
            return items[0]
        else:
            return None

    #获取网页对应的文档题目
    def getPhoto_title(self,url):
        pageCode=self.getPage(url)
        if not pageCode:
            print "页面加载失败...."
            return None
        pattern = re.compile('''<title>(.*?)</title>''',re.S)
        items = re.findall(pattern,pageCode)
        # print items[0]
        judge=['\xe8\xaf\xa5\xe9\xa1\xb5\xe9\x9d\xa2\xe6\x9c\xaa\xe6\x89\xbe\xe5\x88\xb0-\xe5\xae\x85\xe7\x94\xb7\xe5\xa5\xb3\xe7\xa5\x9e']
        # print items[0]
        # print judge
        # print items[0]==judge[0]
        if items[0]!=judge[0]:
            return items[0]
        else:
            return None

    #使用代理
    def proxy_setting(self,http):
        enable_proxy = True
        proxy_handler = urllib2.ProxyHandler({"http" : http})
        null_proxy_handler = urllib2.ProxyHandler({})
        if enable_proxy:
            opener = urllib2.build_opener(proxy_handler)
        else:
            opener = urllib2.build_opener(null_proxy_handler)
        urllib2.install_opener(opener)
        return None

    #创建新目录
    def mkdir(self,path):
        path = path.strip()
        # 判断路径是否存在
        # 存在     True
        # 不存在   False
        isExists=os.path.exists(path)
        # 判断结果
        if not isExists:
            # 如果不存在则创建目录
            print u"新建了名字叫做",path,u'的文件夹'
            # 创建目录操作函数
            os.makedirs(path)
            return True
        else:
            # 如果目录存在则不创建，并提示目录已存在
            print u"名为",path,'的文件夹已经创建成功'
            return False

    #保存图片
    def saveImg(self,data,fileName):
         f = open(fileName, 'wb')
         f.write(data)
         print u"保存她的一张图片为",fileName
         f.close()

    #启动程序
    def start(self,url_download):
        #设置代理
        http='http://www.zngirls.com/'
        self.proxy_setting(http)
        #获取当前目录路径
        currentpath=os.getcwd()
        #对传入的列表进行逐次处理
        for j in url_download:
            #组合获得需要爬虫的页面url
            url_new=self.url+str(j)+'/1.html'
            print url_new
            # 获取网址url对应的图片url
            url_firstphoto=self.getPhoto_url(url_new)
            #获取网址url对应的图片册
            filename=(self.getPhoto_title(url_new))
            # 如果没有得到url及图片集名称则pass
            if not filename or not url_firstphoto:
                continue
            else:
                filename=filename.decode('utf-8','ignore').encode('gbk','ignore')
            filename_file='No.'+str(j)+filename
            #计数器
            i=1
            #创建目录操作函数
            self.mkdir(filename_file)
            #将图片保存路径改到当前新建目录
            os.chdir(filename_file)
            #循环判断初始化，用于确定爬取页面真实有效则进行爬取
            self.enable = True
            while self.enable:
                #图片爬取需要设置代理地址
                # self.proxy_setting('http://t1.zngirls.com/gallery/')
                #d读图片进行排序
                if i==1:
                    url_firstphotoi=url_firstphoto+'.jpg'
                    filename1=filename+str(0)+str(i)+'.jpg'
                elif i<11:
                    url_firstphotoi=url_firstphoto+str(0)+str(i-1)+'.jpg'
                    filename1=filename+str(0)+str(i)+'.jpg'
                else:
                    url_firstphotoi=url_firstphoto+str(i-1)+'.jpg'
                    filename1=filename+str(i)+'.jpg'
                #获取图片url解析data,需要使用新的headers
                print url_firstphotoi
                http = 'http://img.zngirls.com'
                self.proxy_setting(http)
                data = self.getPage(url_firstphotoi)
                if self.enable and data:
                    self.saveImg(data,filename1)
                    i=i+1
                else:
                    break
            #形成新目录保存文件后，转换到原始目录。
            os.chdir(currentpath)
spider=xiazai()
url=[23835,23833,23834]
spider.start(url)

