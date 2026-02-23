import { sanitiseId } from './parse.mjs';

/**
 * Map Boxes flow directions to ELK direction values.
 */
const FLOW_MAP = {
  LR: 'RIGHT',
  RL: 'LEFT',
  TB: 'DOWN',
  BT: 'UP',
};

/**
 * Determine the ELK port side based on port direction and diagram flow.
 *
 * For horizontal flows (LR/RL):
 *   in  -> WEST,  out -> EAST
 * For vertical flows (TB/BT):
 *   in  -> NORTH, out -> SOUTH
 *
 * @param {'in'|'out'} dir - Port direction
 * @param {string} flow - Diagram flow ('LR', 'RL', 'TB', 'BT')
 * @returns {string} ELK port side
 */
function portSide(dir, flow) {
  const isHorizontal = flow === 'LR' || flow === 'RL';
  if (dir === 'in') {
    return isHorizontal ? 'WEST' : 'NORTH';
  }
  return isHorizontal ? 'EAST' : 'SOUTH';
}

/**
 * Estimate pixel width for a compact node.
 * Compact nodes are small coloured shapes — the label text renders below them.
 * Width is based on the name line only (not description).
 * @param {string} name - The node name
 * @returns {number}
 */
function estimateCompactWidth(name) {
  if (!name) return 120;
  return Math.max(120, name.length * 9 + 40);
}

/**
 * Compact node total height — includes the coloured shape (50px)
 * plus space for below-node labels (technology, description).
 * ELK uses this full height for spacing, but the renderer only
 * draws the coloured box for the top 50px.
 * @param {string|null} technology
 * @param {string|null} description
 * @returns {number}
 */
function estimateCompactHeight(technology, description) {
  let h = 50; // coloured shape
  if (technology) h += 18;
  if (description) {
    const lines = description.split('\n').length;
    h += lines * 15 + 4;
  }
  return h;
}

/**
 * Estimate total width needed including below-node labels (for ELK spacing).
 * @param {string} name
 * @param {string} technology
 * @param {string} description
 * @returns {number}
 */
function estimateLabelledWidth(name, technology, description) {
  let maxLen = name ? name.length : 10;
  if (technology) maxLen = Math.max(maxLen, technology.length + 2);
  if (description) {
    const descLines = description.split('\n');
    for (const l of descLines) maxLen = Math.max(maxLen, l.length);
  }
  return Math.max(150, maxLen * 8 + 40);
}

/**
 * Transform a parsed port into an ELK port object.
 *
 * Port IDs are globally unique: `{boxId}_{portId}`.
 *
 * @param {Object} port - Internal port model { id, dir, label }
 * @param {string} boxId - The sanitised parent box ID
 * @param {string} flow - Diagram flow direction
 * @returns {Object} ELK port node
 */
/**
 * Map explicit side names to ELK port side values.
 */
const SIDE_MAP = {
  north: 'NORTH',
  south: 'SOUTH',
  east: 'EAST',
  west: 'WEST',
};

function transformPort(port, boxId, flow) {
  // Use explicit side override if provided, otherwise compute from direction
  const side = port.side ? (SIDE_MAP[port.side] || portSide(port.dir, flow)) : portSide(port.dir, flow);
  return {
    id: `${boxId}_${port.id}`,
    layoutOptions: {
      'elk.port.side': side,
    },
    labels: [{ text: port.label || port.id }],
    width: 8,
    height: 8,
  };
}

/**
 * Recursively transform internal box nodes into ELK children.
 *
 * Compound nodes (those with children) omit explicit width/height so
 * ELK can size them based on their contents.
 *
 * @param {Array} boxes - Internal box tree
 * @param {string} flow - Diagram flow direction
 * @returns {Array} ELK child nodes
 */
function transformBoxes(boxes, flow) {
  if (!boxes || boxes.length === 0) return [];

  return boxes.map((box) => {
    const isCompound = box.children && box.children.length > 0;
    const name = box.label || box.name;

    const elkNode = {
      id: box.id,
      labels: [{ text: name }],
      ports: box.ports.map((p) => transformPort(p, box.id, flow)),
      children: transformBoxes(box.children, flow),
    };

    // Nodes with ports: enforce side constraints and distribute evenly
    if (box.ports.length > 0) {
      elkNode.layoutOptions = {
        ...elkNode.layoutOptions,
        'elk.portConstraints': 'FIXED_SIDE',
        'elk.portAlignment.default': 'DISTRIBUTED',
        'elk.spacing.portPort': '20',
        'elk.portLabels.placement': 'OUTSIDE',
        'elk.portLabels.nextToPortIfPossible': 'true',
        'elk.spacing.portsSurrounding': '[top=10,left=10,bottom=10,right=10]',
      };
    }

    if (isCompound) {
      // Let ELK determine the size for compound nodes
      elkNode.layoutOptions = {
        ...elkNode.layoutOptions,
        'elk.padding': '[top=70,left=24,bottom=60,right=24]',
      };
    } else {
      // Determine if this is a full-sized node (custom multi-line label) or compact
      const hasCustomLabel = box.label && box.label !== box.name && box.label.includes('\n');
      if (hasCustomLabel) {
        // Full-sized node: label rendered inside the box
        const fullLabel = box.label;
        const lines = fullLabel.split('\n');
        const longest = Math.max(...lines.map(l => l.length));
        const w = Math.max(160, longest * 9 + 50);
        const h = lines.length * 20 + 40;
        elkNode.width = w;
        elkNode.height = h;
        elkNode.layoutOptions = {
          ...elkNode.layoutOptions,
          'elk.nodeSize.constraints': 'MINIMUM_SIZE',
          'elk.nodeSize.minimum': `(${w},${h})`,
        };
      } else {
        // Compact node: small shape, labels render below in SVG
        const w = estimateLabelledWidth(box.name, box.technology, box.description);
        const h = estimateCompactHeight(box.technology, box.description);
        elkNode.width = w;
        elkNode.height = h;
        elkNode.layoutOptions = {
          ...elkNode.layoutOptions,
          'elk.nodeSize.constraints': 'MINIMUM_SIZE',
          'elk.nodeSize.minimum': `(${w},${h})`,
        };
      }
    }

    return elkNode;
  });
}

