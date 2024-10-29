async function initMap() {
  const { Map } = await google.maps.importLibrary("maps");
  const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");
  const center = { lat: 19.4260393, lng: -99.1639232 };
  const map = new Map(document.getElementById("map"), {
    zoom: 15,
    center
  });
  
  const markers = []; 

  for (const key in markersData) {
    const markerInfo = markersData[key];
    const icon = {
      url: markerInfo.imagen,
      scaledSize: new google.maps.Size(30, 30), 
      origin: new google.maps.Point(0, 0),
      anchor: new google.maps.Point(0, 0) 
    };
  
    const marker = new google.maps.Marker({
      position: { lat: markerInfo.lat, lng: markerInfo.lng },
      map: map,
      title: markerInfo.title,
      icon: icon 
    }); 

    markers.push(marker); // Agregar el marcador al array
  }

  map.data.addGeoJson(FeatureCollection);

  map.data.setStyle((feature) => {
    return /** @type {google.maps.Data.StyleOptions} */ {
      fillColor: feature.getProperty("color"),
      strokeWeight: 1,
    };
  });

  for (const property of properties) {
    const AdvancedMarkerElement = new google.maps.marker.AdvancedMarkerElement({
      map,
      content: buildContent(property),
      position: property.position,
      title: property.description,
    });

    AdvancedMarkerElement.addListener("click", () => {
      toggleHighlight(AdvancedMarkerElement, property);
    });
  }

  const lineSymbol = {
    path: google.maps.SymbolPath.CIRCLE,
    scale: 4,
    strokeColor: "#393",
  };

  const lines = []; // Store the lines in an array

  coords.forEach((lineCoords, index) => {
      const line = new google.maps.Polyline({
          path: lineCoords,
          icons: [{ icon: lineSymbol, offset: "0%" }],
          map: map, 
      });

      lines.push(line); // Add the line to the array
      animateCircle(line, velocidades[index]); 
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

function toggleHighlight(markerView, property) {
  if (markerView.content.classList.contains("highlight")) {
    markerView.content.classList.remove("highlight");
    markerView.zIndex = null;
  } else {
    markerView.content.classList.add("highlight");
    markerView.zIndex = 1;
  }
}

function buildContent(property) {
  const content = document.createElement("div");

  content.classList.add("property");
  content.innerHTML = `
    <div class="camaras">
      <div class="icon">
        <i aria-hidden="true" class="fa fa-icon fa-${property.type}" title="${property.type}"></i>
        <span class="fa-sr-only">${property.type}</span>
      </div>
      <div class="details">
        <iframe src=${property.url} width="400px" height = "250px" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
      </div>
    </div>
    `;
  return content;
}

const properties = [
  {
    address: "Camara Calle Madero",
    type: "video",
    url: "https://www.youtube.com/embed/2pd8Ah7teLg?si=54bxm7A5xW3SF2Pp",
    position: {
      lat: 19.433616,
      lng: -99.1372766,
    },
  },
];

window.initMap = initMap;

