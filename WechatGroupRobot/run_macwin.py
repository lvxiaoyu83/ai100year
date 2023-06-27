from app import *
import pyperclip as clp
from daily_client import add_url_to_server

window_width = 2560
window_height = 1600

top_banner_height = 58

hao_height = 144
hao_width = 416

one_page_hao_num = 9

article_2rd_width = 672
article_2rd_height = 196

h_sou = 200
v_sou = 70

h_ding = 170
v_ding = 230

h_ding2 = 180
v_ding2 = 180

h_r_top = 65
v_r_top = 110

r_menu_item_height = 54 # 点开右上方三个点、出来的菜单、单项的高度

all_ctt = {}

def re_open_dingyuehao():
    # pag.hotkey('ctrl','alt', 'w')
    # time.sleep(0.3)
    # pag.hotkey('esc')
    # time.sleep(0.3)
    # pag.hotkey('esc')
    # time.sleep(0.3)
    # pag.hotkey('esc')
    # time.sleep(0.3)
    pag.hotkey('ctrl','alt', 'w')
    pag.hotkey('win', 'up')
    pag.moveTo(x = h_sou, y = v_sou)
    pag.click()
    clp.copy("订阅号")
    time.sleep(0.3)
    pag.hotkey('ctrl', 'a')
    time.sleep(0.3)
    pag.hotkey('ctrl', 'v')
    pag.moveTo(x = h_ding, y = v_ding)
    time.sleep(0.3)
    pag.click()
    time.sleep(0.3)
    pag.moveTo(x = h_ding2, y = v_ding2)
    time.sleep(0.3)
    pag.click(clicks=2, interval=0.1, button='right')
    time.sleep(0.3)
    pag.moveTo(x = window_width /2 , y = window_height / 2)
    time.sleep(0.3)
    pag.hotkey('win', 'up')

def locate_hao(i=0):
    foobar = hao_height / 2
    time.sleep(0.3)
    pag.moveTo(x = foobar, y = top_banner_height + hao_height*0.6+ i*hao_height)
    if i == 0:
        pag.scroll(10000000)
    time.sleep(0.3)
    pag.click()

def copy_browser_url():
    time.sleep(1.2)
    pag.hotkey('ctrl', 'l')
    time.sleep(0.3)
    pag.hotkey('ctrl', 'c') 
    url = clp.paste()
    time.sleep(0.4)
    pag.hotkey('ctrl', 'w') 
    return url

def open_curr_article_to_browser():
    pag.moveTo(x = window_width - h_r_top, y = v_r_top)
    pag.click()
    pag.moveTo(x = window_width - h_r_top - 10, y =v_r_top+r_menu_item_height *3.5)
    pag.click()

def article_click(j):
    y = article_2rd_height * (j + 2)
    if y >= window_height - 50:
        print('y is too big, return')
        return
    pag.moveTo(x=hao_width + top_banner_height, y=y)
    time.sleep(0.3)
    pag.click()
    time.sleep(1.3)
 
def click_curr_hao_all_article(num):
    j = -1
    while True:
        j += 1
        if j < num:
            article_click(j)
            open_curr_article_to_browser()
            url = copy_browser_url()
            if url not in all_ctt:
                print(url)
                all_ctt[url] = url
                # add_url_to_server(url)
        else:
            break

def wechat_article_list(hao_num, art_num):
    for i in range(hao_num + 1):
        print(f"------------ {i} -----------")
        if i == 0:
            locate_hao()
        elif 1 <= i <= one_page_hao_num:
            locate_hao(i)
        else:
            locate_hao(one_page_hao_num-1)
            time.sleep(0.4)
            pag.click()
            time.sleep(0.5)
            locate_hao(one_page_hao_num)
            pag.click()
            time.sleep(0.5)
            pag.hotkey('down')
        time.sleep(0.3)
        # click_curr_hao_all_article(art_num)

if __name__ == "__main__":
    # re_open_dingyuehao()
    # locate_hao()
    wechat_article_list(100, 1)
    # time.sleep(1.3)
    # locate_hao(one_page_hao_num)
    # pag.hotkey('down')
    # click_curr_hao_all_article(6)
    # article_click(6)
    # while True:
    #     re_open_dingyuehao()
    #     wechat_article_list(69, 6)
    #     print('sleeping...')
    #     time.sleep(5 * 60)