/* Nexluna — Smart Conversion Search (scoped, deterministic, zero-cost NLP).
   Understands free-text Arabic + English queries over the site's OWN 14 categories
   and answers inline — always correct, instant, no external API, no hallucination.
   Examples it handles:
     "5 كم بالميل"        "كم قدم في المتر"     "٢٠ درجة مئوية بالفهرنهايت"
     "5 km to mi"          "20 celsius to fahrenheit"   "1 gb in mb"   "100 كجم رطل"
   Author: mohamed-khairy-5i */
(function () {
  'use strict';

  /* Unit lexicon: many Arabic + English aliases → canonical [category, unitKey].
     Kept in sync with converter.js DATA keys. */
  var U = {
    // length
    'كم': ['length', 'km'], 'كيلومتر': ['length', 'km'], 'كيلو متر': ['length', 'km'], 'km': ['length', 'km'], 'kilometer': ['length', 'km'], 'kilometre': ['length', 'km'],
    'متر': ['length', 'm'], 'متر واحد': ['length', 'm'], 'm': ['length', 'm'], 'meter': ['length', 'm'], 'metre': ['length', 'm'],
    'سم': ['length', 'cm'], 'سنتيمتر': ['length', 'cm'], 'سنتي متر': ['length', 'cm'], 'cm': ['length', 'cm'], 'centimeter': ['length', 'cm'],
    'مم': ['length', 'mm'], 'مليمتر': ['length', 'mm'], 'ملم': ['length', 'mm'], 'mm': ['length', 'mm'], 'millimeter': ['length', 'mm'],
    'ميل': ['length', 'mi'], 'اميال': ['length', 'mi'], 'أميال': ['length', 'mi'], 'mi': ['length', 'mi'], 'mile': ['length', 'mi'], 'miles': ['length', 'mi'],
    'ياردة': ['length', 'yd'], 'يارده': ['length', 'yd'], 'yd': ['length', 'yd'], 'yard': ['length', 'yd'],
    'قدم': ['length', 'ft'], 'اقدام': ['length', 'ft'], 'أقدام': ['length', 'ft'], 'ft': ['length', 'ft'], 'foot': ['length', 'ft'], 'feet': ['length', 'ft'],
    'انش': ['length', 'in'], 'إنش': ['length', 'in'], 'بوصة': ['length', 'in'], 'in': ['length', 'in'], 'inch': ['length', 'in'], 'inches': ['length', 'in'],
    // weight
    'طن': ['weight', 't'], 'ton': ['weight', 't'], 'tonne': ['weight', 't'],
    'كجم': ['weight', 'kg'], 'كغ': ['weight', 'kg'], 'كيلوغرام': ['weight', 'kg'], 'كيلوجرام': ['weight', 'kg'], 'كيلو': ['weight', 'kg'], 'kg': ['weight', 'kg'], 'kilogram': ['weight', 'kg'], 'kilo': ['weight', 'kg'],
    'غرام': ['weight', 'g'], 'جرام': ['weight', 'g'], 'جم': ['weight', 'g'], 'g': ['weight', 'g'], 'gram': ['weight', 'g'], 'grams': ['weight', 'g'],
    'مليغرام': ['weight', 'mg'], 'مليجرام': ['weight', 'mg'], 'mg': ['weight', 'mg'], 'milligram': ['weight', 'mg'],
    'رطل': ['weight', 'lb'], 'باوند': ['weight', 'lb'], 'lb': ['weight', 'lb'], 'lbs': ['weight', 'lb'], 'pound': ['weight', 'lb'], 'pounds': ['weight', 'lb'],
    'اونصة': ['weight', 'oz'], 'أونصة': ['weight', 'oz'], 'اوقية': ['weight', 'oz'], 'oz': ['weight', 'oz'], 'ounce': ['weight', 'oz'],
    // temperature
    'مئوية': ['temperature', 'C'], 'سيلسيوس': ['temperature', 'C'], 'سلسيوس': ['temperature', 'C'], 'درجة مئوية': ['temperature', 'C'], 'celsius': ['temperature', 'C'], 'c': ['temperature', 'C'],
    'فهرنهايت': ['temperature', 'F'], 'فهرنهيت': ['temperature', 'F'], 'fahrenheit': ['temperature', 'F'], 'f': ['temperature', 'F'],
    'كلفن': ['temperature', 'K'], 'كلفين': ['temperature', 'K'], 'kelvin': ['temperature', 'K'], 'k': ['temperature', 'K'],
    // data
    'بايت': ['data', 'B'], 'byte': ['data', 'B'], 'bytes': ['data', 'B'], 'b': ['data', 'B'],
    'كيلوبايت': ['data', 'KB'], 'kb': ['data', 'KB'], 'kilobyte': ['data', 'KB'],
    'ميغابايت': ['data', 'MB'], 'ميجابايت': ['data', 'MB'], 'mb': ['data', 'MB'], 'megabyte': ['data', 'MB'],
    'غيغابايت': ['data', 'GB'], 'جيجابايت': ['data', 'GB'], 'جيغابايت': ['data', 'GB'], 'gb': ['data', 'GB'], 'gigabyte': ['data', 'GB'],
    'تيرابايت': ['data', 'TB'], 'tb': ['data', 'TB'], 'terabyte': ['data', 'TB'],
    'بت': ['data', 'bit'], 'bit': ['data', 'bit'], 'bits': ['data', 'bit'],
    // speed
    'كم/ساعة': ['speed', 'kmh'], 'كم بالساعة': ['speed', 'kmh'], 'kmh': ['speed', 'kmh'], 'kph': ['speed', 'kmh'],
    'ميل/ساعة': ['speed', 'mph'], 'mph': ['speed', 'mph'],
    'عقدة': ['speed', 'knot'], 'knot': ['speed', 'knot'], 'knots': ['speed', 'knot'],
    // volume
    'لتر': ['volume', 'L'], 'liter': ['volume', 'L'], 'litre': ['volume', 'L'], 'l': ['volume', 'L'],
    'مليلتر': ['volume', 'mL'], 'مل': ['volume', 'mL'], 'ml': ['volume', 'mL'], 'milliliter': ['volume', 'mL'],
    'جالون': ['volume', 'gal'], 'غالون': ['volume', 'gal'], 'gal': ['volume', 'gal'], 'gallon': ['volume', 'gal'],
    'كوب': ['volume', 'cup'], 'cup': ['volume', 'cup'],
    // time
    'ثانية': ['time', 's'], 'ثواني': ['time', 's'], 'second': ['time', 's'], 'seconds': ['time', 's'], 'sec': ['time', 's'],
    'دقيقة': ['time', 'min'], 'دقائق': ['time', 'min'], 'minute': ['time', 'min'], 'min': ['time', 'min'],
    'ساعة': ['time', 'h'], 'ساعات': ['time', 'h'], 'hour': ['time', 'h'], 'hours': ['time', 'h'], 'hr': ['time', 'h'],
    'يوم': ['time', 'day'], 'ايام': ['time', 'day'], 'أيام': ['time', 'day'], 'day': ['time', 'day'], 'days': ['time', 'day'],
    'اسبوع': ['time', 'week'], 'أسبوع': ['time', 'week'], 'week': ['time', 'week'],
    // area
    'م2': ['area', 'm2'], 'متر مربع': ['area', 'm2'], 'm2': ['area', 'm2'],
    'كم2': ['area', 'km2'], 'كيلومتر مربع': ['area', 'km2'], 'km2': ['area', 'km2'],
    'هكتار': ['area', 'ha'], 'hectare': ['area', 'ha'], 'ha': ['area', 'ha'],
    'فدان': ['area', 'acre'], 'acre': ['area', 'acre']
  };

  var CAT_LABEL = {
    length: 'الطول', weight: 'الوزن', temperature: 'الحرارة', data: 'البيانات',
    speed: 'السرعة', volume: 'الحجم', time: 'الوقت', area: 'المساحة'
  };

  /* Question words / connectors that are never units (esp. "كم" = "how much"). */
  var STOP = { 'في': 1, 'الى': 1, 'إلى': 1, 'من': 1, 'to': 1, 'in': 1, 'into': 1, 'is': 1, 'how': 1, 'many': 1, 'much': 1, 'convert': 1, 'كام': 1, 'يساوي': 1, 'تساوي': 1, 'بكم': 1, 'وكم': 1 };

  /* Strip Arabic definite-article / preposition prefixes so "بالميل"→"ميل", "المتر"→"متر".
     Only strips when the remainder is a known unit token (avoids mangling real words). */
  function stripPrefix(tok) {
    if (U[tok]) return tok;                       // already a unit → leave it
    var pres = ['بال', 'وال', 'فال', 'كال', 'لل', 'ال', 'بـ', 'ب', 'و', 'ف'];
    for (var i = 0; i < pres.length; i++) {
      var p = pres[i];
      if (tok.length > p.length && tok.slice(0, p.length) === p) {
        var rest = tok.slice(p.length);
        if (U[rest]) return rest;
      }
    }
    return tok;
  }

  /* Normalize Arabic: strip diacritics, unify alef/hamza/ta-marbuta, map Arabic digits. */
  function normalize(s) {
    return s.toLowerCase()
      .replace(/[\u064B-\u065F\u0670]/g, '')
      .replace(/[٠۰]/g, '0').replace(/[١۱]/g, '1').replace(/[٢۲]/g, '2').replace(/[٣۳]/g, '3').replace(/[٤۴]/g, '4')
      .replace(/[٥۵]/g, '5').replace(/[٦۶]/g, '6').replace(/[٧۷]/g, '7').replace(/[٨۸]/g, '8').replace(/[٩۹]/g, '9')
      .replace(/[إأآ]/g, 'ا')
      .replace(/[\/]/g, ' / ')
      .replace(/\s+/g, ' ').trim();
  }

  /* Longest-match unit lookup over a token list starting at index i. Returns [unit, tokensConsumed]. */
  var UNIT_KEYS = Object.keys(U).sort(function (a, b) { return b.split(' ').length - a.split(' ').length; });
  function matchUnit(tokens, i) {
    for (var k = 0; k < UNIT_KEYS.length; k++) {
      var parts = UNIT_KEYS[k].split(' ');
      if (parts.length > tokens.length - i) continue;
      var ok = true;
      for (var j = 0; j < parts.length; j++) { if (tokens[i + j] !== parts[j]) { ok = false; break; } }
      if (ok) return [U[UNIT_KEYS[k]], parts.length];
    }
    return null;
  }

  function parse(query) {
    var norm = normalize(query);
    var tokens = norm.split(' ').filter(Boolean).map(stripPrefix);
    // A leading "كم" with no explicit digit is the question word "how much", not kilometre.
    var hasDigit = tokens.some(function (t) { return /^-?\d+(\.\d+)?$/.test(t); });
    if (!hasDigit && (tokens[0] === 'كم' || tokens[0] === 'كام')) tokens[0] = '__q__';
    var num = null, units = [];
    for (var i = 0; i < tokens.length;) {
      // number (allow decimals + leading sign)
      if (num === null && /^-?\d+(\.\d+)?$/.test(tokens[i])) { num = parseFloat(tokens[i]); i++; continue; }
      if (STOP[tokens[i]] || tokens[i] === '__q__') { i++; continue; }
      var m = matchUnit(tokens, i);
      if (m) { units.push(m[0]); i += m[1]; }
      else i++;
    }
    if (units.length < 1) return null;
    // Need two units of the SAME category to convert.
    var from = null, to = null;
    for (var a = 0; a < units.length; a++) {
      for (var b = a + 1; b < units.length; b++) {
        if (units[a][0] === units[b][0]) { from = units[a]; to = units[b]; break; }
      }
      if (from) break;
    }
    if (!from) return null;
    if (num === null) num = 1; // "كم قدم في المتر" → assume 1
    return { cat: from[0], from: from[1], to: to[1], value: num };
  }

  /* Deterministic math — mirrors converter.js exactly. */
  var BASE = null;
  function ensureData() {
    if (BASE || !window.NexConvert) return;
    BASE = window.NexConvert.DATA;
  }
  function compute(r) {
    ensureData();
    if (!BASE || !BASE[r.cat]) return null;
    var d = BASE[r.cat];
    var out;
    if (d.temp) { out = window.NexConvert.tempConvert(r.value, r.from, r.to); }
    else if (d.special === 'fuel') { out = window.NexConvert.fuel(r.value, r.from, r.to); }
    else { out = r.value * d.base[r.from] / d.base[r.to]; }
    return out;
  }
  function label(cat, key) {
    ensureData();
    if (!BASE) return key;
    var u = (BASE[cat].units || []).filter(function (x) { return x[0] === key; })[0];
    return u ? u[1] : key;
  }
  function fmt(n) { if (!isFinite(n)) return '—'; var r = Math.round(n * 1e6) / 1e6; return r.toLocaleString('en-US', { maximumFractionDigits: 6 }); }

  /* ---------- UI ---------- */
  function mount(host) {
    var box = document.createElement('div');
    box.className = 'smart-search';
    box.innerHTML =
      '<label class="ss-label" for="ss-input">' + (window.NexIcons ? window.NexIcons.get('search') : '') +
      ' اكتب سؤالك بالعربي أو الإنجليزي</label>' +
      '<div class="ss-field"><input id="ss-input" type="text" autocomplete="off" ' +
      'placeholder="مثال: 5 كم بالميل &nbsp; · &nbsp; كم قدم في المتر &nbsp; · &nbsp; 100 celsius to f" ' +
      'aria-describedby="ss-out"></div>' +
      '<div id="ss-out" class="ss-out" role="status" aria-live="polite"></div>' +
      '<div class="ss-chips">' +
      ['5 كم بالميل', '100 كجم رطل', '20 celsius to fahrenheit', '1 gb in mb', 'كم قدم في المتر']
        .map(function (q) { return '<button type="button" class="ss-chip">' + q + '</button>'; }).join('') +
      '</div>';
    host.appendChild(box);

    var input = box.querySelector('#ss-input');
    var out = box.querySelector('#ss-out');

    function run(q) {
      q = (q || '').trim();
      if (!q) { out.className = 'ss-out'; out.innerHTML = ''; return; }
      var r = parse(q);
      if (!r) {
        out.className = 'ss-out ss-hint';
        out.innerHTML = 'لم أفهم الطلب — جرّب صيغة مثل «5 كم بالميل» أو «100 celsius to f».';
        return;
      }
      var res = compute(r);
      if (res === null || !isFinite(res)) {
        out.className = 'ss-out ss-hint';
        out.innerHTML = 'تعذّر الحساب لهذه الوحدات.';
        return;
      }
      out.className = 'ss-out ss-answer';
      out.innerHTML =
        '<div class="ss-ans-num" dir="ltr">' + fmt(r.value) + ' ' + label(r.cat, r.from) +
        ' <span class="ss-eq">=</span> <strong>' + fmt(res) + '</strong> ' + label(r.cat, r.to) + '</div>' +
        '<a class="ss-open" href="/converters/' + r.cat + '.html">افتح محوّل ' + (CAT_LABEL[r.cat] || '') +
        ' ' + (window.NexIcons ? window.NexIcons.get('arrow') : '') + '</a>';
    }

    var t;
    input.addEventListener('input', function () { clearTimeout(t); t = setTimeout(function () { run(input.value); }, 120); });
    input.addEventListener('keydown', function (e) { if (e.key === 'Enter') { e.preventDefault(); run(input.value); } });
    box.addEventListener('click', function (e) {
      var c = e.target.closest('.ss-chip');
      if (c) { input.value = c.textContent; run(c.textContent); input.focus(); }
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    var host = document.getElementById('smart-search');
    if (host) mount(host);
  });
})();
