from app import *
import pyperclip as clp


def img_loc(img):
    my=CardLocation(config=CardConfig(template_file=img, bias_type=BiasType.NoBias))
    myv=my.get_location
    return myv

def moveby(mv, x, y):
    # if mv is None or mv.status is False:
    #     return
    pag.moveTo(x=mv.x+x,y=mv.y+y)

def open_curr_article():
    my2v=img_loc("images/my2.png")
    moveby(my2v, 60, 60)
    pag.click()
    moveby(my2v, 70, 150)
    pag.click()
    

def move_to_first():
    my1v=img_loc("images/my1.png")
    moveby(my1v, -450, 60)
    pag.click()

def click_article():
    my1v=img_loc("images/my1.png")
    moveby(my1v, -450, 60)
    pag.click()
    clp.set_clipboard()

def open_dingyuehao_1():
    serch_plus = img_loc("images/serch_plus.png")
    moveby(serch_plus, -40, 15)
    pag.click()
    
    clp.copy("订阅号")
    time.sleep(0.1)
    pag.hotkey('ctrl', 'a')
    time.sleep(0.1)
    pag.hotkey('ctrl', 'v')

    serch_plus = img_loc("images/serch_plus.png")
    moveby(serch_plus, -90, 90)
    pag.click()

def open_dingyuehao_2():
    dingyuehao_switch = img_loc("images/dingyuehao_switch.png")
    if dingyuehao_switch.status is True:
        moveby(dingyuehao_switch, 5, 5)
        pag.click()
    
    ding_switch2 = img_loc("images/ding_switch2.png")
    moveby(ding_switch2, 1, 1)
    pag.click()

def now_str():
    now = datetime.now()
    time_str = now.strftime('%Y%m%d_%H%M%S')
    return time_str

def move_to_first():
    my1v=img_loc("images/my1.png")
    moveby(my1v, -450, 60)
    pag.scroll(1000000)
    time.sleep(0.1)
    pag.click()

def open_curr_article_to_browser():
    my2v=img_loc("images/my2.png")
    moveby(my2v, 60, 60)
    pag.click()
    moveby(my2v, 70, 150)
    pag.click()

def check_list(foo, foo_list):
    for fff in foo_list:
        if foo in fff:
            return True
        
def copy_browser_url():
    time.sleep(0.8)

    pag.hotkey('ctrl', 'l') 
    pag.hotkey('ctrl', 'c') 
    url = clp.paste()
#     print("get url: " + url)
    time.sleep(0.8)
    pag.hotkey('ctrl', 'w') 
    return url

def click_curr_hao_all_article(num):
    my1v=img_loc("images/my1.png")
    url_list = []
    for i in range(num):
        moveby(my1v, -180, 220+i*100)
        pag.click()
        time.sleep(1.5)
        open_curr_article_to_browser()
        url = copy_browser_url()
        if not check_list(url, url_list):
            url_list.append(url)
    return url_list

def wechat_article_list(hao_num, art_num):
    url_list = []
    for i in range(hao_num + 1):
        my1v=img_loc("images/my1.png")
        moveby(my1v, -450, 70)
        if i == 0:
            pag.scroll(1000000)
            pag.click()
        elif i <= 10:
            moveby(my1v, -450, 70*i)
            pag.click()
        else:
            moveby(my1v, -450, 770)
            pag.click()
            pag.hotkey('down')#不点击左边列表 只key down不行

        ulist = click_curr_hao_all_article(art_num)
        if ulist:
            url_list.extend(ulist)
        ulist = list(set(ulist))
        # print(url_list)
        print("sleeping...")
        time.sleep(1.3)        
    url_list = list(set(url_list))
    
    return url_list