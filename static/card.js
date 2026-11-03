// A pin opens the card. The gray layer is the dialog. The X sits outside the card.
// Tilt follows a mouse. A click on the card turns it over.
(function () {
  var modal = document.getElementById("modal");
  var reopen = document.getElementById("reopen");
  var closeBtn = document.getElementById("close-card");
  var tilt = document.getElementById("card-tilt");
  var flip = document.getElementById("card-flip");
  var glare = document.getElementById("glare");
  if (!modal || !reopen || !closeBtn || !tilt || !flip) return;

  function openCard() {
    modal.hidden = false;
    reopen.hidden = true;
    closeBtn.focus();
  }

  function closeCard() {
    modal.hidden = true;
    reopen.hidden = false;
    reopen.focus();
  }

  closeBtn.addEventListener("click", function (event) {
    event.stopPropagation();
    closeCard();
  });
  modal.addEventListener("click", function (event) {
    if (event.target === modal) closeCard();
  });
  document.addEventListener("addresscard:open", openCard);
  reopen.addEventListener("click", openCard);

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
