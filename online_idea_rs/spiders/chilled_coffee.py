import os
import re
import datetime
import translators as ts
import scrapy
from scrapy.cmdline import execute
from fake_useragent import UserAgent
import json
from online_idea_rs.items import OnlineIdeaRsItemCoffee

ua = UserAgent()
today = datetime.datetime.today().strftime("%d_%m_%Y")
def separateNumbersAlphabets(str):
    numbers = re.findall(r'[0-9]+', str)
    alphabets = re.findall(r'[a-zA-Z]+', str)
    return {'numbers':numbers,
            'alphabets': alphabets,
            }

class ChilledCoffeeSpider(scrapy.Spider):
    name = "chilled_coffee"

    def start_requests(self):
        urls =[
            'https://online.idea.rs/v2/search?search_term=starbucks+chilled+coffee&page=1&only_tags=false&filter_category=&per_page=48&products_sort_field=relevance',
            'https://online.idea.rs/v2/search?search_term=imlek+flert+strong+coffee&page=1&only_tags=false&filter_category=&per_page=48&products_sort_field=relevance',
            'https://online.idea.rs/v2/search?search_term=hochwald+chilled+coffee&page=1&only_tags=false&filter_category=&per_page=48&products_sort_field=relevance',
            # 'https://online.idea.rs/v2/search?search_term=rauch+chilled+coffee&page=1&only_tags=false&filter_category=&per_page=48&products_sort_field=relevance',
            # 'https://online.idea.rs/v2/search?search_term=landessa+chilled+coffee&page=1&only_tags=false&filter_category=&per_page=48&products_sort_field=relevance',

        ]
        for url in urls:
            headers = {
                'Accept': 'application/json',
                'Accept-Language': 'en-US,en;q=0.9',
                'Connection': 'keep-alive',
                'Content-Type': 'application/json',
                'Referer': 'https://online.idea.rs/',
                'User-Agent': ua.random
            }
            yield scrapy.Request(url=url, headers=headers, callback=self.parse_products)

    def parse_products(self, response):

        jsn = json.loads(response.text)
        for product in jsn['products']:
            sku = product['id']
            product_name = product['name']

            file_dir = f'C:/Users/Actowiz/Desktop/pagesave/online_idea_rs/coffee/{today}'
            if not os.path.exists(file_dir):
                os.makedirs(file_dir)
            filename = fr'{file_dir}/{sku}.json'
            file = open(filename, 'w', encoding='utf8')
            file.write(response.text)
            file.close()

            quantity_digit = ''
            quantity_in = ''
            ml_flag = False
            quantity_flag = False

            for name in product_name.split(' ')[::-1]:
                contains_digit = len(re.findall('\d+', name)) > 0
                if contains_digit==True and 'l' in name and '/' not in name:
                    ml_flag = True
                    seperate_string = separateNumbersAlphabets(name)
                    quantity_in = seperate_string['alphabets'][0]
                    quantity_digit = seperate_string['numbers'][0]
                    if len(seperate_string['numbers']) > 1:
                        quantity_digit = seperate_string['numbers'][0]+'.'+seperate_string['numbers'][1]
                    if 'ml' in quantity_in.lower():
                        quantity_flag = True
                    elif 'l' in quantity_in.lower():
                        quantity_flag = True
                elif contains_digit==True:
                    break

            quantity_final = str(quantity_digit) +' '+quantity_in.lower()
            brand = ''
            if ml_flag and quantity_flag:
                if 'starbucks' in product_name.lower():
                    brand = 'Starbucks'
                # elif 'imlek' in product_name.lower() or 'flert' in product_name.lower():
                elif 'flert' in product_name.lower():
                    brand = 'Imlek'
                elif 'rauch' in product_name.lower():
                    brand = 'Rauch'
                elif 'hochwald' in product_name.lower() and 'kafa' in product_name.lower():
                    brand = 'Hochwald'
                elif 'landessa' in product_name.lower():
                    brand = 'Landessa'
                if brand:
                    product_path = product['product_path']
                    product_url = 'https://online.idea.rs/#!'+product_path
                    product_type = 'Chilled Coffee'
                    price_formatted = product['price']['formatted_price']
                    price_list = price_formatted.split(' ')
                    price = price_list[0]
                    currency = price_list[1]
                    price = price.replace(',','.')
                    mrp = price
                    country = 'Serbia'
                    item = OnlineIdeaRsItemCoffee()
                    # product_name_translated = ts.translate_text(product_name, translator='google', from_language='sr', to_language='en')
                    product_name_translated = ts.translate_text(product_name, translator='bing', from_language='sr-Latn', to_language='en')
                    product_name_translated = product_name_translated.replace('Flirting', 'Flert').replace('Flirt', 'Flert').replace('flirting', 'Flert').replace('flirt', 'Flert')
                    product_name_translated = product_name_translated.replace(brand, '')

                    item['name'] = product_name_translated
                    item['url'] = product_url
                    item['sku'] = sku
                    item['brand'] = brand
                    item['product_type'] = product_type
                    item['currency'] = currency.upper()
                    item['price'] = price
                    item['mrp'] = mrp
                    item['country'] = country
                    item['size'] = quantity_final
                    yield item

if __name__ == '__main__':
    execute('scrapy crawl chilled_coffee'.split())
