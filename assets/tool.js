// Art style finder: each answer adds a point to the movements it points to. Runs only in the browser.
(function () {
  var tool = document.querySelector('[data-tool]');
  if (!tool) return;
  var s = JSON.parse(tool.querySelector('.tool-i18n').textContent);
  var lvl = tool.querySelector('[data-lvl]');
  var cards = tool.querySelectorAll('.mvcard');

  function update() {
    var picked = tool.querySelectorAll('.opts button[aria-pressed="true"]');
    cards.forEach(function (c) { c.hidden = true; });
    if (picked.length < 2) { lvl.textContent = s.need; return; }
    var score = {};
    picked.forEach(function (b) { b.dataset.m.split(' ').forEach(function (m) { score[m] = (score[m] || 0) + 1; }); });
    var top = Object.keys(score).sort(function (a, b) { return score[b] - score[a]; }).slice(0, 3);
    lvl.textContent = tool.dataset.result || '';
    var list = tool.querySelector('.mvcards');
    top.forEach(function (k) {
      var c = tool.querySelector('.mvcard[data-key="' + k + '"]');
      if (c) { c.hidden = false; list.appendChild(c); }
    });
  }

  tool.addEventListener('click', function (e) {
    var b = e.target.closest('button');
    if (!b) return;
    if (b.hasAttribute('data-reset')) {
      tool.querySelectorAll('.opts button').forEach(function (x) { x.setAttribute('aria-pressed', 'false'); });
    } else if (b.dataset.m !== undefined) {
      b.parentNode.querySelectorAll('button').forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
    }
    update();
  });
})();
