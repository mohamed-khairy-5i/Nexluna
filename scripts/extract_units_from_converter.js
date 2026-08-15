'use strict';

const fs = require('fs');
const vm = require('vm');
const path = require('path');

const root = path.resolve(__dirname, '..');
const sourcePath = path.join(root, 'assets/js/converter.js');
const outputPath = path.join(root, 'data/units.json');
const source = fs.readFileSync(sourcePath, 'utf8');
const match = source.match(/var DATA = (\{[\s\S]*?\n  \});\n\n  var STORE/);
if (!match) throw new Error('Could not locate DATA object in converter.js');

const data = vm.runInNewContext('(' + match[1] + ')', { Math });
fs.writeFileSync(outputPath, JSON.stringify(data, null, 2) + '\n');
console.log(`Wrote ${Object.keys(data).length} categories to ${path.relative(root, outputPath)}`);
