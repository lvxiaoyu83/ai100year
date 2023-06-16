from app import *
import pyperclip as clp


def img_loc(img):
    my=CardLocation(config=CardConfig(template_file=img, bias_type=BiasType.NoBias))
    myv=my.get_location
    return myv

def moveby(mv, x, y):
    if mv is None or mv.status is False:
        return
    pag.moveTo(x=mv.x+x,y=mv.y+y)

def open_curr_article():
    my2v=img_loc("images/my2.png")
    moveby(my2v, 60, 60)
    pag.click()
    moveby(my2v, 70, 150)
    pag.click()


def copy_browser_url():
    time.sleep(0.8)

    pag.hotkey('ctrl', 'l') 
    pag.hotkey('ctrl', 'c') 
    url = clp.paste()
    print("get url: " + url)

    time.sleep(0.8)
    pag.hotkey('ctrl', 'w') 
    return url
    

def move_to_first():
    my1v=img_loc("images/my1.png")
    moveby(my1v, -450, 60)
    pag.click()

def click_article():
    my1v=img_loc("images/my1.png")
    moveby(my1v, -450, 60)
    pag.click()
    clp.set_clipboard()