# Feature Specification: Two-Phase CLI (Subcommands: generate-corpus / search)

**Feature Branch**: `002-two-phase-cli`  
**Created**: 2026-04-05  
**Status**: Draft  
**Input**: User description: "Two-phase CLI with subcommands: **`generate-corpus`** requires **`--N`** and optional **`--seed`**, writes **`corpus.json`** and **`metadata.txt`** under **`.rmit/corpus/YYYYMMDD_HHMMSS/`** (relative to cwd) and prints absolute paths on stdout. **`search`** uses **`--corpus`**, **`--query`**, optional **`--strategy`**, **`--benchmark`**. Document **`uv run`** examples; no `sys.path` bootstrap; **`get_synthetic_corpus`** / **`get_synthetic_query`** on search path only."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Generate synthetic corpus only (Priority: P1)

An analyst or developer needs to create a reproducible synthetic dataset of **N** user profiles for experiments or demos, without running similarity search or supplying a query file.

**Why this priority**: Unblocks dataset preparation and repeatable benchmarks independently of query design.

**Independent Test**: Run the tool with the **generate-corpus** subcommand and valid parameters; verify **N** valid profiles are produced and no search step runs.

**Acceptance Scenarios**:

1. **Given** a chosen **N ≥ 1** and optional seed, **When** the operator runs **generate-corpus** with those parameters, **Then** the system persists **N** profiles as **`corpus.json`** (same JSON shape the **search** subcommand accepts) plus **`metadata.txt`**, under a timestamped directory beneath **`.rmit/corpus/`**, and prints the absolute paths to those files; no query is required.
2. **Given** the same seed and **N**, **When** generate-corpus is run twice, **Then** the **`corpus.json`** payloads are identical (reproducibility; paths differ if timestamps differ).

---

### User Story 2 - Search on a prepared corpus (Priority: P1)

An operator has a corpus file (or uses one produced earlier) and a query specification; they need top-**k** lookalike profiles using weighted distance, optional timing, and choice of search strategy (baseline, spatial index, or comparison mode).

**Why this priority**: Delivers the core “lookalike” retrieval value after data is already available.

**Independent Test**: Run the **search** subcommand with corpus and query paths; verify ranked hits and that normalization is consistent with the corpus statistics.

**Acceptance Scenarios**:

1. **Given** a valid corpus path and query file, **When** the search subcommand runs with a chosen strategy, **Then** the system returns up to **k** profile identifiers with distances, using weights from the query file.
2. **Given** benchmark mode enabled (benchmark flag present), **When** search completes, **Then** the operator can see build and search durations (or equivalent summary) suitable for comparing strategies on the same corpus and query.

---

### User Story 3 - Clear separation and errors between modes (Priority: P2)

Operators must not accidentally mix generation and search in one invocation; the CLI must require a recognized subcommand first, then only options valid for that subcommand.

**Why this priority**: Reduces operator error and support burden; makes scripts and documentation easier to follow.

**Independent Test**: Omit the subcommand, use an unknown subcommand, or omit required options for a subcommand; verify explicit, actionable error messages and non-zero exit where appropriate.

**Acceptance Scenarios**:

1. **Given** the operator runs the entry script without a valid subcommand, **When** arguments are parsed, **Then** the system shows usage for available subcommands and exits with an error.
2. **Given** the **search** subcommand without corpus or query path, **When** the tool validates input, **Then** the system rejects the run naming what is missing.

---

### Edge Cases

- **N < 1** for generate-corpus: rejected with a clear message.
- **Missing or invalid JSON** for corpus or query: rejected with a domain-appropriate error (no silent fallback).
- **Search** without required paths: rejected with explicit messages.
- **Unknown subcommand** or **invalid strategy value**: rejected with allowed values listed.
- **Very large N** (e.g. 100,000+): generation writes one **`corpus.json`** per run; memory expectations match building the full list before `dump_json` (same as prior iterator→list approach).

## Requirements *(mandatory)*

### Repository implementation constraints

Implementations in this repository MUST comply with
`.specify/memory/constitution.md`: **Standard Library only** (no PyPI
dependencies), PEP 8, strict type hints, Google-style docstrings on public API,
custom domain exception hierarchies, and `unittest` for automated tests unless
the spec explicitly defers testing (state that deferral here).

Additionally, for this feature:

