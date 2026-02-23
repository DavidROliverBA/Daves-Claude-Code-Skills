import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { parseBoxesYaml } from '../src/parse.mjs';
import { toElkGraph } from '../src/transform.mjs';
import { computeLayout } from '../src/layout.mjs';
import { readFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const fixture = (name) => join(__dirname, 'fixtures', name);

/**
 * Full pipeline helper: parse YAML -> transform -> layout.
 */
async function pipelineLayout(yamlPath) {
  const yaml = readFileSync(yamlPath, 'utf8');
  const model = parseBoxesYaml(yaml);
  const elkGraph = toElkGraph(model);
  return computeLayout(elkGraph);
}

describe('computeLayout', () => {
  it('returns positioned graph with x/y on all nodes', async () => {
    const result = await pipelineLayout(fixture('minimal.boxes.yaml'));

    // Root has dimensions
    assert.ok(result.width > 0, 'root width should be > 0');
    assert.ok(result.height > 0, 'root height should be > 0');

    // Top-level child (Outer) has x/y
    const outer = result.children[0];
    assert.equal(typeof outer.x, 'number', 'Outer should have x');
    assert.equal(typeof outer.y, 'number', 'Outer should have y');
    assert.ok(outer.width > 0, 'Outer width should be > 0');
    assert.ok(outer.height > 0, 'Outer height should be > 0');

    // Nested children have x/y
    for (const child of outer.children) {
      assert.equal(typeof child.x, 'number', `${child.id} should have x`);
      assert.equal(typeof child.y, 'number', `${child.id} should have y`);
      assert.ok(child.width > 0, `${child.id} width should be > 0`);
      assert.ok(child.height > 0, `${child.id} height should be > 0`);
    }
  });

  it('positions ports on nodes with x/y', async () => {
    const result = await pipelineLayout(fixture('minimal.boxes.yaml'));

    // Inner_B has ports
    const innerB = result.children[0].children.find(
      (c) => c.id === 'Inner_B'
    );
    assert.ok(innerB, 'Inner_B should exist');
    assert.ok(innerB.ports.length > 0, 'Inner_B should have ports');

    for (const port of innerB.ports) {
      assert.equal(typeof port.x, 'number', `Port ${port.id} should have x`);
      assert.equal(typeof port.y, 'number', `Port ${port.id} should have y`);
    }
  });

  it('produces edges with sections containing startPoint and endPoint', async () => {
    const result = await pipelineLayout(fixture('minimal.boxes.yaml'));

    assert.ok(result.edges.length > 0, 'should have at least one edge');

    const edge = result.edges[0];
    assert.ok(edge.sections, 'edge should have sections');
    assert.ok(edge.sections.length > 0, 'edge should have at least one section');

    const section = edge.sections[0];
    assert.ok(section.startPoint, 'section should have startPoint');
    assert.equal(typeof section.startPoint.x, 'number', 'startPoint.x should be a number');
    assert.equal(typeof section.startPoint.y, 'number', 'startPoint.y should be a number');

    assert.ok(section.endPoint, 'section should have endPoint');
    assert.equal(typeof section.endPoint.x, 'number', 'endPoint.x should be a number');
    assert.equal(typeof section.endPoint.y, 'number', 'endPoint.y should be a number');
  });
});
