# Feature Specification: Source layout consolidation (DTOs, dataset builder, I/O)

**Feature Branch**: `003-src-module-restructure`  
**Created**: 2026-04-06  
**Status**: Draft  
**Input**: User description: "Restructure application source: centralize dataclasses under `services/dto`; consolidate `core` package into `helper` module; move similarity pipeline responsibilities into `dataset` module behind `DataBuilder`; relocate JSON I/O from `io` subpackage to `services` level."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - One place for structured data shapes (Priority: P1)

As a **maintainer or reviewer**, I need all immutable structured record types (profile records, normalized points, scaling metadata, and related DTOs) defined in **one predictable area** of the source tree so I can review schema changes, imports, and typing without hunting across modules.

**Why this priority**: Reduces cognitive load and merge conflicts; every feature that touches domain records starts from the same location.

**Independent Test**: A reader can open the designated DTO area and enumerate every such record type used by similarity and search; no duplicate competing definitions remain elsewhere.

**Acceptance Scenarios**:

1. **Given** the codebase after the change, **When** a maintainer looks for a domain record type, **Then** it is defined only under the agreed DTO package.
2. **Given** existing JSON corpus and query files, **When** they are loaded and processed, **Then** validation and normalization behavior matches the pre-change system (same accept/reject rules and numeric semantics).

---

### User Story 2 - Clear home for shared errors and low-level helpers (Priority: P2)

As a **maintainer**, I want domain validation errors and small shared numeric/vector utilities to live alongside each other in a **single foundational module** so imports stay shallow and `core` does not duplicate “helper” concerns.

**Why this priority**: Simplifies the mental model: one module for “primitives + errors” used across dataset building, distance, and I/O.

**Independent Test**: Call sites that raised structured validation failures before still raise the same failure kinds with equivalent messages for the same invalid inputs; public symbols remain discoverable from one module entry point.

**Acceptance Scenarios**:

1. **Given** invalid corpus or query payloads, **When** they are processed, **Then** callers receive the same category of structured error as before the move (no silent behavior change).
2. **Given** code that imported from the old `core` package, **When** it is updated to the new layout, **Then** there is a single documented replacement import path.

---

### User Story 3 - Dataset preparation behind a named builder (Priority: P2)

As a **maintainer**, I want corpus preparation (generation, encoding, normalization, stats) orchestrated through a **`DataBuilder`** (or equivalent façade) in the **dataset** module so pipeline steps are grouped for readability and future extension.

**Why this priority**: Separates “how we build tensors/records from raw data” from “how we search them,” without changing search algorithms.

**Independent Test**: Building a normalized corpus from the same raw inputs yields the same normalized vectors and scaling metadata as before the refactor (within existing floating-point tolerance where already defined).

**Acceptance Scenarios**:

1. **Given** a fixed seed and corpus size, **When** synthetic data is generated and written, **Then** file contents match prior deterministic outputs for the same parameters.
2. **Given** a loaded corpus, **When** normalization runs via the new builder API, **Then** downstream search results for a fixed query match prior baseline/k-d tree equivalence expectations.

---

### User Story 4 - Flatter JSON I/O location (Priority: P3)

As a **maintainer**, I want JSON load/dump helpers for corpus and query files to live **directly under the main services package** (not a nested I/O subpackage) so imports are shorter and the package graph is flatter.

**Why this priority**: Cosmetic/ergonomic; lowest risk if behavior is unchanged.

**Independent Test**: Round-trip and invalid-input tests for JSON contracts still pass; CLI entry points still read/write the same paths and formats.

**Acceptance Scenarios**:

1. **Given** valid corpus JSON on disk, **When** it is loaded through the relocated module, **Then** the in-memory structure matches what the previous layout produced.
2. **Given** the CLI generate and search flows, **When** run with identical arguments and files, **Then** stdout/stderr and exit codes match pre-change behavior.

---

### Edge Cases

- Circular imports after moving DTOs, builder, and I/O: layout MUST allow a clear dependency direction (DTOs → helpers/errors → dataset → search).
- Partial migrations: no module should re-export the same type from two paths indefinitely; deprecation comments MAY be used briefly if required by course policy.
- Empty or malformed JSON files MUST still fail with clear, structured errors as today.

