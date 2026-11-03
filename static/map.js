// Flat on purpose. This map is not Mapbox, so it does not pitch or grow buildings.
// The card is the piece that leans. The map only pans and zooms.
(function () {
  var root = document.getElementById("map");
  if (!root) return;

  function fail() {
    root.insertAdjacentHTML(
      "beforeend",
      "<p class='map-fallback'>The map did not load. The card still has the address.</p>"
    );
  }

  if (typeof maplibregl === "undefined") {
    fail();
    return;
  }

  var lat = parseFloat(root.dataset.lat);
  var lon = parseFloat(root.dataset.lon);
  var hasPin = Number.isFinite(lat) && Number.isFinite(lon);

  var map = new maplibregl.Map({
    container: root,
    style: "https://tiles.openfreemap.org/styles/liberty",
    center: hasPin ? [lon, lat] : [121.0, 14.6],
    zoom: hasPin ? 15 : 10,
    pitch: 0,
    bearing: 0,
    maxPitch: 0,
    pitchWithRotate: false,
    dragRotate: false,
    attributionControl: true,
  });

  map.addControl(new maplibregl.NavigationControl(), "top-right");

  map.on("load", function () {
    if (!hasPin) return;
    // The lookup returns one place. A second pin would be a location we do not have.
    var marker = new maplibregl.Marker({ color: "#e07a3d" })
      .setLngLat([lon, lat])
      .addTo(map);
    var pin = marker.getElement();
    pin.style.cursor = "pointer";
    pin.setAttribute("role", "button");
    pin.setAttribute("tabindex", "0");
    pin.setAttribute("aria-label", "Open the address card");
    function openFromPin(event) {
      event.stopPropagation();
      document.dispatchEvent(new CustomEvent("addresscard:open"));
    }
    pin.addEventListener("click", openFromPin);
    pin.addEventListener("keydown", function (event) {
      if (event.key !== "Enter" && event.key !== " ") return;
      openFromPin(event);
    });
  });

  map.on("error", function () {
    if (!root.querySelector(".map-fallback")) fail();
  });
})();
