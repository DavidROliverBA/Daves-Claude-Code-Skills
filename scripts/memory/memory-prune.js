#!/usr/bin/env node
/**
 * memory-prune.js
 *
 * Prunes old SessionSummary and SkillOutcome entities from the MCP memory
 * graph, keeping only the N most recent of each type. Pruned entities are
 * archived to Memory/memory-archive.md before removal so history is preserved.
 * Other entity types (LessonLearned, Convention, etc.) are never pruned.
 *
 * Usage:
 *   node .claude/scripts/memory-prune.js              # Prune (default: keep 20)
 *   node .claude/scripts/memory-prune.js --dry-run    # Preview changes
 *   node .claude/scripts/memory-prune.js --keep 10    # Keep last 10
 */

import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const VAULT_ROOT = path.resolve(__dirname, "../..");
const MEMORY_FILE = path.join(VAULT_ROOT, "Memory/memory.jsonl");
const ARCHIVE_FILE = path.join(VAULT_ROOT, "Memory/memory-archive.md");

const PRUNABLE_TYPES = new Set(["SessionSummary", "SkillOutcome"]);

const dryRun = process.argv.includes("--dry-run");
const keepIdx = process.argv.indexOf("--keep");
const KEEP_COUNT =
  keepIdx !== -1 ? parseInt(process.argv[keepIdx + 1], 10) : 20;

/**
 * Append pruned entities to the markdown archive file.
 * Each entity gets a heading and bullet-point observations.
 */
function archiveEntities(entities) {
  if (entities.length === 0) return;

  const timestamp = new Date().toISOString().slice(0, 10);
  let content = "";

  if (!fs.existsSync(ARCHIVE_FILE)) {
    content += `# Memory Archive\n\nPruned memory entities preserved for historical reference. These were removed from active MCP memory but kept here so nothing is lost.\n\n---\n\n`;
  }

  content += `## Archived ${timestamp}\n\n`;

  for (const entity of entities) {
    content += `### ${entity.name} (${entity.entityType})\n\n`;
    if (entity.observations && entity.observations.length > 0) {
      for (const obs of entity.observations) {
        content += `- ${obs}\n`;
      }
    }
    content += "\n";
  }

  content += "---\n\n";

  fs.appendFileSync(ARCHIVE_FILE, content);
}

function main() {
  console.log(
    `=== Memory Prune ${dryRun ? "(DRY RUN) " : ""}(keep last ${KEEP_COUNT}) ===\n`,
  );

  if (!fs.existsSync(MEMORY_FILE)) {
    console.log("No memory file found. Nothing to prune.");
    return;
  }

  const lines = fs
    .readFileSync(MEMORY_FILE, "utf8")
    .trim()
    .split("\n")
    .filter((l) => l.trim());

  // Separate entities by type
  const prunableEntities = new Map(); // type -> [{line, name, sortKey, parsed}]
  const keptLines = [];
  const relationLines = [];

  for (const line of lines) {
    try {
      const obj = JSON.parse(line);
      if (obj.type === "entity" && PRUNABLE_TYPES.has(obj.entityType)) {
        if (!prunableEntities.has(obj.entityType)) {
          prunableEntities.set(obj.entityType, []);
        }
        prunableEntities.get(obj.entityType).push({
          line,
          name: obj.name,
          sortKey: obj.name, // Names contain dates: Session-YYYY-MM-DD-HHMM, SkillRun-X-YYYY-MM-DD
          parsed: obj,
        });
      } else if (obj.type === "relation") {
        relationLines.push({ line, from: obj.from, to: obj.to });
      } else {
        keptLines.push(line);
      }
    } catch {
      keptLines.push(line); // preserve malformed
    }
  }

  // Determine which prunable entities to keep
  const prunedNames = new Set();
  const entitiesToArchive = [];
  let totalPruned = 0;

  for (const [entityType, entities] of prunableEntities) {
    // Sort descending by name (newest first)
    entities.sort((a, b) => b.sortKey.localeCompare(a.sortKey));

    const toKeep = entities.slice(0, KEEP_COUNT);
    const toPrune = entities.slice(KEEP_COUNT);

    for (const e of toKeep) {
      keptLines.push(e.line);
    }
    for (const e of toPrune) {
      prunedNames.add(e.name);
      entitiesToArchive.push(e.parsed);
    }

    console.log(
      `${entityType}: ${entities.length} total, keeping ${toKeep.length}, pruning ${toPrune.length}`,
    );
    totalPruned += toPrune.length;
  }

  // Filter relations: drop those referencing pruned entities
  let prunedRelations = 0;
  for (const { line, from, to } of relationLines) {
    if (prunedNames.has(from) || prunedNames.has(to)) {
      prunedRelations++;
    } else {
      keptLines.push(line);
    }
  }

  console.log(`\nRelations pruned: ${prunedRelations}`);
  console.log(`Total lines: ${lines.length} → ${keptLines.length}`);

  if (totalPruned === 0) {
    console.log("\nNothing to prune.");
    return;
  }

  if (dryRun) {
    console.log("\nDRY RUN — no changes written.");
    if (prunedNames.size > 0) {
      console.log("\nWould prune (and archive):");
      for (const name of prunedNames) {
        console.log(`  - ${name}`);
      }
    }
    return;
  }

  // Archive pruned entities to markdown
  archiveEntities(entitiesToArchive);
  console.log(
    `\nArchived ${entitiesToArchive.length} entities to ${ARCHIVE_FILE}`,
  );

  // Write memory file atomically
  const tmpFile = MEMORY_FILE + ".tmp";
  fs.writeFileSync(tmpFile, keptLines.join("\n") + "\n");
  fs.renameSync(tmpFile, MEMORY_FILE);

  console.log(
    `Pruned ${totalPruned} entities and ${prunedRelations} relations.`,
  );
  console.log(`Written ${keptLines.length} lines to ${MEMORY_FILE}`);
}

main();
