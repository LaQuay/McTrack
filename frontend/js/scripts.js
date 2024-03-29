var mymap;

function loadMap() {
  mymap = L.map('map').setView([50.074875, 14.437353], 14);

  L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
    maxZoom: 18,
    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, ' +
      '<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
      'Imagery © <a href="http://mapbox.com">Mapbox</a>',
    id: 'mapbox.streets'
  }).addTo(mymap);

  /*L.marker([51.5, -0.09]).addTo(mymap)
    .bindPopup("<b>Hello world!</b><br />I am a popup.").openPopup();

  L.circle([51.508, -0.11], 500, {
    color: 'red',
    fillColor: '#f03',
    fillOpacity: 0.5
  }).addTo(mymap).bindPopup("I am a circle.");

  L.polygon([
    [51.509, -0.08],
    [51.503, -0.06],
    [51.51, -0.047]
  ]).addTo(mymap).bindPopup("I am a polygon.");
  */
  var popup = L.popup();

  function onMapClick(e) {
    popup
      .setLatLng(e.latlng)
      .setContent("You clicked the map at " + e.latlng.toString())
      .openOn(mymap);
  }

  mymap.on('click', onMapClick);
}

function updateMarkers() {
  setInterval(function(){callUpdateMarkers()}, 5000);
  callUpdateMarkers();
}

function callUpdateMarkers() {
  var URL_UPDATE_MARKERS = "https://mctrack-6a99b.firebaseio.com/customers.json?auth=XyGsxNV6kJdDSh4PxPKApPpwi6n051YqVao4uLfV";
  var request = new XMLHttpRequest();
  request.onreadystatechange = function() {
    if (request.readyState === 4) {
      if (request.status === 200) {
        document.body.className = 'ok';
        drawMarkers(request.responseText);
      } else {
        document.body.className = 'error';
        console.log('dep');
      }
    }
  };
  request.open("GET", URL_UPDATE_MARKERS, true);
  request.send(null);
}

function drawMarkers(response) {
  //console.log(response);
  //TODO for each marker
  var responseJson = JSON.parse(response);
  console.log(responseJson);
  for (key in responseJson) {
    //console.log(responseJson[key]);
    for (probes in responseJson[key]['probes']) {
      console.log(responseJson[key]['probes'][probes]['location']);

      var userID = key;
      var locationNames = ["Cartier", "Bikes"]; //TODO
      var locationTypes = ["Establishment", "Sport"];

      var stringToPrint = "<b>" + userID + "</b><br /><br />";

      var index;
      for (index = 0; index < locationNames.length; index++) {
        stringToPrint += locationNames[index] + ", " + locationTypes[index];
        stringToPrint += "<br />";
      }

      L.marker([responseJson[key]['probes'][probes]['location'].lat,  responseJson[key]['probes'][probes]['location'].lng]).addTo(mymap)
        .bindPopup(stringToPrint);
    }
  }
}
