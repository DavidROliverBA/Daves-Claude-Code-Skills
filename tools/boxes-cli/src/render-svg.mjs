import { sanitiseId } from './parse.mjs';

/**
 * Map colour names to hex values for legend rendering.
 */
const COLOUR_MAP = {
  brown: '#8B4513',
  'dark blue': '#1A5276',
  blue: '#2E86C1',
  green: '#1E8449',
  purple: '#7D3C98',
  grey: '#999',
  'grey dashed': '#999',
  orange: '#FF9900',
  cyan: '#00BFFF',
  red: '#E74C3C',
  gold: '#D4AC0D',
  'light blue': '#5DADE2',
  'snowflake blue': '#29B5E8',
  'dbt red': '#FF694B',
};

/**
 * Resolve a colour name to a hex value.
 * If the value is already a hex colour or rgb value, return it as-is.
 */
function resolveColour(name) {
  if (!name) return '#333';
  const lower = name.toLowerCase();
  return COLOUR_MAP[lower] || name;
}

/**
 * Escape XML special characters in text content.
 */
function esc(str) {
  if (!str) return '';
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&apos;');
}

/**
 * Make a CSS-safe ID from a hex colour for marker references.
 */
function colourToId(hex) {
  return hex.replace(/[^a-zA-Z0-9]/g, '');
}

/**
 * Get border weight for a given depth from the model's borderWeight array.
 */
function getBorderWeight(weights, depth) {
  if (!weights || weights.length === 0) return 1;
  const idx = Math.min(depth, weights.length - 1);
  return weights[idx];
}

/**
 * Get background colour for a given depth from the model's backgrounds array.
 */
function getBackground(backgrounds, depth) {
  if (!backgrounds || backgrounds.length === 0) return 'white';
  const idx = Math.min(depth, backgrounds.length - 1);
  return backgrounds[idx];
}

/**
 * Build a lookup map from box ID to model box definition (recursive).
 */
function buildBoxLookup(modelBoxes, map = new Map()) {
  for (const box of modelBoxes) {
    map.set(box.id, box);
    if (box.children && box.children.length > 0) {
      buildBoxLookup(box.children, map);
    }
  }
  return map;
}

/**
 * Collect all ports from all boxes recursively.
 */
function collectAllPorts(modelBoxes) {
  const ports = [];
  for (const box of modelBoxes) {
    if (box.ports && box.ports.length > 0) {
      for (const port of box.ports) {
        ports.push({
          boxName: box.name,
          portLabel: port.label || port.id,
          portDir: port.dir,
        });
      }
    }
    if (box.children && box.children.length > 0) {
      ports.push(...collectAllPorts(box.children));
    }
  }
  return ports;
}

/**
 * Render multi-line text as tspan elements.
 * Returns an array of tspan strings.
 */
function renderTspans(text, x, lineHeight, anchor) {
  const lines = text.split('\n');
  return lines.map((line, i) => {
    const anchorAttr = anchor ? ` text-anchor="${anchor}"` : '';
    return `<tspan x="${x}"${anchorAttr} dy="${i === 0 ? 0 : lineHeight}">${esc(line)}</tspan>`;
  }).join('');
}

/**
 * Render a single positioned ELK node (and its children) as SVG elements.
 *
 * Compact node style: small coloured shape with name inside.
 * Technology and description render BELOW the node as external labels.
 * Compound nodes remain as boundary rectangles.
 */