- The CLI entry module MUST NOT rely on mutating `sys.path` at import time for package resolution; running with `PYTHONPATH` including the `src` directory (or equivalent installed layout) is the supported invocation, consistent with project documentation.
- The CLI MUST expose **subcommands** **`generate-corpus`** and **`search`** (parsed with the standard library argument parser). The first positional token after the script name MUST select the workflow; options MUST be scoped per subcommand so generation options cannot be mixed with search options in one parse.
- **`generate-corpus`** MUST require profile count **N** via **`--N`** (integer ≥ 1). Optional **`--seed`** (integer) controls reproducibility. It MUST write artifacts under **`.rmit/corpus/YYYYMMDD_HHMMSS/`** as specified in the feature contract (corpus JSON + metadata file) and MUST print absolute paths on stdout as the primary operator-visible result besides files.
- **`search`** MUST require **`--corpus`** and **`--query`** paths; MUST support optional **`--strategy`** (`baseline`, `kdtree`, `both`); MUST treat **`--benchmark`** as a boolean flag (present ⇒ benchmark timing behavior).
- Documentation MUST include an example using **`uv run python src/main.py …`** as an optional invocation pattern; plain **`python`** with documented `PYTHONPATH` remains supported.
- Corpus preparation for **search** MUST be encapsulated in **`get_synthetic_corpus`** (load corpus file → normalize). Query preparation MUST be encapsulated in **`get_synthetic_query`** (load query JSON → normalized query vector + weights + **k**). **generate-corpus** does not call these helpers.
- Automated tests MUST use the subcommand argv shape. **Backward compatibility** for the prior flat-flag CLI (`--generate`, single-parser) is **out of scope** unless added in a follow-up change.

### Functional Requirements

- **FR-001**: The tool MUST support a **generate-corpus** subcommand that persists **N** synthetic profiles as **`corpus.json`** (and companion **`metadata.txt`**) on disk under **`.rmit/corpus/<timestamp>/`**, prints absolute paths on stdout, does not run search, and does not accept corpus/query search parameters on that subcommand.
- **FR-002**: The tool MUST support a **search** subcommand that requires corpus and query inputs and runs weighted top-**k** retrieval with optional strategy and optional benchmark flag, with the same ranking semantics as today for equivalent files and options.
- **FR-003**: The tool MUST reject invocations that omit a required subcommand or use an unknown subcommand, with clear usage guidance.
- **FR-004**: The tool MUST reject **search** when corpus or query path is missing, naming the omission.
- **FR-005**: Normalization for search MUST derive feature scaling statistics from the loaded corpus only, and the reference profile in the query MUST be normalized with those same statistics before distance computation.
- **FR-006**: Automated tests MUST cover generate-corpus, search, and at least one invalid invocation (unknown subcommand or missing required option).

### Key Entities *(include if feature involves data)*

- **Synthetic / file corpus**: Collection of user profiles; **generate-corpus** writes **`corpus.json`** under **`.rmit/corpus/`**; **search** reads a corpus path on disk.
- **Query specification**: Reference profile attributes, per-attribute weights, and **k**; used only in the search subcommand.
- **Normalized representation**: Profiles and query reference transformed using min-max (or equivalent) statistics from the corpus, plus strategy-specific index structures built from normalized corpus points.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of new or updated automated tests for the subcommand CLI pass in the project test suite.
- **SC-002**: For a fixed seed and **N**, two generate-corpus runs produce byte-identical **`corpus.json`** file contents (determinism).
- **SC-003**: For the same corpus file, query file, **k**, weights, and strategy, search results (ordered profile ids and distances within a tight numerical tolerance) match pre-subcommand baseline behavior for equivalent inputs.
- **SC-004**: Operators can document two separate command recipes—**generate-corpus** and **search**—with no shared flags between subcommands beyond documented conventions (e.g. JSON formats).

## Assumptions

- Operators run the CLI from an environment where the `services` package is importable without runtime `sys.path` hacks (e.g. `PYTHONPATH` includes `src`, as documented).
- **Uv** is an optional team convenience for invoking Python; it is not a runtime dependency of the library.
- Generation persists JSON under **`.rmit/corpus/<timestamp>/corpus.json`**; stdout carries path lines for automation, not the corpus body.
- The five weighted attributes, distance definition, and strategy semantics remain as in feature 001; this feature changes **CLI structure**, **tests**, and **docs** accordingly.
- Function names **`get_synthetic_corpus`** and **`get_synthetic_query`** remain required; docstrings SHOULD clarify that **get_synthetic_corpus** loads an on-disk corpus for search only.
