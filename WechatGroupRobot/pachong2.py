import requests
from bs4 import BeautifulSoup
import urllib.request as request
import os
from hashlib import sha1
 
def download_img(imgurl):
	#将图片保存到本地
	path = './'
	if not os.path.exists(path):
		os.makedirs(path)
	s1 = sha1()  #创建sha1加密对象
	s1.update(imgurl.encode("utf-8")) 
	_imgurl = s1.hexdigest()  
	# imgpath = path + '//' + _imgurl
	# imgpath = path + '//' + os.path.split(imgurl)[1]
	imgpath = os.path.split(imgurl)[1]
	local_img_url = request.urlretrieve(imgurl, imgpath)
	return local_img_url

def get_wechat_artile_content(vgm_url):
	html_text = requests.get(vgm_url).text
	soup = BeautifulSoup(html_text, 'html.parser')

	# share_title = soup.find_all(property='og:title') #分享标题,返回的列表，实际中只有一条，用find()更合适
	share_title = soup.find(property='og:title') #分享标题行
	share_title_con = share_title.get('content') #分享标题文本
	# print(share_title_con)
	
	share_url = soup.find(property='og:url') #分享url行
	share_url_con = share_url.get('content') #分享url地址文本
	# print(share_url_con)
	
	share_desc = soup.find(property='og:description') #分享描述行
	share_desc_con = share_desc.get('content') #分享描述文本
	# print(share_desc_con)
	
	share_img = soup.find(property='og:image') #分享头图行
	share_img_con = share_img.get('content') #分享头图地址，微信有防盗链机制，所以图片需要下载到本地

	h1 = soup.find_all('h1')
	body = soup.find(id='activity-detail')
	content=body.find(id='js_content')
	imgs = content.find_all('img')  #文章中的所有图片
	# for img in imgs:
	# 	if img.get('data-src'):
	# 		new_src = download_img(img.get('data-src'))[0]
	# 		img['data-src'] = new_src   #前端图片展示时需要用延迟加载
	# 		print(img)
			
	name = soup.select('#meta_content > span.rich_media_meta_text')
	if len(name) > 0:
		author_name = name[0].get_text() #作者名字
		print(author_name)

	title = body.find(id='activity-name') #标题(带html标签的内容)
	title_txt = title.get_text() #标题的文本
	# print(title_txt)

	tags = body.find(id='js_tags') #话题(带html标签)，有的文章在标题作者与正文中间，有一组收录于**话题
	content = body.find(id="js_content") #文章正文内容
	# print(content.prettify()) #格式化输出内容
	content_text = content.get_text()


	#直接soup筛选公众号名字
	wx_account_name = soup.select('#meta_content > #profileBt > #js_name')[0].get_text() #微信公众号的名字
	wx_account = soup.find(id="meta_content")
	wx_account_name = wx_account.select('#profileBt > #js_name')[0].get_text() #微信公众号的名字
	wx_account_content = wx_account.select('#profileBt > #js_profile_qrcode > .profile_inner > .profile_meta') #获得列表，内容依次为公众号微信名，公众号描述
	wx_account_account = wx_account_content[0].select('.profile_meta_value')[0].get_text() #公众号微信名
	wx_account_desc = wx_account_content[1].select('.profile_meta_value')[0].get_text() #公众号描述

	# print(wx_account_name)
	# print(wx_account_account)
	# print(wx_account_desc)
	return content_text

# get_wechat_artile_content('https://mp.weixin.qq.com/s/tztm1ic7B7z4klXBzGv6vg')