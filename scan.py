#多线程端口扫描
import sys
from socket import *
from datetime import datetime
from multiprocessing.dummy import Pool  #导入线程池，实现线程并发

host = input("请输入要扫描的目的主机：")
ip = gethostbyname(host)  #获取目标主机的ip地址
port_range = input("输入要扫描的端口范围：").split("-")

def scan(port):
    try:
        s = socket(AF_INET,SOCK_STREAM)  #建立套接字
        result = s.connect_ex((ip,port)) #建立TCP连接
        if result == 0:  #开启状态
            print("Port {}: OPEN,service: {}".format(port,getservbyport(port)))
        s.close()  #关闭连接
    except Exception as e:
        print(str(e.message))
def main():
    start = int(port_range[0])
    end = int(port_range[1])
    ports = []
    if start<end:
        for i in range(end-start):
            ports.append(i)
    else:
        print("输入范围错误，请重新输入！")
        sys.exit(1)
    print("正在扫描主机{}：".format(ip))
    setdefaulttimeout(0.1)  #设置超时时间限制为0.5s

    starttime = datetime.now()  #记录开始时间

    pool = Pool(10) #创建10个容量的线程池并发执行
    #map函数会将第二个参数所需要迭代的列表元素一个个传入第一个参数中（即scan函数）
    pool.map(scan,ports)  #可以有返回值，但这里不需要
    pool.close()
    pool.join()

    print("多线程端口扫描耗时：", datetime.now() - starttime)
main()
