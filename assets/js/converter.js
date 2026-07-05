/* Nexluna — premium unit conversion engine.
   14 categories · copy · history · favorites · keyboard shortcuts · share.
   Mount into #converter-app. data-only="length" restricts to one category. */
(function () {
  'use strict';

  /* ---------- Data (base-unit factor tables) ---------- */
  var DATA = {
    length: { icon: 'length', label: 'الطول', title: 'محول وحدات الطول',
      units: [['km','كيلومتر (km)'],['m','متر (m)'],['cm','سنتيمتر (cm)'],['mm','مليمتر (mm)'],['mi','ميل (mi)'],['yd','ياردة (yd)'],['ft','قدم (ft)'],['in','إنش (in)'],['nmi','ميل بحري (nmi)']],
      base: { km:1000, m:1, cm:0.01, mm:0.001, mi:1609.344, yd:0.9144, ft:0.3048, 'in':0.0254, nmi:1852 },
      formulas: ['1 متر = 100 سم = 1000 مم','1 كم = 1000 متر','1 ميل = 1.60934 كم','1 قدم = 0.3048 متر','1 إنش = 2.54 سم'],
      common: ['1 متر = 3.28084 قدم','1 كم = 0.621371 ميل','1 ياردة = 0.9144 متر','1 قدم = 12 إنش'] },
    weight: { icon: 'weight', label: 'الوزن', title: 'محول وحدات الوزن',
      units: [['t','طن (t)'],['kg','كيلوغرام (kg)'],['g','غرام (g)'],['mg','مليغرام (mg)'],['lb','رطل (lb)'],['oz','أونصة (oz)'],['st','ستون (st)'],['ct','قيراط (ct)']],
      base: { t:1000, kg:1, g:0.001, mg:0.000001, lb:0.45359237, oz:0.028349523, st:6.35029318, ct:0.0002 },
      formulas: ['1 كغ = 1000 غرام','1 طن = 1000 كغ','1 رطل = 0.453592 كغ','1 أونصة = 28.3495 غرام'],
      common: ['1 كغ = 2.20462 رطل','1 رطل = 16 أونصة','1 طن = 2204.62 رطل'] },
    area: { icon: 'area', label: 'المساحة', title: 'محول وحدات المساحة',
      units: [['km2','كم مربع (km²)'],['m2','متر مربع (m²)'],['cm2','سم مربع (cm²)'],['ha','هكتار (ha)'],['acre','فدان (acre)'],['ft2','قدم مربع (ft²)'],['in2','إنش مربع (in²)'],['mi2','ميل مربع (mi²)']],
      base: { km2:1000000, m2:1, cm2:0.0001, ha:10000, acre:4046.8564224, ft2:0.09290304, in2:0.00064516, mi2:2589988.11 },
      formulas: ['1 م² = 10,000 سم²','1 كم² = 1,000,000 م²','1 هكتار = 10,000 م²','1 فدان = 4046.86 م²'],
      common: ['1 هكتار = 2.47105 فدان','1 م² = 10.7639 قدم²','1 فدان = 43,560 قدم²'] },
    volume: { icon: 'volume', label: 'الحجم', title: 'محول الحجم والسعة',
      units: [['m3','متر مكعب (m³)'],['L','لتر (L)'],['mL','مليلتر (mL)'],['gal','جالون (gal)'],['qt','كوارت (qt)'],['pt','باينت (pt)'],['cup','كوب (cup)'],['floz','أونصة سائلة (fl oz)'],['tbsp','ملعقة كبيرة'],['tsp','ملعقة صغيرة']],
      base: { m3:1000, L:1, mL:0.001, gal:3.785411784, qt:0.946352946, pt:0.473176473, cup:0.2365882365, floz:0.0295735296, tbsp:0.0147867648, tsp:0.0049289216 },
      formulas: ['1 لتر = 1000 مل','1 م³ = 1000 لتر','1 جالون = 3.78541 لتر','1 كوب = 236.588 مل'],
      common: ['1 لتر = 0.264172 جالون','1 جالون = 4 كوارت','1 كوب = 8 أونصة سائلة'] },
    temperature: { icon: 'temperature', label: 'الحرارة', title: 'محول درجة الحرارة', temp: true,
      units: [['C','سيلسيوس (°C)'],['F','فهرنهايت (°F)'],['K','كلفن (K)']],
      formulas: ['°F = (°C × 9/5) + 32','°C = (°F − 32) × 5/9','K = °C + 273.15'],
      common: ['تجمّد الماء: 0°C = 32°F = 273.15K','غليان الماء: 100°C = 212°F = 373.15K'] },
    data: { icon: 'data', label: 'البيانات', title: 'محول وحدات البيانات الرقمية',
      units: [['bit','بت (bit)'],['B','بايت (B)'],['KB','كيلوبايت (KB)'],['MB','ميغابايت (MB)'],['GB','غيغابايت (GB)'],['TB','تيرابايت (TB)'],['KiB','كيبي بايت (KiB)'],['MiB','ميبي بايت (MiB)'],['GiB','غيبي بايت (GiB)']],
      base: { bit:0.125, B:1, KB:1000, MB:1000000, GB:1000000000, TB:1000000000000, KiB:1024, MiB:1048576, GiB:1073741824 },
      formulas: ['1 بايت = 8 بت','1 كيلوبايت = 1000 بايت','1 ميغابايت = 1000 كيلوبايت','1 كيبي بايت = 1024 بايت'],
      common: ['1 غيغابايت = 1000 ميغابايت','1 تيرابايت = 1000 غيغابايت','1 ميبي بايت = 1,048,576 بايت'] },
    speed: { icon: 'speed', label: 'السرعة', title: 'محول وحدات السرعة',
      units: [['kmh','كم/ساعة (km/h)'],['ms','متر/ثانية (m/s)'],['mph','ميل/ساعة (mph)'],['knot','عقدة (knot)'],['fts','قدم/ثانية (ft/s)']],
      base: { kmh:1, ms:3.6, mph:1.609344, knot:1.852, fts:1.09728 },
      formulas: ['1 م/ث = 3.6 كم/س','1 ميل/س = 1.60934 كم/س','1 عقدة = 1.852 كم/س'],
      common: ['100 كم/س = 27.78 م/ث','60 ميل/س = 96.56 كم/س','1 عقدة = 1.15078 ميل/س'] },
    time: { icon: 'time', label: 'الوقت', title: 'محول وحدات الوقت',
      units: [['ms','مليثانية (ms)'],['s','ثانية (s)'],['min','دقيقة (min)'],['h','ساعة (h)'],['day','يوم'],['week','أسبوع'],['month','شهر'],['year','سنة']],
      base: { ms:0.001, s:1, min:60, h:3600, day:86400, week:604800, month:2629800, year:31557600 },
      formulas: ['1 دقيقة = 60 ثانية','1 ساعة = 3600 ثانية','1 يوم = 24 ساعة','1 سنة ≈ 365.25 يوم'],
      common: ['1 أسبوع = 7 أيام','1 شهر ≈ 30.44 يوم','1 سنة = 12 شهر'] },
    pressure: { icon: 'pressure', label: 'الضغط', title: 'محول وحدات الضغط',
      units: [['pa','باسكال (Pa)'],['kpa','كيلوباسكال (kPa)'],['bar','بار (bar)'],['atm','ضغط جوي (atm)'],['psi','psi'],['mmhg','ملم زئبق (mmHg)'],['torr','تور (Torr)']],
      base: { pa:1, kpa:1000, bar:100000, atm:101325, psi:6894.757293, mmhg:133.322368, torr:133.322368 },
      formulas: ['1 بار = 100,000 باسكال','1 ضغط جوي = 101,325 باسكال','1 psi ≈ 6894.76 باسكال'],
      common: ['1 atm = 1.01325 بار','1 بار = 14.5038 psi','1 atm = 760 ملم زئبق'] },
    energy: { icon: 'energy', label: 'الطاقة', title: 'محول وحدات الطاقة',
      units: [['j','جول (J)'],['kj','كيلوجول (kJ)'],['cal','سعرة (cal)'],['kcal','كيلوسعرة (kcal)'],['wh','واط·ساعة (Wh)'],['kwh','كيلوواط·ساعة (kWh)'],['btu','BTU'],['ev','إلكترون فولت (eV)']],
      base: { j:1, kj:1000, cal:4.184, kcal:4184, wh:3600, kwh:3600000, btu:1055.05585, ev:1.602176634e-19 },
      formulas: ['1 كيلوجول = 1000 جول','1 كيلوسعرة = 4184 جول','1 كيلوواط·ساعة = 3,600,000 جول'],
      common: ['1 kWh = 860.42 كيلوسعرة','1 BTU = 1055.06 جول','1 سعرة = 4.184 جول'] },
    power: { icon: 'power', label: 'القدرة', title: 'محول وحدات القدرة',
      units: [['w','واط (W)'],['kw','كيلوواط (kW)'],['mw','ميغاواط (MW)'],['hp','حصان (hp)'],['btuh','BTU/ساعة']],
      base: { w:1, kw:1000, mw:1000000, hp:745.699872, btuh:0.293071 },
      formulas: ['1 كيلوواط = 1000 واط','1 حصان ≈ 745.7 واط','1 ميغاواط = 1,000,000 واط'],
      common: ['1 hp = 0.7457 كيلوواط','1 كيلوواط = 1.34102 حصان'] },
    angle: { icon: 'angle', label: 'الزوايا', title: 'محول وحدات الزوايا',
      units: [['deg','درجة (°)'],['rad','راديان (rad)'],['grad','غراد (grad)'],['arcmin','دقيقة قوسية'],['arcsec','ثانية قوسية'],['turn','دورة']],
      base: { deg:1, rad:57.29577951, grad:0.9, arcmin:0.016666667, arcsec:0.000277778, turn:360 },
      formulas: ['180 درجة = π راديان','1 دورة = 360 درجة','1 درجة = 60 دقيقة قوسية'],
      common: ['1 راديان ≈ 57.2958 درجة','90 درجة = 100 غراد','1 دورة = 2π راديان'] },
    fuel: { icon: 'fuel', label: 'الوقود', title: 'محول استهلاك الوقود',
      units: [['kml','كم/لتر (km/L)'],['l100','لتر/100كم (L/100km)'],['mpg','ميل/جالون (mpg)']],
      special: 'fuel',
      formulas: ['km/L → L/100km: 100 ÷ (km/L)','mpg → km/L: mpg × 0.425144','L/100km → km/L: 100 ÷ (L/100km)'],
      common: ['10 كم/لتر = 10 لتر/100كم','30 mpg ≈ 12.75 كم/لتر','5 لتر/100كم = 20 كم/لتر'] },
    frequency: { icon: 'frequency', label: 'التردد', title: 'محول وحدات التردد',
      units: [['hz','هيرتز (Hz)'],['khz','كيلوهيرتز (kHz)'],['mhz','ميغاهيرتز (MHz)'],['ghz','غيغاهيرتز (GHz)'],['rpm','دورة/دقيقة (rpm)']],
      base: { hz:1, khz:1000, mhz:1000000, ghz:1000000000, rpm:0.016666667 },
      formulas: ['1 كيلوهيرتز = 1000 هيرتز','1 ميغاهيرتز = 1000 كيلوهيرتز','1 هيرتز = 60 دورة/دقيقة'],
      common: ['1 GHz = 1000 MHz','60 rpm = 1 هيرتز'] }
  };

  var STORE = { hist: 'nx-history', fav: 'nx-favorites' };

  /* ---------- Helpers ---------- */
  function tempConvert(v, f, t) { var c = f === 'C' ? v : f === 'F' ? (v - 32) * 5 / 9 : v - 273.15; return t === 'C' ? c : t === 'F' ? c * 9 / 5 + 32 : c + 273.15; }
  function fuelToKmL(v, u) { return u === 'kml' ? v : u === 'l100' ? 100 / v : v * 0.425143707; }
  function kmLToUnit(v, u) { return u === 'kml' ? v : u === 'l100' ? 100 / v : v / 0.425143707; }
  function fmt(n) { if (!isFinite(n)) return '—'; var r = Math.round(n * 1e6) / 1e6; return r.toLocaleString('en-US', { maximumFractionDigits: 6 }); }
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

  /* ---------- Mount ---------- */
  function mount(root) {
    var only = root.getAttribute('data-only');
    var cats = only ? [only] : Object.keys(DATA);
    var current = cats[0];

    var tabs = el('div', { class: 'tabs', role: 'tablist', 'aria-label': 'فئات التحويل' });
    if (!only) cats.forEach(function (c) {
      var b = el('button', { class: 'tab-btn', role: 'tab', type: 'button', id: 'tab-' + c, 'aria-selected': String(c === current), 'data-cat': c });
      b.innerHTML = ic(DATA[c].icon) + '<span>' + DATA[c].label + '</span>';
      tabs.appendChild(b);
    });

    /* Toolbar: title + favorite + copy */
    var titleEl = el('span', { class: 'converter-title' }, DATA[current].title);
    var favBtn = el('button', { class: 'pill-btn', type: 'button', 'data-fav': '', 'aria-pressed': 'false', title: 'حفظ كمفضّلة' });
    favBtn.innerHTML = ic('star') + '<span>مفضّلة</span>';
    var toolbar = el('div', { class: 'converter-toolbar' });
    var tRight = el('div', { class: 'toolbar-actions' });
    tRight.appendChild(favBtn);
    toolbar.appendChild(titleEl); toolbar.appendChild(tRight);

    /* Inputs */
    var fromSel = el('select', { id: 'nx-from', 'aria-label': 'الوحدة المصدر' });
    var toSel = el('select', { id: 'nx-to', 'aria-label': 'الوحدة الهدف' });
    var fromInput = el('input', { id: 'nx-in', type: 'number', inputmode: 'decimal', placeholder: 'أدخل القيمة', 'aria-label': 'القيمة المدخلة', 'aria-describedby': 'nx-result' });
    var toInput = el('input', { id: 'nx-out', type: 'text', readonly: 'readonly', 'aria-label': 'القيمة الناتجة', tabindex: '-1' });
    var swap = el('button', { class: 'swap-btn', type: 'button', 'aria-label': 'تبديل الوحدات (زر التبديل)', title: 'تبديل (Enter)' }); swap.innerHTML = ic('swap');

    var f1 = el('div', { class: 'field' }); f1.appendChild(el('label', { for: 'nx-in' }, ic('arrow') + '<span>من</span>')); f1.appendChild(fromInput); f1.appendChild(fromSel);
    var f2 = el('div', { class: 'field' }); f2.appendChild(el('label', { for: 'nx-out' }, ic('check') + '<span>إلى</span>')); f2.appendChild(toInput); f2.appendChild(toSel);
    var grid = el('div', { class: 'conv-grid' }); grid.appendChild(f1); grid.appendChild(swap); grid.appendChild(f2);

    var result = el('div', { class: 'result', id: 'nx-result', role: 'status', 'aria-live': 'polite' }, '<span class="hint">أدخل قيمة لعرض النتيجة</span>');
    var copyBtn = el('button', { class: 'copy-result', type: 'button', 'aria-label': 'نسخ النتيجة', title: 'نسخ النتيجة' }); copyBtn.innerHTML = ic('copy'); copyBtn.style.display = 'none';
    result.appendChild(copyBtn);

    var info = el('div', { class: 'info-block' });

    /* History */
    var histWrap = el('div', { class: 'history' });
    var histHead = el('h3', null, '<span>' + ic('history') + ' آخر التحويلات</span>');
    var clearBtn = el('button', { class: 'clear', type: 'button' }, 'مسح الكل');
    histHead.appendChild(clearBtn);
    var histList = el('div', { class: 'history-list' });
    histWrap.appendChild(histHead); histWrap.appendChild(histList);

    var panel = el('div', { id: 'panel', role: 'tabpanel' });
    panel.appendChild(toolbar); panel.appendChild(grid); panel.appendChild(result); panel.appendChild(histWrap); panel.appendChild(info);
    if (!only) root.appendChild(tabs);
    root.appendChild(panel);

    var lastResult = '';

    function fillUnits() {
      var d = DATA[current]; var opts = (d.units || []).map(function (u) { return '<option value="' + u[0] + '">' + u[1] + '</option>'; }).join('');
      fromSel.innerHTML = opts; toSel.innerHTML = opts;
      fromSel.selectedIndex = 0; toSel.selectedIndex = Math.min(1, d.units.length - 1);
    }
    function renderInfo() {
      var d = DATA[current]; info.innerHTML = '';
      info.appendChild(el('h3', { style: 'margin-bottom:var(--sp-2)' }, 'صيغ التحويل'));
      info.appendChild(el('div', { class: 'formula' }, d.formulas.join('<br>')));
      info.appendChild(el('h3', { style: 'margin:var(--sp-4) 0 var(--sp-2)' }, 'تحويلات شائعة'));
      var ul = el('ul', { class: 'conv-list' }); d.common.forEach(function (c) { ul.appendChild(el('li', null, c)); }); info.appendChild(ul);
    }
    function calc(v) {
      var d = DATA[current];
      if (d.temp) return tempConvert(v, fromSel.value, toSel.value);
      if (d.special === 'fuel') return kmLToUnit(fuelToKmL(v, fromSel.value), toSel.value);
      return v * d.base[fromSel.value] / d.base[toSel.value];
    }
    function convert(pushHist) {
      var raw = fromInput.value.trim();
      if (raw === '') { toInput.value = ''; fromInput.removeAttribute('aria-invalid'); result.className = 'result'; result.innerHTML = '<span class="hint">أدخل قيمة لعرض النتيجة</span>'; result.appendChild(copyBtn); copyBtn.style.display = 'none'; return; }
      var v = parseFloat(raw);
      if (isNaN(v)) { fromInput.setAttribute('aria-invalid', 'true'); result.className = 'result error'; result.innerHTML = '<span class="value">قيمة غير صحيحة — أدخل رقمًا</span>'; result.appendChild(copyBtn); copyBtn.style.display = 'none'; toInput.value = ''; return; }
      fromInput.removeAttribute('aria-invalid');
      var out = calc(v); toInput.value = fmt(out);
      var fu = fromSel.options[fromSel.selectedIndex].text, tu = toSel.options[toSel.selectedIndex].text;
      lastResult = fmt(v) + ' ' + fu + ' = ' + fmt(out) + ' ' + tu;
      result.className = 'result';
      result.innerHTML = '<div><span class="value">' + fmt(v) + ' → ' + fmt(out) + '</span><div class="hint">' + fu + ' = ' + tu + '</div></div>';
      result.appendChild(copyBtn); copyBtn.style.display = 'grid';
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
      if (!h.length) { histList.appendChild(el('div', { class: 'history-empty' }, 'لا توجد تحويلات محفوظة بعد.')); return; }
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
      favBtn.innerHTML = ic(on ? 'star-fill' : 'star') + '<span>' + (on ? 'محفوظة' : 'مفضّلة') + '</span>';
    }
    function selectCat(cat) {
      current = cat; titleEl.textContent = DATA[cat].title;
      tabs.querySelectorAll('.tab-btn').forEach(function (b) { b.setAttribute('aria-selected', String(b.getAttribute('data-cat') === cat)); });
      fillUnits(); renderInfo(); updateFav(); fromInput.value = ''; convert(false);
    }

    /* Events */
    tabs.addEventListener('click', function (e) { var b = e.target.closest('.tab-btn'); if (b) selectCat(b.getAttribute('data-cat')); });
    var debounce; fromInput.addEventListener('input', function () { clearTimeout(debounce); convert(false); debounce = setTimeout(function () { if (fromInput.value.trim() !== '') convert(true); }, 900); });
    fromSel.addEventListener('change', function () { convert(true); });
    toSel.addEventListener('change', function () { convert(true); });
    swap.addEventListener('click', function () { var t = fromSel.value; fromSel.value = toSel.value; toSel.value = t; if (toInput.value) fromInput.value = toInput.value.replace(/,/g, ''); convert(true); });
    copyBtn.addEventListener('click', function () { if (!toInput.value) return; navigator.clipboard && navigator.clipboard.writeText(lastResult).then(function () { toast('تم نسخ النتيجة ✓'); }).catch(function () { toast('تعذّر النسخ'); }); });
    favBtn.addEventListener('click', function () { var favs = ls(STORE.fav, []); var i = favs.indexOf(current); if (i === -1) { favs.push(current); toast('أُضيفت إلى المفضّلة ★'); } else { favs.splice(i, 1); toast('أُزيلت من المفضّلة'); } save(STORE.fav, favs); updateFav(); });
    clearBtn.addEventListener('click', function () { save(STORE.hist, []); renderHistory(); toast('تم مسح السجل'); });

    /* Keyboard: Enter = swap, Escape = clear */
    root.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' && document.activeElement === fromInput) { e.preventDefault(); swap.click(); }
      else if (e.key === 'Escape') { fromInput.value = ''; convert(false); fromInput.focus(); }
    });

    fillUnits(); renderInfo(); updateFav(); renderHistory();
  }

  document.addEventListener('DOMContentLoaded', function () {
    var root = document.getElementById('converter-app');
    if (root) mount(root);
  });
})();
