from selenium import webdriver
import time
import csv
import os

def getHeuristic(Destination):
	browser = webdriver.Firefox()

	# get the places names from the file
	inp_path = "/home/manish/Manish/Documents/5th_Sem/AI/AI_Project/ai_project/places.csv"
	places_list = []
	heuristicList = []
	with open(inp_path,"r") as ip:
		try:
			for row in ip:
				place = csv.reader(ip, delimiter = ",")
				
				for i in place:
					places_list.append(i[0])
		except:
			print("cant open")	
	ip.close()
		
	for i in places_list:
					browser.get('https://www.mapdevelopers.com/distance_from_to.php')
					time.sleep(3)
					source =  browser.find_element_by_id("fromInput")
					source.send_keys(i)
					dest = browser.find_element_by_id("toInput")
					dest.send_keys(Destination)
					btn =  browser.find_element_by_xpath("//*[contains(text(), 'Calculate Distance')]")
					btn.click()
					time.sleep(1)

					try:
						# get the heuristic distance
						h_n = browser.execute_script("return document.getElementById('status').innerHTML")
						h_n = h_n.split(",")[1]
						h_n = h_n.split(" ")[1]


					except:
						# if doesn't work set distance to zero
						heuristicList.append([i, Destination,0])

					heuristicList.append([i, Destination, h_n])
	return heuristicList


