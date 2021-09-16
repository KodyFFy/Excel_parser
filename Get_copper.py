import time
import os

from selenium import webdriver

def parse_cooper():
	print("Для получения данных с сайта меди, нужно выбрать установленный браузер!")
	print("1 - Google Chrome, 2 - Mozila FireFox, 3 - Opera, Yandex - 4")
	a = int(input("Введите номер браузера(Пример: 1 и enter): "))
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
