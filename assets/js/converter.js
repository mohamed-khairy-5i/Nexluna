/* Nexluna — premium unit conversion engine.
   14 categories · copy · history · favorites · keyboard shortcuts · share.
   Mount into #converter-app. data-only="length" restricts to one category. */
(function () {
  'use strict';

  /* ---------- Data (generated canonical source) ---------- */
  var DATA = window.NexlunaUnits || {};
  if (!Object.keys(DATA).length) throw new Error('Nexluna units data not loaded');
  var LOCALE = window.NexlunaLocale || {};
  var UI = LOCALE.ui || {};
  function tx(key, fallback) { return UI[key] || fallback; }
  function catText(cat, key, fallback) {
    var c = LOCALE.categories && LOCALE.categories[cat];
    return c && c[key] != null ? c[key] : fallback;
  }
  function unitText(cat, key, fallback) {
    var map = LOCALE.units && LOCALE.units[cat];
    return map && map[key] ? map[key] : fallback;
  }
  function template(key, fallback, vars) {
    var out = tx(key, fallback);
    Object.keys(vars || {}).forEach(function (name) { out = out.replace(new RegExp('\\\\{' + name + '\\\\}', 'g'), vars[name]); });
    return out;
  }

  var STORE = { hist: 'nx-history', fav: 'nx-favorites' };

  /* ---------- Helpers ---------- */
  function tempConvert(v, f, t) { var c = f === 'C' ? v : f === 'F' ? (v - 32) * 5 / 9 : v - 273.15; return t === 'C' ? c : t === 'F' ? c * 9 / 5 + 32 : c + 273.15; }
  /* mpg factors: US gal = 3.785411784 L, Imperial gal = 4.54609 L (1 mi = 1.609344 km). */
  var MPG_US = 0.425143707430272, MPG_UK = 0.3540061899346471;
  function mpgFactor(u) { return u === 'mpgUK' ? MPG_UK : MPG_US; }
  function fuelToKmL(v, u) { return u === 'kml' ? v : u === 'l100' ? 100 / v : v * mpgFactor(u); }
  function kmLToUnit(v, u) { return u === 'kml' ? v : u === 'l100' ? 100 / v : v / mpgFactor(u); }
  function fmt(n) { if (!isFinite(n)) return '—'; var r = Math.round(n * 1e6) / 1e6; return r.toLocaleString('en-US', { maximumFractionDigits: 6 }); }
  var REDUCED = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  /* Spring-eased count-up — the signature motion moment. Honors reduced-motion. */
  function countUp(node, from, to) {
    if (node._raf) cancelAnimationFrame(node._raf);
    if (REDUCED || !isFinite(from) || !isFinite(to) || from === to) { node.textContent = fmt(to); return; }
    var dur = 520, t0 = 0;
    function ease(x) { return 1 - Math.pow(1 - x, 3); } /* easeOutCubic — settles, no linear tell */
    function step(ts) {
      if (!t0) t0 = ts;
      var p = Math.min((ts - t0) / dur, 1);
      node.textContent = fmt(from + (to - from) * ease(p));
      if (p < 1) node._raf = requestAnimationFrame(step); else node.textContent = fmt(to);
    }
    node._raf = requestAnimationFrame(step);
  }
  function ls(k, d) { try { return JSON.parse(localStorage.getItem(k)) || d; } catch (e) { return d; } }
  function save(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }
  function el(tag, attrs, html) { var e = document.createElement(tag); if (attrs) Object.keys(attrs).forEach(function (k) { e.setAttribute(k, attrs[k]); }); if (html != null) e.innerHTML = html; return e; }
  function ic(name) { return window.NexIcons ? window.NexIcons.get(name) : ''; }

  function toast(msg) {
    var t = document.getElementById('nx-toast');
    if (!t) { t = el('div', { id: 'nx-toast', class: 'toast', role: 'status', 'aria-live': 'polite' }); document.body.appendChild(t); }
    t.textContent = msg; t.classList.add('show');
    clearTimeout(t._t); t._t = setTimeout(function () { t.classList.remove('show'); }, 1800);
  }
  function copyText(text, ok, fail) {
    if (navigator.clipboard && window.isSecureContext !== false) {
      navigator.clipboard.writeText(text).then(ok).catch(function () { copyTextFallback(text, ok, fail); });
      return;
    }
    copyTextFallback(text, ok, fail);
  }
  function copyTextFallback(text, ok, fail) {
    var area = el('textarea', { readonly: 'readonly', 'aria-hidden': 'true' });
    area.value = text; area.style.position = 'fixed'; area.style.opacity = '0';
    document.body.appendChild(area); area.select();
    var copied = false;
    try { copied = document.execCommand('copy'); } catch (e) {}
    area.remove();
    if (copied) ok(); else fail();
  }

  /* ---------- Mount ---------- */
  function mount(root) {
    root.innerHTML = ''; /* clear any skeleton placeholder */
    var only = root.getAttribute('data-only');
    var cats = only ? [only] : Object.keys(DATA);
    var current = cats[0];

    var tabs = el('div', { class: 'tabs', role: 'tablist', 'aria-label': tx('categories_aria', 'فئات التحويل') });
    if (!only) cats.forEach(function (c) {
      var b = el('button', { class: 'tab-btn', role: 'tab', type: 'button', id: 'tab-' + c, 'aria-controls': 'panel', 'aria-selected': String(c === current), 'data-cat': c });
      b.innerHTML = ic(DATA[c].icon) + '<span>' + catText(c, 'label', DATA[c].label) + '</span>';
      tabs.appendChild(b);
    });

    /* Toolbar: title + favorite + copy */
    var titleEl = el('span', { class: 'converter-title' }, catText(current, 'label', DATA[current].title));
    var favBtn = el('button', { class: 'pill-btn', type: 'button', 'data-fav': '', 'aria-pressed': 'false', title: tx('favorite', 'حفظ كمفضّلة') });
    favBtn.innerHTML = ic('star') + '<span>' + tx('favorite', 'مفضّلة') + '</span>';
    var explainBtn = el('button', { class: 'pill-btn explain-btn', type: 'button', 'aria-expanded': 'false', title: tx('explain', 'شرح الحساب') });
    explainBtn.innerHTML = ic('spark') + '<span>' + tx('explain', 'اشرح الحساب') + '</span>'; explainBtn.style.display = 'none';
    var dataSystem = ls('nx-data-system', 'decimal');
    var dataSystemSelect = el('select', { class: 'data-system-select', 'aria-label': 'نظام وحدات البيانات' });
    dataSystemSelect.innerHTML = '<option value="decimal">' + tx('decimal', 'عشري (1000)') + '</option><option value="binary">' + tx('binary', 'ثنائي (1024)') + '</option>';
    dataSystemSelect.value = dataSystem;
    var dataSystemControl = el('label', { class: 'data-system-control' }, '<span>' + tx('system', 'النظام') + '</span>');
    dataSystemControl.appendChild(dataSystemSelect); dataSystemControl.hidden = true;
    var toolbar = el('div', { class: 'converter-toolbar' });
    var tRight = el('div', { class: 'toolbar-actions' });
    tRight.appendChild(dataSystemControl); tRight.appendChild(explainBtn); tRight.appendChild(favBtn);
    toolbar.appendChild(titleEl); toolbar.appendChild(tRight);

    /* Inputs */
    var fromSel = el('select', { id: 'nx-from', 'aria-label': tx('from', 'الوحدة المصدر') });
    var toSel = el('select', { id: 'nx-to', 'aria-label': tx('to', 'الوحدة الهدف') });
    var fromInput = el('input', { id: 'nx-in', type: 'number', inputmode: 'decimal', placeholder: tx('enter_value', 'أدخل القيمة'), 'aria-label': tx('enter_value', 'القيمة المدخلة'), 'aria-describedby': 'nx-result' });
    var toInput = el('input', { id: 'nx-out', type: 'text', readonly: 'readonly', 'aria-label': tx('output', 'القيمة الناتجة'), tabindex: '-1' });
    var swap = el('button', { class: 'swap-btn', type: 'button', 'aria-label': tx('swap', 'تبديل الوحدات (زر التبديل)'), title: tx('swap', 'تبديل (Enter)') }); swap.innerHTML = ic('swap');

    var f1 = el('div', { class: 'field' }); f1.appendChild(el('label', { for: 'nx-in' }, ic('arrow') + '<span>' + tx('from', 'من') + '</span>')); f1.appendChild(fromInput); f1.appendChild(fromSel);
    var f2 = el('div', { class: 'field' }); f2.appendChild(el('label', { for: 'nx-out' }, ic('check') + '<span>' + tx('to', 'إلى') + '</span>')); f2.appendChild(toInput); f2.appendChild(toSel);
    var grid = el('div', { class: 'conv-grid' }); grid.appendChild(f1); grid.appendChild(swap); grid.appendChild(f2);

    var result = el('div', { class: 'result', id: 'nx-result', role: 'status', 'aria-live': 'polite' }, '<span class="hint">' + tx('result_hint', 'أدخل قيمة لعرض النتيجة') + '</span>');
    var copyBtn = el('button', { class: 'copy-result', type: 'button', 'aria-label': tx('copy', 'نسخ النتيجة'), title: tx('copy', 'نسخ النتيجة') }); copyBtn.innerHTML = ic('copy'); copyBtn.style.display = 'none';
    var shareBtn = el('button', { class: 'copy-result share-result', type: 'button', 'aria-label': tx('share', 'نسخ رابط المشاركة'), title: tx('share', 'نسخ رابط المشاركة') }); shareBtn.innerHTML = ic('share'); shareBtn.style.display = 'none';
    result.appendChild(copyBtn);
    result.appendChild(shareBtn);

    var info = el('div', { class: 'info-block' });
    var explainBox = el('div', { class: 'explain-box', role: 'status', 'aria-live': 'polite' });
    explainBox.hidden = true;

    /* History */
    var histWrap = el('div', { class: 'history' });
    var histHead = el('h2', null, '<span>' + ic('history') + ' آخر التحويلات</span>');
    var clearBtn = el('button', { class: 'clear', type: 'button' }, 'مسح الكل');
    histHead.appendChild(clearBtn);
    var histList = el('div', { class: 'history-list' });
    histWrap.appendChild(histHead); histWrap.appendChild(histList);

    var panel = el('div', { id: 'panel', role: 'tabpanel', 'aria-live': 'polite', tabindex: '-1' });
    panel.appendChild(toolbar); panel.appendChild(grid); panel.appendChild(result); panel.appendChild(explainBox); panel.appendChild(histWrap); panel.appendChild(info);
    if (!only) root.appendChild(tabs);
    root.appendChild(panel);

    var lastResult = '';

    function hideExplain() {
      explainBox.hidden = true; explainBox.textContent = '';
      explainBtn.style.display = 'none'; explainBtn.setAttribute('aria-expanded', 'false');
    }
    function fillUnits() {
      var d = DATA[current];
      var units = (d.units || []).slice();
      if (current === 'data') {
        var allowed = dataSystem === 'binary' ? ['bit', 'B', 'KiB', 'MiB', 'GiB'] : ['bit', 'B', 'KB', 'MB', 'GB', 'TB'];
        units = units.filter(function (u) { return allowed.indexOf(u[0]) !== -1; });
      }
      var previousFrom = fromSel.value, previousTo = toSel.value;
      var opts = units.map(function (u) { return '<option value="' + u[0] + '">' + unitText(current, u[0], u[1]) + '</option>'; }).join('');
      fromSel.innerHTML = opts; toSel.innerHTML = opts;
      fromSel.value = units.some(function (u) { return u[0] === previousFrom; }) ? previousFrom : units[0][0];
      toSel.value = units.some(function (u) { return u[0] === previousTo; }) ? previousTo : units[Math.min(1, units.length - 1)][0];
    }
    function renderInfo() {
      var d = DATA[current];
      var formulas = catText(current, 'formulas', d.formulas || []);
      var common = catText(current, 'common', d.common || []);
      info.innerHTML = '';
      info.appendChild(el('h2', { style: 'margin-bottom:var(--sp-2)' }, tx('formulas', 'صيغ التحويل')));
      info.appendChild(el('div', { class: 'formula' }, formulas.join('<br>')));
      info.appendChild(el('h2', { style: 'margin:var(--sp-4) 0 var(--sp-2)' }, tx('common', 'تحويلات شائعة')));
      var ul = el('ul', { class: 'conv-list' }); common.forEach(function (c) { ul.appendChild(el('li', null, c)); }); info.appendChild(ul);
      if (current === 'data') {
        var note = dataSystem === 'decimal' ? tx('data_decimal_note', 'النظام العشري يستخدم مضاعفات 1000 مثل KB وMB وGB.') : tx('data_binary_note', 'النظام الثنائي يستخدم مضاعفات 1024 مثل KiB وMiB وGiB.');
        info.appendChild(el('p', { class: 'data-system-note' }, note));
      }
    }
    function calc(v) {
      var d = DATA[current];
      if (d.temp) return tempConvert(v, fromSel.value, toSel.value);
      if (d.special === 'fuel') return kmLToUnit(fuelToKmL(v, fromSel.value), toSel.value);
      return v * d.base[fromSel.value] / d.base[toSel.value];
    }
    function shareURL(v) {
      var base = window.location.origin + window.location.pathname;
      var qs = 'from=' + encodeURIComponent(fromSel.value) + '&to=' + encodeURIComponent(toSel.value) + '&v=' + encodeURIComponent(v);
      return base + '?' + qs;
    }
    var prevOut = null;
    function convert(pushHist) {
      var raw = fromInput.value.trim();
      if (raw === '') { toInput.value = ''; prevOut = null; fromInput.removeAttribute('aria-invalid'); result.className = 'result'; result.innerHTML = '<span class="hint">' + tx('result_hint', 'أدخل قيمة لعرض النتيجة') + '</span>'; result.appendChild(copyBtn); result.appendChild(shareBtn); copyBtn.style.display = 'none'; shareBtn.style.display = 'none'; hideExplain(); return; }
      var v = parseFloat(raw);
      if (isNaN(v)) { fromInput.setAttribute('aria-invalid', 'true'); prevOut = null; result.className = 'result error'; result.innerHTML = '<span class="value">' + tx('invalid', 'قيمة غير صحيحة — أدخل رقمًا') + '</span>'; result.appendChild(copyBtn); result.appendChild(shareBtn); copyBtn.style.display = 'none'; shareBtn.style.display = 'none'; toInput.value = ''; hideExplain(); return; }
      fromInput.removeAttribute('aria-invalid');
      var out = calc(v); toInput.value = fmt(out);
      var fu = unitText(current, fromSel.value, fromSel.options[fromSel.selectedIndex].text), tu = unitText(current, toSel.value, toSel.options[toSel.selectedIndex].text);
      lastResult = fmt(v) + ' ' + fu + ' = ' + fmt(out) + ' ' + tu;
      result.className = 'result';
      /* Signature: the output number count-ups from its previous value (spring-eased). */
      result.innerHTML = '<div class="result-inner"><span class="result-num"><span class="result-out" aria-live="off">0</span></span><div class="hint"><span class="result-in">' + fmt(v) + '</span> ' + fu + ' &rarr; ' + tu + '</div></div>';
      result.appendChild(copyBtn); result.appendChild(shareBtn); copyBtn.style.display = 'grid'; shareBtn.style.display = 'grid';
      var outNode = result.querySelector('.result-out');
      countUp(outNode, prevOut === null ? out : prevOut, out);
      result.setAttribute('aria-label', lastResult);
      explainBtn.style.display = 'grid';
      prevOut = out;
      /* Keep the address bar shareable without reloading (Roadmap 1.4). */
      if (pushHist) { try { history.replaceState(null, '', shareURL(v)); } catch (e) {} }
      if (pushHist) addHistory(v, out, fu, tu);
    }
    function addHistory(v, out, fu, tu) {
      var h = ls(STORE.hist, []);
      var entry = { c: current, t: fmt(v) + ' ' + fu + ' = ' + fmt(out) + ' ' + tu, ts: Date.now() };
      if (h.length && h[0].t === entry.t) return;
      h.unshift(entry); h = h.slice(0, 8); save(STORE.hist, h); renderHistory();
    }
    function renderHistory() {
      var h = ls(STORE.hist, []); histList.innerHTML = '';
      if (!h.length) { histList.appendChild(el('div', { class: 'history-empty' }, tx('history_empty', 'لا توجد تحويلات محفوظة بعد.'))); return; }
        h.forEach(function (e) {
        var item = el('div', { class: 'history-item' });
        var d = new Date(e.ts); var tm = d.toLocaleTimeString('ar-EG', { hour: '2-digit', minute: '2-digit' });
        item.innerHTML = '<span>' + e.t + '</span><span class="t">' + tm + '</span>';
        histList.appendChild(item);
      });
    }
    function updateFav() {
      var favs = ls(STORE.fav, []); var on = favs.indexOf(current) !== -1;
      favBtn.setAttribute('aria-pressed', String(on)); favBtn.classList.toggle('active', on);
      favBtn.innerHTML = ic(on ? 'star-fill' : 'star') + '<span>' + (on ? tx('favorited', 'محفوظة') : tx('favorite', 'مفضّلة')) + '</span>';
    }
    function selectCat(cat) {
      current = cat; titleEl.textContent = catText(cat, 'label', DATA[cat].title);
      dataSystemControl.hidden = current !== 'data';
      tabs.querySelectorAll('.tab-btn').forEach(function (b) { b.setAttribute('aria-selected', String(b.getAttribute('data-cat') === cat)); });
      fillUnits(); renderInfo(); updateFav(); fromInput.value = ''; convert(false);
    }

    /* Events */
    tabs.addEventListener('click', function (e) { var b = e.target.closest('.tab-btn'); if (b) selectCat(b.getAttribute('data-cat')); });
    var debounce; fromInput.addEventListener('input', function () { clearTimeout(debounce); convert(false); debounce = setTimeout(function () { if (fromInput.value.trim() !== '') convert(true); }, 900); });
    fromSel.addEventListener('change', function () { convert(true); });
    toSel.addEventListener('change', function () { convert(true); });
    swap.addEventListener('click', function () { var t = fromSel.value; fromSel.value = toSel.value; toSel.value = t; if (toInput.value) fromInput.value = toInput.value.replace(/,/g, ''); convert(true); });
    copyBtn.addEventListener('click', function () { if (!toInput.value) return; copyText(lastResult, function () { toast(tx('copy_success', 'تم نسخ النتيجة ✓')); }, function () { toast(tx('copy_failed', 'تعذّر النسخ')); }); });
    shareBtn.addEventListener('click', function () {
      if (!toInput.value) return;
      var v = parseFloat(fromInput.value); if (isNaN(v)) return;
      var url = shareURL(v);
      if (navigator.share) { navigator.share({ title: 'Nexluna', text: lastResult, url: url }).catch(function () {}); return; }
      copyText(url, function () { toast(tx('share_success', 'تم نسخ رابط المشاركة ✓')); }, function () { toast(tx('copy_failed', 'تعذّر النسخ')); });
    });
    explainBtn.addEventListener('click', function () {
      var v = parseFloat(fromInput.value); if (isNaN(v) || !toInput.value) return;
      explainBox.hidden = false; explainBox.textContent = tx('explain_loading', 'يتم إعداد شرح محلي موثوق...');
      explainBtn.setAttribute('aria-expanded', 'true');
      var request = { category: current, from: fromSel.value, to: toSel.value, value: v };
      var run = window.NexExplain && window.NexExplain.explain;
      if (!run) { explainBox.textContent = tx('explain_unavailable', 'الحساب حتمي بواسطة NexConvert، ولا تتوفر طبقة شرح إضافية الآن.'); return; }
      Promise.resolve(run(request)).then(function (payload) {
        var source = payload && payload.source === 'optional-model-verified' ? tx('explain_verified', 'شرح لغوي موثّق؛ الرقم صادر من NexConvert.') : tx('explain_local', 'شرح محلي؛ الرقم صادر حتميًا من NexConvert.');
        explainBox.textContent = (payload && payload.explanation ? payload.explanation + ' ' : '') + source;
      }).catch(function () { explainBox.textContent = tx('explain_error', 'الحساب حتمي بواسطة NexConvert، وتعذّر إنشاء شرح إضافي.'); });
    });
    dataSystemSelect.addEventListener('change', function () {
      dataSystem = dataSystemSelect.value === 'binary' ? 'binary' : 'decimal';
      save('nx-data-system', dataSystem); fillUnits(); renderInfo(); convert(false);
    });
    favBtn.addEventListener('click', function () { var favs = ls(STORE.fav, []); var i = favs.indexOf(current); if (i === -1) { favs.push(current); toast(tx('favorite_added', 'أُضيفت إلى المفضّلة ★')); } else { favs.splice(i, 1); toast(tx('favorite_removed', 'أُزيلت من المفضّلة')); } save(STORE.fav, favs); updateFav(); });
    clearBtn.addEventListener('click', function () { save(STORE.hist, []); renderHistory(); toast(tx('history_cleared', 'تم مسح السجل')); });

    /* Keyboard: Enter = swap, Escape = clear */
    root.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' && document.activeElement === fromInput) { e.preventDefault(); swap.click(); }
      else if (e.key === 'Escape') { fromInput.value = ''; convert(false); fromInput.focus(); }
    });

    dataSystemControl.hidden = current !== 'data';
    fillUnits(); renderInfo(); updateFav(); renderHistory();

    /* Deep-link prefill: /converters/x.html?from=&to=&v=  (Roadmap 1.4).
       Lets pair pages & shared links open the converter pre-filled. */
    (function applyDeepLink() {
      try {
        var q = new URLSearchParams(window.location.search);
        var qc = q.get('cat'), qf = q.get('from'), qt = q.get('to'), qv = q.get('v');
        if (qc && !only && DATA[qc]) { selectCat(qc); }
        var d = DATA[current];
        var has = function (k) { return d && d.base && (d.base[k] !== undefined) || (d && d.temp && ['C', 'F', 'K'].indexOf(k) !== -1); };
        if (qf && has(qf)) fromSel.value = qf;
        if (qt && has(qt)) toSel.value = qt;
        if (qv !== null && qv !== '' && isFinite(parseFloat(qv))) { fromInput.value = qv; }
        if (qf || qt || qv) convert(false);
      } catch (e) { /* no-op */ }
    })();
  }

  /* Expose deterministic data + math for the Smart Search module (single source of truth). */
  window.NexConvert = {
    DATA: DATA,
    tempConvert: tempConvert,
    fuel: function (v, f, t) { return kmLToUnit(fuelToKmL(v, f), t); },
    convert: function (cat, from, to, v) {
      var d = DATA[cat]; if (!d) return NaN;
      if (d.temp) return tempConvert(v, from, to);
      if (d.special === 'fuel') return kmLToUnit(fuelToKmL(v, from), to);
      return v * d.base[from] / d.base[to];
    }
  };

  document.addEventListener('DOMContentLoaded', function () {
    var root = document.getElementById('converter-app');
    if (root) mount(root);
  });
})();
