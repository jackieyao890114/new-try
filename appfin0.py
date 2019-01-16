# -*- coding: utf-8 -*-
#ＡＵＴＨＯＲ：ＪＡＣＫＩＥ　ＹＡＯ
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import os
import time
import pytesseract
from PIL import Image



def moot_auto():
    driver = webdriver.Chrome()
    id='15018706212'
    
    password='wing0114Gan'
    no_main_object = 1
    driver.get("http://mooc.ctt.cn")
    driver.maximize_window()
    time.sleep(1)
    js="$('.shen_con').scrollTop(2000)"     #通过审查元素，看到JS有定义指令，用定义指令滚动条。至于为什么能用？？？
    driver.execute_script(js)
    time.sleep(1)
    driver.find_element_by_id('button_1').click()     #确认申明                                               
    login(driver,id,password)
    el=WebDriverWait(driver,15).until(EC.presence_of_element_located((By.NAME,'courseMore')))
    '''while el:
        time.sleep(2)
        driver.find_element_by_css_selector("img[onclick='changeImageCode']").click()
        input_code('code','image-code',r'd:\code.png',driver)'''
        
        
    duc = 'watched_%s.txt'%id
    if os.path.exists(duc):                                                         
        with open(duc,'r') as f:                                       #打印出记录下的已看专题
            watched_li=f.read()
        li=watched_li.split(',')
    else:
        li=[]
    print('记录了您已观看%s'%li) 
    find_more(driver)
    time.sleep(2)
    search_input(driver,'宪法')
    time.sleep(2)
    pick_subject(driver,li,duc,'.pic img')
    time.sleep(3)
    find_elements_by_css_selector("a[data-dir='next']").click()
    pick_subject(driver,li,duc,'.pic img')
    
    
    '''
    if no_main_object:
        pick_subject(driver,li,duc,'.text-ellipsis > a')
    else:
        choose_pri_oj(driver,li,num,duc,'.info + .btn')'''
def search_input(driver,data):
    input_data = driver.find_element_by_css_selector("input[name='name']")
    input_data.send_keys(data)
    input_data.send_keys(Keys.RETURN)
def find_more(driver):
    
    driver.find_element_by_name('courseMore').click()
    
def choose_pri_oj(driver,li,num,duc,ad='.info + .btn'):                  #主页主题元素搜索地址 ad为CSS查找到的主题定位
    buttoms=driver.find_elements_by_css_selector(ad)
    buttoms_n=len(buttoms)
    print('共有%d个主题\n'%buttoms_n) 
    buttoms[num].click()
    time.sleep(5)
    driver.switch_to.window(driver.window_handles[-1])   
    pick_subject(driver,li,duc)
    
    for n in range(buttoms_n):    
        buttoms[n].click()
        time.sleep(5)
        driver.switch_to.window(driver.window_handles[-1])   
        pick_subject(driver,li,duc)
                
def login(driver,id,password):         #登陆
    driver.find_element_by_id("loginId").clear()     
    driver.find_element_by_id("loginId").send_keys(id)
    driver.find_element_by_id("password").clear()
    driver.find_element_by_id("password").send_keys(password)
    input_code('code','image-code',r'd:\code.png',driver)
    '''while driver.find_element_by_css_selector("div[id='msg']").text == '请输入验证码':
        time.sleep(1)
        driver.find_element_by_css_selector("img[onclick='changeImageCode']").click()
        input_code('code','image-code',r'd:\code.png',driver)'''
            #调用验证码指令 
    
    
def pick_subject(driver,li,duc,ad):                                                      #选择课题
    sub_names = driver.find_elements_by_css_selector(ad)     #获取副标题名字
    contents_num = len(sub_names)                                                 
    print('该主题共有%d个课程'%contents_num)                                        #主题下副主题数目
    text_li=list(map(lambda x:x.get_attribute('alt'),sub_names))                                  #构造福题目列表
    for n in range(contents_num):      
        #print('CHOOSEN'+text_li[n])                                            #看哪个？
        if text_li[n] not in li:
            time.sleep(3)
            print('开始学习《%s》\n'%text_li[n])        
            contents=driver.find_elements_by_css_selector(ad)   #副题目按钮
            contents[n].click()
            driver.switch_to.window(driver.window_handles[-1])
            time.sleep(5)
            start_redio(driver)        
            driver.switch_to.window(driver.window_handles[-1])    
            with open(duc,'a+') as f:
                f.write(text_li[n]+',')
                print("已观看《%s》\n"%text_li[n])       
    driver.close()
    driver.switch_to.window(driver.window_handles[-1])
