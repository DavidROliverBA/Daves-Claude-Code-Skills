import sharp from 'sharp';

/**
 * Convert an SVG string to a PNG buffer using sharp.
 *
 * @param {string} svgString - Complete SVG document as a string
 * @param {number} [dpi=150] - Resolution in dots per inch (passed as density to sharp)
 * @returns {Promise<Buffer>} PNG image as a Node.js Buffer
 */
export async function exportPng(svgString, dpi = 150) {
  return sharp(Buffer.from(svgString), { density: dpi })
    .png()
    .toBuffer();
}
