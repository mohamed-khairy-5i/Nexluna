#!/usr/bin/env node
'use strict';

const fs = require('fs');
const vm = require('vm');
const assert = require('assert');
const path = require('path');

const root = { console, navigator: {} };
root.globalThis = root;
const context = vm.createContext(root);
for (const relative of ['assets/js/units.generated.js', 'assets/js/webmcp.js']) {
  vm.runInContext(fs.readFileSync(path.join(__dirname, relative), 'utf8'), context, { filename: relative });
}

assert.strictEqual(root.NexMCP.apiVersion, '1.0.0');
assert.strictEqual(root.NexMCP.categories.length, 14);
assert.ok(root.NexMCP.tools.some((tool) => tool.name === 'convert_units'));
assert.ok(root.NexMCP.tools.some((tool) => tool.name === 'list_units'));
assert.ok(root.NexMCP.tools.some((tool) => tool.name === 'get_unit_info'));

const convertTool = root.NexMCP.tools.find((tool) => tool.name === 'convert_units');
const listTool = root.NexMCP.tools.find((tool) => tool.name === 'list_units');
const infoTool = root.NexMCP.tools.find((tool) => tool.name === 'get_unit_info');

(async () => {
  const converted = await convertTool.execute({ category: 'area', from: 'feddan', to: 'm2', value: 1 });
  assert.strictEqual(converted.isError, undefined);
  assert.strictEqual(converted.structuredContent.output.value, 4200.833);
  assert.strictEqual(converted.structuredContent.calculation.deterministic, true);
  assert.strictEqual(converted.structuredContent.calculation.network_required, false);
  assert.strictEqual(converted.structuredContent.provenance.input.region, 'Egypt');
  assert.strictEqual(converted.structuredContent.provenance.output.region, 'international / Egypt');

  const categories = await listTool.execute({});
  assert.strictEqual(categories.structuredContent.categories.length, 14);
  const area = await listTool.execute({ category: 'area' });
  assert.ok(area.structuredContent.units.includes('feddan'));
  assert.strictEqual(area.structuredContent.provenance.schema_version, '1.0');

  const info = await infoTool.execute({ category: 'area', unit: 'feddan' });
  assert.strictEqual(info.structuredContent.data.provenance.region, 'Egypt');
  assert.strictEqual(info.structuredContent.data.provenance.reviewed, '2026-08-15');

  const invalid = await convertTool.execute({ category: 'area', from: 'feddan', to: 'not-a-unit', value: 1 });
  assert.strictEqual(invalid.isError, true);
  assert.strictEqual(invalid.structuredContent.error.code, 'UNKNOWN_UNIT');

  console.log('PASS — WebMCP/API v1 contract, deterministic conversion, provenance, and typed errors verified.');
})().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
