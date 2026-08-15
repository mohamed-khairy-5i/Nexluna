#!/usr/bin/env node
'use strict';

const fs = require('fs');
const path = require('path');
const vm = require('vm');

const ROOT = __dirname;
const REPORT_DIR = path.join(ROOT, 'reports');
const REPORT_FILE = path.join(REPORT_DIR, 'week7_webmcp_eval.json');
const contextRoot = { console, navigator: {} };
contextRoot.globalThis = contextRoot;
const context = vm.createContext(contextRoot);
for (const file of ['assets/js/units.generated.js', 'assets/js/explain.js', 'assets/js/webmcp.js']) {
  vm.runInContext(fs.readFileSync(path.join(ROOT, file), 'utf8'), context, { filename: file });
}

const cases = [
  ['length', 'km', 'm', 1, 1000],
  ['weight', 'kg', 'lb', 1, 2.2046226218487757],
  ['area', 'feddan', 'm2', 1, 4200.833],
  ['volume', 'L', 'mL', 1, 1000],
  ['temperature', 'C', 'F', 0, 32],
  ['data', 'KB', 'B', 1, 1000],
  ['speed', 'kmh', 'mph', 100, 62.13711922373339],
  ['time', 'h', 's', 1, 3600],
  ['pressure', 'atm', 'pa', 1, 101325],
  ['energy', 'kwh', 'j', 1, 3600000],
  ['power', 'kw', 'w', 1, 1000],
  ['angle', 'deg', 'rad', 180, Math.PI],
  ['fuel', 'kml', 'l100', 1, 100],
  ['frequency', 'ghz', 'hz', 1, 1000000000]
];
const tolerance = 1e-9;
const rows = [];
let passed = 0;
let maxRelativeError = 0;

function assert(condition, message) {
  if (!condition) throw new Error(message);
}
function relativeError(actual, expected) {
  return Math.abs(actual - expected) / Math.max(1, Math.abs(expected));
}

(async () => {
  const tools = contextRoot.NexMCP.tools;
  const convertTool = tools.find((tool) => tool.name === 'convert_units');
  const explainTool = tools.find((tool) => tool.name === 'explain_conversion');
  const listTool = tools.find((tool) => tool.name === 'list_units');
  const infoTool = tools.find((tool) => tool.name === 'get_unit_info');
  assert(convertTool && explainTool && listTool && infoTool, 'required WebMCP tools are missing');
  assert(contextRoot.NexMCP.categories.length === 14, 'category count must remain 14');

  for (const [category, from, to, value, expected] of cases) {
    const response = await convertTool.execute({ category, from, to, value });
    assert(!response.isError, `${category}/${from}->${to}: conversion returned ${response.structuredContent && response.structuredContent.error ? response.structuredContent.error.code : 'an error'}`);
    assert(response.structuredContent && response.structuredContent.output, `${category}/${from}->${to}: output is missing`);
    const actual = response.structuredContent.output.value;
    const error = relativeError(actual, expected);
    maxRelativeError = Math.max(maxRelativeError, error);
    assert(error <= tolerance, `${category}: relative error ${error} exceeds ${tolerance}`);
    assert(response.structuredContent.calculation.deterministic === true, `${category}: not deterministic`);
    assert(response.structuredContent.calculation.network_required === false, `${category}: network required`);
    assert(response.structuredContent.provenance.input && response.structuredContent.provenance.output, `${category}: provenance missing`);

    const explanation = await explainTool.execute({ category, from, to, value });
    assert(!explanation.isError, `${category}: explanation returned error`);
    assert(explanation.structuredContent.output.value === actual, `${category}: explanation changed numeric result`);
    assert(String(explanation.structuredContent.source).includes('deterministic'), `${category}: explanation source is not deterministic fallback`);
    rows.push({ category, from, to, value, expected, actual, relative_error: error, deterministic: true, network_required: false, explanation_source: explanation.structuredContent.source });
    passed += 1;
  }

  const categories = await listTool.execute({});
  assert(categories.structuredContent.categories.length === 14, 'list_units category contract failed');
  const info = await infoTool.execute({ category: 'data', unit: 'KB' });
  assert(info.structuredContent.data.provenance, 'get_unit_info provenance contract failed');
  const invalid = await convertTool.execute({ category: 'length', from: 'km', to: 'not-a-unit', value: 1 });
  assert(invalid.isError === true && invalid.structuredContent.error.code === 'UNKNOWN_UNIT', 'typed UNKNOWN_UNIT error contract failed');

  const report = {
    schema_version: '1.0',
    generated_at: new Date().toISOString(),
    api_version: contextRoot.NexMCP.apiVersion,
    cases_total: cases.length,
    cases_passed: passed,
    pass_rate: passed / cases.length,
    max_relative_error: maxRelativeError,
    tolerance,
    deterministic_invariants: { all_deterministic: true, network_required: false, explanation_numeric_match: true },
    typed_error_contract: { unknown_unit: true },
    cases: rows
  };
  fs.mkdirSync(REPORT_DIR, { recursive: true });
  fs.writeFileSync(REPORT_FILE, JSON.stringify(report, null, 2) + '\n');
  console.log(`PASS — WebMCP eval: ${passed}/${cases.length} cases, max relative error ${maxRelativeError}`);
  console.log(`REPORT — ${path.relative(ROOT, REPORT_FILE)}`);
})().catch((error) => {
  console.error('FAIL — WebMCP eval:', error.message);
  process.exitCode = 1;
});