function renderNode(node, style, boxLookup, depth) {
  const parts = [];
  const x = node.x || 0;
  const y = node.y || 0;
  const w = node.width || 0;
  const h = node.height || 0;
  const isCompound = node.children && node.children.length > 0;

  const modelBox = boxLookup.get(node.id);
  const boxStyle = modelBox?.style || {};
  const isActor = modelBox?.actor === true;

  const fill = boxStyle.background || getBackground(style.backgrounds, depth);
  const stroke = boxStyle.color || '#1B2A4A';
  const strokeWidth = getBorderWeight(style.borderWeight, depth);

  parts.push(`<g transform="translate(${x}, ${y})">`);

  if (isCompound) {
    // Compound node — boundary rectangle with label
    parts.push(
      `  <rect width="${w}" height="${h}" rx="6" ry="6" ` +
      `fill="${esc(fill)}" stroke="${esc(stroke)}" stroke-width="${strokeWidth}" />`
    );

    const label = node.labels?.[0]?.text || '';
    if (label) {
      const tspans = renderTspans(label, 12, 16);
      parts.push(
        `  <text x="12" y="22" font-size="13" font-weight="bold" ` +
        `fill="${esc(stroke)}">${tspans}</text>`
      );
    }

    // Zoom annotation for compound nodes
    const zoom = modelBox?.zoom;
    if (zoom) {
      const labelLines = (node.labels?.[0]?.text || '').split('\n').length;
      const zoomY = 22 + labelLines * 16 + 2;
      parts.push(
        `  <text x="12" y="${zoomY}" font-size="10" font-style="italic" ` +
        `fill="#666">\u2192 Zoom in: ${esc(zoom)}</text>`
      );
    }
  } else {
    // Leaf node — check if full-sized (custom multi-line label) or compact
    const hasCustomLabel = modelBox?.label && modelBox.label !== modelBox.name && modelBox.label.includes('\n');

    if (hasCustomLabel) {
      // Full-sized node: coloured box fills the entire ELK area
      const rx = 8;
      const compactFill = boxStyle.background || fill;
      parts.push(
        `  <rect width="${w}" height="${h}" rx="${rx}" ry="${rx}" ` +
        `fill="${esc(compactFill)}" stroke="${esc(stroke)}" stroke-width="${strokeWidth}" />`
      );

      const fullLabel = modelBox.label;
      const lines = fullLabel.split('\n');
      const lineHeight = 18;
      const totalH = lines.length * lineHeight;
      const startY = (h - totalH) / 2 + 14;
      lines.forEach((line, i) => {
        const isBold = i === 0;
        const fontSize = i === 0 ? 14 : (i <= 1 ? 11 : 10);
        const fontWeight = isBold ? 'font-weight="bold"' : '';
        const fillCol = i === 0 ? stroke : (i <= 1 ? '#555' : '#777');
        parts.push(
          `  <text x="${w / 2}" y="${startY + i * lineHeight}" text-anchor="middle" ` +
          `font-size="${fontSize}" ${fontWeight} fill="${esc(fillCol)}">${esc(line)}</text>`
        );
      });

      // Zoom annotation inside full-sized box
      const zoom = modelBox?.zoom;
      if (zoom) {
        parts.push(
          `  <text x="${w / 2}" y="${h - 8}" text-anchor="middle" font-size="9" font-style="italic" ` +
          `fill="#666">\u2192 ${esc(zoom)}</text>`
        );
      }
    } else {
      // Compact node: coloured box is only top 50px, labels below
      const boxH = 50;
      const rx = isActor ? Math.min(boxH / 2, 20) : 8;
      const compactFill = boxStyle.background || (isActor ? '#E8DAEF' : fill);
      parts.push(
        `  <rect width="${w}" height="${boxH}" rx="${rx}" ry="${rx}" ` +
        `fill="${esc(compactFill)}" stroke="${esc(stroke)}" stroke-width="${strokeWidth}" />`
      );

      // Name inside the compact shape (bold, centred)
      const name = modelBox?.name || '';
      if (name) {
        parts.push(
          `  <text x="${w / 2}" y="${boxH / 2 + 5}" text-anchor="middle" ` +
          `font-size="13" font-weight="bold" fill="${esc(stroke)}">${esc(name)}</text>`
        );
      }

      // Technology + description BELOW the visible box
      let belowY = boxH + 15;
      const technology = modelBox?.technology;
      if (technology) {
        parts.push(
          `  <text x="${w / 2}" y="${belowY}" text-anchor="middle" ` +
          `font-size="10" font-style="italic" fill="#666">[${esc(technology)}]</text>`
        );
        belowY += 14;
      }
      const description = modelBox?.description;
      if (description) {
        const descLines = description.split('\n');
        descLines.forEach((dl, i) => {
          parts.push(
            `  <text x="${w / 2}" y="${belowY + i * 13}" text-anchor="middle" ` +
            `font-size="10" fill="#555">${esc(dl)}</text>`
          );
        });
      }

      // Zoom annotation below description
      const zoom = modelBox?.zoom;
      if (zoom) {
        const descLineCount = description ? description.split('\n').length : 0;
        const zoomY = belowY + descLineCount * 12 + (description ? 4 : 0);
        parts.push(
          `  <text x="${w / 2}" y="${zoomY}" text-anchor="middle" font-size="9" font-style="italic" ` +
          `fill="#666">\u2192 ${esc(zoom)}</text>`
        );
      }
    }
  }

  // Ports — coloured circles on boundary
  if (node.ports && node.ports.length > 0) {
    for (const port of node.ports) {
      const px = port.x || 0;
      const py = port.y || 0;
      const pw = port.width || 8;
      const ph = port.height || 8;
      const r = 5;
      const cx = px + pw / 2;
      const cy = py + ph / 2;

      parts.push(
        `  <circle class="port" cx="${cx}" cy="${cy}" r="${r}" ` +
        `fill="${esc(stroke)}" stroke="white" stroke-width="1.5" />`
      );
    }
  }

  // Recurse into children
  if (isCompound) {
    for (const child of node.children) {
      parts.push(renderNode(child, style, boxLookup, depth + 1));
    }
  }

  parts.push('</g>');
  return parts.join('\n');
}

