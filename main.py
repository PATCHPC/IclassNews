from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
import time,re,csv
from bs4 import BeautifulSoup
# 数据抓取相关的库

import smtplib
from email.mime.text import MIMEText
# email 用于构建邮件内容
from email.header import Header
# 用于构建邮件头

def extract_html():
    browser.get(url)
    time.sleep(2)
    browser.find_element_by_xpath('/html/body/div/div[3]/div[1]/div/form/input[1]').send_keys(userid)
    browser.find_element_by_xpath('/html/body/div/div[3]/div[1]/div/form/input[2]').send_keys(passwd)
    browser.find_element_by_xpath('/html/body/div/div[3]/div[1]/div/form/input[3]').click()

    # browser.find_element_by_xpath('//*[@id="global-nav-link"]').click()
    # browser.execute_script('window.open()')
    # print(browser.window_handles)
    # time.sleep(2)
    browser.get('https://iclass.bupt.edu.cn/webapps/bb-social-learning-BBLEARN/execute/mybb?cmd=display&toolId=AlertsOnMyBb_____AlertsTool')
    time.sleep(2)


    browser.switch_to_frame(browser.find_element_by_id("mybbCanvas"))
    time.sleep(2)
    html = BeautifulSoup(browser.execute_script("return document.documentElement.outerHTML"),"html.parser")

    return html

def extract_data(html, new_list):
    items = html.find_all(name = 'div', attrs={'class':'stream_item'})
    getId = re.compile(r'id="bb-nautilus(\d{6})"')
    getTitle = re.compile(r'<span class="eventTitle">(.*?)</span>')
    getClass = re.compile(r'<span class="stream_area_name">(.*?)</span>')
    # getType = re.compile(r'>(.*?)<span class="eventTitle">')

    i = 0

    for item in items:
        item = str(item)
        textid = re.findall(getId,item) #获取消息对应的id
        title = re.findall(getTitle,item) #获取消息对应的标题
        textClass = re.findall(getClass,item) #获取消息对应的课程名
        new_list.append([textid[0],title[0],textClass[0]])
        i = i + 1
        if i == 5:
            break

    return new_list

def read_csv(old_list):
    csv_reader = csv.reader(open('msg.csv', "rt",encoding="utf-8"))
    for row in csv_reader:
        old_list.append(row)
    return old_list

def compare_data(new_list, old_list, send_list):
    former_id = old_list[0][0] 
    # 提取出前一个的序号

    # print(new_list[0][0],old_list[0][0])
    
    for item in new_list:
        if item[0] != former_id:
            send_list.append(item)
        else:
            break

    return send_list


def update_data(new_list):
    f = open('msg.csv','r+',newline='',encoding='utf-8')
    f_csv = csv.writer(f)
    f_csv.writerow(new_list[0])
    


def send_email(send_list):
    

    for item in send_list:
        # 邮箱正文内容，第一个参数为内容，第二个参数为格式(plain 为纯文本)，第三个参数为编码
        msg = MIMEText(item[1]+"来自"+item[2],'plain','utf-8')
        # 邮件头信息
        msg['From'] = Header(from_addr)
        msg['To'] = Header(to_addr)
        msg['Subject'] = Header('爱课堂有新作业啦'+",来自"+item[2])
        # 开启发信服务，这里使用的是加密传输
        server = smtplib.SMTP_SSL()
        server.connect(smtp_server,465)
        # 登录发信邮箱
        server.login(from_addr, password)
        # 发送邮件
        server.sendmail(from_addr, to_addr, msg.as_string())
        # 关闭服务器
        server.quit()
    # else:
    #     break
    exit()

if __name__ == '__main__':
    from_addr = '1132680329@qq.com'
    password = 'jncqbojqjdcujcbc'
    to_addr = 'singledogepc@foxmail.com'
    smtp_server = 'smtp.qq.com'
    # 邮件相关

    url = "https://iclass.bupt.edu.cn/webapps/portal/execute/tabs/tabAction?tab_tab_group_id=_1_1"
    userid = '2018211197'
    passwd = '065527'

    new_list = []
    old_list = []
    send_list = []
    
    browser = Chrome()
    html = extract_html()
    new_list = extract_data(html,new_list)
    old_list = read_csv(old_list)
    send_list = compare_data(new_list, old_list, send_list)
    
    update_data(new_list)
    send_email(send_list)

    browser.close()

    


