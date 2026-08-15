/* Nexluna — WebMCP/API v1 provider.
 * The canonical source is assets/js/units.generated.js, generated from
 * data/units.json. This adapter never owns a second conversion table.
 * Spec reference: https://webmachinelearning.github.io/webmcp/
 */
(function (root) {
  'use strict';

  var API_VERSION = '1.0.0';
  var DATA = root.NexlunaUnits || {};
  var CATEGORIES = Object.keys(DATA);

  function fail(code, message, details) {
    var error = { code: code, message: message };
    if (details) error.details = details;
    var out = new Error(message);
    out.code = code;
    out.details = details;
    return out;
  }

  function assertCategory(category) {
    if (!category || !DATA[category]) {
      throw fail('UNKNOWN_CATEGORY', 'فئة القياس غير معروفة: ' + (category || ''));
    }
    return DATA[category];
  }

  function assertUnit(category, unit, role) {
    var definition = assertCategory(category);
    var ids = (definition.units || []).map(function (entry) { return entry[0]; });
    if (ids.indexOf(unit) === -1) {
      throw fail('UNKNOWN_UNIT', 'وحدة ' + role + ' غير معروفة: ' + (unit || ''), {
        category: category,
        available: ids
      });
    }
    return definition;
  }

  function tempConvert(value, from, to) {
    var c = from === 'C' ? value : from === 'F' ? (value - 32) * 5 / 9 : value - 273.15;
    return to === 'C' ? c : to === 'F' ? c * 9 / 5 + 32 : c + 273.15;
  }

  /* mpg factors: US gallon = 3.785411784 L, Imperial gallon = 4.54609 L. */
  var MPG_US = 0.425143707430272;
  var MPG_UK = 0.3540061899346471;
  function mpgFactor(unit) { return unit === 'mpgUK' ? MPG_UK : MPG_US; }
  function fuelToKmL(value, unit) {
    return unit === 'kml' ? value : unit === 'l100' ? 100 / value : value * mpgFactor(unit);
  }
  function kmLToUnit(value, unit) {
    return unit === 'kml' ? value : unit === 'l100' ? 100 / value : value / mpgFactor(unit);
  }

  function convert(category, from, to, value) {
    var definition = assertCategory(category);
    assertUnit(category, from, 'المصدر');
    assertUnit(category, to, 'الهدف');
    var numeric = Number(value);
    if (!isFinite(numeric)) throw fail('INVALID_VALUE', 'القيمة يجب أن تكون رقمًا صالحًا');
    if (root.NexConvert && typeof root.NexConvert.convert === 'function') {
      var result = root.NexConvert.convert(category, from, to, numeric);
      if (isFinite(result)) return result;
    }
    if (definition.temp) return tempConvert(numeric, from, to);
    if (definition.special === 'fuel') return kmLToUnit(fuelToKmL(numeric, from), to);
    return numeric * definition.base[from] / definition.base[to];
  }

  function unitsFor(category) {
    var definition = assertCategory(category);
    return (definition.units || []).map(function (entry) { return entry[0]; });
  }

  function labelsFor(category) {
    var definition = assertCategory(category);
    return (definition.units || []).map(function (entry) {
      return { id: entry[0], label: entry[1] };
    });
  }

  function provenanceFor(category, unit) {
    var definition = assertCategory(category);
    if (!unit) {
      return {
        category: category,
        provenance: definition.provenance || null,
        units: definition.unit_provenance || {}
      };
    }
    assertUnit(category, unit, 'المطلوبة');
    return {
      category: category,
      unit: unit,
      provenance: (definition.unit_provenance || {})[unit] || definition.provenance || null
    };
  }

  function success(payload) {
    return {
      content: [{ type: 'text', text: JSON.stringify(payload) }],
      structuredContent: payload
    };
  }

  function failure(error) {
    var payload = {
      api_version: API_VERSION,
      error: {
        code: error.code || 'CONVERSION_ERROR',
        message: error.message || 'تعذّر تنفيذ الأداة',
        details: error.details || null
      }
    };
    return {
      content: [{ type: 'text', text: JSON.stringify(payload) }],
      structuredContent: payload,
      isError: true
    };
  }

  /* ---- Tool definitions ---- */
  var tools = [
    {
      name: 'convert_units',
      description: 'حوّل قيمة رقمية حتميًا بين وحدتين من الفئة نفسها. الحساب يتم داخل NexConvert وليس داخل نموذج لغوي. Returns a precise deterministic result with provenance.',
      inputSchema: {
        type: 'object',
        properties: {
          category: { type: 'string', enum: CATEGORIES, description: 'فئة القياس / measurement category' },
          from: { type: 'string', description: 'رمز الوحدة المصدر. استخدم list_units.' },
          to: { type: 'string', description: 'رمز الوحدة الهدف. استخدم list_units.' },
          value: { type: 'number', description: 'القيمة الرقمية المراد تحويلها' }
        },
        required: ['category', 'from', 'to', 'value'],
        additionalProperties: false
      },
      async execute(args) {
        var a = args || {};
        try {
          var result = convert(a.category, a.from, a.to, a.value);
          var payload = {
            api_version: API_VERSION,
            category: a.category,
            input: { value: Number(a.value), unit: a.from },
            output: { value: result, unit: a.to },
            expression: Number(a.value) + ' ' + a.from + ' = ' + result + ' ' + a.to,
            calculation: { engine: 'NexConvert', deterministic: true, network_required: false },
            provenance: {
              input: provenanceFor(a.category, a.from).provenance,
              output: provenanceFor(a.category, a.to).provenance
            }
          };
          return success(payload);
        } catch (error) {
          return failure(error);
        }
      }
    },
    {
      name: 'list_units',
      description: 'أعد قائمة فئات القياس أو رموز الوحدات المتاحة مع تعريف المصدر. Returns typed unit metadata.',
      inputSchema: {
        type: 'object',
        properties: {
          category: { type: 'string', enum: CATEGORIES, description: 'فئة القياس الاختيارية' }
        },
        required: [],
        additionalProperties: false
      },
      async execute(args) {
        try {
          var a = args || {};
          if (a.category) {
            var definition = assertCategory(a.category);
            return success({
              api_version: API_VERSION,
              category: a.category,
              label: definition.label,
              units: unitsFor(a.category),
              unit_labels: labelsFor(a.category),
              provenance: definition.provenance || null
            });
          }
          return success({
            api_version: API_VERSION,
            categories: CATEGORIES.map(function (category) {
              return {
                id: category,
                label: DATA[category].label,
                units: unitsFor(category),
                provenance: DATA[category].provenance || null
              };
            })
          });
        } catch (error) {
          return failure(error);
        }
      }
    },
    {
      name: 'get_unit_info',
      description: 'أعد تعريف الوحدة ومصدرها الإقليمي ووقت مراجعة provenance. Use this before high-stakes or ambiguous conversions.',
      inputSchema: {
        type: 'object',
        properties: {
          category: { type: 'string', enum: CATEGORIES },
          unit: { type: 'string', description: 'رمز الوحدة الاختياري؛ عند غيابه تعاد معلومات الفئة كاملة.' }
        },
        required: ['category'],
        additionalProperties: false
      },
      async execute(args) {
        try {
          var a = args || {};
          return success({ api_version: API_VERSION, data: provenanceFor(a.category, a.unit) });
        } catch (error) {
          return failure(error);
        }
      }
    },
    {
      name: 'explain_conversion',
      description: 'اشرح نتيجة تحويل حتمي بلغة بسيطة. الحساب لا يمر عبر النموذج؛ أي تفسير اختياري يجب أن يطابق النتيجة الموثقة أو يعود إلى fallback المحلي.',
      inputSchema: {
        type: 'object',
        properties: {
          category: { type: 'string', enum: CATEGORIES },
          from: { type: 'string' },
          to: { type: 'string' },
          value: { type: 'number' }
        },
        required: ['category', 'from', 'to', 'value'],
        additionalProperties: false
      },
      async execute(args) {
        try {
          var a = args || {};
          var explanation = root.NexExplain && typeof root.NexExplain.explain === 'function'
            ? await root.NexExplain.explain(a)
            : { output: { value: convert(a.category, a.from, a.to, a.value) }, explanation: 'النتيجة حُسبت حتميًا بواسطة NexConvert.', source: 'deterministic-fallback' };
          return success({ api_version: API_VERSION, ...explanation });
        } catch (error) {
          return failure(error);
        }
      }
    }
  ];

  function register() {
    try {
      if (root.navigator && root.navigator.modelContext && typeof root.navigator.modelContext.provideContext === 'function') {
        root.navigator.modelContext.provideContext({ tools: tools });
        return 'provideContext';
      }
      if (root.navigator && root.navigator.modelContext && typeof root.navigator.modelContext.registerTool === 'function') {
        tools.forEach(function (tool) { root.navigator.modelContext.registerTool(tool); });
        return 'registerTool';
      }
    } catch (error) {
      root.NexMCPRegistrationError = error;
    }
    return 'fallback';
  }

  root.NexMCP = {
    apiVersion: API_VERSION,
    tools: tools,
    convert: convert,
    categories: CATEGORIES,
    unitsFor: unitsFor,
    provenanceFor: provenanceFor,
    registration: register()
  };
})(typeof window !== 'undefined' ? window : globalThis);
