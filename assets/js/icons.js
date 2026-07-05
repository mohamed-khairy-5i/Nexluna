/* Nexluna — modern inline SVG icon set.
   Usage: <span data-icon="length"></span>  → replaced with the SVG.
   Stroke-based, currentColor, 24x24 grid. */
(function () {
  'use strict';
  var P = 'stroke="currentColor" stroke-width="1.8" fill="none" stroke-linecap="round" stroke-linejoin="round"';
  var ICONS = {
    length: '<path ' + P + ' d="M3 8h18v8H3z"/><path ' + P + ' d="M7 8v3M11 8v4M15 8v3M19 8v4"/>',
    weight: '<path ' + P + ' d="M6.5 8h11l2.5 11H4z"/><circle cx="12" cy="5.5" r="2.5" ' + P + '/><path ' + P + ' d="M12 8v0"/>',
    area: '<path ' + P + ' d="M4 4h16v16H4z"/><path ' + P + ' d="M4 9h16M4 14h16M9 4v16M14 4v16" stroke-dasharray="0.5 3"/>',
    temperature: '<path ' + P + ' d="M14 14.76V5a2 2 0 1 0-4 0v9.76a4 4 0 1 0 4 0z"/>',
    volume: '<path ' + P + ' d="M6 3h12l-1 4a5 5 0 0 1-10 0z"/><path ' + P + ' d="M8 21h8M12 12v9"/>',
    data: '<ellipse cx="12" cy="5" rx="7" ry="3" ' + P + '/><path ' + P + ' d="M5 5v6c0 1.66 3.13 3 7 3s7-1.34 7-3V5M5 11v6c0 1.66 3.13 3 7 3s7-1.34 7-3v-6"/>',
    speed: '<path ' + P + ' d="M12 14a2 2 0 1 0 0-4 2 2 0 0 0 0 4z"/><path ' + P + ' d="M12 10 15 7"/><path ' + P + ' d="M4.5 17a9 9 0 1 1 15 0"/>',
    time: '<circle cx="12" cy="12" r="8.5" ' + P + '/><path ' + P + ' d="M12 7v5l3.5 2"/>',
    pressure: '<circle cx="12" cy="12" r="8.5" ' + P + '/><path ' + P + ' d="M12 12 8 8"/><circle cx="12" cy="12" r="1.4" fill="currentColor" stroke="none"/>',
    energy: '<path ' + P + ' d="M13 2 4 14h7l-1 8 9-12h-7z"/>',
    power: '<path ' + P + ' d="M12 3v9"/><path ' + P + ' d="M7.5 6.5a7 7 0 1 0 9 0"/>',
    fuel: '<path ' + P + ' d="M4 20V6a2 2 0 0 1 2-2h6a2 2 0 0 1 2 2v14"/><path ' + P + ' d="M3 20h13"/><path ' + P + ' d="M14 9h2.5a2 2 0 0 1 2 2v5a1.5 1.5 0 0 0 3 0V9l-3-3"/>',
    angle: '<path ' + P + ' d="M4 20h16"/><path ' + P + ' d="M4 20 18 6"/><path ' + P + ' d="M4 20V9"/><path ' + P + ' d="M9 20a5 5 0 0 0-5-5"/>',
    bmi: '<circle cx="12" cy="6" r="2.5" ' + P + '/><path ' + P + ' d="M8 21v-5l-2-3 3-3h6l3 3-2 3v5"/>',
    frequency: '<path ' + P + ' d="M2 12h3l2-6 3 12 3-16 3 12 2-2h4"/>',
    swap: '<path ' + P + ' d="M7 4 4 7l3 3"/><path ' + P + ' d="M4 7h13a3 3 0 0 1 3 3v0"/><path ' + P + ' d="M17 20l3-3-3-3"/><path ' + P + ' d="M20 17H7a3 3 0 0 1-3-3v0"/>',
    copy: '<rect x="9" y="9" width="11" height="11" rx="2" ' + P + '/><path ' + P + ' d="M5 15V5a2 2 0 0 1 2-2h10"/>',
    star: '<path ' + P + ' d="M12 3l2.6 5.5 6 .9-4.3 4.2 1 6-5.3-2.8-5.3 2.8 1-6L3.4 9.4l6-.9z"/>',
    'star-fill': '<path fill="currentColor" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round" d="M12 3l2.6 5.5 6 .9-4.3 4.2 1 6-5.3-2.8-5.3 2.8 1-6L3.4 9.4l6-.9z"/>',
    history: '<path ' + P + ' d="M3 12a9 9 0 1 0 3-6.7L3 8"/><path ' + P + ' d="M3 4v4h4"/><path ' + P + ' d="M12 8v4l3 2"/>',
    trash: '<path ' + P + ' d="M4 7h16"/><path ' + P + ' d="M9 7V5a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2"/><path ' + P + ' d="M6 7l1 13h10l1-13"/>',
    share: '<circle cx="18" cy="5" r="2.5" ' + P + '/><circle cx="6" cy="12" r="2.5" ' + P + '/><circle cx="18" cy="19" r="2.5" ' + P + '/><path ' + P + ' d="M8.2 10.7 15.8 6.3M8.2 13.3l7.6 4.4"/>',
    sun: '<circle cx="12" cy="12" r="4" ' + P + '/><path ' + P + ' d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
    moon: '<path ' + P + ' d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/>',
    menu: '<path ' + P + ' d="M4 6h16M4 12h16M4 18h16"/>',
    arrow: '<path ' + P + ' d="M5 12h14"/><path ' + P + ' d="M13 6l6 6-6 6"/>',
    check: '<path ' + P + ' d="M20 6 9 17l-5-5"/>',
    bolt: '<path ' + P + ' d="M13 2 4 14h7l-1 8 9-12h-7z"/>',
    grid: '<rect x="3" y="3" width="7" height="7" rx="1.5" ' + P + '/><rect x="14" y="3" width="7" height="7" rx="1.5" ' + P + '/><rect x="3" y="14" width="7" height="7" rx="1.5" ' + P + '/><rect x="14" y="14" width="7" height="7" rx="1.5" ' + P + '/>',
    offline: '<path ' + P + ' d="M5 12.55a11 11 0 0 1 14 0M8.5 16.1a6 6 0 0 1 7 0M12 20h.01"/><path ' + P + ' d="M3 3l18 18"/>',
    shield: '<path ' + P + ' d="M12 3l7 3v5c0 5-3.5 8-7 10-3.5-2-7-5-7-10V6z"/><path ' + P + ' d="M9 12l2 2 4-4"/>',
    globe: '<circle cx="12" cy="12" r="9" ' + P + '/><path ' + P + ' d="M3 12h18M12 3a15 15 0 0 1 0 18M12 3a15 15 0 0 0 0 18"/>',
    book: '<path ' + P + ' d="M4 5a2 2 0 0 1 2-2h13v16H6a2 2 0 0 0-2 2z"/><path ' + P + ' d="M4 19a2 2 0 0 1 2-2h13"/>',
    mail: '<rect x="3" y="5" width="18" height="14" rx="2" ' + P + '/><path ' + P + ' d="M3 7l9 6 9-6"/>',
    check2: '<circle cx="12" cy="12" r="9" ' + P + '/><path ' + P + ' d="M8 12l3 3 5-6"/>'
  };
  function render(root) {
    (root || document).querySelectorAll('[data-icon]').forEach(function (el) {
      var name = el.getAttribute('data-icon');
      if (!ICONS[name] || el.dataset.iconDone) return;
      el.innerHTML = '<svg viewBox="0 0 24 24" width="24" height="24" aria-hidden="true" focusable="false">' + ICONS[name] + '</svg>';
      el.dataset.iconDone = '1';
    });
  }
  window.NexIcons = { render: render, get: function (n) { return ICONS[n] ? '<svg viewBox="0 0 24 24" aria-hidden="true">' + ICONS[n] + '</svg>' : ''; } };
  document.addEventListener('DOMContentLoaded', function () { render(document); });
})();
