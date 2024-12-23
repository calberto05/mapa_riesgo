function cargarPoligonos(listaPoligonos) {
  for (let i = 0; i < listaPoligonos.length; i++) {
    const poligonoData = listaPoligonos[i];
    const coordenadas = poligonoData.Feature.value.coordinates[0].map(coord => ({
      lat: coord[1], 
      lng: coord[0] 
    }));

    const poligono = new google.maps.Polygon({
      paths: coordenadas,
      strokeColor: poligonoData.Feature.value.color,
      strokeOpacity: 0.8,
      strokeWeight: 2,
      fillColor: poligonoData.Feature.value.color,
      fillOpacity: 0.35,
    });

    poligono.setMap(map); 

    // Opcional: Agregar un evento click para mostrar información del polígono
    poligono.addListener("click", function(event) {
      infoWindow.setContent(poligonoData.Feature.value.name);
      infoWindow.setPosition(event.latLng);
      infoWindow.open(map);
    });
  }
}

let map;

async function initMap() {
  const { Map } = await google.maps.importLibrary("maps");
  const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");
  const center = { lat: 19.4260393, lng: -99.1639232 };
  map = new Map(document.getElementById("map"), {
    zoom: 15,
    center,
    styles: [
      {
        featureType: "poi",
        stylers: [{ visibility: "off" }] 
      },
      {
        featureType: "transit.station",
        stylers: [{ visibility: "off" }]
      },
      {
        featureType: "road.local", // O "road.highway", "road.arterial", etc. según el tipo de calle
        elementType: "labels",
        stylers: [{ visibility: "off" }]
      }
    ]
  });
  
  const markers = []; 

  for (const key in markersData) {
    const markerInfo = markersData[key];
    const icon = {
      url: markerInfo.Reporte.value.img,
      scaledSize: new google.maps.Size(30, 30), 
      origin: new google.maps.Point(0, 0),
      anchor: new google.maps.Point(0, 0) 
    };
  
    const marker = new google.maps.Marker({
      position: { lat: markerInfo.Reporte.value.lat, lng: markerInfo.Reporte.value.lon},
      map: map,
      title: markerInfo.id,
      icon: icon 
    }); 

    markers.push(marker); // Agregar el marcador al array
  }

  cargarPoligonos(FeatureCollection); 

  map.data.setStyle((feature) => {
    return /** @type {google.maps.Data.StyleOptions} */ {
      fillColor: feature.getProperty("color"),
      strokeWeight: 1,
    };
  });

  const lineSymbol = {
    path: google.maps.SymbolPath.CIRCLE,
    scale: 4,
    strokeColor: "#393",
  };

  const lines = []; // Store the lines in an array

  velocidades.forEach((lineCoords, index) => {
      const line = new google.maps.Polyline({
          path: [
            { lat: lineCoords.Velocidad.value.lat_inicial, lng: lineCoords.Velocidad.value.lon_inicial },
            { lat: lineCoords.Velocidad.value.lat_final, lng: lineCoords.Velocidad.value.lon_final }
          ],
          icons: [{ icon: lineSymbol, offset: "0%" }],
          map: map, 
      });

      lines.push(line); // Add the line to the array
      animateCircle(line, lineCoords.Velocidad.value.velocidad); 
  });

  map.addListener("zoom_changed", () => {
    const zoom = map.getZoom();
    if (zoom) {
      // Ocultar/mostrar líneas (tu código original)
      lines.forEach(line => {
        line.setMap(zoom > 13 ? map : null); 
      });

      // Ocultar/mostrar marcadores con imágenes
      markers.forEach(marker => {
        marker.setMap(zoom > 11 ? map : null); 
      });
    }
  });
}

function animateCircle(line, velocidad) {
  let count = 0;

  window.setInterval(() => {
      count = (count + velocidad) % 100;

      const icons = line.get("icons");
      icons[0].offset = count + "%";
      line.set("icons", icons); 
  }, 20); 
} 

window.initMap = initMap;