(function () {
  'use strict';
  var root = window;
  var data = root.NexlunaUnits || {};
  var category = document.querySelector('#embed-category');
  var from = document.querySelector('#embed-from');
  var to = document.querySelector('#embed-to');
  var value = document.querySelector('#embed-value');
  var result = document.querySelector('#embed-result');
  var form = document.querySelector('#embed-form');

  function entries(key) { return (data[key] && data[key].units) || []; }
  function fill(select, items, selected) {
    select.innerHTML = '';
    items.forEach(function (item) {
      var option = document.createElement('option');
      option.value = item[0]; option.textContent = item[1];
      if (item[0] === selected) option.selected = true;
      select.appendChild(option);
    });
  }
  function setCategory(next, nextFrom, nextTo) {
    category.value = next;
    var items = entries(next);
    fill(from, items, nextFrom || (items[0] && items[0][0]));
    fill(to, items, nextTo || (items[1] && items[1][0]) || (items[0] && items[0][0]));
  }
  function run() {
    try {
      var output = root.NexMCP.convert(category.value, from.value, to.value, value.value);
      result.textContent = String(output);
      result.dataset.state = 'success';
      window.parent.postMessage({ type: 'nexluna-result', category: category.value, from: from.value, to: to.value, value: Number(value.value), result: output }, '*');
    } catch (error) {
      result.textContent = error.message || 'تعذر إجراء التحويل';
      result.dataset.state = 'error';
    }
  }
  Object.keys(data).forEach(function (key) {
    var option = document.createElement('option'); option.value = key; option.textContent = data[key].label || key; category.appendChild(option);
  });
  var params = new URLSearchParams(window.location.search);
  setCategory(params.get('category') || 'length', params.get('from') || 'm', params.get('to') || 'ft');
  value.value = params.get('v') || '1';
  form.addEventListener('submit', function (event) { event.preventDefault(); run(); });
  category.addEventListener('change', function () { setCategory(category.value); run(); });
  from.addEventListener('change', run); to.addEventListener('change', run); value.addEventListener('input', run);
  run();
})();
