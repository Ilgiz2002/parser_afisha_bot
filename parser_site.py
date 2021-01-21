import requests
import bs4


class Parser:

    def __init__(self, url):
        self.URL = url
        self.HOST = 'https://www.afisha.uz'
        self.HEADERS = {
            'accept': 'text/html',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
        }

    def get_html(self, url):
        try:
            response = requests.get(url, headers=self.HEADERS)
            # response.encoding('utf-8')
            response.raise_for_status()
        except requests.HTTPError:
            print(f'Ошибка {response.status_code}')

        return response

    def get_content(self, html):
        soup = bs4.BeautifulSoup(html, 'html.parser')
        cards = []
        for elm in soup.select('table', class_='when-list'):
            if "passed" in elm["class"]:
                continue
            cards.append(elm)

        content = []

        for item in cards:
            card_news = item.find_all('div', class_='item2')
            card_imgs = item.find_all('div', class_='fl')

            for j in range(0, len(card_news)):
                content.append({
                    'title': card_news[j].find('h3').get_text(strip=True),
                    'content': card_news[j].find('p', 'desc').get_text(
                        strip=True),
                    'date': item.find('td', class_='whenblock').find('p',
                                                                     class_='w-num').get_text(
                        strip=True) + ' ' + item.find('td',
                                                      class_='whenblock').find(
                        'p', class_='w-month').get_text(strip=True),
                    'week_day': item.find('td', class_='whenblock').find('p',
                                                                         class_='w-day').get_text(
                        strip=True),
                    'place': card_news[j].find('p', 'place').get_text(
                        strip=True),
                    'url': self.HOST + card_news[j].find('h3').find(
                        'a').get('href'),
                    # 'img': card_imgs[j].find('img').get('src'),
                })
        return content

    def run(self):
        html = self.get_html(self.URL).content.decode('utf-8')
        content = self.get_content(html)

        return content


znaniya = Parser(url='https://www.afisha.uz/znaniya/')
content = znaniya.run()