/**
 * Compute a point at a given fraction (0–1) along the full edge path.
 * Generalises the old midpoint function to support collision avoidance.
 *
 * @param {Object} section - ELK edge section with startPoint, endPoint, bendPoints
 * @param {number} offsetX - Container X offset
 * @param {number} offsetY - Container Y offset
 * @param {number} [fraction=0.5] - Position along the path (0 = start, 1 = end)
 * @returns {{ x: number, y: number }}
 */
function edgePointAtFraction(section, offsetX, offsetY, fraction = 0.5) {
  const sp = section.startPoint;
  const ep = section.endPoint;
  const bends = section.bendPoints || [];

  const pts = [
    { x: sp.x + offsetX, y: sp.y + offsetY },
    ...bends.map(bp => ({ x: bp.x + offsetX, y: bp.y + offsetY })),
    { x: ep.x + offsetX, y: ep.y + offsetY },
  ];

  let totalLen = 0;
  for (let i = 1; i < pts.length; i++) {
    const dx = pts[i].x - pts[i - 1].x;
    const dy = pts[i].y - pts[i - 1].y;
    totalLen += Math.sqrt(dx * dx + dy * dy);
  }

  const target = totalLen * fraction;
  let walked = 0;
  for (let i = 1; i < pts.length; i++) {
    const dx = pts[i].x - pts[i - 1].x;
    const dy = pts[i].y - pts[i - 1].y;
    const segLen = Math.sqrt(dx * dx + dy * dy);
    if (walked + segLen >= target && segLen > 0) {
      const t = (target - walked) / segLen;
      return {
        x: pts[i - 1].x + dx * t,
        y: pts[i - 1].y + dy * t,
      };
    }
    walked += segLen;
  }

  // Fallback: simple midpoint
  return {
    x: (sp.x + ep.x) / 2 + offsetX,
    y: (sp.y + ep.y) / 2 + offsetY,
  };
}

/**
 * Check whether two axis-aligned rectangles overlap (with padding).
 * Each rect is { x, y, w, h } where (x, y) is the top-left corner.
 * A padding of 4px is added around each rect to prevent labels from
 * touching each other even when they don't technically overlap.
 */
function rectsOverlap(a, b, pad = 4) {
  return !(a.x + a.w + pad < b.x || b.x + b.w + pad < a.x ||
           a.y + a.h + pad < b.y || b.y + b.h + pad < a.y);
}

/**
 * Find a position for an edge label that doesn't overlap previously placed labels.
 *
 * Strategy:
 *   1. Try the midpoint (0.5) first
 *   2. Try alternative fractions along the path (0.35, 0.65, 0.25, 0.75, 0.15, 0.85)
 *   3. If all path positions overlap, nudge perpendicular to the edge direction
 *   4. Last resort: accept the midpoint as-is
 *
 * @param {Object} section - ELK edge section
 * @param {number} offsetX - Container X offset
 * @param {number} offsetY - Container Y offset
 * @param {number} textW - Estimated label width in pixels
 * @param {number} textH - Estimated label height in pixels
 * @param {Array} placedRects - Already-placed label bounding boxes
 * @returns {{ point: {x,y}, rect: {x,y,w,h} }}
 */
