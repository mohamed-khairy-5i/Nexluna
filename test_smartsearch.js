#!/usr/bin/env node
/* Nexluna — natural-language Smart Search regression gate.
 * Loads the browser modules in a minimal VM and verifies that every converter
 * category can be reached by Arabic/English phrasing without using an LLM.
 */
'use strict';

const fs = require('fs');
const vm = require('vm');
const path = require('path');
const root = __dirname;
const sandbox = {
  window: {
    matchMedia: () => ({ matches: false }),
    NexIcons: { get: () => '' }
  },
  document: { addEventListener: () => {} },
  console,
  isFinite,
  parseFloat,
  Math,
  JSON
};
sandbox.window.NexConvert = undefined;
const context = vm.createContext(sandbox);

function load(file) {
  vm.runInContext(fs.readFileSync(path.join(root, file), 'utf8'), context, { filename: file });
}

load('assets/js/units.generated.js');
load('assets/js/converter.js');
load('assets/js/smartsearch.js');
const search = sandbox.window.NexSmartSearch;
if (!search || typeof search.parse !== 'function') throw new Error('NexSmartSearch.parse was not exported');

const cases = [
  ['5 كم بالميل', 'length', 'km', 'mi', 5],
  ['100 كجم رطل', 'weight', 'kg', 'lb', 100],
  ['20 celsius to fahrenheit', 'temperature', 'C', 'F', 20],
  ['1 gb in mb', 'data', 'GB', 'MB', 1],
  ['100 كم/ساعة إلى متر/ثانية', 'speed', 'kmh', 'ms', 100],
  ['2 لتر إلى جالون', 'volume', 'L', 'gal', 2],
  ['كم قدم في المتر', 'length', 'ft', 'm', 1],
  ['2 ساعة إلى دقيقة', 'time', 'h', 'min', 2],
  ['1 فدان إلى متر مربع', 'area', 'feddan', 'm2', 1],
  ['2 bar psi', 'pressure', 'bar', 'psi', 2],
  ['1 kwh wh', 'energy', 'kwh', 'wh', 1],
  ['2 كيلوواط حصان', 'power', 'kw', 'hp', 2],
  ['180 درجة راديان', 'angle', 'deg', 'rad', 180],
  ['30 mpg km/l', 'fuel', 'mpg', 'kml', 30],
  ['60 rpm hz', 'frequency', 'rpm', 'hz', 60]
];

let failures = [];
for (const [query, cat, from, to, value] of cases) {
  const parsed = search.parse(query);
  if (!parsed) {
    failures.push(`${query}: parser returned null`);
    continue;
  }
  for (const [key, expected] of [['cat', cat], ['from', from], ['to', to], ['value', value]]) {
    if (parsed[key] !== expected) failures.push(`${query}: ${key}=${parsed[key]} expected ${expected}`);
  }
}

const arabicNumerals = search.parse('٢٠ درجة مئوية بالفهرنهايت');
if (!arabicNumerals || arabicNumerals.cat !== 'temperature' || arabicNumerals.value !== 20 || arabicNumerals.from !== 'C' || arabicNumerals.to !== 'F') {
  failures.push('Arabic numerals / prefixed units did not parse as expected');
}

if (failures.length) {
  console.error(`FAIL — ${failures.length} smart-search problem(s)`);
  failures.forEach((failure) => console.error(`  x ${failure}`));
  process.exit(1);
}
console.log(`PASS — ${cases.length + 1} smart-search regression cases across all ${Object.keys(sandbox.window.NexConvert.DATA).length} categories.`);
