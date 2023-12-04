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
            if key == 'Availability':
                cleaned_val = value.split(' ')
                adapter[key] = int(cleaned_val[2][1:])

        return item