function findLabelPosition(section, offsetX, offsetY, textW, textH, placedRects) {
  const fractions = [0.5, 0.35, 0.65, 0.25, 0.75, 0.15, 0.85];

  for (const frac of fractions) {
    const pt = edgePointAtFraction(section, offsetX, offsetY, frac);
    const rect = { x: pt.x - textW / 2, y: pt.y - textH + 2, w: textW, h: textH };

    if (!placedRects.some(placed => rectsOverlap(rect, placed))) {
      return { point: pt, rect };
    }
  }

  // All path positions overlap — try nudges from multiple path points
  // For each of several reference fractions, try offsets in all directions
  const refFracs = [0.5, 0.3, 0.7];
  const offsets = [
    { dx: 0, dy: -20 }, { dx: 0, dy: 20 },
    { dx: 30, dy: 0 }, { dx: -30, dy: 0 },
    { dx: 0, dy: -40 }, { dx: 0, dy: 40 },
    { dx: 50, dy: 0 }, { dx: -50, dy: 0 },
    { dx: 30, dy: -20 }, { dx: -30, dy: 20 },
    { dx: 0, dy: -60 }, { dx: 0, dy: 60 },
    { dx: 70, dy: 0 }, { dx: -70, dy: 0 },
    { dx: 50, dy: -30 }, { dx: -50, dy: 30 },
    { dx: 0, dy: -80 }, { dx: 0, dy: 80 },
    { dx: 90, dy: 0 }, { dx: -90, dy: 0 },
    { dx: 0, dy: -100 }, { dx: 0, dy: 100 },
    { dx: 110, dy: 0 }, { dx: -110, dy: 0 },
    { dx: 80, dy: -40 }, { dx: -80, dy: 40 },
    { dx: 0, dy: -120 }, { dx: 0, dy: 120 },
    { dx: 130, dy: 0 }, { dx: -130, dy: 0 },
  ];
  for (const refFrac of refFracs) {
    const ref = edgePointAtFraction(section, offsetX, offsetY, refFrac);
    for (const { dx, dy } of offsets) {
      const pt = { x: ref.x + dx, y: ref.y + dy };
      const rect = { x: pt.x - textW / 2, y: pt.y - textH + 2, w: textW, h: textH };

      if (!placedRects.some(placed => rectsOverlap(rect, placed))) {
        return { point: pt, rect };
      }
    }
  }

  // Last resort: accept the midpoint
  const mid = edgePointAtFraction(section, offsetX, offsetY, 0.5);
  const rect = { x: mid.x - textW / 2, y: mid.y - textH + 2, w: textW, h: textH };
  return { point: mid, rect };
}

/**
 * Render the legend panel as SVG elements.
 * Fix 9: Dynamic width based on content.
 */
