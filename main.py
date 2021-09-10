import configparser as cfg
import datetime
import time
import sys
import os

import requests
import lxml
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

	row = _row
	row = int(row) + 7

	date2 = datetime.date.today()
	date2 = date2 + datetime.timedelta(days = 1)
	date2 = str(date2)
	date2 = date2.replace("-", ".")	
	
	med = parse_cooper()
	dollar = parse_dollar(URL, date2)
	dollar = dollar.replace(",",".")	
	med = med.replace(",",".")
	
	employees_sheet.cell(row=row - 1, column=2).value = med ### Медь
	employees_sheet.cell(row=row, column=3).value = dollar ### Медь

	excel_file.save(PATH)

def get_html(url, params=None):
	r = requests.get(url, params = params)
	return r

def parse_dollar(URL, date=None):
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
	print("Для получения данных с сайта меди, нужно выбрать установленный браузер!")
	print("1 - Google Chrome, 2 - Mozila FireFox, 3 - Opera, Yandex - 4")
	a = int(input("Введите номер браузера(Пример: 1 и enter)"))
	binary = ["Drivers\\Chrom\\chromedriver.exe", "Drivers\\FireFox\\geckodriver.exe", "Drivers\\Opera\\operadriver.exe","Drivers\\Yandex\\yandexdriver.exe"]
	if a == 1:
		binar = binary[0]
		try:
			driver = webdriver.Chrome(executable_path=binar, options=options)	
			driver.get("https://www.lme.com/en/Metals/Non-ferrous/LME-Copper#Trading+day+summary")
			print("Браузер Chrome успешно найден. Устанавливаю соединение...")
			print("Соединение с сайтом установлено успешно!")
		except:
			print("Браузер не найден или что-то пошло не так :(")
	elif a == 2:
		binar = binary[1]
		try:
			options = webdriver.FirefoxOptions()
			options.add_argument('headless')
			driver = webdriver.Firefox(executable_path=binar, options=options)	
			driver.get("https://www.lme.com/en/Metals/Non-ferrous/LME-Copper#Trading+day+summary")
			print("Браузер Firefox успешно найден. Устанавливаю соединение...")
			print("Соединение с сайтом установлено успешно!")
		except:
			print("Браузер не найден или что-то пошло не так :(")        
	elif a == 3:
		binar = binary[2]
		try:
			options = webdriver.Opera()
			options.add_argument('headless')
			driver = webdriver.Opera(executable_path=binar, options=options)	
			driver.get("https://www.lme.com/en/Metals/Non-ferrous/LME-Copper#Trading+day+summary")
			print("Браузер Opera успешно найден. Устанавливаю соединение...")
			print("Соединение с сайтом установлено успешно!")
		except:
			print("Браузер не найден или что-то пошло не так :(")     
	elif a == 4:
		binar = binary[3]
		try:
			options = webdriver.ChromeOptions()
			options.add_argument('headless')
			driver = webdriver.Opera(executable_path=binar, options=options)	
			driver.get("https://www.lme.com/en/Metals/Non-ferrous/LME-Copper#Trading+day+summary")
			print("Браузер Yandex успешно найден. Устанавливаю соединение...")
			print("Соединение с сайтом установлено успешно!")
		except:
			print("Браузер не найден или что-то пошло не так :(")     			
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
			count = count[:b - 3]
		else:
			pass
		return count

	except:
	 	print("Произошла ошибка! Данные не будут записаны!", "Перезапуск операции!")
	 	driver.close()
	 	parse_cooper()


menu(URL1)

