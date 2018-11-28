var div = document.getElementsByClassName("place")            // After the all the places with the coordinates are loaded into HTML,we get all the places 
                                                              // all div are assigned to a common class name place so get all elements by class name place
		var numberOfSubArrays=div.length;                         // Making X number of sublist Ex: If we have 4 places in path including source and destination,we make 4 sublist
	  var start=0,end=4,m=0;
    locations = []                                            // list which will have all sublist,Format locations [[ placeName,latitude,longitude ]]
	    for(i=0;i<numberOfSubArrays;i++)
	      locations.push([])                                     // push X number of empty sublist to locations for future use
		for(i=0;i<div.length;i++){
			for(j=0;j<div[i].children.length;j++){
				locations[i].push(div[i].children[j].innerHTML)        // append each sub list of the locations with name, latitude, longitude obtained from the HTML by doing DOM
			}
		}
    var source = locations[0][0]                              // getting source name
    var destination = locations[locations.length-1][0]        // getting destination name
    document.getElementById("select1").value = source         // setting the value
    document.getElementById("select2").value = destination    // setting the value, bcos since the route is being redirected to different page,if we dont do this
                                                              // the page where we get route ,will have nothing in the source and desination box
    var flightPlanCoordinates = []                            //flihtPlacCoordinates list which will have the longitude and latitude of each place, used for drawing line
        for (i=0;i<locations.length;i++){
          var obj = {}
          obj["lat"] = parseFloat(locations[i][1])
          obj["lng"] = parseFloat(locations[i][2])
          flightPlanCoordinates.push(obj)
        }
	    var map = new google.maps.Map(document.getElementById('map'), {    // Initialising the map
      zoom: 13,
      center: new google.maps.LatLng(locations[0][1],locations[0][2]),    // setting the start place of the route as center
      mapTypeId: google.maps.MapTypeId.ROADMAP
    });

    var infowindow = new google.maps.InfoWindow();

    var marker, i;                                                // creating marker for each location
    for (i = 0; i < locations.length; i++) {  
        marker = new google.maps.Marker({
        position: new google.maps.LatLng(locations[i][1], locations[i][2]),   // latitude and longitude for the marker
        map: map

      });
      if (locations[i][0] == source || locations[i][0] == destination )
        marker.setIcon('http://maps.google.com/mapfiles/ms/icons/green-dot.png')        // if the marker locaiton is either source or destination then set the marker colour to green
      google.maps.event.addListener(marker, 'click', (function(marker, i) {             // Event listener for marker which on clicking gives the detail about the place
        return function() {
          infowindow.setContent(locations[i][0]);                               // setting the marker content with the place name Ex: PES University
          infowindow.open(map, marker);
        }
      })(marker, i));
      
          var flightPath = new google.maps.Polyline({             // line which joins all the marker
          path: flightPlanCoordinates,  
          geodesic: true,
          strokeColor: '#FF0000',
          strokeOpacity: 1.0,
          strokeWeight: 2
        });

        flightPath.setMap(map);  
    }