def start_redio(driver):                                                   #处理视频
    try:
        my_study=driver.find_element_by_css_selector(".course-state button") 
        if my_study.get_attribute('textContent')=='我要学习':
            my_study.click()                                               #点击我要学习按钮
    except NoSuchElementException:
       #print('no such button')
        pass
    time.sleep(2)
    redios = driver.find_elements_by_css_selector(".title")               #读取视频数
    redios_num = len(redios)
    print('该课程共有%s个视频'%redios_num)    
    for n in range(redios_num):                                         
        titles = driver.find_elements_by_css_selector(".title")
        vedio_buttons=driver.find_elements_by_css_selector('.title + button')
        if vedio_buttons[n].text != '复习':       #选择标记非‘复习’的视频
            try:
                t2go=titles[n].find_element_by_css_selector('span').get_attribute('textContent')
            except NoSuchElementException:
                t2go=0            
            print('准备看第%s个视频 ：'%(n+1)) 
            vedio_buttons[n].click()
            driver.switch_to.window(driver.window_handles[-1])
            if t2go:
                wait_time=int(t2go.split()[1])
                print('需要观看%d分钟'%wait_time)
                time.sleep(wait_time*60)
                
            else:
                time.sleep(15)          
                driver.switch_to.frame(driver.find_elements_by_tag_name("iframe")[0])   #转入Iframe
                time.sleep(45)
                try:                           
                    a=driver.find_element_by_id('jwplayer_place_controlbar_duration')
                    total_t = con2time(a)
               #print('总时间为%d\n'%total_t)  
                    b=driver.find_element_by_id('jwplayer_place_controlbar_elapsed')
                    fin_t = con2time(b)
               #print('已看时间为%d\n'%fin_t)                   
                except NoSuchElementException: 
                    print('找不到元素')
                if total_t:                
                    wait_time = total_t - fin_t
                    if wait_time<60:
                        wait_time=180                
                else:
                    wait_time=60
                print('需观看时间为%s\n'%wait_time) 
                time.sleep(wait_time)
            driver.close()
            driver.switch_to.window(driver.window_handles[-1])
        
    time.sleep(5)
    state = driver.find_element_by_css_selector("strong[class='green']")
    print(state.text)
    if state.text == '学习中':
        start_redio(driver)
        print('还有没学完的课程')
    else:
        driver.close()
def find_unfin(driver):
    contins=driver.find_elements_by_css_selector('.title span')
    

def con2time(content):    #元素转时间
    t_text = content.get_attribute('textContent')
    t_li=list(t_text)
    print(t_li)
    t =int(t_li[0])*600+int(t_li[1])*60
    return t
    
def input_code(code_id,image_id,ad,driver):  #输入
    driver.find_element_by_id(code_id).clear()
    get_code_img(image_id,ad,driver)
    im_code=img2str(ad)
    inp = driver.find_element_by_id(code_id)
    inp.send_keys(im_code)
    inp.send_keys(Keys.RETURN)
    
   
def get_code_img(img_id,ad,driver):
    driver.save_screenshot(ad)
    code_img = driver.find_element_by_id(img_id)
    print(code_img.location['x'])
    print(code_img.location['y'])
    left = code_img.location['x']
    top = code_img.location['y']
    right =left + code_img.size['width']
    bottom = top + code_img.size['height']
    im = Image.open(ad)
    im = im.crop((left,top,right,bottom))
    im.save(ad)

def img2str(ad_from):
    image = Image.open(ad_from)
    pytesseract.pytesseract.tesseract_cmd = r'e:\tesseract-ocr\tesseract.exe'                      #tesseract-orc地址
    code = pytesseract.image_to_string(image)
    print(code)
    return code

if __name__ == "__main__":
    moot_auto()
