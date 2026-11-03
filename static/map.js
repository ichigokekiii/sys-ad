// The camera can pitch. The tiles are OpenFreeMap Liberty, not Mapbox.
// A searched place gets its own pin. The visitor pin stays on the lookup.
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
    center: hasPin ? [lon, lat] : [120.9842, 14.5995],
    zoom: hasPin ? 15 : 11,
    pitch: 50,
    bearing: -18,
    maxPitch: 70,
    pitchWithRotate: true,
    dragRotate: true,
    touchPitch: true,
    attributionControl: true,
  });

  map.addControl(new maplibregl.NavigationControl(), "bottom-right");

  function wire(marker, label, open) {
    var pin = marker.getElement();
    pin.style.cursor = "pointer";
    pin.setAttribute("role", "button");
    pin.setAttribute("tabindex", "0");
    pin.setAttribute("aria-label", label);
    function activate(event) {
      event.stopPropagation();
      open();
    }
    pin.addEventListener("click", activate);
    pin.addEventListener("keydown", function (event) {
      if (event.key !== "Enter" && event.key !== " ") return;
      activate(event);
    });
  }

  var placeMarker = null;

  map.on("load", function () {
    if (!hasPin) return;
    var marker = new maplibregl.Marker({ color: "#e07a3d" })
      .setLngLat([lon, lat])
      .addTo(map);
    wire(marker, "Open your address card", function () {
      document.dispatchEvent(new CustomEvent("addresscard:open"));
    });
  });

  document.addEventListener("addresscard:place", function (event) {
    var place = event.detail;
    if (!place) return;
    var point = [place.longitude, place.latitude];
    if (!placeMarker) {
      placeMarker = new maplibregl.Marker({ color: "#1d4ed8" });
      wire(placeMarker, "Open this place", function () {
        document.dispatchEvent(new CustomEvent("addresscard:place", { detail: placeMarker._place }));
      });
    }
    placeMarker._place = place;
    placeMarker.setLngLat(point).addTo(map);
    // The card covers the map center, so the pin sits in the gap above it.
    requestAnimationFrame(function () {
      var frame = document.querySelector(".modal-frame");
      var top = frame ? frame.getBoundingClientRect().top : 160;
      var shift = window.innerHeight / 2 - Math.max(top, 80) / 2;
      map.flyTo({
        center: point,
        zoom: 16,
        pitch: 55,
        bearing: -18,
        padding: { bottom: Math.max(0, shift * 2) },
      });
    });
  });

  map.on("error", function () {
    if (!root.querySelector(".map-fallback")) fail();
  });
})();
