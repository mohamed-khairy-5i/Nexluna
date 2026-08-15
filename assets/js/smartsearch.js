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
    'متر': ['length', 'm'], 'm': ['length', 'm'], 'meter': ['length', 'm'], 'metre': ['length', 'm'],
    'سم': ['length', 'cm'], 'سنتيمتر': ['length', 'cm'], 'سنتي متر': ['length', 'cm'], 'cm': ['length', 'cm'], 'centimeter': ['length', 'cm'],
    'مم': ['length', 'mm'], 'مليمتر': ['length', 'mm'], 'ملم': ['length', 'mm'], 'mm': ['length', 'mm'], 'millimeter': ['length', 'mm'],
    'ميل': ['length', 'mi'], 'اميال': ['length', 'mi'], 'أميال': ['length', 'mi'], 'mi': ['length', 'mi'], 'mile': ['length', 'mi'], 'miles': ['length', 'mi'],
    'ياردة': ['length', 'yd'], 'يارده': ['length', 'yd'], 'yd': ['length', 'yd'], 'yard': ['length', 'yd'],
    'قدم': ['length', 'ft'], 'اقدام': ['length', 'ft'], 'أقدام': ['length', 'ft'], 'ft': ['length', 'ft'], 'foot': ['length', 'ft'], 'feet': ['length', 'ft'],
    'انش': ['length', 'in'], 'إنش': ['length', 'in'], 'بوصة': ['length', 'in'], 'in': ['length', 'in'], 'inch': ['length', 'in'], 'inches': ['length', 'in'],
    'ميل بحري': ['length', 'nmi'], 'ميل/بحري': ['length', 'nmi'], 'nmi': ['length', 'nmi'], 'nautical mile': ['length', 'nmi'],
    // weight
    'طن': ['weight', 't'], 'ton': ['weight', 't'], 'tonne': ['weight', 't'],
    'كجم': ['weight', 'kg'], 'كغ': ['weight', 'kg'], 'كيلوغرام': ['weight', 'kg'], 'كيلوجرام': ['weight', 'kg'], 'كيلو': ['weight', 'kg'], 'kg': ['weight', 'kg'], 'kilogram': ['weight', 'kg'], 'kilo': ['weight', 'kg'],
    'غرام': ['weight', 'g'], 'جرام': ['weight', 'g'], 'جم': ['weight', 'g'], 'g': ['weight', 'g'], 'gram': ['weight', 'g'], 'grams': ['weight', 'g'],
    'مليغرام': ['weight', 'mg'], 'مليجرام': ['weight', 'mg'], 'mg': ['weight', 'mg'], 'milligram': ['weight', 'mg'],
    'رطل': ['weight', 'lb'], 'باوند': ['weight', 'lb'], 'lb': ['weight', 'lb'], 'lbs': ['weight', 'lb'], 'pound': ['weight', 'lb'], 'pounds': ['weight', 'lb'],
    'اونصة': ['weight', 'oz'], 'أونصة': ['weight', 'oz'], 'اوقية': ['weight', 'oz'], 'oz': ['weight', 'oz'], 'ounce': ['weight', 'oz'],
    'ستون': ['weight', 'st'], 'stone': ['weight', 'st'], 'st': ['weight', 'st'], 'قيراط ذهب': ['weight', 'ct'], 'carat': ['weight', 'ct'], 'ct': ['weight', 'ct'],
    // temperature
    'مئوية': ['temperature', 'C'], 'سيلسيوس': ['temperature', 'C'], 'سلسيوس': ['temperature', 'C'], 'درجة مئوية': ['temperature', 'C'], 'celsius': ['temperature', 'C'], 'c': ['temperature', 'C'],
    'فهرنهايت': ['temperature', 'F'], 'فهرنهيت': ['temperature', 'F'], 'fahrenheit': ['temperature', 'F'], 'f': ['temperature', 'F'],
    'كلفن': ['temperature', 'K'], 'كلفين': ['temperature', 'K'], 'kelvin': ['temperature', 'K'], 'k': ['temperature', 'K'],
    // data
    'بت': ['data', 'bit'], 'bit': ['data', 'bit'], 'bits': ['data', 'bit'],
    'بايت': ['data', 'B'], 'byte': ['data', 'B'], 'bytes': ['data', 'B'], 'b': ['data', 'B'],
    'كيلوبايت': ['data', 'KB'], 'kb': ['data', 'KB'], 'kilobyte': ['data', 'KB'],
    'ميغابايت': ['data', 'MB'], 'ميجابايت': ['data', 'MB'], 'mb': ['data', 'MB'], 'megabyte': ['data', 'MB'],
    'غيغابايت': ['data', 'GB'], 'جيجابايت': ['data', 'GB'], 'جيغابايت': ['data', 'GB'], 'gb': ['data', 'GB'], 'gigabyte': ['data', 'GB'],
    'تيرابايت': ['data', 'TB'], 'tb': ['data', 'TB'], 'terabyte': ['data', 'TB'],
    'كيبي بايت': ['data', 'KiB'], 'kib': ['data', 'KiB'], 'kibibyte': ['data', 'KiB'],
    'ميبي بايت': ['data', 'MiB'], 'mib': ['data', 'MiB'], 'mebibyte': ['data', 'MiB'],
    'غيبي بايت': ['data', 'GiB'], 'gib': ['data', 'GiB'], 'gibibyte': ['data', 'GiB'],
    // speed
    'كم/ساعة': ['speed', 'kmh'], 'كم/س': ['speed', 'kmh'], 'كم بالساعة': ['speed', 'kmh'], 'km/h': ['speed', 'kmh'], 'kmh': ['speed', 'kmh'], 'kph': ['speed', 'kmh'],
    'ميل/ساعة': ['speed', 'mph'], 'ميل بالساعة': ['speed', 'mph'], 'mph': ['speed', 'mph'],
    'متر/ثانية': ['speed', 'ms'], 'م/ث': ['speed', 'ms'], 'm/s': ['speed', 'ms'], 'metre per second': ['speed', 'ms'],
    'قدم/ثانية': ['speed', 'fts'], 'قدم/ث': ['speed', 'fts'], 'ft/s': ['speed', 'fts'],
    'عقدة': ['speed', 'knot'], 'knot': ['speed', 'knot'], 'knots': ['speed', 'knot'],
    // volume
    'متر مكعب': ['volume', 'm3'], 'م3': ['volume', 'm3'], 'm3': ['volume', 'm3'], 'cubic meter': ['volume', 'm3'],
    'لتر': ['volume', 'L'], 'liter': ['volume', 'L'], 'litre': ['volume', 'L'], 'l': ['volume', 'L'],
    'مليلتر': ['volume', 'mL'], 'مل': ['volume', 'mL'], 'ml': ['volume', 'mL'], 'milliliter': ['volume', 'mL'],
    'جالون': ['volume', 'gal'], 'غالون': ['volume', 'gal'], 'gal': ['volume', 'gal'], 'gallon': ['volume', 'gal'], 'جالون امريكي': ['volume', 'gal'], 'us gal': ['volume', 'gal'],
    'جالون امبراطوري': ['volume', 'galUK'], 'جالون بريطاني': ['volume', 'galUK'], 'uk gal': ['volume', 'galUK'], 'galuk': ['volume', 'galUK'],
    'كوارت': ['volume', 'qt'], 'qt': ['volume', 'qt'], 'quart': ['volume', 'qt'], 'باينت': ['volume', 'pt'], 'pt': ['volume', 'pt'], 'pint': ['volume', 'pt'],
    'كوب': ['volume', 'cup'], 'cup': ['volume', 'cup'], 'اونصة سائلة': ['volume', 'floz'], 'fl oz': ['volume', 'floz'], 'floz': ['volume', 'floz'],
    'ملعقة كبيرة': ['volume', 'tbsp'], 'tbsp': ['volume', 'tbsp'], 'ملعقة صغيرة': ['volume', 'tsp'], 'tsp': ['volume', 'tsp'],
    // time
    'ملي ثانية': ['time', 'ms'], 'مللي ثانية': ['time', 'ms'], 'millisecond': ['time', 'ms'], 'milliseconds': ['time', 'ms'], 'ms': ['time', 'ms'],
    'ثانية': ['time', 's'], 'ثواني': ['time', 's'], 'second': ['time', 's'], 'seconds': ['time', 's'], 'sec': ['time', 's'],
    'دقيقة': ['time', 'min'], 'دقائق': ['time', 'min'], 'minute': ['time', 'min'], 'min': ['time', 'min'],
    'ساعة': ['time', 'h'], 'ساعات': ['time', 'h'], 'hour': ['time', 'h'], 'hours': ['time', 'h'], 'hr': ['time', 'h'],
    'يوم': ['time', 'day'], 'ايام': ['time', 'day'], 'أيام': ['time', 'day'], 'day': ['time', 'day'], 'days': ['time', 'day'],
    'اسبوع': ['time', 'week'], 'أسبوع': ['time', 'week'], 'week': ['time', 'week'], 'شهر': ['time', 'month'], 'month': ['time', 'month'], 'سنة': ['time', 'year'], 'عام': ['time', 'year'], 'year': ['time', 'year'],
    // area
    'م2': ['area', 'm2'], 'متر مربع': ['area', 'm2'], 'm2': ['area', 'm2'], 'square meter': ['area', 'm2'],
    'سم2': ['area', 'cm2'], 'سم مربع': ['area', 'cm2'], 'cm2': ['area', 'cm2'], 'square centimeter': ['area', 'cm2'],
    'كم2': ['area', 'km2'], 'كيلومتر مربع': ['area', 'km2'], 'km2': ['area', 'km2'], 'square kilometer': ['area', 'km2'],
    'هكتار': ['area', 'ha'], 'hectare': ['area', 'ha'], 'ha': ['area', 'ha'],
    /* Arabic land units are NOT the acre — kept distinct on purpose (this exact confusion generic models make). */
    'فدان': ['area', 'feddan'], 'فدّان': ['area', 'feddan'], 'الفدان': ['area', 'feddan'], 'feddan': ['area', 'feddan'], 'faddan': ['area', 'feddan'],
    'قيراط': ['area', 'kirat'], 'قيراط ارض': ['area', 'kirat'], 'kirat': ['area', 'kirat'], 'qirat': ['area', 'kirat'],
    'سهم': ['area', 'sahm'], 'sahm': ['area', 'sahm'],
    'دونم': ['area', 'dunam'], 'دنم': ['area', 'dunam'], 'dunam': ['area', 'dunam'], 'donum': ['area', 'dunam'],
    'اكر': ['area', 'acre'], 'أكر': ['area', 'acre'], 'acre': ['area', 'acre'], 'قدم2': ['area', 'ft2'], 'ft2': ['area', 'ft2'], 'square foot': ['area', 'ft2'], 'انش2': ['area', 'in2'], 'in2': ['area', 'in2'], 'square inch': ['area', 'in2'], 'ميل2': ['area', 'mi2'], 'mi2': ['area', 'mi2'], 'square mile': ['area', 'mi2'],
    // pressure
    'باسكال': ['pressure', 'pa'], 'pa': ['pressure', 'pa'], 'pascal': ['pressure', 'pa'], 'كيلوباسكال': ['pressure', 'kpa'], 'kpa': ['pressure', 'kpa'], 'kilopascal': ['pressure', 'kpa'],
    'بار': ['pressure', 'bar'], 'bar': ['pressure', 'bar'], 'ضغط جوي': ['pressure', 'atm'], 'atm': ['pressure', 'atm'], 'atmosphere': ['pressure', 'atm'],
    'رطل/بوصة': ['pressure', 'psi'], 'psi': ['pressure', 'psi'], 'ملم زئبق': ['pressure', 'mmhg'], 'mmhg': ['pressure', 'mmhg'], 'تور': ['pressure', 'torr'], 'torr': ['pressure', 'torr'],
    // energy
    'جول': ['energy', 'j'], 'j': ['energy', 'j'], 'joule': ['energy', 'j'], 'كيلوجول': ['energy', 'kj'], 'kj': ['energy', 'kj'], 'kilojoule': ['energy', 'kj'],
    'سعرة': ['energy', 'cal'], 'كالوري': ['energy', 'cal'], 'cal': ['energy', 'cal'], 'calorie': ['energy', 'cal'], 'كيلوسعرة': ['energy', 'kcal'], 'kcal': ['energy', 'kcal'],
    'واط/ساعة': ['energy', 'wh'], 'wh': ['energy', 'wh'], 'watt hour': ['energy', 'wh'], 'كيلوواط/ساعة': ['energy', 'kwh'], 'kwh': ['energy', 'kwh'], 'kilowatt hour': ['energy', 'kwh'],
    'btu': ['energy', 'btu'], 'إلكترون فولت': ['energy', 'ev'], 'الكترون فولت': ['energy', 'ev'], 'ev': ['energy', 'ev'], 'electron volt': ['energy', 'ev'],
    // power
    'واط': ['power', 'w'], 'w': ['power', 'w'], 'watt': ['power', 'w'], 'كيلوواط': ['power', 'kw'], 'kw': ['power', 'kw'], 'kilowatt': ['power', 'kw'], 'ميغاواط': ['power', 'mw'], 'mw': ['power', 'mw'], 'megawatt': ['power', 'mw'],
    'حصان': ['power', 'hp'], 'hp': ['power', 'hp'], 'horsepower': ['power', 'hp'], 'btu/ساعة': ['power', 'btuh'], 'btuh': ['power', 'btuh'], 'btu per hour': ['power', 'btuh'],
    // angle
    'درجة': ['angle', 'deg'], 'deg': ['angle', 'deg'], 'degree': ['angle', 'deg'], 'degrees': ['angle', 'deg'], 'راديان': ['angle', 'rad'], 'rad': ['angle', 'rad'], 'radian': ['angle', 'rad'],
    'غراد': ['angle', 'grad'], 'grad': ['angle', 'grad'], 'دقيقة قوسية': ['angle', 'arcmin'], 'arcmin': ['angle', 'arcmin'], 'ثانية قوسية': ['angle', 'arcsec'], 'arcsec': ['angle', 'arcsec'], 'دورة': ['angle', 'turn'], 'turn': ['angle', 'turn'],
    // fuel
    'كم/لتر': ['fuel', 'kml'], 'كم لكل لتر': ['fuel', 'kml'], 'km/l': ['fuel', 'kml'], 'kml': ['fuel', 'kml'], 'كيلومتر لكل لتر': ['fuel', 'kml'],
    'لتر/100كم': ['fuel', 'l100'], 'لتر/100 كم': ['fuel', 'l100'], 'l/100km': ['fuel', 'l100'], 'l100': ['fuel', 'l100'], 'liter per 100km': ['fuel', 'l100'],
    'ميل/جالون': ['fuel', 'mpg'], 'ميل لكل جالون': ['fuel', 'mpg'], 'mpg': ['fuel', 'mpg'], 'us mpg': ['fuel', 'mpg'], 'ميل/جالون امريكي': ['fuel', 'mpg'],
    'ميل/جالون امبراطوري': ['fuel', 'mpgUK'], 'ميل لكل جالون امبراطوري': ['fuel', 'mpgUK'], 'mpguk': ['fuel', 'mpgUK'], 'uk mpg': ['fuel', 'mpgUK'],
    // frequency
    'هرتز': ['frequency', 'hz'], 'هيرتز': ['frequency', 'hz'], 'hz': ['frequency', 'hz'], 'hertz': ['frequency', 'hz'], 'كيلوهرتز': ['frequency', 'khz'], 'khz': ['frequency', 'khz'], 'kilohertz': ['frequency', 'khz'],
    'ميغاهرتز': ['frequency', 'mhz'], 'mhz': ['frequency', 'mhz'], 'megahertz': ['frequency', 'mhz'], 'غيغاهرتز': ['frequency', 'ghz'], 'ghz': ['frequency', 'ghz'], 'gigahertz': ['frequency', 'ghz'], 'دورة/دقيقة': ['frequency', 'rpm'], 'rpm': ['frequency', 'rpm']
  };

  var CAT_LABEL = {
    length: 'الطول', weight: 'الوزن', temperature: 'الحرارة', data: 'البيانات',
    speed: 'السرعة', volume: 'الحجم', time: 'الوقت', area: 'المساحة',
    pressure: 'الضغط', energy: 'الطاقة', power: 'القدرة', angle: 'الزوايا',
    fuel: 'استهلاك الوقود', frequency: 'التردد'
  };
  var LOCALE = window.NexlunaLocale || {};
  var SUI = LOCALE.ui || {};
  function stx(key, fallback) { return SUI[key] || fallback; }
  function scat(cat) { return LOCALE.categories && LOCALE.categories[cat] ? LOCALE.categories[cat].label : (CAT_LABEL[cat] || cat); }

  /* Question words / connectors that are never units (esp. "كم" = "how much"). */
  var STOP = { 'في': 1, 'الى': 1, 'إلى': 1, 'من': 1, 'to': 1, 'in': 1, 'into': 1, 'is': 1, 'how': 1, 'many': 1, 'much': 1, 'convert': 1, 'كام': 1, 'يساوي': 1, 'تساوي': 1, 'بكم': 1, 'وكم': 1, 'لكل': 1, 'per': 1, 'على': 1 };

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
      .replace(/[²]/g, '2').replace(/[³]/g, '3').replace(/[°]/g, '')
      .replace(/\s*\/\s*/g, '/')
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
    var localized = LOCALE.units && LOCALE.units[cat];
    if (localized && localized[key]) return localized[key];
    if (!BASE) return key;
    var u = (BASE[cat].units || []).filter(function (x) { return x[0] === key; })[0];
    return u ? u[1] : key;
  }
  function fmt(n) { if (!isFinite(n)) return '—'; var r = Math.round(n * 1e6) / 1e6; return r.toLocaleString(LOCALE.locale || 'en-US', { maximumFractionDigits: 6 }); }

  /* ---------- UI ---------- */
  function mount(host) {
    var box = document.createElement('div');
    box.className = 'smart-search';
    var chips = SUI.search_chips || ['5 كم بالميل', '100 كجم رطل', '20 celsius to fahrenheit', '1 gb in mb', '2 bar psi', '1 kwh wh', '30 mpg km/l', 'كم قدم في المتر'];
    box.innerHTML =
      '<label class="ss-label" for="ss-input">' + (window.NexIcons ? window.NexIcons.get('search') : '') +
      ' ' + stx('search_label', 'اكتب سؤالك بالعربي أو الإنجليزي') + '</label>' +
      '<div class="ss-field"><input id="ss-input" type="text" autocomplete="off" ' +
      'placeholder="' + stx('search_placeholder', 'مثال: 5 كم بالميل · كم قدم في المتر · 100 celsius to f') + '" ' +
      'aria-describedby="ss-out"></div>' +
      '<div id="ss-out" class="ss-out" role="status" aria-live="polite"></div>' +
      '<div class="ss-chips">' + chips
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
        out.innerHTML = stx('search_not_understood', 'لم أفهم الطلب — جرّب صيغة مثل «5 كم بالميل» أو «100 celsius to f».');
        return;
      }
      var res = compute(r);
      if (res === null || !isFinite(res)) {
        out.className = 'ss-out ss-hint';
        out.innerHTML = stx('search_failed', 'تعذّر الحساب لهذه الوحدات.');
        return;
      }
      out.className = 'ss-out ss-answer';
      out.innerHTML =
        '<div class="ss-ans-num" dir="ltr">' + fmt(r.value) + ' ' + label(r.cat, r.from) +
        ' <span class="ss-eq">=</span> <strong>' + fmt(res) + '</strong> ' + label(r.cat, r.to) + '</div>' +
        '<a class="ss-open" href="' + (LOCALE.root || '/') + 'converters/' + r.cat + '.html">' + stx('open_converter', 'افتح محوّل {name}').replace('{name}', scat(r.cat)) +
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

  window.NexSmartSearch = { parse: parse, normalize: normalize };

  document.addEventListener('DOMContentLoaded', function () {
    var host = document.getElementById('smart-search');
    if (host) mount(host);
  });
})();
