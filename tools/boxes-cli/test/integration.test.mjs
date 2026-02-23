import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { parseBoxesYaml } from '../src/parse.mjs';
import { validateSchema } from '../src/schema.mjs';
import { toElkGraph } from '../src/transform.mjs';
import { computeLayout } from '../src/layout.mjs';
import { renderSvg } from '../src/render-svg.mjs';
import { exportPng } from '../src/export-png.mjs';
import { readFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const fixture = (name) => join(__dirname, 'fixtures', name);

async function fullPipeline(fixtureName) {
  const yaml = readFileSync(fixture(fixtureName), 'utf8');
  const model = parseBoxesYaml(yaml);
  const errors = validateSchema(model);
  if (errors.length > 0) throw new Error(`Validation: ${errors.join(', ')}`);
  const elkInput = toElkGraph(model);
  const positioned = await computeLayout(elkInput);
  const svg = renderSvg(positioned, model);
  const png = await exportPng(svg, model.dpi);
  return { model, svg, png };
}

describe('Full pipeline integration', () => {
  it('renders minimal fixture end-to-end', async () => {
    const { svg, png } = await fullPipeline('minimal.boxes.yaml');
    assert.ok(svg.includes('<svg'), 'SVG output malformed');
    assert.equal(png[0], 0x89, 'PNG magic bytes missing');
    assert.ok(svg.includes('Inner A'), 'Missing box label');
    assert.ok(svg.includes('data flow'), 'Missing edge label');
  });

  it('renders AlertHub.Context end-to-end', async () => {
    const { model, svg, png } = await fullPipeline('example-context.boxes.yaml');
    assert.equal(model.diagram, 'AlertHub.Context');
    assert.ok(svg.includes('AlertHub'), 'Missing AlertHub box');
    assert.ok(svg.includes('SAP'), 'Missing source system');
    assert.ok(svg.includes('A-CAP'), 'Missing consumer');
    assert.ok(png.length > 1000, 'PNG suspiciously small');
  });

  it('renders AlertHub.System end-to-end', async () => {
    const { model, svg, png } = await fullPipeline('example-system.boxes.yaml');
    assert.equal(model.diagram, 'AlertHub.System');
    assert.ok(svg.includes('Mercury'), 'Missing Mercury container');
    assert.ok(svg.includes('CloudStack'), 'Missing CloudStack container');
    assert.ok(svg.includes('API Layer') || svg.includes('API_Layer'), 'Missing API Layer');
    assert.ok(png.length > 1000, 'PNG suspiciously small');
  });
});
