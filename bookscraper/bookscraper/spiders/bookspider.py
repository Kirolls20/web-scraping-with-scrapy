
import scrapy
from bookscraper.items import BookItem

class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    custom_settings = {
        'FEEDS':{
            'booksdata.json':{'format':'json','overwrite':True}
        }
    }
    def parse(self, response):
        books = response.css('article.product_pod')
        for book in books:
            relative_url  = book.css('h3 a::attr(href)').get()
            if relative_url is not None:
                if 'catalogue/' in relative_url:
                    book_url = 'https://books.toscrape.com/' + relative_url
                else: 
                    book_url = 'https://books.toscrape.com/catalogue/' + relative_url
                yield response.follow(book_url,callback= self.parse_book)

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            if 'catalogue/' in next_page:
                next_page_url = 'https://books.toscrape.com/' + next_page
            else:
                next_page_url = 'https://books.toscrape.com/catalogue/' + next_page
            yield response.follow(next_page_url,callback = self.parse)

    def parse_book(self,response):
        title = response.css('.product_main h1::text').get()
        kind = response.xpath("//ul[@class='breadcrumb']/li[@class='active']/preceding-sibling::li[1]/a/text()").get()
        table_rows= response.css('table tr')
        stars = response.css('p.star-rating').attrib['class'][12:]
        description = response.xpath("//div[@id='product_description']/following-sibling::p/text()").get()
        img_element = response.css('.item img')
        src = img_element.css('::attr(src)').get()
        correct_img_path = src.replace('../../','https://books.toscrape.com/')

        book_items =BookItem()
        book_items['title'] = title,
        book_items['book_type']= kind,
        book_items['image_url'] = correct_img_path,
        book_items['stars'] = stars,
        book_items['price'] = response.css('.price_color::text').get()[1:]
        book_items['description'] = description,
        book_items['Availability'] = table_rows[5].css('td::text').get(),
        book_items['number_of_reviews'] = table_rows[6].css('td::text').get(),

        yield book_items
        

