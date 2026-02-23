const VALID_FLOW_DIRECTIONS = ['LR', 'TB', 'RL', 'BT'];
const VALID_PORT_DIRECTIONS = ['in', 'out'];

/**
 * Recursively validate ports in all boxes.
 * @param {Array} boxes - Parsed box tree
 * @param {Array<string>} errors - Error accumulator
 */
function validatePorts(boxes, errors) {
  for (const box of boxes) {
    if (box.ports && box.ports.length > 0) {
      for (const port of box.ports) {
        if (!VALID_PORT_DIRECTIONS.includes(port.dir)) {
          errors.push(
            `Box "${box.name}", port "${port.id}": invalid dir "${port.dir}" — must be one of: ${VALID_PORT_DIRECTIONS.join(', ')}`
          );
        }
      }
    }
    if (box.children && box.children.length > 0) {
      validatePorts(box.children, errors);
    }
  }
}

/**
 * Validate the internal diagram model against the boxes schema.
 * Returns an array of error strings (empty = valid).
 * @param {Object} model - The parsed internal model from parseBoxesYaml
 * @returns {Array<string>} Validation errors
 */
export function validateSchema(model) {
  const errors = [];

  // Required field: diagram
  if (!model.diagram) {
    errors.push('Missing required field: "diagram"');
  }

  // Flow direction
  if (model.flow && !VALID_FLOW_DIRECTIONS.includes(model.flow)) {
    errors.push(
      `Invalid flow direction: "${model.flow}" — must be one of: ${VALID_FLOW_DIRECTIONS.join(', ')}`
    );
  }

  // Validate ports recursively
  if (model.boxes && Array.isArray(model.boxes)) {
    validatePorts(model.boxes, errors);
  }

  return errors;
}
