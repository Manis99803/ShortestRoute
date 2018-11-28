from geopy.geocoders import Nominatim
import csv

filePointer = open("Coordinates.csv","w")
writer = csv.writer(filePointer)
writer.writerow(["Place Name","Latitude","Longiute"])
geolocator = Nominatim(user_agent="Project")
places = ["Madiwala Bengaluru",
"Banashankari Bengaluru",
"JP-Nagar Bengaluru",
"BTM-Layouts Bengaluru",
"Jayanagar Bengaluru",
"Kathriguppe Bengaluru",
"Basavangudi Bengaluru",
"Hosakerahalli Bengaluru",
"Koramangala Bengaluru",
"Chamrajpet Bengaluru",
"Attiguppe Bengaluru",
"Girinagar Bengaluru",
"Lakkasandra Bengaluru",
"Deepanjali-Nagar Bengaluru",
"PES-University Bengaluru",
"MG-Road Bengaluru"]

coordinates = {}
for i in places:
	coordinates[i] = {}
	location = geolocator.geocode(i,timeout = 15)	
	print(location)
	try:
		coordinates[i]= (location.latitude,location.longitude)
	except:
		continue
for key,value in coordinates.items():
	try:
		writer.writerow([key,coordinates[key][0],coordinates[key][1]])
	except:
		writer.writerow([key,12.9166, 77.6101])