## Requirements *(mandatory)*

### Repository implementation constraints

Implementations in this repository MUST comply with  
`.specify/memory/constitution.md`: **standard library only** (no PyPI dependencies), PEP 8, strict type hints, Google-style docstrings on public API, and **`unittest`** for automated tests.

### Functional Requirements

- **FR-001**: All types implemented with the language’s **immutable structured record** facility for domain data (profiles, normalized points, scaling metadata, and any other such DTOs used across similarity/search) MUST reside under **`src/services/dto/`** (one module or split modules under that package is acceptable; duplicates elsewhere MUST be removed).
- **FR-002**: Types and re-exports currently defined under **`src/services/core/`** (including domain exceptions and package `__init__` surface) MUST be **relocated into `src/services/helper.py`** (or submodules only if needed to avoid cycles, with `helper` as the documented entry); the **`core` package MUST be removed** once call sites are updated.
- **FR-003**: Responsibilities currently in **`src/services/similarity/pipeline.py`** (synthetic iteration, categorical mapping, Min–Max normalization, corpus/query preparation) MUST live under **`src/services/dataset.py`**, with a **`DataBuilder`** (or equivalent class name agreed at plan time) as the primary façade for orchestrating those steps; the **`similarity` package MUST be removed or reduced** to thin re-exports only if required for backward compatibility during migration (target end state: no duplicate pipeline logic).
- **FR-004**: JSON corpus and query load/save logic currently in **`src/services/io/jsonio.py`** MUST be moved to **`src/services/`** (e.g. `jsonio.py` sibling to `helper.py`); the **`io` subpackage MUST be removed** after imports are updated.
- **FR-005**: **No change** to on-disk **JSON schemas** for corpus arrays and query objects; external files produced by `generate-corpus` and consumed by `search` MUST remain compatible.
- **FR-006**: **All existing automated tests** MUST pass without weakening assertions; new tests SHOULD cover import paths and `DataBuilder` wiring if gaps appear.
- **FR-007**: **`src/main.py`** and all `services.*` imports MUST be updated to the new layout; **`PYTHONPATH`** usage documented for the project MUST remain valid (application root + `src`).

### Key Entities *(data concepts)*

- **Raw profile record**: Identifier, numeric demographics, categorical labels before normalization.
- **Normalized profile record**: Identifier plus fixed-dimension numeric vector in bounded range after scaling.
- **Scaling metadata**: Per-dimension min/max (or equivalent) derived from a corpus for query alignment.
- **Query specification**: Reference profile, per-dimension weights, and top-k parameter as exchanged in JSON.
- **DTO package**: The single namespace holding immutable record types shared across dataset building and search.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: **100%** of automated tests that passed on the pre-change baseline **continue to pass** on the refactored tree (same test command and discovery rules).
- **SC-002**: For a **fixed seed** and corpus size, **generated corpus bytes** (and metadata sidecar text) are **byte-identical** to the pre-change generator output, OR any intentional difference is documented in the plan with an explicit migration note (default: byte-identical).
- **SC-003**: For a **fixed corpus file, query file, strategy, and k**, **search JSON stdout** is **identical** to the pre-change CLI output (ordering and tie-breaking unchanged).
- **SC-004**: A new contributor can locate **all** domain DTO definitions by inspecting **only** the DTO package and its documented index (qualitative review: ≤10 minutes to list types from docs or module listing).

## Assumptions

- **A-001**: “All `@dataclass`” means **all domain DTOs** used in similarity/search/I/O; **stdlib or internal utility dataclasses** (e.g. private heap keys in search) MAY remain colocated with their algorithm if moving them would harm encapsulation—**prefer** DTO package for **shared** shapes only; final split is finalized in `/speckit.plan`.
- **A-002**: Renaming `DataBuilder` methods to match old free functions is acceptable as long as **behavior and test coverage** are preserved.
- **A-003**: No new file formats (CSV, Parquet, etc.) are introduced by this feature.
- **A-004**: Git branch creation may be manual if the Specify script does not detect a repository root from `group_project/` alone; spec path remains under `specs/003-src-module-restructure/`.