/**
 * Resolve an edge endpoint (from/to) to an ELK source/target ID.
 *
 * If a port is specified, returns `{boxId}_{portId}`.
 * If no port, returns the sanitised box ID.
 *
 * @param {{ box: string, port: string|null }} ref - Edge endpoint reference
 * @returns {{ nodeId: string, portId: string|undefined }}
 */
function resolveEdgeEndpoint(ref) {
  const boxId = sanitiseId(ref.box);
  if (ref.port) {
    return { nodeId: boxId, portId: `${boxId}_${ref.port}` };
  }
  return { nodeId: boxId, portId: undefined };
}

/**
 * Transform internal edges into ELK edge objects.
 *
 * @param {Array} edges - Internal edge model
 * @returns {Array} ELK edge objects
 */
function transformEdges(edges) {
  if (!edges || edges.length === 0) return [];

  return edges.map((edge, index) => {
    const from = resolveEdgeEndpoint(edge.from);
    const to = resolveEdgeEndpoint(edge.to);

    const elkEdge = {
      id: `e${index}`,
      sources: [from.portId || from.nodeId],
      targets: [to.portId || to.nodeId],
    };

    if (edge.label) {
      elkEdge.labels = [{ text: edge.label }];
    }

    return elkEdge;
  });
}

/**
 * Transform the internal Boxes diagram model into an ELK JSON graph.
 *
 * This is the main entry point for the transform module. It takes the
 * output of `parseBoxesYaml()` and produces a graph suitable for
 * `elk.layout()`.
 *
 * @param {Object} model - Internal model from parse.mjs
 * @returns {Object} ELK JSON graph
 */
export function toElkGraph(model) {
  const direction = FLOW_MAP[model.flow] || 'RIGHT';

  return {
    id: 'root',
    layoutOptions: {
      'elk.algorithm': 'layered',
      'elk.direction': direction,

      // Hierarchy
      'elk.hierarchyHandling': 'INCLUDE_CHILDREN',

      // Edge routing — orthogonal with smooth corners rendered in SVG
      'elk.edgeRouting': 'ORTHOGONAL',
      'elk.layered.nodePlacement.favorStraightEdges': 'true',

      // Node spacing — generous for clean layout
      'elk.spacing.nodeNode': '40',
      'elk.layered.spacing.nodeNodeBetweenLayers': '160',
      'elk.spacing.componentComponent': '40',

      // Edge spacing
      'elk.spacing.edgeNode': '35',
      'elk.spacing.edgeEdge': '25',
      'elk.layered.spacing.edgeNodeBetweenLayers': '50',
      'elk.layered.spacing.edgeEdgeBetweenLayers': '30',

      // Edge labels
      'elk.spacing.edgeLabel': '10',
      'elk.layered.edgeLabels.sideSelection': 'SMART_UP',
      'elk.layered.edgeLabels.centerLabelPlacementStrategy': 'MEDIAN_LAYER',

      // Crossing minimisation
      'elk.layered.crossingMinimization.strategy': 'LAYER_SWEEP',
      'elk.layered.crossingMinimization.greedySwitch.type': 'TWO_SIDED',
      'elk.layered.crossingMinimization.greedySwitchHierarchical.type': 'TWO_SIDED',
      'elk.layered.thoroughness': '7',

      // Node placement
      'elk.layered.nodePlacement.strategy': 'BRANDES_KOEPF',
      'elk.layered.nodePlacement.bk.fixedAlignment': 'BALANCED',

      // Post-compaction — reclaim whitespace while minimising edge length
      'elk.layered.compaction.postCompaction.strategy': 'EDGE_LENGTH',
      'elk.layered.compaction.connectedComponents': 'true',
    },
    children: transformBoxes(model.boxes, model.flow),
    edges: transformEdges(model.edges),
  };
}
