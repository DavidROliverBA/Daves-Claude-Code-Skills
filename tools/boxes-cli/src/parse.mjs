import yaml from 'js-yaml';

/**
 * Sanitise a name into a valid identifier for ELK node IDs.
 * Replaces non-alphanumeric characters with underscores.
 * @param {string} name
 * @returns {string}
 */
export function sanitiseId(name) {
  return name.replace(/[^a-zA-Z0-9]/g, '_');
}

/**
 * Parse port definitions from a box's `ports` object.
 * @param {Object} portsObj - e.g. { PortIn: { dir: 'in', label: 'Input' } }
 * @returns {Array<{ id: string, dir: string, label: string }>}
 */
export function parsePorts(portsObj) {
  if (!portsObj || typeof portsObj !== 'object') return [];
  return Object.entries(portsObj).map(([id, def]) => ({
    id,
    dir: def?.dir || 'in',
    label: def?.label || id,
    side: def?.side || null,
  }));
}

/**
 * Recursively parse boxes from the YAML `boxes` object into a tree structure.
 * @param {Object} obj - The boxes object (keys are box names, values are box defs)
 * @param {number} depth - Current nesting depth (0 = top level)
 * @returns {Array<Object>} Array of box nodes with children
 */
export function parseBoxes(obj, depth = 0) {
  if (!obj || typeof obj !== 'object') return [];
  return Object.entries(obj).map(([name, def]) => {
    const boxDef = def || {};

    // Merge children and actors — actors become children with actor: true
    const childBoxes = parseBoxes(boxDef.children, depth + 1);
    const actorBoxes = parseActorEntries(boxDef.actors, depth + 1);

    return {
      id: sanitiseId(name),
      name,
      label: boxDef.label || name,
      description: boxDef.description || null,
      technology: boxDef.technology || null,
      depth,
      zoom: boxDef.zoom || null,
      style: boxDef.style || null,
      ports: parsePorts(boxDef.ports),
      children: [...childBoxes, ...actorBoxes],
      actor: boxDef.actor || false,
    };
  });
}

/**
 * Parse actor entries from a box's `actors` object into box nodes with actor: true.
 * Actors are rendered as stick-figure nodes in the diagram.
 * @param {Object} actorsObj - e.g. { "Data Engineer": {}, "Business Analyst": {} }
 * @param {number} depth - Current nesting depth
 * @returns {Array<Object>}
 */
function parseActorEntries(actorsObj, depth) {
  if (!actorsObj || typeof actorsObj !== 'object') return [];
  return Object.entries(actorsObj).map(([name, def]) => {
    const actorDef = def || {};
    return {
      id: sanitiseId(name),
      name,
      label: actorDef.label || name,
      description: actorDef.description || null,
      technology: null,
      depth,
      zoom: null,
      style: actorDef.style || null,
      ports: parsePorts(actorDef.ports),
      children: [],
      actor: true,
    };
  });
}

/**
 * Parse a `Box:Port` reference string into its components.
 * @param {string} ref - e.g. "Inner B:PortIn" or "Inner A"
 * @returns {{ box: string, port: string|null }}
 */
function parseRef(ref) {
  const lastColon = ref.lastIndexOf(':');
  if (lastColon === -1) {
    return { box: ref, port: null };
  }
  return {
    box: ref.slice(0, lastColon),
    port: ref.slice(lastColon + 1),
  };
}

/**
 * Parse the `edges` array from YAML into internal edge model.
 * @param {Array} arr - Array of edge objects with from, to, label, colour, etc.
 * @returns {Array<Object>}
 */
export function parseEdges(arr) {
  if (!Array.isArray(arr)) return [];
  return arr.map((e) => ({
    from: parseRef(e.from || ''),
    to: parseRef(e.to || ''),
    label: e.label || null,
    colour: e.colour || null,
    style: e.style || null,
  }));
}

/**
 * Recursively find actors at any nesting level within boxes.
 * An actor is a box with `actor: true` set.
 * @param {Array} boxes - Parsed box tree
 * @returns {Array<Object>}
 */
export function parseActors(boxes) {
  const actors = [];
  for (const box of boxes) {
    if (box.actor) {
      actors.push(box);
    }
    if (box.children && box.children.length > 0) {
      actors.push(...parseActors(box.children));
    }
  }
  return actors;
}

/**
 * Parse a raw YAML boxes object looking for actor flags,
 * before the boxes have been fully parsed.
 * @param {Object} rawBoxes - The raw YAML boxes object
 * @returns {Array<string>} Actor names
 */
function findRawActors(rawBoxes, depth = 0) {
  if (!rawBoxes || typeof rawBoxes !== 'object') return [];
  const actors = [];
  for (const [name, def] of Object.entries(rawBoxes)) {
    if (def?.actor) {
      actors.push(name);
    }
    // Collect actors from the `actors` key within a box
    if (def?.actors && typeof def.actors === 'object') {
      actors.push(...Object.keys(def.actors));
    }
    if (def?.children) {
      actors.push(...findRawActors(def.children, depth + 1));
    }
  }
  return actors;
}

/**
 * Main entry point: parse a YAML string into the internal boxes diagram model.
 * @param {string} yamlString - Raw YAML content
 * @returns {Object} Internal model
 */
export function parseBoxesYaml(yamlString) {
  const raw = yaml.load(yamlString);
  if (!raw || typeof raw !== 'object') {
    throw new Error('Invalid YAML: expected an object at the top level');
  }

  const boxes = parseBoxes(raw.boxes, 0);
  const actors = findRawActors(raw.boxes);
  const edges = parseEdges(raw.edges);

  const defaultStyle = {
    font: 'Helvetica',
    borderWeight: [3],
    backgrounds: ['white'],
  };

  const legend = {
    edgeColours: raw.legend?.edgeColours || {},
    portTable: raw.legend?.portTable || false,
  };

  const metadata = raw.metadata || null;

  return {
    diagram: raw.diagram || null,
    title: raw.title || null,
    flow: raw.flow || 'LR',
    dpi: raw.dpi || 150,
    style: raw.style ? { ...defaultStyle, ...raw.style } : defaultStyle,
    boxes,
    actors,
    edges,
    legend,
    metadata,
  };
}
