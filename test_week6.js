#!/usr/bin/env node
'use strict';

const fs = require('fs');
const vm = require('vm');
const path = require('path');

const root = path.resolve(__dirname);
function load(file, context) {
  vm.runInContext(fs.readFileSync(path.join(root, file), 'utf8'), context, { filename: file });
}
function assert(condition, message) {
  if (!condition) throw new Error(message);
}

// Contract test for the deterministic explanation layer.
const explainContext = vm.createContext({
  console,
  Number,
  String,
  Promise,
  isFinite,
  NexlunaUnits: {
    length: {
      label: 'الطول',
      units: [['m', 'متر'], ['ft', 'قدم']],
      provenance: { source: 'test-fixture' },
      factors: { m: 1, ft: 0.3048 }
    }
  },
  NexMCP: {
    convert(category, from, to, value) {
      assert(category === 'length' && from === 'm' && to === 'ft', 'unexpected deterministic request');
      return Number(value) / 0.3048;
    },
    provenanceFor() { return { source: 'test-fixture' }; }
  }
});
explainContext.window = explainContext;
load('assets/js/explain.js', explainContext);
(async () => {
  const baseline = explainContext.NexExplain.deterministic('length', 'm', 'ft', 1);
  assert(baseline.output.value > 3.2808 && baseline.output.value < 3.2809, 'deterministic explanation value is wrong');
  assert(baseline.calculation.deterministic === true, 'baseline is not marked deterministic');
  assert(baseline.calculation.network_required === false, 'baseline unexpectedly requires network');
  const fallback = await explainContext.NexExplain.explain({ category: 'length', from: 'm', to: 'ft', value: 1 });
  assert(fallback.source === 'deterministic-fallback', 'missing-model fallback contract failed');
  const verified = explainContext.NexExplain.verifyModelResult({ value: baseline.output.value, explanation: 'verified' }, baseline);
  assert(verified && verified.source === 'optional-model-verified', 'verified model result contract failed');
  const rejected = explainContext.NexExplain.verifyModelResult({ value: 999, explanation: 'wrong' }, baseline);
  assert(rejected === null, 'wrong model value was accepted');

  // Lightweight DOM fixture for embed.js, including URL prefill and postMessage.
  function element() {
    return {
      value: '', textContent: '', innerHTML: '', dataset: {}, options: [], listeners: {},
      appendChild(child) {
        this.options.push(child);
        if (child.selected || (this.value === '' && this.options.length === 1)) this.value = child.value;
      },
      addEventListener(type, fn) { this.listeners[type] = fn; }
    };
  }
  const elements = {
    '#embed-category': element(), '#embed-from': element(), '#embed-to': element(),
    '#embed-value': element(), '#embed-result': element(), '#embed-form': element()
  };
  const messages = [];
  const embedContext = vm.createContext({
    console,
    Number,
    String,
    URLSearchParams,
    window: null,
    document: {
      querySelector(selector) { return elements[selector]; },
      createElement() { return { value: '', textContent: '', selected: false }; }
    },
    NexlunaUnits: {
      length: { label: 'الطول', units: [['m', 'متر'], ['ft', 'قدم']] }
    },
    NexMCP: {
      convert(category, from, to, value) {
        assert(category === 'length' && from === 'm' && to === 'ft', 'embed request was not prefilled');
        return Number(value) / 0.3048;
      }
    }
  });
  embedContext.window = embedContext;
  embedContext.location = { search: '?category=length&from=m&to=ft&v=2' };
  embedContext.parent = { postMessage(message, origin) { messages.push({ message, origin }); } };
  load('assets/js/embed.js', embedContext);
  assert(elements['#embed-category'].value === 'length', 'embed category prefill failed');
  assert(elements['#embed-from'].value === 'm' && elements['#embed-to'].value === 'ft', 'embed unit prefill failed');
  assert(elements['#embed-value'].value === '2', 'embed value prefill failed');
  assert(elements['#embed-result'].dataset.state === 'success', 'embed initial conversion did not succeed');
  assert(messages.length === 1, 'embed did not emit exactly one result message');
  assert(messages[0].message.type === 'nexluna-result', 'wrong postMessage type');
  assert(messages[0].message.result > 6.56 && messages[0].message.result < 6.57, 'wrong embed result');
  assert(messages[0].origin === '*', 'unexpected postMessage origin contract');

  console.log('PASS: test_week6.js');
})().catch((error) => {
  console.error('FAIL: test_week6.js:', error.message);
  process.exitCode = 1;
});
