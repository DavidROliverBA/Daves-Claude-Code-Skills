import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { parseBoxesYaml } from '../src/parse.mjs';
import { validateSchema } from '../src/schema.mjs';
import { readFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const fixture = (name) => join(__dirname, 'fixtures', name);

describe('parseBoxesYaml', () => {
  it('parses minimal fixture into internal model', () => {
    const yaml = readFileSync(fixture('minimal.boxes.yaml'), 'utf8');
    const model = parseBoxesYaml(yaml);
    assert.equal(model.diagram, 'Test.Context');
    assert.equal(model.title, 'Minimal Test');
    assert.equal(model.flow, 'LR');
    assert.equal(model.dpi, 150);
  });

  it('flattens nested boxes into a tree with depth', () => {
    const yaml = readFileSync(fixture('minimal.boxes.yaml'), 'utf8');
    const model = parseBoxesYaml(yaml);
    assert.equal(model.boxes.length, 1);
    assert.equal(model.boxes[0].name, 'Outer');
    assert.equal(model.boxes[0].depth, 0);
    const children = model.boxes[0].children;
    assert.equal(children.length, 2);
    assert.equal(children[0].name, 'Inner A');
    assert.equal(children[0].depth, 1);
    assert.equal(children[1].name, 'Inner B');
  });

  it('extracts ports from box definitions', () => {
    const yaml = readFileSync(fixture('minimal.boxes.yaml'), 'utf8');
    const model = parseBoxesYaml(yaml);
    const innerB = model.boxes[0].children[1];
    assert.equal(innerB.ports.length, 2);
    assert.equal(innerB.ports[0].id, 'PortIn');
    assert.equal(innerB.ports[0].dir, 'in');
    assert.equal(innerB.ports[0].label, 'Input');
  });

  it('parses edges with box:port references', () => {
    const yaml = readFileSync(fixture('minimal.boxes.yaml'), 'utf8');
    const model = parseBoxesYaml(yaml);
    assert.equal(model.edges.length, 1);
    assert.equal(model.edges[0].from.box, 'Inner A');
    assert.equal(model.edges[0].from.port, null);
    assert.equal(model.edges[0].to.box, 'Inner B');
    assert.equal(model.edges[0].to.port, 'PortIn');
    assert.equal(model.edges[0].label, 'data flow');
  });

  it('parses legend', () => {
    const yaml = readFileSync(fixture('minimal.boxes.yaml'), 'utf8');
    const model = parseBoxesYaml(yaml);
    assert.deepEqual(model.legend.edgeColours, { Blue: 'Data flow' });
    assert.equal(model.legend.portTable, true);
  });
});

describe('validateSchema', () => {
  it('accepts valid YAML', () => {
    const yaml = readFileSync(fixture('minimal.boxes.yaml'), 'utf8');
    const model = parseBoxesYaml(yaml);
    const errors = validateSchema(model);
    assert.equal(errors.length, 0);
  });

  it('rejects missing diagram field', () => {
    const model = { title: 'Test', flow: 'LR', boxes: [], edges: [], legend: { edgeColours: {}, portTable: false }, actors: [], style: { font: 'Helvetica', borderWeight: [3], backgrounds: ['white'] }, dpi: 150 };
    const errors = validateSchema(model);
    assert.ok(errors.some(e => e.includes('diagram')));
  });

  it('rejects invalid flow direction', () => {
    const model = { diagram: 'X', flow: 'DIAGONAL', boxes: [], edges: [], legend: { edgeColours: {}, portTable: false }, actors: [], style: { font: 'Helvetica', borderWeight: [3], backgrounds: ['white'] }, dpi: 150 };
    const errors = validateSchema(model);
    assert.ok(errors.some(e => e.includes('flow')));
  });

  it('rejects invalid port direction', () => {
    const yaml = `
diagram: Test
flow: LR
boxes:
  A:
    ports:
      P1: { dir: sideways, label: "Bad" }
`;
    const model = parseBoxesYaml(yaml);
    const errors = validateSchema(model);
    assert.ok(errors.some(e => e.includes('dir')));
  });
});
