// This example adds an animated symbol to a polyline.
function initMap() {
  const map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 20.291, lng: 153.027 },
    zoom: 6,
    mapTypeId: "terrain",
  });

  const lineSymbol = {
    path: google.maps.SymbolPath.CIRCLE,
    scale: 8,
    strokeColor: "#393",
  };

  const line = new google.maps.Polyline({
    path: [
      { lat: 19.4037031532808, lng: -99.1692699611328 },
      { lat: 19.4229921001133, lng: -99.163152275508 },
    ],
    icons: [
      {
        icon: lineSymbol,
        offset: "100%",
      },
    ],
    map: map,
  });

  animateCircle(line);
}

function animateCircle(line) {
  let count = 0;

  window.setInterval(() => {
    count = (count + 1) % 200;

    const icons = line.get("icons");

    icons[0].offset = count / 2 + "%";
    line.set("icons", icons);
  }, 20);
}

export { initMap };