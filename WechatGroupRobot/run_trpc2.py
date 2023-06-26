from app import *
from openai_tools import *
from pachong2 import *
import pyperclip as clp
from db import SqliteDb




hao_width = 258
hao_height = 90
top_height = 38
window_width = 1920
wi1ndow_height = 1080

def img_loc(img):
    my=CardLocation(config=CardConfig(template_file=img, bias_type=BiasType.NoBias))
    myv=my.get_location
    return myv

def find_my1():
    my1v = img_loc("images2/my1.png")
    return my1v

def moveby(mv, x, y):
    time.sleep(0.4)
    pag.moveTo(x=mv.x+x,y=mv.y+y)
    time.sleep(0.3)

def re_open_dingyuehao():
    pag.hotkey('ctrl','alt', 'w')
    time.sleep(0.2)
    pag.hotkey('esc')
    time.sleep(0.2)
    pag.hotkey('esc')
    time.sleep(0.2)
    pag.hotkey('esc')
    time.sleep(0.2)
    pag.hotkey('ctrl','alt', 'w')
    mpls = img_loc("images2/main_plus.png")
    moveby(mpls, -60, 16)
    pag.click()
    clp.copy("订阅号")
    time.sleep(0.2)
    pag.hotkey('ctrl', 'a')
    time.sleep(0.2)
    pag.hotkey('ctrl', 'v')
    moveby(mpls, -60, 100)
    pag.click()
    moveby(mpls, -60, 100)
    pag.click(clicks=2, interval=0.1, button='right')
    moveby(mpls, 0, 0)
    pag.click(clicks=2, interval=0.1, button='right')#最大化
    mpls = find_my1()
    moveby(mpls, 2, 2)

def close_dingyuehao():
    my1v = find_my1()
    moveby(my1v, 2, 2)
    pag.click()
    pag.hotkey('alt', 'f4')

def locate_first():
    # my1v = find_my1()
    # pag.click()
    pag.moveTo(x = hao_height / 2, y = top_height + hao_height / 2)
    # moveby(my1v, 44, top_height + hao_height / 2)
    pag.click()
    time.sleep(0.3)
    pag.scroll(100000000)
    pag.click()

def open_curr_article_to_browser():
    pag.moveTo(x = window_width-36, y = top_height + 30)
    pag.click()
    pag.moveTo(x = window_width-48, y = top_height + 150)
    pag.click()


def copy_browser_url():
    time.sleep(1.4)
    pag.hotkey('ctrl', 'l') 
    pag.hotkey('ctrl', 'c') 
    url = clp.paste()
    print("get url: " + url)
    time.sleep(0.6)
    pag.hotkey('ctrl', 'w') 
    return url

def click_curr_hao_all_article(num):
    # my1v=find_my1()
    i = 0

    pag.moveTo(x = 290, y = 220)
    pag.click()
    time.sleep(1.3)
    open_curr_article_to_browser()
    url = copy_browser_url()
    if url in all_ctt:
        return 

    hao, title, desc, ctt = get_wechat_artile_content(url)
    if hao is not None:
        f_meta.write("## %s \n\n" % hao)
        f_meta.flush()

    while True:
        if i >= num:
            break
        pag.moveTo(x = 290, y = 220 + i * 120)
        pag.click()
        time.sleep(1.3)
        open_curr_article_to_browser()
        url = copy_browser_url()
        if url in all_ctt:
            i += 1
            continue

        all_ctt[url] = title

        if db.check_url(url):
            i += 1
            hao, title, desc, abst, ctt = db.read('article', columns=' hao, title, desc, abst, ctt ', where=f"url='{url}'")[0]
        else:
            hao, title, desc, abst, ctt = fetch_url_ctt(url)
            if hao is None:
                i += 1
                continue
            db.create('article', {
                'title': title,
                'hao': hao,
                'url': url,
                'desc': desc,
                'abst': abst,
                'ctt': ctt
            })

        f_meta.write("### %s \n\n %s\n\n %s\n" % (title, abst, url))
        f_meta.flush()
        
        f_ctt.write("%s : %s \n %s\n%s\n\n" % (hao, title, desc, url))
        f_ctt.write("%s\n\n" % abst)
        f_ctt.write("%s\n\n\n\n\n\n" % ctt)
        f_ctt.flush()
        i += 1
        

    if hao is not None:
        f_meta.write("<hr/>\n\n\n\n\n\n")
        f_meta.flush()

def fetch_url_ctt(url):
    hao, title, desc, ctt = get_wechat_artile_content(url)
    if hao is None:
        return None, None, None, None, None
    if ctt:
        try:
            _, abst = call_with_sys(sys_prompt, ctt[:6500], 512)
            time.sleep(20)
        except openai.error.APIError:
            return None, None, None, None, None
    else:
        _, abst = '', ''
    print("%s : %s : %s" % (hao, title, url))
    return hao, title, desc, abst, ctt   


def wechat_article_list(hao_num, art_num):
    my1v=find_my1()
    moveby(my1v, 0, 0)
    pag.click()

    for i in range(hao_num):
        my1v=find_my1()
        if i == 0:
            locate_first()
            pag.click()
        elif 0 < i <= 10:
            pag.moveTo(x = hao_height / 2, y = top_height + hao_height / 2 + hao_height * i)
            # moveby(my1v, 44, top_height + hao_height / 2 + i * 88)
            pag.click()
        else:
            pag.moveTo(x = hao_height / 2, y = top_height + hao_height / 2 + hao_height * 10)
            pag.click()
            pag.hotkey('down')#不点击左边列表 只key down不行

        time.sleep(0.8)
        click_curr_hao_all_article(art_num)

if __name__ == "__main__":
    
    while True:
        try:
            close_dingyuehao()
        except:
            pass
        re_open_dingyuehao()
        # break
        all_ctt = {}
        sys_prompt = "跟据用户给出的文章提取80-120字的摘要，具体时间、人物等信息不可以省略。"
        db = SqliteDb('test.sqlite')
        db.create_table('article', 'hao TEXT, title TEXT, url TEXT, desc TEXT, abst TEXT, ctt TEXT')
        now = datetime.now().strftime('%Y%m%d_%H%M%S')
        f_meta = open("C:\\Users\\Administrator\\OneDrive\\model_daily\\_wechat_url" + "_" + now + ".md", "w", encoding="utf-8")
        f_ctt = open("_wechat_content" + "_" + now + ".txt", "w", encoding="utf-8")
        wechat_article_list(69, 1)
        f_meta.close()
        f_ctt.close()
        db.close()

        time.sleep(2 * 60)


        