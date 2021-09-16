import requests
import lxml
from bs4 import BeautifulSoup


def get_html(url, params=None):
	r = requests.get(url, params = params)
	return r

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

def parse_dollar(URL, date=None):
	link = str(URL) + str(date)
	html = get_html(link)
	if html.status_code == 200:
		print("Данные с сайта $ с курсом валют успешно получены!")
		count = get_con_Dollar(html.text)
	else:
		print("Ошибка")
	return count