function renderLegend(legend, modelBoxes, startY) {
  if (!legend) return { svg: '', height: 0 };

  const edgeColours = legend.edgeColours || {};
  const showPortTable = legend.portTable === true;
  const entries = Object.entries(edgeColours);
  const allPorts = showPortTable ? collectAllPorts(modelBoxes) : [];

  if (entries.length === 0 && allPorts.length === 0) {
    return { svg: '', height: 0 };
  }

  const parts = [];
  const padding = 15;
  const lineHeight = 20;
  const legendX = 20;
  let currentY = 0;

  // Compute dynamic width from content (Fix 9)
  const charWidth = 6.5;
  let maxTextLen = 10; // "LEGEND"
  for (const [colourName, description] of entries) {
    maxTextLen = Math.max(maxTextLen, `${colourName}: ${description}`.length);
  }
  for (const port of allPorts) {
    maxTextLen = Math.max(maxTextLen, `${port.boxName} / ${port.portLabel} (OUT)`.length);
  }
  const legendWidth = Math.max(260, maxTextLen * charWidth + padding * 2 + 20);

  // Title
  currentY += lineHeight;
  const titleLine = currentY;
  currentY += 8;

  // Colour entries
  const colourLines = [];
  for (const [colourName, description] of entries) {
    currentY += lineHeight;
    colourLines.push({ y: currentY, colourName, description });
  }

  // Port table
  const portLines = [];
  if (showPortTable && allPorts.length > 0) {
    currentY += lineHeight + 4;
    portLines.push({ y: currentY, isTitle: true });

    for (const port of allPorts) {
      currentY += lineHeight;
      portLines.push({
        y: currentY,
        boxName: port.boxName,
        portLabel: port.portLabel,
        portDir: port.portDir,
      });
    }
  }

  currentY += padding;
  const legendHeight = currentY;
  const legendY = startY + 10;

  // Background
  parts.push(
    `<rect x="${legendX}" y="${legendY}" width="${legendWidth}" height="${legendHeight}" ` +
    `rx="4" ry="4" fill="#FAFAFA" stroke="#CCC" stroke-width="1" />`
  );

  // Title
  parts.push(
    `<text x="${legendX + padding}" y="${legendY + titleLine}" ` +
    `font-size="11" font-weight="bold" fill="#333">LEGEND</text>`
  );

  // Colour swatches
  for (const cl of colourLines) {
    const hex = resolveColour(cl.colourName);
    parts.push(
      `<circle cx="${legendX + padding + 6}" cy="${legendY + cl.y - 4}" r="6" ` +
      `fill="${esc(hex)}" />`
    );
    parts.push(
      `<text x="${legendX + padding + 18}" y="${legendY + cl.y}" ` +
      `font-size="10" fill="#333">${esc(cl.colourName)}: ${esc(cl.description)}</text>`
    );
  }

  // Port table
  for (const pl of portLines) {
    if (pl.isTitle) {
      parts.push(
        `<text x="${legendX + padding}" y="${legendY + pl.y}" ` +
        `font-size="11" font-weight="bold" fill="#333">Ports</text>`
      );
    } else {
      const dirLabel = pl.portDir === 'in' ? 'IN' : 'OUT';
      parts.push(
        `<text x="${legendX + padding}" y="${legendY + pl.y}" ` +
        `font-size="10" fill="#333">${esc(pl.boxName)} / ${esc(pl.portLabel)} (${dirLabel})</text>`
      );
    }
  }

  return { svg: parts.join('\n'), height: legendHeight + 20 };
}

/**
 * Find the absolute position of a container node by walking the positioned tree.
 */
function findContainerOffset(root, containerId) {
  if (containerId === 'root' || !containerId) {
    return { x: 0, y: 0 };
  }

  function walk(node, accX, accY) {
    const nx = accX + (node.x || 0);
    const ny = accY + (node.y || 0);
    if (node.id === containerId) {
      return { x: nx, y: ny };
    }
    if (node.children) {
      for (const child of node.children) {
        const result = walk(child, nx, ny);
        if (result) return result;
      }
    }
    return null;
  }

  if (root.children) {
    for (const child of root.children) {
      const result = walk(child, 0, 0);
      if (result) return result;
    }
  }
  return { x: 0, y: 0 };
}

/**
 * Collect all unique edge colours for generating per-colour arrowhead markers.
 * Fix 5: Arrowheads match edge colour.
 */
function collectEdgeColours(modelEdges) {
  const colours = new Set(['#555']); // default
  for (const edge of modelEdges || []) {
    if (edge.style?.color) {
      colours.add(resolveColour(edge.style.color));
    }
  }
  return [...colours];
}

/**
 * Render a positioned ELK graph as an SVG string.
 */
