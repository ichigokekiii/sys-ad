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
  var backAddress = document.getElementById("back-address");
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
    if (backWhere && backAddress) {
      backWhere.hidden = true;
      backAddress.textContent = "";
    }
  }

  function showPlace(place) {
    title.textContent = place.name;
    meta.textContent = place.address;
    meta.title = place.address;
    backLat.textContent = Number(place.latitude).toFixed(5);
    backLon.textContent = Number(place.longitude).toFixed(5);
    if (backWhere && backAddress) {
      backWhere.hidden = false;
      backAddress.textContent = place.address;
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

  var scroller = document.querySelector(".face-scroll");
  flip.addEventListener("wheel", function (event) {
    if (!flip.classList.contains("is-flipped") || !scroller) return;
    scroller.scrollTop += event.deltaY;
    event.preventDefault();
  }, { passive: false });

  var touchY = 0;
  flip.addEventListener("touchstart", function (event) {
    if (!event.touches.length) return;
    touchY = event.touches[0].clientY;
  }, { passive: true });
  flip.addEventListener("touchmove", function (event) {
    if (!flip.classList.contains("is-flipped") || !scroller || !event.touches.length) return;
    var y = event.touches[0].clientY;
    scroller.scrollTop += touchY - y;
    touchY = y;
    event.preventDefault();
  }, { passive: false });

  var verdict = document.getElementById("verdict");
  if (verdict) {
    if (verdict.classList.contains("is-right")) {
      burst();
      document.dispatchEvent(new CustomEvent("addresscard:reveal-pin"));
    }
    window.setTimeout(function () {
      verdict.classList.add("is-gone");
    }, 1500);
  }

  function burst() {
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    var canvas = document.getElementById("confetti");
    if (!canvas) return;
    canvas.hidden = false;
    var ctx = canvas.getContext("2d");
    var w = canvas.width = window.innerWidth;
    var h = canvas.height = window.innerHeight;
    var colors = ["#ffe14a", "#ffffff", "#1d4ed8", "#e07a3d"];
    var bits = [];
    var i;
    for (i = 0; i < 90; i += 1) {
      bits.push({
        x: w * 0.5 + (Math.random() - 0.5) * 120,
        y: h * 0.4,
        vx: (Math.random() - 0.5) * 16,
        vy: -7 - Math.random() * 9,
        g: 0.28,
        s: 4 + Math.random() * 6,
        c: colors[i % colors.length],
        r: Math.random() * 6,
      });
    }
    var start = performance.now();
    function frame(now) {
      ctx.clearRect(0, 0, w, h);
      bits.forEach(function (bit) {
        bit.vy += bit.g;
        bit.x += bit.vx;
        bit.y += bit.vy;
        bit.r += 0.15;
        ctx.save();
        ctx.translate(bit.x, bit.y);
        ctx.rotate(bit.r);
        ctx.fillStyle = bit.c;
        ctx.fillRect(-bit.s / 2, -bit.s / 4, bit.s, bit.s / 2);
        ctx.restore();
      });
      if (now - start < 1600) requestAnimationFrame(frame);
      else canvas.remove();
    }
    requestAnimationFrame(frame);
  }

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
