# Contracts: similarity search

**Feature**: `001-similarity-search-topk`  
**Purpose**: Stable shapes for JSON interchange and CLI-adjacent integration (stdlib
`json` only).

| File | Role |
|------|------|
| [corpus-record.schema.json](./corpus-record.schema.json) | One raw profile in a corpus file |
| [query-request.schema.json](./query-request.schema.json) | Query + weights + k |
| [search-response.schema.json](./search-response.schema.json) | Ranked hits + optional timing |

Validation in code can be done with explicit field checks (no third-party JSON
Schema validator required).
