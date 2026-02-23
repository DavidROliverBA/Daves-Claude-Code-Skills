import ELK from 'elkjs';

const elk = new ELK();

/**
 * Run the ELK layout algorithm on an ELK JSON graph.
 *
 * Takes the output of `toElkGraph()` and returns a positioned graph
 * where all nodes, ports, and edges have x/y coordinates assigned.
 *
 * @param {Object} elkGraph - ELK JSON graph from transform.mjs
 * @returns {Promise<Object>} Positioned ELK graph with layout coordinates
 */
export async function computeLayout(elkGraph) {
  return elk.layout(elkGraph);
}
