#!/usr/bin/python

import requests

from bs4 import python.ini

BASE_URL = 'http://10.0.5.208/prpall'
BASE_SUB_URL = '{kind}/tbcbpg/UIPrPoEn{kind}Show.jsp?BIZTYPE=POLICY&BizNo=110{region}{kind}{year}{number}YD&SHOWTYPE=SHOW&RiskCode={kind}'

KINDS = ["0507", "0508"]                          #险种
REGIONS = ["01", "02", "03"]
YEARS = ["2015", "2016"]
NUMBERS = range(1, 999999)
PAGE_404 = 'Sorry! No Products found'


def soup_factory(content):
	return BeautifulSoup(content, 'html.parser')


def extract_content(value):
	if not value:
		return ''
	else:
		return value[0]


def extract_sku(soup):
	section = soup.find('section', { 'class' : 'detail-bread-crumb' })
	items = section.findAll('li')

	for item in items:
		if item.get('itemprop') and item.get('itemprop') == 'sku':
			return extract_content(item.contents)


def extrac_details(soup):
	details_list = soup\
				.find('section', {'class' : 'detail-bot-product-details-content'})\
				.find('ul')\
				.findAll('li')

	details = []
	for item in details_list:
		details.append(extract_content(item.contents).strip())

	return details


def extract_images(soup):
	images_carousel = soup.find('ul', { 'id' : 'mycarousel5' })
	images_html = images_carousel.findAll('a')

	images = []
	for image in images_html:
		if extract_content(image.get('rev')):
			image_url = BASE_URL + extract_content(image.get('rev'))
			images.append(image_url)

	return images


def extract_prices(soup):

	divs_prices = soup.findAll('div', { 'class' : 'fullcolordetails' })

	final_prices = []
	categories_prices = []

	for div in divs_prices:

		table_prices = div.findAll('table')[3]
		rows = table_prices.findAll('tr')

		#qtys
		row = rows[0]
		tds = row.findAll('td')
		qtys = []
		for td in tds:
			qtys.append(extract_content(td.contents))

		#categories prices
		for i in xrange(1, len(rows)):
			row = rows[i]
			tds = row.findAll('td')
			category_prices = []
			for td in tds:
				category_prices.append(extract_content(td.contents))

			categories_prices.append(category_prices)

		for i in xrange(0, len(categories_prices)):
			category = categories_prices[i]
			for j in xrange(0, len(qtys)):
				final_prices.append( { 'qty' : qtys[j], 'price' : category[j] } )

	return final_prices


def process_product(url = ''):

	if not url:
		return

	response = requests.get(url)
	soup = soup_factory(response.content)

	title = extract_content(soup.find('h1').contents)
	sku = extract_sku(soup)
	details = extrac_details(soup)
	images = extract_images(soup)
	prices = extract_prices(soup)

	return { 'title' : title, 'sku' : sku, 'details' : details, 'prices' : prices, 'images' : images }

	'''import ipdb
	ipdb.set_trace()'''


def create_csv_item(product, category):

	max_details = 10
	max_images = 50

	item = product.get('title', '').encode('utf-8') + '; '
	item += product.get('sku', '') + '; '
	item += category + '; '

	for detail in product.get('details'):
		item += detail + '; '
	for i in xrange(len(product.get('details')), max_details):
		item +=  ' ; '

	for image in product.get('images'):
		item += image + '; '
	for i in xrange(len(product.get('images')), max_images):
		item +=  ' ; '

	for price in product.get('prices'):
		print price.get('qty').encode('utf-8').strip()
		item += price.get('qty').encode('utf-8').strip() + ' = ' + price.get('price') + ';'



	output_file = open("Output.csv", "w")

	output_file.write(item)

	output_file.close()


	# import ipdb
	# ipdb.set_trace()
	# rows = max(len(product.get('details'), product.get('')))
	# print rows
	pass


def process():

    flag = 0
    count = 100
	for kind in range KINDS:
        for region in range REGIONS:
            for year in range YEARS:
                for number in range NUMBERS:
                    if count > 100:
                        return

                    url = BASE_URL + BASE_CATEGORY.replace("{kind}", kind).replace("{region}", region).replace("{year}", year).replace("{number}", str(number).zfill(6))
                    print url
                    response = requests.get(url)
                	if PAGE_404 in response.content:
                        flag += 1
                		break
                    else:
                        flag = 0

                		soup = soup_factory(response.content)
                		print soup
                        time.sleep(1000)
                    count++
                if count > 0:
                    break
            if count > 1:
                break
        if count > 2:
            break


if __name__ == '__main__':

	process()
