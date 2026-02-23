import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { renderSvg } from '../src/render-svg.mjs';
import { computeLayout } from '../src/layout.mjs';
import { toElkGraph } from '../src/transform.mjs';
import { parseBoxesYaml } from '../src/parse.mjs';
import { readFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const fixture = (name) => join(__dirname, 'fixtures', name);

async function renderFixture(name) {
  const yaml = readFileSync(fixture(name), 'utf8');
  const model = parseBoxesYaml(yaml);
  const elkInput = toElkGraph(model);
  const positioned = await computeLayout(elkInput);
  return renderSvg(positioned, model);
}

describe('renderSvg', () => {
  it('produces valid SVG with correct root element', async () => {
    const svg = await renderFixture('minimal.boxes.yaml');
    assert.ok(svg.startsWith('<svg'));
    assert.ok(svg.includes('xmlns="http://www.w3.org/2000/svg"'));
    assert.ok(svg.endsWith('</svg>'));
  });

  it('renders boxes as rect elements', async () => {
    const svg = await renderFixture('minimal.boxes.yaml');
    assert.ok(svg.includes('<rect'), 'No rect elements found');
    const rectCount = (svg.match(/<rect /g) || []).length;
    assert.ok(rectCount >= 3, `Expected >= 3 rects, got ${rectCount}`);
  });

  it('renders box labels as text elements', async () => {
    const svg = await renderFixture('minimal.boxes.yaml');
    assert.ok(svg.includes('Inner A'), 'Missing Inner A label');
    assert.ok(svg.includes('Inner B'), 'Missing Inner B label');
    assert.ok(svg.includes('Outer'), 'Missing Outer label');
  });

  it('renders edges as path elements', async () => {
    const svg = await renderFixture('minimal.boxes.yaml');
    assert.ok(svg.includes('<path'), 'No path elements for edges');
  });

  it('renders edge labels', async () => {
    const svg = await renderFixture('minimal.boxes.yaml');
    assert.ok(svg.includes('data flow'), 'Missing edge label');
  });

  it('renders port markers', async () => {
    const svg = await renderFixture('minimal.boxes.yaml');
    assert.ok(svg.includes('class="port"'), 'No port markers found');
  });

  it('renders diagram title', async () => {
    const svg = await renderFixture('minimal.boxes.yaml');
    assert.ok(svg.includes('Minimal Test'), 'Missing diagram title');
  });

  it('positions NORTH port labels above port with middle anchor', async () => {
    const svg = await renderFixture('example-cloudstack.boxes.yaml');
    const northPortPattern = /text-anchor="middle"[^>]*>Raw Data In</;
    assert.ok(northPortPattern.test(svg), 'NORTH port label should use text-anchor="middle"');
  });

  it('positions SOUTH port labels below port with middle anchor', async () => {
    const svg = await renderFixture('example-cloudstack.boxes.yaml');
    const southPortPattern = /text-anchor="middle"[^>]*>Curated Out</;
    assert.ok(southPortPattern.test(svg), 'SOUTH port label should use text-anchor="middle"');
  });
});
