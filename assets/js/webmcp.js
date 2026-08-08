/* Nexluna — WebMCP tool provider.
 * Exposes the site's unit-conversion capability to AI agents via the
 * WebMCP browser API (navigator.modelContext.provideContext).
 * Spec: https://webmachinelearning.github.io/webmcp/
 * Self-contained: carries its own base-factor tables so it works on every
 * page (even those that do not load converter.js).                          */
(function () {
  'use strict';

  /* ---- Conversion data (base-unit factor tables) — mirror of converter.js ---- */
  var DATA = {
    length:      { label: 'الطول', base: { km:1000, m:1, cm:0.01, mm:0.001, mi:1609.344, yd:0.9144, ft:0.3048, 'in':0.0254, nmi:1852 } },
    weight:      { label: 'الوزن', base: { t:1000, kg:1, g:0.001, mg:0.000001, lb:0.45359237, oz:0.028349523, st:6.35029318, ct:0.0002 } },
    area:        { label: 'المساحة', base: { km2:1000000, m2:1, cm2:0.0001, ha:10000, acre:4046.8564224, ft2:0.09290304, in2:0.00064516, mi2:2589988.11 } },
    volume:      { label: 'الحجم', base: { m3:1000, L:1, mL:0.001, gal:3.785411784, qt:0.946352946, pt:0.473176473, cup:0.2365882365, floz:0.0295735296, tbsp:0.0147867648, tsp:0.0049289216 } },
    temperature: { label: 'درجة الحرارة', temp: true, units: ['C', 'F', 'K'] },
    data:        { label: 'البيانات الرقمية', base: { bit:0.125, B:1, KB:1000, MB:1000000, GB:1000000000, TB:1000000000000, KiB:1024, MiB:1048576, GiB:1073741824 } },
    speed:       { label: 'السرعة', base: { kmh:1, ms:3.6, mph:1.609344, knot:1.852, fts:1.09728 } },
    time:        { label: 'الوقت', base: { ms:0.001, s:1, min:60, h:3600, day:86400, week:604800, month:2629800, year:31557600 } },
    pressure:    { label: 'الضغط', base: { pa:1, kpa:1000, bar:100000, atm:101325, psi:6894.757293, mmhg:133.322368, torr:133.322368 } },
    energy:      { label: 'الطاقة', base: { j:1, kj:1000, cal:4.184, kcal:4184, wh:3600, kwh:3600000, btu:1055.05585, ev:1.602176634e-19 } },
    power:       { label: 'القدرة', base: { w:1, kw:1000, mw:1000000, hp:745.699872, btuh:0.293071 } },
    angle:       { label: 'الزوايا', base: { deg:1, rad:57.29577951, grad:0.9, arcmin:0.016666667, arcsec:0.000277778, turn:360 } },
    fuel:        { label: 'استهلاك الوقود', special: 'fuel', units: ['kml', 'l100', 'mpg'] },
    frequency:   { label: 'التردد', base: { hz:1, khz:1000, mhz:1000000, ghz:1000000000, rpm:0.016666667 } }
  };

  function tempConvert(v, f, t) {
    var c = f === 'C' ? v : f === 'F' ? (v - 32) * 5 / 9 : v - 273.15;
    return t === 'C' ? c : t === 'F' ? c * 9 / 5 + 32 : c + 273.15;
  }
  function fuelToKmL(v, u) { return u === 'kml' ? v : u === 'l100' ? 100 / v : v * 0.425143707; }
  function kmLToUnit(v, u) { return u === 'kml' ? v : u === 'l100' ? 100 / v : v / 0.425143707; }

  /* Deterministic conversion — prefers converter.js's NexConvert if present,
   * otherwise uses the local tables (identical math). */
  function convert(category, from, to, value) {
    if (window.NexConvert && typeof window.NexConvert.convert === 'function') {
      var r = window.NexConvert.convert(category, from, to, value);
      if (isFinite(r)) return r;
    }
    var d = DATA[category];
    if (!d) throw new Error('فئة غير معروفة: ' + category);
    if (d.temp) return tempConvert(value, from, to);
    if (d.special === 'fuel') return kmLToUnit(fuelToKmL(value, from), to);
    if (!(from in d.base)) throw new Error('وحدة مصدر غير معروفة: ' + from);
    if (!(to in d.base)) throw new Error('وحدة هدف غير معروفة: ' + to);
    return value * d.base[from] / d.base[to];
  }

  function unitsFor(category) {
    var d = DATA[category];
    if (!d) return [];
    return d.units ? d.units.slice() : Object.keys(d.base);
  }
  var CATEGORIES = Object.keys(DATA);

  /* ---- Tool definitions ---- */
  var tools = [
    {
      name: 'convert_units',
      description: 'حوّل قيمة رقمية بين وحدتين قياس ضمن نفس الفئة (طول، وزن، مساحة، حجم، درجة حرارة، بيانات رقمية، سرعة، وقت، ضغط، طاقة، قدرة، زوايا، استهلاك وقود، تردد). Convert a numeric value between two units of the same measurement category. Returns a precise deterministic result.',
      inputSchema: {
        type: 'object',
        properties: {
          category: { type: 'string', enum: CATEGORIES, description: 'فئة القياس / measurement category' },
          from: { type: 'string', description: 'رمز الوحدة المصدر (مثل: m, kg, C, KB). استخدم list_units لمعرفة الرموز المتاحة.' },
          to: { type: 'string', description: 'رمز الوحدة الهدف (مثل: ft, lb, F, MB).' },
          value: { type: 'number', description: 'القيمة الرقمية المراد تحويلها / the numeric value to convert' }
        },
        required: ['category', 'from', 'to', 'value']
      },
      async execute(args) {
        var a = args || {};
        try {
          var result = convert(a.category, a.from, a.to, Number(a.value));
          if (!isFinite(result)) throw new Error('نتيجة غير صالحة');
          return {
            content: [{
              type: 'text',
              text: JSON.stringify({
                category: a.category,
                input: { value: Number(a.value), unit: a.from },
                output: { value: result, unit: a.to },
                expression: Number(a.value) + ' ' + a.from + ' = ' + result + ' ' + a.to
              })
            }]
          };
        } catch (e) {
          return { content: [{ type: 'text', text: 'خطأ: ' + (e && e.message ? e.message : 'تعذّر التحويل') }], isError: true };
        }
      }
    },
    {
      name: 'list_units',
      description: 'أعِد قائمة رموز الوحدات المتاحة لفئة قياس معيّنة، أو قائمة الفئات كلها عند عدم تحديد فئة. List available unit symbols for a category (or all categories when none is given).',
      inputSchema: {
        type: 'object',
        properties: {
          category: { type: 'string', enum: CATEGORIES, description: 'فئة القياس (اختياري) / optional category' }
        },
        required: []
      },
      async execute(args) {
        var a = args || {};
        var payload;
        if (a.category) {
          payload = { category: a.category, units: unitsFor(a.category) };
        } else {
          payload = { categories: CATEGORIES.map(function (c) { return { id: c, label: DATA[c].label, units: unitsFor(c) }; }) };
        }
        return { content: [{ type: 'text', text: JSON.stringify(payload) }] };
      }
    }
  ];

  /* ---- Register with the browser agent (WebMCP) ---- */
  function register() {
    try {
      if (navigator.modelContext && typeof navigator.modelContext.provideContext === 'function') {
        navigator.modelContext.provideContext({ tools: tools });
      } else if (navigator.modelContext && typeof navigator.modelContext.registerTool === 'function') {
        tools.forEach(function (t) { navigator.modelContext.registerTool(t); });
      }
    } catch (e) { /* WebMCP not supported in this browser — no-op */ }
  }
  register();

  /* Also expose for programmatic (non-WebMCP) callers. */
  window.NexMCP = { tools: tools, convert: convert, categories: CATEGORIES, unitsFor: unitsFor };
})();
