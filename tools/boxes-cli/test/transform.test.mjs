import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { parseBoxesYaml } from '../src/parse.mjs';
import { toElkGraph } from '../src/transform.mjs';
import { readFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const fixture = (name) => join(__dirname, 'fixtures', name);

describe('toElkGraph', () => {
  it('sets correct layout options and LR direction', () => {
    const yaml = readFileSync(fixture('minimal.boxes.yaml'), 'utf8');
    const model = parseBoxesYaml(yaml);
    const elk = toElkGraph(model);

    assert.equal(elk.id, 'root');
    assert.equal(elk.layoutOptions['elk.algorithm'], 'layered');
    assert.equal(elk.layoutOptions['elk.direction'], 'RIGHT');
    assert.equal(elk.layoutOptions['elk.edgeRouting'], 'ORTHOGONAL');
    assert.equal(elk.layoutOptions['elk.hierarchyHandling'], 'INCLUDE_CHILDREN');
    assert.equal(elk.layoutOptions['elk.spacing.nodeNode'], '40');
    assert.equal(elk.layoutOptions['elk.spacing.edgeNode'], '35');
    assert.equal(
      elk.layoutOptions['elk.layered.spacing.nodeNodeBetweenLayers'],
      '160'
    );
    assert.equal(
      elk.layoutOptions['elk.layered.crossingMinimization.strategy'],
      'LAYER_SWEEP'
    );
    assert.equal(
      elk.layoutOptions['elk.layered.nodePlacement.strategy'],
      'BRANDES_KOEPF'
    );
    // Layout tuning options
    assert.equal(elk.layoutOptions['elk.spacing.edgeEdge'], '25');
    assert.equal(elk.layoutOptions['elk.layered.spacing.edgeNodeBetweenLayers'], '50');
    assert.equal(elk.layoutOptions['elk.layered.spacing.edgeEdgeBetweenLayers'], '30');
    assert.equal(elk.layoutOptions['elk.layered.crossingMinimization.greedySwitchHierarchical.type'], 'TWO_SIDED');
    assert.equal(elk.layoutOptions['elk.layered.compaction.postCompaction.strategy'], 'EDGE_LENGTH');
    assert.equal(elk.layoutOptions['elk.layered.nodePlacement.bk.fixedAlignment'], 'BALANCED');
    assert.equal(elk.layoutOptions['elk.layered.thoroughness'], '7');
  });

  it('maps nested boxes to ELK children hierarchy', () => {
    const yaml = readFileSync(fixture('minimal.boxes.yaml'), 'utf8');
    const model = parseBoxesYaml(yaml);
    const elk = toElkGraph(model);

    // Top level: one box (Outer)
    assert.equal(elk.children.length, 1);
    const outer = elk.children[0];
    assert.equal(outer.id, 'Outer');
    assert.deepEqual(outer.labels, [{ text: 'Outer' }]);

    // Outer is compound — should not have explicit width/height
    assert.equal(outer.width, undefined);
    assert.equal(outer.height, undefined);

    // Two children: Inner_A and Inner_B
    assert.equal(outer.children.length, 2);
    assert.equal(outer.children[0].id, 'Inner_A');
    assert.equal(outer.children[1].id, 'Inner_B');

    // Leaf nodes have explicit width/height
    assert.ok(outer.children[0].width > 0);
    assert.ok(outer.children[0].height > 0);
  });

  it('maps ports to ELK port objects with correct side constraints', () => {
    const yaml = readFileSync(fixture('minimal.boxes.yaml'), 'utf8');
    const model = parseBoxesYaml(yaml);
    const elk = toElkGraph(model);

    const innerB = elk.children[0].children[1]; // Inner_B
    assert.equal(innerB.ports.length, 2);

    // PortIn: dir=in + LR flow -> WEST
    const portIn = innerB.ports[0];
    assert.equal(portIn.id, 'Inner_B_PortIn');
    assert.equal(portIn.layoutOptions['elk.port.side'], 'WEST');
    assert.deepEqual(portIn.labels, [{ text: 'Input' }]);

    // PortOut: dir=out + LR flow -> EAST
    const portOut = innerB.ports[1];
    assert.equal(portOut.id, 'Inner_B_PortOut');
    assert.equal(portOut.layoutOptions['elk.port.side'], 'EAST');
    assert.deepEqual(portOut.labels, [{ text: 'Output' }]);
  });

  it('maps edges with correct source/target port IDs', () => {
    const yaml = readFileSync(fixture('minimal.boxes.yaml'), 'utf8');
    const model = parseBoxesYaml(yaml);
    const elk = toElkGraph(model);

    assert.equal(elk.edges.length, 1);
    const edge = elk.edges[0];

    // from: Inner A (no port) -> source is box ID
    assert.deepEqual(edge.sources, ['Inner_A']);

    // to: Inner B:PortIn -> target is boxId_portId
    assert.deepEqual(edge.targets, ['Inner_B_PortIn']);

    // Label preserved
    assert.deepEqual(edge.labels, [{ text: 'data flow' }]);
  });

  it('maps TB direction to DOWN', () => {
    const model = parseBoxesYaml(`
diagram: Test.TB
flow: TB
boxes:
  A: {}
  B: {}
edges:
  - from: A
    to: B
`);
    const elk = toElkGraph(model);
    assert.equal(elk.layoutOptions['elk.direction'], 'DOWN');
  });

  it('maps port sides correctly for TB flow', () => {
    const model = parseBoxesYaml(`
diagram: Test.TB
flow: TB
boxes:
  Node:
    ports:
      Top: { dir: in, label: "In" }
      Bottom: { dir: out, label: "Out" }
`);
    const elk = toElkGraph(model);
    const node = elk.children[0];

    // dir=in + TB -> NORTH
    assert.equal(node.ports[0].layoutOptions['elk.port.side'], 'NORTH');
    // dir=out + TB -> SOUTH
    assert.equal(node.ports[1].layoutOptions['elk.port.side'], 'SOUTH');
  });

  it('maps RL direction to LEFT', () => {
    const model = parseBoxesYaml(`
diagram: Test.RL
flow: RL
boxes:
  X: {}
`);
    const elk = toElkGraph(model);
    assert.equal(elk.layoutOptions['elk.direction'], 'LEFT');
  });

  it('maps BT direction to UP', () => {
    const model = parseBoxesYaml(`
diagram: Test.BT
flow: BT
boxes:
  X: {}
`);
    const elk = toElkGraph(model);
    assert.equal(elk.layoutOptions['elk.direction'], 'UP');
  });
});
