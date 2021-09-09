import configparser as cfg
import datetime
import requests
import lxml
import time
import os

import openpyxl as xcl
from bs4 import BeautifulSoup
from selenium import webdriver

URL1 = "https://cbr.ru/currency_base/daily/?UniDbQuery.Posted=True&UniDbQuery.To=" # Цена на доллар
URL2 = "https://www.lme.com/en/Metals/Non-ferrous/LME-Copper#Trading+day+summary" # Цена на медь

def menu(URL):
	print("ПАРСЕР ЦЕНЫ НА ДОЛЛАР И НА МЕДЬ")
	
	files = os.listdir(".")
	excels = list(filter(lambda x: x.endswith(".xlsx"), files))
	excel = excels[0] 
	
	PATH = f"{os.getcwd()}\\{excel}"

	excel_file = xcl.load_workbook(PATH)

	sheets = excel_file.sheetnames[-1] # Выбрается последний (Массив страниц)
	employees_sheet = excel_file[sheets]

	row = datetime.datetime.today()
	_row = row.strftime("%d")
	
	if _row[0] == "0":
		row = _row[1] # 9 +7
	else:
		pass
	row = int(row) + 7

	date2 = str(datetime.date.today())
	date2 = date2.replace("-", ".")

	med = parse_cooper()
	dollar = parse_dollar(URL, date2)

	employees_sheet.cell(row=row-1, column=2).value = med ### Медь
	employees_sheet.cell(row=row, column=3).value = dollar ### Медь

	excel_file.save(PATH)

def get_html(url, params = None):
	r = requests.get(url, params = params)
	return r

def parse_dollar(URL, date = None):
	link = str(URL) + str(date)
	html = get_html(link)
	if html.status_code == 200:
		print("Данные с сайта $ с курсом валют успешно получены!")
		count = get_con_Dollar(html.text)
	else:
		print("Ошибка")
	return count

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

def parse_cooper():
	options = webdriver.ChromeOptions()
	options.add_argument('headless')
	options.add_argument('window-size=1920x935')
	
	binary = ["Drivers\\Chrom\\chromedriver.exe", "Drivers\\FireFox\\geckodriver.exe", "Drivers\\Opera\\operadriver.exe"]

	driver = webdriver.Chrome(executable_path=binary[0], options=options)
	print("Соединение с сайтами установленно!")
	
	try:
		driver.get("https://www.lme.com/en/Metals/Non-ferrous/LME-Copper#Trading+day+summary")
	except:
		try:
			print("Не установлен Google Chrome. Ищу другой браузер")
			driver = webdriver.Chrome(executable_path=binary[1], options=options)
		except:
			try:
				print("Не установлен FireFox. Ищу другой браузер")
				driver = webdriver.Chrome(executable_path=binary[2], options=options)
			except:
				print("Я не нашёл браузер! Завершаю программу!")
				exit(1)
	try:
		driver.implicitly_wait(7)
		time.sleep(4)
		a = driver.find_elements_by_class_name("data-set-table__table")
		temp_mass = list()
		
		for elememt in a:
			temp_mass.append(elememt.text)
		
		mass = temp_mass[0].split()
		count = mass[4]
		
		b = len(count)

		if count[-1] == "0" and count[-2] == "0":
			count = count[:b-3]
		else:
			pass
		return count

	except:
	 	print("Произошла ошибка! Данные не будут записаны!", "Перезапуск операции!")
	 	driver.close()
	 	parse_cooper()


menu(URL1)

