# Unified Meta Collector Plan

## Objective

Create one unified operational database that every script can read/write safely,
so we can:

- consolidate project and file intelligence in one place,
- grow coverage continuously across repositories,
- detect gaps early,
- prioritize high-value enrichment work automatically.

This plan treats the database as a product, not a side artifact.

---

## North Star

`project_catalog.db` (or successor `meta_ops.db`) becomes the canonical source
for all repository intelligence used by operations scripts.

Every automation tool should be able to answer these questions from one DB:

- What projects exist and what state are they in?
- What files are indexed and how recently?
- Which files behave like scanners/collectors/auditors?
- What is missing, stale, duplicated, or risky?
- What should run next to maximize value?

---

## System Concept: Meta Collector

The **Meta Collector** is an orchestration layer that merges outputs from
CodeGraphX + project crawlers + script heuristics into unified facts.

### Responsibilities

1. Ingest
- Pull scan/enrichment artifacts and project metadata into normalized tables.

2. Classify
- Tag files/scripts by operational role (collector, transformer, reporter, fixer).

3. Detect Gaps
- Identify unindexed projects/files, stale scans, duplicate mirrors, missing docs/tests.

4. Prioritize
- Produce ranked "next best actions" for enrichment and cleanup.

5. Publish
- Expose stable views and query APIs usable by any script.

---

## Data Model (Unified DB v1)

Use additive schema evolution. Never break existing consumers abruptly.

### Core tables

- `projects`
  - project inventory and coarse metadata.
- `codegraphx_enrichment`
  - scan/enrichment artifacts and graph metrics.
- `codegraphx_file_signals`
  - per-file classifier signals (collector behavior, evidence, score).
- `codegraphx_project_signals`
  - project-level rolled-up signals.

### New tables to add

- `files`
  - canonical file registry: `project_path`, `file_path`, `ext`, `size`, `mtime`, `sha256`.
- `ingest_runs`
  - one row per pipeline/script run with status, duration, counts, errors.
- `gap_findings`
  - detected issues: `gap_type`, `severity`, `scope`, `evidence`, `first_seen`, `last_seen`.
- `action_queue`
  - prioritized next actions with owner, status, and replayable command payload.

### Stable views

- `v_project_health`
- `v_index_coverage`
- `v_collector_projects`
- `v_gap_backlog`
- `v_next_actions`

These views are the contract that scripts consume.

---

## Operating Principles

1. Idempotent writes
- Re-runs should converge to the same state.

2. Additive migrations
- `CREATE TABLE IF NOT EXISTS`, `ALTER TABLE ADD COLUMN` guarded by checks.

3. Deterministic paths
- Canonicalize paths before writing (`resolve`, lowercase key where appropriate).

4. Run traceability
- Every pipeline writes a run record with artifact pointers.

5. Separation of concerns
- Graph indexing, keyword indexing, and operational classification are separate layers.

6. Signal-first indexing
- Index what is useful, not everything by default.

---

## Phased Plan

## Phase 0: Contract Freeze (1-2 days)

Deliverables:
- Confirm canonical DB file and backup policy.
- Define naming contract for all tables/views.
- Publish "DB consumer contract" doc for scripts.

Exit criteria:
- Any script can discover DB path via one environment variable:
  - `META_DB_PATH`

## Phase 1: Schema Unification (3-5 days)

Deliverables:
- Add `files`, `ingest_runs`, `gap_findings`, `action_queue`.
- Add indexes for hot query paths.
- Add compatibility views over old/new fields.

Exit criteria:
- Existing scripts still run.
- New schema migrates in place without data loss.

## Phase 2: Meta Collector Ingestion (5-7 days)

Deliverables:
- Build `meta_collector.py` orchestrator:
  - pull project inventory,
  - pull latest CodeGraphX scan artifacts,
  - populate `files`,
  - store run logs in `ingest_runs`.
- Add dry-run and resume modes.

Exit criteria:
- Single command refreshes unified DB for a root scope.

## Phase 3: Classification + Gap Engine (5-7 days)

