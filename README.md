# ShortestRoute

This project is about finding an optimal path using A star algorithm.

Description about the packages and frame work used

All this pacakge should to be installed to run the program

		selenium : package which helps us in scraping the dynamic content of the webpage
		Flask : Python frame work used for building the interface
		geopy : package which gets the latitude and longitude of a given place

Folder description
		template : Folder in which all the HTML files are present ,flask looks for all the html files in the template folder

		static : Folder which has all the  external css and javascript files which are being used in the webpage, flask looks for all the external css and js file of HTML page in the static files

File description:
		Astar.py : Program which implements the astar algorithm

		GetPath.py : Program which checks for the places which are not present in the database,gets even the latitude and longitude ,does even some preprocessing stuffs.

		selenium_code.py : Program which returns the  euclidean distance heuristic. 

		ShortestRouteMain.py : Flask code which does the job connecting the backend codes with the front end codes.

		ShortestRoute.html : The html page where the user gives the input (source and desintaion)

		ShortestRoute2.html : The html pages which gives the route between the two points.

		Coordinatess.csv : File which has latiude and longitude of all the places present in the database.

		places.csv : File which has the place names of all the places which are used to build graph

		timeHeuristic.csv : File which has time required reach a particular destination .


Commands to run the program.

		python3 ShortestMainRoute.

		(This will start our local server, 
		go to the browser http://127.0.0.1:5000/shortestPath, a HTML page can be seen with two fields source and destination.
