# boxes-cli

A YAML-to-SVG/PNG diagram renderer using ELK.js for hierarchical layout.

## Installation

```bash
cd tools/boxes-cli
npm install
```

## Usage

```bash
# Render YAML to SVG
node bin/boxes.mjs render input.yaml -o output.svg

# Render to PNG
node bin/boxes.mjs render input.yaml -o output.png --format png
```

## YAML Format

Define systems, containers, and relationships in a simple YAML notation:

```yaml
name: My System
boxes:
  - id: web
    label: Web App
    type: container
  - id: api
    label: API Service
    type: container
  - id: db
    label: Database
    type: database
edges:
  - from: web
    to: api
    label: REST
  - from: api
    to: db
    label: SQL
```

## Dependencies

- **elkjs** — Hierarchical graph layout (Eclipse Layout Kernel)
- **js-yaml** — YAML parsing
- **sharp** — PNG rendering from SVG
- **commander** — CLI framework

## Testing

```bash
npm test
```
