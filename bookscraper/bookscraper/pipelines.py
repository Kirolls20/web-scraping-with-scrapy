# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter



class BookscraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        # Clear the values from  the list or tuples
        for key, value in adapter.items():
            if isinstance(value, tuple):
                adapter[key] = value[0] if value else None

        # Lowercase the booktype
        for key,value in adapter.items():
            if  key == 'book_type':
                adapter[key] = value.lower()
        # Convert the price from str to float
        for key ,value in adapter.items():
            if key == 'price':
                adapter[key] = float(value)
                
        # Convert the str of Number of reviews to int         
        for key,value in adapter.items():
            if key == 'number_of_reviews':
                adapter[key] = int(value)

        # Clean up the Availability Data
        for key, value in adapter.items():
            if key == 'availability':
                cleaned_val = value.split(' ')
                adapter[key] = int(cleaned_val[2][1:])

        return item

import mysql.connector
class SaveToMysqlPipline:
    def __init__(self):
        # try:
        self.conn = mysql.connector.connect(
            host= 'localhost',
            user= 'root',
            password='Password here',
            database = 'books',
            auth_plugin='caching_sha2_password'
        )
        # except Exception as e:
        #     print('Error*************',e)
        self.cur = self.conn.cursor()
        # Create Books Table if NOT exists
        self.cur.execute("""
    CREATE TABLE IF NOT EXISTS books(
        id INT NOT NULL AUTO_INCREMENT,
        title TEXT,
        book_type TEXT,
        image_url VARCHAR(255),
        stars VARCHAR(128),
        price DECIMAL,
        description TEXT,
        availability INT,
        number_of_reviews INT,
        PRIMARY KEY (id)
    );
""")
        
    def process_item(self, item, spider):
        self.cur.execute("""
            INSERT INTO books (
                title,
                book_type,
                image_url,
                stars,
                price,
                description,
                availability,
                number_of_reviews  -- Remove the extra comma here
            ) VALUES (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            )
        """, (
            item['title'],
            item['book_type'],
            item['image_url'],
            item['stars'],
            item['price'],
            item['description'],
            item['availability'],
            item['number_of_reviews']
        ))
        self.conn.commit()
        return item

    def close_spider(self,spider):
        self.cur.close()
        self.conn.close()