import requests
from bs4 import BeautifulSoup
import datetime

URL1 = "https://cbr.ru/currency_base/daily/?UniDbQuery.Posted=True&UniDbQuery.To=" # ÷ена на доллар
URL2 = "https://www.lme.com/en-GB/Metals/Non-ferrous/Copper#tabIndex=0" # ÷ена на медь


def get_html(url, params = None):
	r = requests.get(url, params = params)
	return r

def parseDollar(URL, date = None): # для долларового
	link = str(URL) + str(date)
	html = get_html(link)
	if html.status_code == 200:
		print("Данные с сайта $ с курсом валют успешно получены !")
		#print(link)
		count = get_con_Dollar(html.text)

	else:
		print("Ошибка")
	return count
def parseMed(URL): # для цены на медь
	html = get_html(URL)
	if html.status_code == 200:
		print("Данные с сайта с курсом меди успешно получены !")
		#get_con(html.text)
		get_con_Med(html.text)
	else:
		print("Ошибка")



def get_con_Dollar(html): # ГОТОВ
	soup = BeautifulSoup(html, 'html.parser')
	items = soup.find_all("tr")

	temp_mass = []
	count = 0
	i = 0
	for item in items:
		cols = item.find_all("td")
		cols = [ele.text.strip() for ele in cols]
		temp_mass.append([ele for ele in cols if ele])

	while True:
		i += 1 

		if str(temp_mass[i][1]) == "USD":
			count = temp_mass[i][4]
			break
	return count


def get_con_Med(html):
	soup = BeautifulSoup(html, 'html.parser')
	items = soup.find("div", {"class":"table-wrapper", "data-arm-module":"app/widget/ScrollableTable"})
	items = items.find("table")
	items = items.find_all("tbody")
	#print(html)
	print(items)
	temp_mass = []
	for item in items:
		cols = item.find_all("td")
		cols = [ele.text.strip() for ele in cols]
		temp_mass.append([ele for ele in cols if ele])
	print(temp_mass)
	#while True:
	#	i += 1 

	#	if str(temp_mass[i][1]) == "USD":
	#		count = temp_mass[i][4]
	#		break
	#return count

date2 = str(datetime.date.today())
print(date2)
date2 = date2.replace("-",".")

parseMed(URL2)
cash_for_dollar = parseDollar(URL1, date2)
print(cash_for_dollar)


