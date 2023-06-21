from openai_tools import *
from tools import moveby, open_curr_article_to_browser, copy_browser_url, img_loc, now_str
from pachong2 import *
from app import *

all_ctt = {}
sys_prompt = "跟据用户给出的文章提取80-120字的摘要，具体时间、人物、地点等信息不可以省略。"

def click_curr_hao_all_article(num):
    my1v=img_loc("images2/my1.png")
    i = 0
    while True:
        if i >= num:
            break
        moveby(my1v, -180, 220+i*100)
        pag.click()
        time.sleep(1.8)
        open_curr_article_to_browser()
        url = copy_browser_url()
        if url not in all_ctt:
            success = fetch_url_ctt(url)
            if success:
                i += 1
                time.sleep(15)
                continue
            else:
                time.sleep(1.5)
                continue
        else:
            i += 1
            continue

def fetch_url_ctt(url):
    # try:
    hao, title, desc, ctt = get_wechat_artile_content(url)
    _, abst = call_with_sys(sys_prompt, ctt[:6000], 1024)
    time.sleep(1.2)
    all_ctt[url] = {
                'hao' : hao,
                'title' : title,
                'ctt' : ctt,
                'abst' : abst,
            }
    f_meta.write("### %s || %s \n\n %s\n\n %s\n<hr/>\n\n\n\n\n" % (hao, title, abst, url))
    f_meta.flush()
    
    f_ctt.write("%s : %s : %s: %s\n\n" % (hao, title, desc, url))
    f_ctt.write("%s\n\n" % abst)
    f_ctt.write("%s\n\n\n\n\n\n" % ctt)
    f_ctt.flush()
    print("%s : %s : %s" % (hao, title, url))
    # except:
    #     print('error!')
    #     return False
    return True

def wechat_article_list(hao_num, art_num):
    for i in range(hao_num + 1):
        my1v=img_loc("images2/my1.png")
        
        if i == 0:
            moveby(my1v, -450, 70)
            pag.click()
            time.sleep(1.2)
            pag.scroll(1000000)
            time.sleep(1.2)
            pag.click()
        elif i <= 10:
            moveby(my1v, -450, 70+70*i)
            pag.click()
        else:
            moveby(my1v, -450, 770)
            pag.click()
            pag.hotkey('down')#不点击左边列表 只key down不行

        time.sleep(1.5)
        click_curr_hao_all_article(art_num)
        time.sleep(2.8)


def gooo():
    my1v=img_loc("images2/my1.png")
    moveby(my1v, -450, 70)
    pag.click()
    pag.scroll(1000000)
    pag.click()

    wechat_article_list(80, 5)
    
    for k, v in all_ctt:
        print("%s || %s \n" % (v['hao'], v['title']))#desc
        print(v['abst'])
        print("\n")
        
        # time.sleep(5.0)
    


if __name__ == "__main__":
    # open_dingyuehao_1()
    # open_dingyuehao_2()
    now = now_str()
    f_meta = open("_wechat_url" + "_" + now + ".md", "w", encoding="utf-8")
    f_ctt = open("_wechat_content" + "_" + now + ".txt", "w", encoding="utf-8")
    gooo()

    f_meta.close()
    f_ctt.close()