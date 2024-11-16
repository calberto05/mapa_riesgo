async function initMap() {
    // Request needed libraries.
    const { Map } = await google.maps.importLibrary("maps");
    const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");
    const center = { lat: 19.4261142, lng: -99.1938703 };
    const map = new Map(document.getElementById("map"), {
      zoom: 13,
      center,
      mapId: "4504f8b37365c3d0",
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
      <div class="icon">
          <i aria-hidden="true" class="fa fa-icon fa-${property.type}" title="${property.type}"></i>
          <span class="fa-sr-only">${property.type}</span>
      </div>
      <div class="details">
          <iframe src="${property.src}" height="200" width="300" title="Iframe Example"></iframe>
      </div>
      `;
    return content;
  }
  
  const properties = [
    {
      src: "https://www.youtube.com/embed/43_j654Jfn0?si=HTBfJRn4OntCIuCU",
      type: "video",
      position: {
        lat: 19.4261142,
        lng: -99.1938703,
      },
    },
    {
      src: "https://www.youtube.com/embed/VjqWE79jhZU?si=cGGQt-9HdlIOvOVF",
      type: "video",
      position: {
        lat: 19.4335748,
        lng: -99.137305,
      },
    }
  ];
  
  initMap();