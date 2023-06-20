from tools import *
from pachong2 import *


def wechat_article_list_2(hao_num, art_num):
    url_list = []
    for i in range(hao_num + 1):
        my1v=img_loc("images/my1.png")
        
        if i == 0:
            moveby(my1v, -450, 70)
            pag.click()
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
        time.sleep(1.3)        
    url_list = list(set(url_list))
    
    return url_list

def gooo():
    ulist = wechat_article_list_2(99, 1)
    now = now_str()
    
    f_meta = open("_wechat_url" + "_" + now + ".txt", "w", encoding="utf-8")
    f_ctt = open("_wechat_content" + "_" + now + ".txt", "w", encoding="utf-8")
    
    for url in ulist:
        hao, title, desc, ctt = get_wechat_artile_content(url)
        print("%s : %s : %s" % (hao, title, ""))#desc
        
        f_meta.write("%s : %s : %s: %s\n" % (hao, title, desc, url))
        f_meta.flush()
        
        f_ctt.write("%s : %s : %s: %s\n" % (hao, title, desc, url))
        f_ctt.write("%s\n\n\n\n\n\n" % ctt)
        f_ctt.flush()
        
        time.sleep(0.8)
    
    f_meta.close()
    f_ctt.close()


if __name__ == "__main__":
    open_dingyuehao_1()
    open_dingyuehao_2()
    gooo()