#!/usr/bin/env node
/**
 * memory-search.js
 *
 * Unified search across active MCP memory (Memory/memory.jsonl) and the
 * archive (Memory/memory-archive.md). Searches entity names and observations
 * using case-insensitive substring matching, consistent with MCP search_nodes.
 *
 * Usage:
 *   node .claude/scripts/memory-search.js <query>                    # Search both active + archive
 *   node .claude/scripts/memory-search.js <query> --active           # Active memory only
 *   node .claude/scripts/memory-search.js <query> --archive          # Archive only
 *   node .claude/scripts/memory-search.js <query> --type LessonLearned  # Filter by entity type
 *   node .claude/scripts/memory-search.js --list-types               # Show all entity types and counts
 *   node .claude/scripts/memory-search.js --stats                    # Show memory statistics
 */

import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const VAULT_ROOT = path.resolve(__dirname, "../..");
const MEMORY_FILE = path.join(VAULT_ROOT, "Memory/memory.jsonl");
const ARCHIVE_FILE = path.join(VAULT_ROOT, "Memory/memory-archive.md");

// --- Parse CLI args ---

const args = process.argv.slice(2);
const activeOnly = args.includes("--active");
const archiveOnly = args.includes("--archive");
const listTypes = args.includes("--list-types");
const showStats = args.includes("--stats");

const typeIdx = args.indexOf("--type");
const typeFilter = typeIdx !== -1 ? args[typeIdx + 1] : null;

// Query is all non-flag args
const query = args
  .filter(
    (a) =>
      !a.startsWith("--") &&
      (typeIdx === -1 || args.indexOf(a) !== typeIdx + 1),
  )
  .join(" ")
  .toLowerCase();

// --- Parse active memory (JSONL) ---

function parseActiveMemory() {
  if (!fs.existsSync(MEMORY_FILE)) return [];

  const lines = fs
    .readFileSync(MEMORY_FILE, "utf8")
    .trim()
    .split("\n")
    .filter((l) => l.trim());

  const entities = [];
  for (const line of lines) {
    try {
      const obj = JSON.parse(line);
      if (obj.type === "entity" || obj.entityType) {
        entities.push({
          name: obj.name || "unknown",
          entityType: obj.entityType || "unknown",
          observations: obj.observations || [],
          source: "active",
        });
      }
    } catch {
      // skip malformed
    }
  }
  return entities;
}

// --- Parse archive (markdown) ---

