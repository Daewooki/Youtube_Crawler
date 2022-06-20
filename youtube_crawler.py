import time
import re
import pandas as pd
from selenium import webdriver as wd
from bs4 import BeautifulSoup
import requests

def crawl_uid_and_comments(url='https://www.youtube.com/watch?v=0n-qDDrFo2w'):
    driver = wd.Chrome(executable_path="chromedriver.exe")
    driver.get(url)

    # 유튜브 댓글 스크롤해야 더보기 가능
    total_page_height = driver.execute_script("return document.documentElement.scrollHeight")
    while True: 
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);") 
        time.sleep(3.0)
        now_page_height = driver.execute_script("return document.documentElement.scrollHeight") 
        if now_page_height == total_page_height:
            break 
        total_page_height = now_page_height 
        
    html_source = driver.page_source 
    driver.close() 

    soup = BeautifulSoup(html_source, 'lxml')

    youtube_user_IDs = soup.select('#author-text > span')
    youtube_comments = soup.select('yt-formatted-string#content-text')

    str_youtube_userIDs = [] 
    str_youtube_comments = [] 
    print(len(youtube_user_IDs))
    print(len(youtube_comments))

    df = None

    for i in range(len(youtube_user_IDs)):
        str_tmp = str(youtube_user_IDs[i].text)
        regex = re.compile(r'[\n\r\t]')
        str_tmp = regex.sub('', str_tmp)
        #닉네임에 앞14개, 뒤12개 공백
        str_tmp = str_tmp.replace('              ','')
        str_tmp = str_tmp.replace('            ','')
        str_youtube_userIDs.append(str_tmp) 
    
        str_tmp = str(youtube_comments[i].text) 
        regex = re.compile(r'[\n\r\t]')
        str_tmp = regex.sub('', str_tmp)
        str_tmp = str_tmp.replace('              ','')
        str_tmp = str_tmp.replace('            ','')
        str_youtube_comments.append(str_tmp)

    data_dict = {"ID":str_youtube_userIDs, "Comment":str_youtube_comments}

    df = pd.DataFrame(data_dict)
    return df

    # for i in range(len(str_youtube_userIDs)):
    #     print(str(i)+"/"+str_youtube_userIDs[i]+"/"+str_youtube_comments[i])


def crawl_urls_with_keyword(keyword):
    titles = []
    urls = []
    
    search_keyword_encode = requests.utils.quote(keyword)
    
    url = "https://www.youtube.com/results?search_query=" + search_keyword_encode
    
    driver = wd.Chrome(executable_path="chromedriver.exe")
    
    driver.get(url)
    
    total_page_height = driver.execute_script("return document.documentElement.scrollHeight")
    scroll_cnt = 0 
    while True: 
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);") 
        time.sleep(3.0)
        now_page_height = driver.execute_script("return document.documentElement.scrollHeight") 
        if now_page_height == total_page_height or scroll_cnt==10:
            break 
        scroll_cnt+=1
        total_page_height = now_page_height 
        
    html_source = driver.page_source 
    
    driver.quit()
    
    soup = BeautifulSoup(html_source, 'lxml')
    
    datas = soup.select("a#video-title")

    for data in datas:
        title = data.text.replace('\n', '')
        url = "https://www.youtube.com/" + data.get('href')
        
        titles.append(title)
        urls.append(url)
        
    for i in range(len(titles)):
        print(str(i)+"/"+titles[i]+"/"+urls[i])

    return titles, urls



if __name__ == '__main__':
    titles, urls = crawl_urls_with_keyword('딥러닝')
    df = crawl_uid_and_comments(url='https://www.youtube.com/watch?v=qPMeuL2LIqY&list=PLlMkM4tgfjnLSOjrEJN31gZATbcj_MpUm')
