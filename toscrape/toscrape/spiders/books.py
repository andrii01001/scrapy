import scrapy


class BooksSpider(scrapy.Spider):
    name = 'books_spider'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com']
    
    def parse(self, response):
        books = response.css('article.product_pod')
        
        for book in books:
            yield {
                'name' : book.css('h3 a::text').get(),
                'price' : book.css('.product_price .price_color::text').get(),
                #'url' : book.css('h3 a::attr(href)').get(),
            }
        
        relative_page_url = response.css('li.next a ::attr(href)').get()
        if relative_page_url is not None:
            if 'catalogue/' in relative_page_url:
                next_page_url = 'https://books.toscrape.com' + relative_page_url
            else:
                next_page_url = 'https://books.toscrape.com/catalogue/' + relative_page_url
            yield response.follow(next_page_url, callback=self.parse)