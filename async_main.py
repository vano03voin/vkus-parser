import requests
import lxml
from bs4 import BeautifulSoup
import aiohttp
import asyncio

async def collect_data():
    items=[]
    link='https://vkusvill.ru/cart/'
    cookies={'Your cocies': 'here'}

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'User-Agent': 'mozilla/5.0 (macintosh; intel mac os x 10_9_2) applewebkit/537.36 (khtml, like gecko) chrome/34.0.1847.131 safari/537.36'}
    async with aiohttp.ClientSession() as session:
        response = requests.get(link, headers=headers, cookies=cookies)
        data=response.text
        soup=BeautifulSoup(data,'lxml')
        try:
            a=soup.find('div',class_='OrderFormProdSliderSwiperWrapper swiper-wrapper js-order-form-green-labels js-log-place js-datalayer-catalog-list').find_all('div',class_='Slider__itemInner')
            for i in a:
                card=i.find('img',class_='ProductCard__imageImg lazyload')
                items.append(str(card.get("title").replace(',',' ').replace('   ',' ').strip()))#name
                items.append(str(card.get("data-src")))#link
        except AttributeError:
            print('красных товаров нет')
        return(items)
            
async def main():
    await collect_data()

if __name__ == '__main__':
    asyncio.run(main())

