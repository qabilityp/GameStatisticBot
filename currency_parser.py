import asyncio
import aiohttp
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

url = 'https://minfin.com.ua/currency/'
headers = {'User-Agent': UserAgent().random}

async def average_usd_rate():
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url, headers=headers) as response:
            text = await response.text()
            with open("page.html", "w", encoding="utf-8") as f:
                f.write(text)

            soup = BeautifulSoup(text, 'html.parser')
            items = soup.find_all('tr', {'class':'sc-1x32wa2-4 dKDsVV'})

            for item in items:
                td = item.find_all('div', {'class':'sc-1x32wa2-9 bKmKjX'})
                td_usd = item.find('td', {'class':'sc-1x32wa2-6 bIIiwq', 'type': 'average'})

                if td_usd and 'USD' in td_usd.text:
                    buy = td[0].text.split()[0]
                    sell = td[1].text.split()[0]
                    nbu = td[2].text.split()[0]

            return f"USD 💵\nПокупка: {buy}\nПродажа: {sell}\nНБУ: {nbu}"


if __name__ == '__main__':
    asyncio.run(average_usd_rate())