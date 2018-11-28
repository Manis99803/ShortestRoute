from flask import Flask, render_template, request
import GetPath as getPath


app = Flask("__name__")

@app.route("/shortestPath")
def shortestPath():
	return render_template("ShortestRoute.html")			# Initial Page to be redirected

@app.route("/getShortestPath",methods=["POST","GET"])
def getShortestPath():
	if request.method == "POST":
		source = request.form['Source']
		destination = request.form['Destination']
	route = getPath.getRoute(source,destination)

	return render_template("ShortestRoute2.html",rows = route)	# Page to be redirected after getting the route

if __name__=="__main__":
	app.run(debug=True)
