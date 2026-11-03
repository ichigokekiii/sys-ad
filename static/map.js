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

  var desktop = window.matchMedia("(min-width: 1100px)").matches;
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
    padding: desktop ? { left: 480, top: 40, right: 40, bottom: 40 } : { bottom: 220 },
  });

  map.addControl(new maplibregl.NavigationControl(), "top-right");

  map.on("load", function () {
    if (!hasPin) return;
    new maplibregl.Marker({ color: "#e07a3d" })
      .setLngLat([lon, lat])
      .addTo(map);
  });

  map.on("error", function () {
    if (!root.querySelector(".map-fallback")) fail();
  });
})();