function parseArchive() {
  if (!fs.existsSync(ARCHIVE_FILE)) return [];

  const content = fs.readFileSync(ARCHIVE_FILE, "utf8");
  const entities = [];
  let currentEntity = null;

  for (const line of content.split("\n")) {
    // Match entity headings: ### EntityName (EntityType)
    const entityMatch = line.match(/^### (.+?) \((.+?)\)/);
    if (entityMatch) {
      if (currentEntity) entities.push(currentEntity);
      currentEntity = {
        name: entityMatch[1],
        entityType: entityMatch[2],
        observations: [],
        source: "archive",
      };
      continue;
    }

    // Match archive date headings for context
    const dateMatch = line.match(/^## Archived (\d{4}-\d{2}-\d{2})/);
    if (dateMatch && currentEntity) {
      currentEntity.archivedDate = dateMatch[1];
    }

    // Match observation bullets
    if (currentEntity && line.startsWith("- ")) {
      currentEntity.observations.push(line.slice(2));
    }
  }

  if (currentEntity) entities.push(currentEntity);
  return entities;
}

// --- Search ---

function matchesQuery(entity, query) {
  if (!query) return true;

  const terms = query.split(/\s+/);
  const searchText = [entity.name, entity.entityType, ...entity.observations]
    .join(" ")
    .toLowerCase();

  // All terms must match (AND logic) — each term is a substring check
  return terms.every((term) => searchText.includes(term));
}

function matchesType(entity, typeFilter) {
  if (!typeFilter) return true;
  return entity.entityType.toLowerCase() === typeFilter.toLowerCase();
}

// --- Display ---

function displayEntity(entity, index) {
  const sourceTag = entity.source === "archive" ? " [ARCHIVED]" : "";
  const dateTag = entity.archivedDate
    ? ` (archived ${entity.archivedDate})`
    : "";

  console.log(
    `\n${index}. ${entity.name} (${entity.entityType})${sourceTag}${dateTag}`,
  );
  console.log("   " + "-".repeat(60));

  for (const obs of entity.observations) {
    // Truncate very long observations for readability
    const display = obs.length > 200 ? obs.slice(0, 197) + "..." : obs;
    console.log(`   • ${display}`);
  }
}

function displayStats(activeEntities, archiveEntities) {
  console.log("=== Memory Statistics ===\n");

  console.log(`Active entities:   ${activeEntities.length}`);
  console.log(`Archived entities: ${archiveEntities.length}`);
  console.log(
    `Total:             ${activeEntities.length + archiveEntities.length}`,
  );
  console.log(`Cap:               200\n`);

  // Type breakdown for active
  const typeCounts = new Map();
  for (const e of activeEntities) {
    typeCounts.set(e.entityType, (typeCounts.get(e.entityType) || 0) + 1);
  }

  console.log("Active by type:");
  const sorted = [...typeCounts.entries()].sort((a, b) => b[1] - a[1]);
  for (const [type, count] of sorted) {
    console.log(`  ${type.padEnd(25)} ${count}`);
  }

  if (archiveEntities.length > 0) {
    const archiveTypeCounts = new Map();
    for (const e of archiveEntities) {
      archiveTypeCounts.set(
        e.entityType,
        (archiveTypeCounts.get(e.entityType) || 0) + 1,
      );
    }
    console.log("\nArchived by type:");
    const archiveSorted = [...archiveTypeCounts.entries()].sort(
      (a, b) => b[1] - a[1],
    );
    for (const [type, count] of archiveSorted) {
      console.log(`  ${type.padEnd(25)} ${count}`);
    }
  }
}

function displayTypeList(activeEntities, archiveEntities) {
  console.log("=== Entity Types ===\n");

  const allTypes = new Map();
  for (const e of activeEntities) {
    if (!allTypes.has(e.entityType))
      allTypes.set(e.entityType, { active: 0, archived: 0 });
    allTypes.get(e.entityType).active++;
  }
  for (const e of archiveEntities) {
    if (!allTypes.has(e.entityType))
      allTypes.set(e.entityType, { active: 0, archived: 0 });
    allTypes.get(e.entityType).archived++;
  }

  console.log(
    `${"Type".padEnd(25)} ${"Active".padStart(8)} ${"Archived".padStart(10)} ${"Total".padStart(8)}`,
  );
  console.log("-".repeat(55));

  const sorted = [...allTypes.entries()].sort((a, b) =>
    a[0].localeCompare(b[0]),
  );
  for (const [type, counts] of sorted) {
    const total = counts.active + counts.archived;
    console.log(
      `${type.padEnd(25)} ${String(counts.active).padStart(8)} ${String(counts.archived).padStart(10)} ${String(total).padStart(8)}`,
    );
  }
}

// --- Main ---

function main() {
  const activeEntities = parseActiveMemory();
  const archiveEntities = parseArchive();

  if (showStats) {
    displayStats(activeEntities, archiveEntities);
    return;
  }

  if (listTypes) {
    displayTypeList(activeEntities, archiveEntities);
    return;
  }

  if (!query && !typeFilter) {
    console.log(
      "Usage: node .claude/scripts/memory-search.js <query> [--active|--archive] [--type <type>]",
    );
    console.log(
      "       node .claude/scripts/memory-search.js --stats | --list-types",
    );
    console.log("\nExamples:");
    console.log('  memory-search.js "pre-commit"');
    console.log('  memory-search.js "worktree" --type LessonLearned');
    console.log('  memory-search.js "session" --archive');
    console.log("  memory-search.js --stats");
    return;
  }

  // Build search pool
  let pool = [];
  if (!archiveOnly) pool.push(...activeEntities);
  if (!activeOnly) pool.push(...archiveEntities);

  // Filter
  const results = pool.filter(
    (e) => matchesQuery(e, query) && matchesType(e, typeFilter),
  );

  // Display
  const activeCount = results.filter((r) => r.source === "active").length;
  const archiveCount = results.filter((r) => r.source === "archive").length;

  if (results.length === 0) {
    console.log(`No results for "${query || typeFilter}".`);
    if (activeOnly)
      console.log("Tip: try without --active to also search the archive.");
    return;
  }

  console.log(
    `=== ${results.length} result${results.length === 1 ? "" : "s"} (${activeCount} active, ${archiveCount} archived) ===`,
  );

  let i = 1;

  // Show active results first
  const activeResults = results.filter((r) => r.source === "active");
  if (activeResults.length > 0) {
    for (const entity of activeResults) {
      displayEntity(entity, i++);
    }
  }

  // Then archived results
  const archiveResults = results.filter((r) => r.source === "archive");
  if (archiveResults.length > 0) {
    if (activeResults.length > 0) {
      console.log("\n" + "=".repeat(60));
      console.log("  ARCHIVED RESULTS (no longer in active memory)");
      console.log("=".repeat(60));
    }
    for (const entity of archiveResults) {
      displayEntity(entity, i++);
    }
  }
}

main();
