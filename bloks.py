#import datetime
import requests
import lxml
from bs4 import BeautifulSoup
#from fake_useragent import UserAgent
import aiohttp
import asyncio




def zapiz(how,teg,row):
    with open(f'benzocos{teg}.csv',how, encoding = 'utf-8' ,newline = '') as file:
        writer=csv.writer(file,delimiter='\t')
        writer.writerow(row)

def getddata(link):
    global cookies
    #ua = UserAgent()
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'User-Agent': 'mozilla/5.0 (macintosh; intel mac os x 10_9_2) applewebkit/537.36 (khtml, like gecko) chrome/34.0.1847.131 safari/537.36'}
    async with aiohttp.ClientSession() as session:
        response = requests.get(link, headers=headers, cookies=cookies)
    return(response.text)

async def collect_data():
    items=[]
    link='https://vkusvill.ru/cart/'
    cookies = {'Your cocies': 'here'}
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'User-Agent': 'mozilla/5.0 (macintosh; intel mac os x 10_9_2) applewebkit/537.36 (khtml, like gecko) chrome/34.0.1847.131 safari/537.36'}
    async with aiohttp.ClientSession() as session:
        response = requests.get(link, headers=headers, cookies=cookies)
        data=response.text
        soup=BeautifulSoup(data,'lxml')
        #print(data)
        try:
            a=soup.find('div',class_='OrderFormProdSliderSwiperWrapper swiper-wrapper js-order-form-green-labels js-log-place js-datalayer-catalog-list').find_all('div',class_='Slider__itemInner')
            #print(a)
            #OrderFormProdSliderSwiper swiper-container js-order-form-vv-recoms-slider swiper-container-initialized swiper-container-horizontal swiper-container-pointer-events swiper-container-free-mode
            for i in a:
                #print(i)
                card=i.find('img',class_='ProductCard__imageImg lazyload')
                name=str(card.get("title").replace(',',' ').strip())+'\t'+str(card.get("data-src"))
                #print(name)
                items.append(name)          
        except AttributeError:
            print('красных товаров нет')
            return([])
        #print(items)
        return(items)

async def main():
    cookies={'Your cocies': 'here'}
    await collect_data()
    
if __name__ == '__main__':
    asyncio.run(main())