Deliverables:
- Extend role detection beyond collectors:
  - `collector`, `analyzer`, `reporter`, `fixer`, `orchestrator`.
- Compute gaps:
  - unindexed project,
  - stale scan,
  - duplicate mirror subtree,
  - low-doc/high-complexity project,
  - missing tests on high-change projects.

Exit criteria:
- `gap_findings` populated and queryable.

## Phase 4: Prioritization + Action Queue (3-5 days)

Deliverables:
- Implement scoring model for next actions.
- Write top-N actions into `action_queue`.
- Attach replayable command template per action.

Exit criteria:
- One query returns "what to run next" with rationale.

## Phase 5: Script Access Standardization (3-4 days)

Deliverables:
- Provide shared helper module for DB reads/writes.
- Refactor existing scripts to use common helper and views.
- Add CLI commands:
  - `enrich gaps`
  - `enrich next-actions`
  - `enrich refresh-meta`

Exit criteria:
- Scripts use shared contract, not custom SQL copies.

## Phase 6: Governance + Continuous Growth (ongoing)

Deliverables:
- Weekly scheduled enrichment campaign.
- Monthly schema/index audit.
- Quality checks for stale or noisy signals.

Exit criteria:
- Coverage and data quality trend upward month-over-month.

---

## Gap Taxonomy (v1)

- `PROJECT_UNINDEXED`
- `PROJECT_STALE_SCAN`
- `FILE_MISSING_FROM_SCAN`
- `DUPLICATE_MIRROR_CONTENT`
- `HIGH_SIZE_LOW_TEST_COVERAGE`
- `HIGH_COLLECTOR_DENSITY_NO_DOCS`
- `ORPHANED_ARTIFACT_PATH`

Each gap includes:
- `severity` (`low`, `medium`, `high`, `critical`)
- `impact_score` (numeric)
- `recommended_action`

---

## Prioritization Strategy

Action score formula (initial):

`priority = impact + freshness_penalty + dependency_weight + confidence`

Where:
- `impact`: estimated value/risk reduction,
- `freshness_penalty`: higher for stale data,
- `dependency_weight`: blocks many downstream tasks,
- `confidence`: confidence in classifier/gap signal.

Start simple and tune based on outcomes.

---

## Implementation Backlog (First Sprint)

1. Add migration script for new tables and views.
2. Add `meta_collector.py` skeleton with run logging.
3. Add `gap_engine.py` for first 3 gap types.
4. Add `action_planner.py` producing `action_queue`.
5. Add `--db` default resolution via `META_DB_PATH`.
6. Add dashboard query script (`meta_status.py`).
7. Add tests for migration idempotence and scoring determinism.

---

## Success Metrics

- Project coverage:
  - `% projects with fresh scan <= 14 days`
- File coverage:
  - `% tracked files represented in current scan scope`
- Gap closure:
  - `# high-severity gaps opened vs closed per week`
- Operational velocity:
  - `median time from gap detection to queued action`
- DB adoption:
  - `% scripts using shared DB helper/views`

---

## Immediate Commands to Standardize

- `codegraphx enrich backlog`
- `codegraphx enrich campaign`
- `codegraphx enrich collectors`
- `codegraphx enrich index-audit`

Then add:
- `codegraphx enrich refresh-meta`
- `codegraphx enrich gaps`
- `codegraphx enrich next-actions`

---

## Risks and Mitigations

Risk: Schema drift across scripts.
- Mitigation: one migration entrypoint + shared query views.

Risk: Noisy duplicate paths (mirrors/incoming snapshots).
- Mitigation: path normalization + configurable exclude profiles + duplicate detector.

Risk: Performance degradation as data grows.
- Mitigation: index policy + periodic vacuum/analyze + bounded batch writes.

Risk: False positives in role classification.
- Mitigation: confidence score + manual override table + periodic review.

---

## Decision

Proceed with Meta Collector architecture and unified DB contract now.
This gives consolidation + growth + gap detection in one operational loop.
