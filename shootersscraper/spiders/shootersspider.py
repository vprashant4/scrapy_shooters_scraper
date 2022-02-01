import scrapy

class ShootersSpider(scrapy.Spider):

	#name of the spider
	name = "shooters"

	#lookup urls 
	def start_requests(self):
		urls = [
				'https://www.midsouthshooterssupply.com/dept/reloading/primers?currentpage=1',
		]
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	#this parse fuction will use upper link to scrap data from them use css selector	
	def parse(self, response):
		for products in response.css('div.product'):
			try:
				yield {
					'price': float(products.css('span.price span::text').get().replace('$', '')),
					'title': products.css('a.catalog-item-name::text').get(),
					'stock': False, #products.css('span.out-of-stock::text').get(),
					'maftr': products.css('a.catalog-item-brand::text').get(),

				}
			except:
				yield {
					'price': float(products.css('span.price span::text').get().replace('$', '')),
					'title': products.css('a.catalog-item-name::text').get(),
					'stock': True, #products.css('span.out-of-stock::text').get(),
					'maftr': products.css('a.catalog-item-brand::text').get(),

				}

		#this next page variable will find the next page link when the next 
		#page is available then call the parse function to extract the page information until reached the end.
		next_page = response.css('div.pagination a::attr(href)').get()
		#current = 'https://www.midsouthshooterssupply.com' + next_page
		if next_page is not None:
			yield response.follow(next_page, callback=self.parse)
		

