// A pin opens the card. The gray layer is the dialog. The X sits outside the card.
// Tilt follows a mouse. A click on the card turns it over.
(function () {
  var modal = document.getElementById("modal");
  var closeBtn = document.getElementById("close-card");
  var tilt = document.getElementById("card-tilt");
  var flip = document.getElementById("card-flip");
  var glare = document.getElementById("glare");
  var front = document.querySelector(".face.front");
  if (!modal || !closeBtn || !tilt || !flip || !front) return;

  var title = document.getElementById("card-title");
  var meta = document.getElementById("card-meta");
  var statA = document.getElementById("stat-a");
  var statB = document.getElementById("stat-b");
  var statC = document.getElementById("stat-c");
  var labelA = document.getElementById("stat-a-label");
  var labelB = document.getElementById("stat-b-label");
  var labelC = document.getElementById("stat-c-label");
  var v6Label = document.getElementById("v6-label");
  var badge = document.getElementById("ipv6-badge");
  var backLat = document.getElementById("back-lat");
  var backLon = document.getElementById("back-lon");
  var backWhere = document.getElementById("back-where");
  var network = {
    title: title.textContent,
    meta: meta.textContent,
    a: statA.textContent,
    b: statB.textContent,
    c: statC.textContent,
    labelA: labelA.textContent,
    labelB: labelB.textContent,
    labelC: labelC.textContent,
    v6: v6Label.textContent,
    lat: backLat.textContent,
    lon: backLon.textContent,
  };

  function openCard() {
    modal.hidden = false;
  }

  function closeCard() {
    modal.hidden = true;
  }

  function showNetwork() {
    title.textContent = network.title;
    meta.textContent = network.meta;
    meta.removeAttribute("title");
    statA.textContent = network.a;
    statB.textContent = network.b;
    statC.textContent = network.c;
    labelA.textContent = network.labelA;
    labelB.textContent = network.labelB;
    labelC.textContent = network.labelC;
    v6Label.textContent = network.v6;
    badge.textContent = badge.dataset.connection || badge.textContent;
    backLat.textContent = network.lat;
    backLon.textContent = network.lon;
    if (backWhere) {
      backWhere.hidden = true;
      backWhere.textContent = "";
    }
  }

  function showPlace(place) {
    title.textContent = place.name;
    meta.textContent = place.address;
    meta.title = place.address;
    backLat.textContent = Number(place.latitude).toFixed(5);
    backLon.textContent = Number(place.longitude).toFixed(5);
    if (backWhere) {
      backWhere.hidden = false;
      backWhere.textContent = place.address;
    }
    flip.classList.remove("is-flipped");
    flip.setAttribute("aria-pressed", "false");
  }

  closeBtn.addEventListener("click", function (event) {
    event.stopPropagation();
    closeCard();
  });
  modal.addEventListener("click", function (event) {
    if (event.target === modal) closeCard();
  });
  document.addEventListener("addresscard:open", function () {
    showNetwork();
    openCard();
  });
  document.addEventListener("addresscard:place", function (event) {
    if (!event.detail) return;
    showPlace(event.detail);
    openCard();
  });

  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape" && !modal.hidden) closeCard();
  });

  function toggleFlip() {
    var turned = flip.classList.toggle("is-flipped");
    flip.setAttribute("aria-pressed", turned ? "true" : "false");
  }

  flip.addEventListener("click", function (event) {
    if (event.target.closest("button, a, input, label, select, textarea")) return;
    toggleFlip();
  });

  flip.addEventListener("keydown", function (event) {
    if (event.target !== flip) return;
    if (event.key !== "Enter" && event.key !== " ") return;
    event.preventDefault();
    toggleFlip();
  });

  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)");
  var fine = window.matchMedia("(hover: hover) and (pointer: fine)");
  if (reduce.matches || !fine.matches) return;

  var frame = 0;
  tilt.addEventListener("pointermove", function (event) {
    var rect = tilt.getBoundingClientRect();
    var px = (event.clientX - rect.left) / rect.width;
    var py = (event.clientY - rect.top) / rect.height;
    var rx = (py - 0.5) * -10;
    var ry = (px - 0.5) * 12;
    if (frame) cancelAnimationFrame(frame);
    frame = requestAnimationFrame(function () {
      frame = 0;
      tilt.style.setProperty("--rx", rx.toFixed(2) + "deg");
      tilt.style.setProperty("--ry", ry.toFixed(2) + "deg");
      tilt.classList.add("is-lit");
      if (glare) {
        glare.style.setProperty("--gx", (px * 100).toFixed(1) + "%");
        glare.style.setProperty("--gy", (py * 100).toFixed(1) + "%");
      }
    });
  });

  tilt.addEventListener("pointerleave", function () {
    tilt.classList.remove("is-lit");
    tilt.style.setProperty("--rx", "0deg");
    tilt.style.setProperty("--ry", "0deg");
    if (glare) {
      glare.style.setProperty("--gx", "50%");
      glare.style.setProperty("--gy", "18%");
    }
  });
})();