export function renderSvg(positioned, model) {
  const padding = 60;
  const hasMetadata = model.metadata && Object.keys(model.metadata).length > 0;
  const metadataHeight = hasMetadata ? 20 : 0;
  const titleHeight = (model.title ? 40 : 0) + metadataHeight;

  const boxLookup = buildBoxLookup(model.boxes);

  // Render all top-level nodes
  const nodesSvg = (positioned.children || [])
    .map((child) => renderNode(child, model.style, boxLookup, 0))
    .join('\n');

  // Collect unique edge colours for marker defs (Fix 5)
  const edgeColours = collectEdgeColours(model.edges);

  // Port labels are not rendered (to avoid overlap with edge labels),
  // so no port label rects to collect for collision avoidance.
  const portLabelRects = [];

  // Collect compound node title strip regions so edge labels avoid overlapping headers.
  // Leaf node bexamples are NOT protected — edge labels have white backgrounds and remain
  // readable when overlaying leaf nodes. This gives the algorithm much more room to
  // place labels near their edges in dense diagrams.
  const nodeLabelRects = [];
  function collectNodeLabelRects(node, accX, accY) {
    const nx = accX + (node.x || 0);
    const ny = accY + (node.y || 0);
    const nw = node.width || 0;
    const nh = node.height || 0;
    const isCompound = node.children && node.children.length > 0;
    if (nw > 0 && nh > 0 && isCompound) {
      // Only protect the title strip of compound nodes
      nodeLabelRects.push({ x: nx, y: ny, w: nw, h: Math.min(50, nh) });
    }
    if (node.children) {
      for (const child of node.children) {
        collectNodeLabelRects(child, nx, ny);
      }
    }
  }
  for (const child of positioned.children || []) {
    collectNodeLabelRects(child, 0, 0);
  }

  // Render edges — two-pass: paths first, then labels with collision avoidance
  const edgePathParts = [];
  const edgeLabelParts = [];
  const placedLabelRects = [...portLabelRects, ...nodeLabelRects];

  for (let i = 0; i < (positioned.edges || []).length; i++) {
    const edge = positioned.edges[i];
    const modelEdge = model.edges?.[i] || {};
    const containerId = edge.container || null;
    const offset = findContainerOffset(positioned, containerId);

    const edgeColour = modelEdge.style?.color
      ? resolveColour(modelEdge.style.color)
      : '#555';

    const dashAttr = modelEdge.style?.dashed
      ? ' stroke-dasharray="6,3"'
      : '';

    const markerId = `arrow-${colourToId(edgeColour)}`;

    if (!edge.sections || edge.sections.length === 0) continue;

    // Pass 1: render edge paths with rounded corners at bends
    for (const section of edge.sections) {
      const sp = section.startPoint;
      const ep = section.endPoint;
      const bends = section.bendPoints || [];
      const r = 12; // corner radius

      const allPts = [
        { x: sp.x + offset.x, y: sp.y + offset.y },
        ...bends.map(bp => ({ x: bp.x + offset.x, y: bp.y + offset.y })),
        { x: ep.x + offset.x, y: ep.y + offset.y },
      ];

      let d;
      if (allPts.length <= 2) {
        d = `M ${allPts[0].x} ${allPts[0].y} L ${allPts[allPts.length - 1].x} ${allPts[allPts.length - 1].y}`;
      } else {
        // Rounded corner path: at each bend, use a quadratic bezier arc
        d = `M ${allPts[0].x} ${allPts[0].y}`;
        for (let j = 1; j < allPts.length - 1; j++) {
          const prev = allPts[j - 1];
          const curr = allPts[j];
          const next = allPts[j + 1];

          // Vector from prev to curr, and curr to next
          const dx1 = curr.x - prev.x, dy1 = curr.y - prev.y;
          const dx2 = next.x - curr.x, dy2 = next.y - curr.y;
          const len1 = Math.sqrt(dx1 * dx1 + dy1 * dy1);
          const len2 = Math.sqrt(dx2 * dx2 + dy2 * dy2);

          if (len1 === 0 || len2 === 0) {
            d += ` L ${curr.x} ${curr.y}`;
            continue;
          }

          // Limit radius to half the shortest segment
          const rr = Math.min(r, len1 / 2, len2 / 2);

          // Point before bend (rr pixels back along incoming segment)
          const ax = curr.x - (dx1 / len1) * rr;
          const ay = curr.y - (dy1 / len1) * rr;
          // Point after bend (rr pixels forward along outgoing segment)
          const bx = curr.x + (dx2 / len2) * rr;
          const by = curr.y + (dy2 / len2) * rr;

          d += ` L ${ax} ${ay}`;
          d += ` Q ${curr.x} ${curr.y}, ${bx} ${by}`;
        }
        d += ` L ${allPts[allPts.length - 1].x} ${allPts[allPts.length - 1].y}`;
      }

      edgePathParts.push(
        `<path d="${d}" fill="none" stroke="${esc(edgeColour)}" ` +
        `stroke-width="2" marker-end="url(#${markerId})"${dashAttr} />`
      );
    }

    // Pass 2: place label with collision avoidance
    const edgeLabel = edge.labels?.[0]?.text || modelEdge.label || '';
    if (edgeLabel) {
      const section = edge.sections[0];

      const lines = edgeLabel.split('\n');
      const longestLine = Math.max(...lines.map(l => l.length));
      const textW = longestLine * 7 + 16;
      const textH = lines.length * 14 + 8;

      const { point, rect } = findLabelPosition(
        section, offset.x, offset.y, textW, textH, placedLabelRects
      );
      placedLabelRects.push(rect);

      // White background behind label
      edgeLabelParts.push(
        `<rect x="${rect.x}" y="${rect.y}" ` +
        `width="${textW}" height="${textH}" fill="white" opacity="0.85" rx="2" ry="2" />`
      );

      if (lines.length === 1) {
        edgeLabelParts.push(
          `<text x="${point.x}" y="${point.y - 2}" text-anchor="middle" ` +
          `font-size="10" fill="${esc(edgeColour)}">${esc(edgeLabel)}</text>`
        );
      } else {
        const startY = point.y - (lines.length - 1) * 14 + 2;
        const tspans = lines.map((line, idx) =>
          `<tspan x="${point.x}" dy="${idx === 0 ? 0 : 14}">${esc(line)}</tspan>`
        ).join('');
        edgeLabelParts.push(
          `<text x="${point.x}" y="${startY}" text-anchor="middle" ` +
          `font-size="10" fill="${esc(edgeColour)}">${tspans}</text>`
        );
      }
    }
  }
  const edgesSvg = [...edgePathParts, ...edgeLabelParts].join('\n');

  // Compute content area
  const contentWidth = (positioned.width || 400) + padding * 2;
  const contentHeight = (positioned.height || 300) + padding * 2 + titleHeight;

  // Render legend (Fix 9: dynamic width)
  const { svg: legendSvg, height: legendHeight } = renderLegend(
    model.legend,
    model.boxes,
    contentHeight - padding
  );

  const svgWidth = contentWidth;
  const svgHeight = contentHeight + legendHeight;
  const font = model.style?.font || 'Helvetica';

  const parts = [];

  // SVG root
  parts.push(
    `<svg xmlns="http://www.w3.org/2000/svg" ` +
    `width="${svgWidth}" height="${svgHeight}" ` +
    `viewBox="0 0 ${svgWidth} ${svgHeight}" ` +
    `font-family="${esc(font)}, Arial, sans-serif">`
  );

  // White background
  parts.push(
    `<rect width="${svgWidth}" height="${svgHeight}" fill="white" />`
  );

  // Defs: per-colour arrowhead markers (Fix 5)
  parts.push(`<defs>`);
  for (const colour of edgeColours) {
    const id = `arrow-${colourToId(colour)}`;
    parts.push(
      `  <marker id="${id}" markerWidth="10" markerHeight="7" ` +
      `refX="10" refY="3.5" orient="auto" markerUnits="strokeWidth">` +
      `<polygon points="0 0, 10 3.5, 0 7" fill="${esc(colour)}" /></marker>`
    );
  }
  parts.push(`</defs>`);

  // Title
  if (model.title) {
    parts.push(
      `<text x="${svgWidth / 2}" y="28" text-anchor="middle" ` +
      `font-size="18" font-weight="bold" fill="#1B2A4A">${esc(model.title)}</text>`
    );
  }

  // Metadata line (author, date, version, status)
  if (hasMetadata) {
    const md = model.metadata;
    const metaParts = [];
    if (md.status) metaParts.push(md.status);
    if (md.version) metaParts.push(`v${md.version}`);
    if (md.author) metaParts.push(md.author);
    if (md.date) metaParts.push(md.date);
    if (md.scope) metaParts.push(md.scope);
    const metaText = metaParts.join(' | ');
    parts.push(
      `<text x="${svgWidth / 2}" y="46" text-anchor="middle" ` +
      `font-size="10" fill="#888">${esc(metaText)}</text>`
    );
  }

  // Main content group
  parts.push(`<g transform="translate(${padding}, ${padding + titleHeight})">`);
  parts.push(nodesSvg);
  parts.push(edgesSvg);
  parts.push('</g>');

  // Legend
  if (legendSvg) {
    parts.push(legendSvg);
  }

  parts.push('</svg>');
  return parts.join('\n');
}
