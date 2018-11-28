from geopy.geocoders import Nominatim
import csv
import math
import Astar as getPath

geolocator = Nominatim(user_agent="Project")
# Format placeCoordinates = { placeName:{ lat:0 , lng:0 } }
placeCoordinates = {}
# Foramt shortestRoute = { placeName : ( lat:0,lng:0 ) }
shortestRoute = {}
# Format Ex: modfiedSourceName = "PES-University Bengaluru" 
modifiedSourceName = ''
modifiedDestinationName = ''

# Function which will read the coordinate file and get all the cooridnates of place present in our database
def preProcessing():
	filePointer = open("Coordinates.csv","r")
	reader = csv.reader(filePointer)
	next(reader)
	for  i in reader:
		placeCoordinates[i[0]] = {"lat":i[1],"lng":i[2]}


# Function which checks the wheter the source and destination are present in the database or no
def checkPlaces(source,destination):
	sourceCheck = -1								# Initial assumption -1 not present
	destinationCheck = -1
	for key in list(placeCoordinates.keys()):
		if key == source:
			sourceCheck = 1							# If present update the flag
		if key == destination:
			destinationCheck = 1
	finalReturnValue =[[source,sourceCheck],[destination,destinationCheck]]
	return finalReturnValue

# Function which returns the coordinates of any given place
def getCordinates(placeName):
	location = geolocator.geocode(placeName,timeout = 15)
	return (location.latitude,location.longitude)


# Function which will return nearest place to some unknown place given from our database by comparing the euclidian distance with all the coordinates 
# present in the database
# Ex: Majestic is not present in our data base so get the nearest place to majestic in our database
# Format : nearestPlaceList = [[ actualPlaceGiven,nearestPlace ]] 
# Takes variable number of argument cos we might get one or two arguments depending on the source and destination
def getNearestPlaceNames(*argv):
	nearestPlaceList = []
	for i in range(len(argv)):
		nearestPlaceList.append([])
		minimumDistance = 100000000000000000					# Initial minimum distance
		currentPlaceCoordinate = getCordinates(argv[i])			# getting the coordinates of the given place
		for key,value in placeCoordinates.items():				# getting all the coordinates of places present in our database
			if (key != modifiedSourceName) and (key != modifiedDestinationName):
				# computing the euclidean distance
				computeDistance = math.sqrt((float(placeCoordinates[key]["lat"]) - float(currentPlaceCoordinate[0])) ** 2 + (float(placeCoordinates[key]["lng"]) - float(currentPlaceCoordinate[1])) ** 2) 
			if computeDistance < minimumDistance:		# if computed distanace minimum compared to the previous distance update the value
					minimumDistance = computeDistance
					nearestPlaceList[i] = [] 
					nearestPlaceList[i].extend([argv[i],key])
	return nearestPlaceList


# Function which checks for all the combination of source and destination
def checkNearestPlace(checkPlacesReturn):
	finalPlaceList = []											
	if checkPlacesReturn[0][1] == -1 and checkPlacesReturn[1][1] == -1:					# If both source and destination are not present in the database
		finalPlaceList =  getNearestPlaceNames(checkPlacesReturn[0][0],checkPlacesReturn[1][0])
	elif checkPlacesReturn[0][1] == -1:													# Only source not present
		finalPlaceList =  getNearestPlaceNames(checkPlacesReturn[0][0])
	elif checkPlacesReturn[1][1] == -1:													# Only desination not present
		finalPlaceList =  getNearestPlaceNames(checkPlacesReturn[1][0])
	return finalPlaceList

# Function which retrun the coordinates of the places in our shortest route
def getRouteCordinates(routeList):
	shortestRoute = {}
	for i in routeList:	
		if i in placeCoordinates:			# If place name is present in our database get the cooridnates directly from the database[placeCoordinates]
			temp = i.split(" ")[0]			# Split is being performed here because ,the place name is in the format PES-University Bengaluru, we just remove the Bengaluru part,and make that as a key	
			shortestRoute[temp] = {}
			shortestRoute[temp] = (placeCoordinates[i]["lat"],placeCoordinates[i]["lng"])
		else:
			temp = i.split(" ")[0]			# If place name not present get the coordinates from the geocoders
			location = geolocator.geocode(i,timeout = 15)
			shortestRoute[temp] = {}
			shortestRoute[temp] = (location.latitude,location.longitude)
	return shortestRoute


# Function which is called by the flask code
def getRoute(source,destination):

	preProcessing()
	source = source.split(" ")								
	destination = destination.split(" ")	
	if len(source) > 1:														# If list has more than one name after splitting,PES University will split as "PES","University"
		modifiedSourceName = ""
		for i in source:
			modifiedSourceName += i+"-"										#Replacing every space with "-" Ex: PES University = PES-University
		modifiedSourceName = modifiedSourceName.rstrip("-")
		modifiedSourceName += " Bengaluru"									#Suffixing the Place name with Bengaluru so that coordinates which we get are of Bengaluru only.
	else:
		modifiedSourceName = source[0]+" Bengaluru"							#If no spaces in the names ,Ex : Majestic will split as Majestic only,since we are appyling
																			# split operation source will become a list source = ["Majestic"] so we take source[0]					

	if len(destination) > 1:
		modifiedDestinationName = ""
		for i in destination:
			modifiedDestinationName += i+"-"
		modifiedDestinationName = modifiedDestinationName.rstrip("-")
		modifiedDestinationName += " Bengaluru"
	else:
		modifiedDestinationName = destination[0]+" Bengaluru"
	
	finalPath = []

	checkPlacesReturn = checkPlaces(modifiedSourceName,modifiedDestinationName)			#Function to check if the source and destination are present in our database
	#checkPlacesReturn will be a list which will have two sublist
	#Format : checkPlacesReturn = [[source,1],[destination,1]] ,If the names are present in the database we return [name,1] and if not [name,-1]

	if checkPlacesReturn[0][1] == 1 and checkPlacesReturn[1][1] == 1:					# Checking if both are 1 then we can directly go and get the shortest Path
		finalPath = getPath.shortestPath(modifiedSourceName,modifiedDestinationName)
		return getRouteCordinates(finalPath)	
	finalList = checkNearestPlace(checkPlacesReturn)								# If either of the name is not present we get nearest place
	# print(finalList)
	if len(finalList) > 0:
		if checkPlacesReturn[0][1] == -1 and checkPlacesReturn[1][1] == -1:			# If both source and destinatio are not present 
			finalPath = getPath.shortestPath(finalList[0][1],finalList[1][1])		# Take the nearest place get the path between them
			finalPath.insert(0,finalList[0][0])										# After getting path put source in the front of list ,put desination at the end of list
			finalPath.insert(len(finalPath),finalList[1][0])
		elif checkPlacesReturn[0][1] == -1:												# If only source in not present
			finalPath = getPath.shortestPath(finalList[0][1],modifiedDestinationName)	# Take the nearest place get the path between
			finalPath.insert(0,finalList[0][0])											# After getting the path put source ini the front of list				
		else:
			finalPath = getPath.shortestPath(modifiedSourceName,finalList[0][1])
			finalPath.insert(len(finalPath),finalList[0][0])
	
	#finalPath will have the shortestroute and all the coordinates of intermediate nodes
	return getRouteCordinates(finalPath)				
	





