#!/usr/bin/env node

import { Command } from 'commander';
import { readFileSync, writeFileSync } from 'node:fs';
import { parseBoxesYaml } from '../src/parse.mjs';
import { validateSchema } from '../src/schema.mjs';
import { toElkGraph } from '../src/transform.mjs';
import { computeLayout } from '../src/layout.mjs';
import { renderSvg } from '../src/render-svg.mjs';
import { exportPng } from '../src/export-png.mjs';

const program = new Command();

program
  .name('boxes')
  .description('Boxes notation diagram renderer')
  .version('0.1.0');

program
  .command('render <file>')
  .description('Render a .boxes.yaml file to SVG/PNG')
  .option('-f, --format <format>', 'Output format: svg, png, or both', 'both')
  .option('-o, --output <path>', 'Output file path (without extension)')
  .option('--dpi <number>', 'PNG resolution', '150')
  .action(async (file, options) => {
    try {
      const yaml = readFileSync(file, 'utf8');
      const model = parseBoxesYaml(yaml);

      const errors = validateSchema(model);
      if (errors.length > 0) {
        console.error('[boxes] Validation errors:');
        errors.forEach(e => console.error(`  - ${e}`));
        process.exit(1);
      }

      console.log(`[boxes] Laying out ${model.diagram}...`);
      const elkInput = toElkGraph(model);
      const positioned = await computeLayout(elkInput);
      const svg = renderSvg(positioned, model);

      const baseName = options.output || file.replace(/\.boxes\.yaml$/, '').replace(/\.yaml$/, '');
      const dpi = parseInt(options.dpi, 10);
      const format = options.format;

      if (format === 'svg' || format === 'both') {
        const svgPath = `${baseName}.svg`;
        writeFileSync(svgPath, svg);
        console.log(`[boxes] SVG written: ${svgPath}`);
      }

      if (format === 'png' || format === 'both') {
        const pngPath = `${baseName}.png`;
        const pngBuffer = await exportPng(svg, dpi);
        writeFileSync(pngPath, pngBuffer);
        console.log(`[boxes] PNG written: ${pngPath} (${dpi} DPI)`);
      }
    } catch (err) {
      console.error(`[boxes] Error: ${err.message}`);
      process.exit(1);
    }
  });

program
  .command('validate <file>')
  .description('Validate a .boxes.yaml file without rendering')
  .action(async (file) => {
    try {
      const yaml = readFileSync(file, 'utf8');
      const model = parseBoxesYaml(yaml);
      const errors = validateSchema(model);
      if (errors.length > 0) {
        console.error('[boxes] Validation errors:');
        errors.forEach(e => console.error(`  - ${e}`));
        process.exit(1);
      } else {
        console.log(`[boxes] ${file} is valid (${model.diagram})`);
      }
    } catch (err) {
      console.error(`[boxes] Error: ${err.message}`);
      process.exit(1);
    }
  });

program.parse();
