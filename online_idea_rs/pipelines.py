# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from online_idea_rs.items import OnlineIdeaRsItemCoffee
from online_idea_rs.db_config import DbConfig

obj = DbConfig()


class OnlineIdeaRsPipeline:
    def process_item(self, item, spider):
        if isinstance(item, OnlineIdeaRsItemCoffee):
            qr = f'''
            insert into {obj.data_table}(name, url, sku, brand, product_type, currency, price, mrp, country, size)
            values(
            "{item['name']}",
            "{item['url']}",
            "{item['sku']}",
            "{item['brand']}",
            "{item['product_type']}",
            "{item['currency']}",
            "{item['price']}",
            "{item['mrp']}",
            "{item['country']}",
            "{item['size']}"
            )
            '''
            try:
                obj.cur.execute(qr)
                obj.con.commit()
            except Exception as e:print(e)
        return item
