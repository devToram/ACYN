import requests
from bs4 import BeautifulSoup
import csv
import re

genre_id = ['101', '109', '102', '110', '103', '104', '106']

all_nvl_ids  = []

for genre in genre_id:
    naver_nvl_URL = 'https://novel.naver.com/webnovel/ranking.nhn?genre='+genre+'&periodType=DAILY#'

    naver_response = requests.get(naver_nvl_URL)

    soup = BeautifulSoup(naver_response.text,'html.parser')

    naver_nvls = soup.select('#content > div.section_ranking > div.ranking_lst > div.ranking_wrap_left > ul > li')

    for naver_nvl in naver_nvls:
        nvl_id = naver_nvl.select_one('a')['href'].split('=')[-1]
        all_nvl_ids.append(nvl_id)

all_nvl_name = []
all_nvl_intro = []
all_nvl_url = []

for nvl_ids in all_nvl_ids:
    detail_nvl_URL = 'https://novel.naver.com/webnovel/list.nhn?novelId='+nvl_ids
    detail_response = requests.get(detail_nvl_URL)
    soup = BeautifulSoup(detail_response.text, 'html.parser')

    detail_intro = soup.select_one('#content > div.section_area_info > p.dsc').text
    detail_name = soup.select_one('#content > h2').text

    all_nvl_intro.append(detail_intro)
    all_nvl_name.append(detail_name)
    all_nvl_url.append(detail_nvl_URL)


naver_novel = {}

for i in range(len(all_nvl_name)):
    naver_novel[all_nvl_name[i]] = {
        'intro' : all_nvl_intro[i],
        'url' : all_nvl_url[i]
    }
    # naver_novel[all_nvl_name[i]] = all_nvl_intro[i] 

with open('naver_novel.csv', 'w', newline='',encoding='utf-8-sig') as file:
  writer = csv.DictWriter(file, fieldnames = ['name', 'intro', 'url'])
  for key in naver_novel.keys():
      writer.writerow({'name' : key, 'intro' : naver_novel[key]['intro'], 'url' : naver_novel[key]['url']})

