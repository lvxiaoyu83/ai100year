from app import *
from openai_tools import *
# from tools import moveby, open_curr_article_to_browser, copy_browser_url, img_loc, now_str
# from tools import open_dingyuehao_1, open_dingyuehao_2
from pachong2 import *
# from app import *
import pyperclip as clp

all_ctt = {}
sys_prompt = "跟据用户给出的文章提取80-120字的摘要，具体时间、人物、地点等信息不可以省略。"

h_plus_hao = -520
h_3point_right = 70
v_3point_down = 60
v_3point_down_down = v_3point_down + 120

def find_my2():
    my2v=img_loc("images2/my2_2.png")
    return my2v


def open_curr_article_to_browser():
    my2v=find_my2()
    moveby(my2v, h_3point_right, v_3point_down)
    pag.click()
    moveby(my2v, h_3point_right+10, v_3point_down_down)
    pag.click()

def moveby(mv, x, y):
    time.sleep(0.8)
    pag.moveTo(x=mv.x+x,y=mv.y+y)
    time.sleep(0.8)

def img_loc(img):
    my=CardLocation(config=CardConfig(template_file=img, bias_type=BiasType.NoBias))
    myv=my.get_location
    return myv


def find_my1():
    my1v = img_loc("images2/my1_2.png")
    return my1v

def copy_browser_url():
    time.sleep(1.2)

    pag.hotkey('ctrl', 'l') 
    pag.hotkey('ctrl', 'c') 
    url = clp.paste()
    print("get url: " + url)
    time.sleep(1.4)
    pag.hotkey('ctrl', 'w') 
    return url

def click_curr_hao_all_article(num):
    my1v=find_my1()
    i = 0
    curr_hao = None
    while True:
        if i >= num:
            break
        moveby(my1v, -180, 220+i*100)
        pag.click()
        time.sleep(1.8)
        open_curr_article_to_browser()
        url = copy_browser_url()
        if url not in all_ctt:
            hao, title, desc, abst, ctt = fetch_url_ctt(url)
            all_ctt[url] = title

            if curr_hao is None:
                curr_hao = hao
                f_meta.write("## %s \n\n" % hao)
                f_meta.flush()
            else:
                f_meta.write("### %s \n\n %s\n\n %s\n" % (title, abst, url))
                f_meta.flush()
            f_meta.flush()
            
            f_ctt.write("%s : %s : %s: %s\n\n" % (hao, title, desc, url))
            f_ctt.write("%s\n\n" % abst)
            f_ctt.write("%s\n\n\n\n\n\n" % ctt)
            f_ctt.flush()
            time.sleep(15)
        else:
            i += 1
            continue
    if curr_hao is not None:
        f_meta.write("<hr/>\n\n\n\n\n\n")
        f_meta.flush()

def fetch_url_ctt(url):
    hao, title, desc, ctt = get_wechat_artile_content(url)
    _, abst = call_with_sys(sys_prompt, ctt[:6500], 512)
    print("%s : %s : %s" % (hao, title, url))
    return hao, title, desc, abst, ctt   


def wechat_article_list(hao_num, art_num):
    for i in range(hao_num + 1):
        my1v=find_my1()
        
        if i == 0:
            moveby(my1v, h_plus_hao, 70)
            pag.click()
            time.sleep(1.2)
            pag.scroll(1000000)
            time.sleep(1.2)
            pag.click()
        elif i <= 10:
            moveby(my1v, h_plus_hao, 70+70*i)
            pag.click()
        else:
            moveby(my1v, h_plus_hao, 770)
            pag.click()
            pag.hotkey('down')#不点击左边列表 只key down不行

        time.sleep(1.5)
        click_curr_hao_all_article(art_num)
        time.sleep(2.8)


def gooo():
    my1v=find_my1()
    moveby(my1v, -520, 70)
    pag.click()
    pag.scroll(1000000)
    pag.click()

    wechat_article_list(80, 5)
    
    for _, v in all_ctt:
        print("%s || %s \n" % (v['hao'], v['title']))#desc
        print(v['abst'])
        print("\n")
        
        # time.sleep(5.0)
    
def now_str():
    now = datetime.now()
    time_str = now.strftime('%Y%m%d_%H%M%S')
    return time_str

if __name__ == "__main__":
    # open_dingyuehao_1()
    # open_dingyuehao_2()
    now = now_str()
    f_meta = open("_wechat_url" + "_" + now + ".md", "w", encoding="utf-8")
    f_ctt = open("_wechat_content" + "_" + now + ".txt", "w", encoding="utf-8")
    gooo()

    f_meta.close()
    f_ctt.close()