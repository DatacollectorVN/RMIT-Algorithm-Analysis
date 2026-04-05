# Data model: 003 Source layout consolidation

**Spec**: [spec.md](./spec.md)  
**Note**: This feature does **not** change JSON shapes or field semantics — only **where** Python types are defined.

## Entities (unchanged fields)

### RawProfile

- **Module (after refactor)**: `services.dto`
- **Fields**: `profile_id` (str), `age`, `monthly_income`, `daily_learning_hours` (float), `highest_degree`, `favourite_domain` (str)
- **Validation**: JSON parsing and range checks remain in `jsonio` / dataset logic as today

### NormalizedProfile

- **Module**: `services.dto`
- **Fields**: `profile_id` (str), `vector` (5-tuple float in [0, 1] per dimension after Min–Max)

### ScalingStats

- **Module**: `services.dto`
- **Fields**: `mins`, `maxs` (each 5-tuple float)

### Query payload (JSON, not a dataclass today)

- **reference**: same shape as a corpus record object
- **weights**: fixed keys (`age`, `monthly_income`, `education`, `daily_learning_hours`, `domain`)
- **k**: positive int

## Relationships

```text
JSON file  --jsonio-->  list[RawProfile]  --dataset/DataBuilder-->  list[NormalizedProfile] + ScalingStats
Query JSON --jsonio-->  raw reference + weights + k  --dataset-->  normalized query vector (tuple)
```

## Validation rules

- Same as pre-refactor: unknown degree/domain → `ValidationError`; malformed JSON → `ValidationError`; weight constraints unchanged in `jsonio` / distance layer.

## State transitions

N/A (batch CLI; no long-lived server state).
