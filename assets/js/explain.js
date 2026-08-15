/* Nexluna optional explanation adapter.
 * The numeric result is always produced by NexConvert/NexMCP first.
 * A model may only add wording after its structured result matches that value.
 */
(function (root) {
  'use strict';

  function round(value) {
    return Number(Number(value).toPrecision(12));
  }

  function label(category, unit) {
    var localized = root.NexlunaLocale && root.NexlunaLocale.units && root.NexlunaLocale.units[category];
    if (localized && localized[unit]) return localized[unit];
    var data = root.NexlunaUnits && root.NexlunaUnits[category];
    if (!data) return unit;
    var entry = (data.units || []).find(function (item) { return item[0] === unit; });
    return entry ? entry[1] : unit;
  }

  function deterministic(category, from, to, value) {
    if (!root.NexMCP || typeof root.NexMCP.convert !== 'function') {
      throw new Error('NexMCP is required for verified explanations');
    }
    var numeric = Number(value);
    var result = root.NexMCP.convert(category, from, to, numeric);
    return {
      api_version: '1.0.0',
      category: category,
      input: { value: numeric, unit: from, label: label(category, from) },
      output: { value: result, unit: to, label: label(category, to) },
      expression: numeric + ' ' + from + ' = ' + result + ' ' + to,
      calculation: { engine: 'NexConvert', deterministic: true, network_required: false },
      provenance: root.NexMCP.provenanceFor(category, from),
      explanation: ((root.NexlunaLocale && root.NexlunaLocale.ui && root.NexlunaLocale.ui.explain_deterministic) || 'النتيجة حُسبت حتميًا بواسطة NexConvert من {from} إلى {to}.').replace('{from}', label(category, from)).replace('{to}', label(category, to)),
      source: 'deterministic-fallback'
    };
  }

  function verifiedModelResult(modelResult, deterministicResult) {
    if (!modelResult || typeof modelResult !== 'object') return null;
    var reported = Number(modelResult.value);
    if (!isFinite(reported) || round(reported) !== round(deterministicResult.output.value)) return null;
    return {
      value: deterministicResult.output.value,
      explanation: String(modelResult.explanation || deterministicResult.explanation),
      source: 'optional-model-verified'
    };
  }

  function explain(request, options) {
    var args = request || {};
    var baseline = deterministic(args.category, args.from, args.to, args.value);
    var model = options && typeof options.model === 'function' ? options.model : null;
    if (!model) return Promise.resolve(baseline);
    return Promise.resolve(model({
      category: args.category,
      from: args.from,
      to: args.to,
      value: Number(args.value),
      deterministic_result: baseline.output.value,
      provenance: baseline.provenance
    })).then(function (modelResult) {
      var verified = verifiedModelResult(modelResult, baseline);
      if (!verified) return baseline;
      baseline.explanation = verified.explanation;
      baseline.source = verified.source;
      return baseline;
    }).catch(function () { return baseline; });
  }

  root.NexExplain = {
    deterministic: deterministic,
    explain: explain,
    verifyModelResult: verifiedModelResult
  };
})(typeof window !== 'undefined' ? window : globalThis);
