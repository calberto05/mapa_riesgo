const coords = {{ coords | tojson }};  // Convertir coordenadas a JSON válido
const velocidades = {{ velocidades | tojson }};  // Convertir velocidades a JSON válido

function initMap() {
  const map = new google.maps.Map(document.getElementById("map"), {
      center: { lat: coords[0][0].lat, lng: coords[0][0].lng },
      zoom: 14,
      mapTypeId: "terrain",
  });

  const lineSymbol = {
      path: google.maps.SymbolPath.CIRCLE,
      scale: 4,
      strokeColor: "#393",
  };

coords.forEach((lineCoords, index) => {
  const line = new google.maps.Polyline({
      path: lineCoords,
      icons: [{ icon: lineSymbol, offset: "0%" }],
      map: map,
  });

  animateCircle(line, velocidades[index]); 
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