// Suggestions come from /places. A choice is a Metro Manila place, not an IP.
(function () {
  var form = document.getElementById("place-search");
  var input = document.getElementById("place-query");
  var list = document.getElementById("place-results");
  if (!form || !input || !list) return;

  var timer = 0;
  var request = 0;

  form.addEventListener("submit", function (event) {
    event.preventDefault();
  });

  input.addEventListener("input", function () {
    window.clearTimeout(timer);
    var query = input.value.trim();
    if (query.length < 2) {
      clearList();
      return;
    }
    timer = window.setTimeout(function () {
      load(query);
    }, 300);
  });

  document.addEventListener("click", function (event) {
    if (!form.contains(event.target)) clearList();
  });

  function clearList() {
    list.hidden = true;
    list.replaceChildren();
  }

  function load(query) {
    var token = ++request;
    fetch("/places?q=" + encodeURIComponent(query))
      .then(function (response) {
        if (!response.ok) throw new Error("status");
        return response.json();
      })
      .then(function (places) {
        if (token !== request) return;
        show(places);
      })
      .catch(function () {
        if (token !== request) return;
        show([]);
      });
  }

  function show(places) {
    list.replaceChildren();
    if (!places.length) {
      var empty = document.createElement("li");
      empty.className = "search-empty";
      empty.textContent = "No places in Metro Manila. Try Quiapo or Makati.";
      list.appendChild(empty);
      list.hidden = false;
      return;
    }
    places.forEach(function (place) {
      var item = document.createElement("li");
      var button = document.createElement("button");
      button.type = "button";
      button.textContent = place.name;
      var address = document.createElement("small");
      address.textContent = place.address;
      button.appendChild(document.createElement("br"));
      button.appendChild(address);
      button.addEventListener("click", function () {
        input.value = place.name;
        clearList();
        document.dispatchEvent(new CustomEvent("addresscard:place", { detail: place }));
      });
      item.appendChild(button);
      list.appendChild(item);
    });
    list.hidden = false;
  }
})();
