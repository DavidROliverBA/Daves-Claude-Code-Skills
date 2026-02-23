import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { exportPng } from '../src/export-png.mjs';

describe('exportPng', () => {
  it('converts SVG string to PNG buffer', async () => {
    const svg = '<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100"><rect width="100" height="100" fill="white"/><text x="50" y="50" text-anchor="middle">Test</text></svg>';
    const buffer = await exportPng(svg, 150);
    assert.ok(Buffer.isBuffer(buffer), 'Result should be a Buffer');
    assert.ok(buffer.length > 100, 'PNG should have substantial size');
    assert.equal(buffer[0], 0x89);
    assert.equal(buffer[1], 0x50);
    assert.equal(buffer[2], 0x4E);
    assert.equal(buffer[3], 0x47);
  });
});
