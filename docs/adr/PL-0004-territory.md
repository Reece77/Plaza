## PL-0004: Territory

- New system; regions underneath come from PT's `geo/`

**Decision.**

1. A **plaza** is a node on a map: a district, crossing, port or corridor segment, each with a kind, a holder and four values: **control** (0–100), **tax yield**, **local loyalty** (0–100) and **contested** status.
2. Plazas connect by **edges** that routes use. Holding a plaza lowers costs and risk for routes through it; passing through another organisation's plaza costs a toll or risks conflict.
3. Control drifts monthly toward a target set by the holder's presence (members assigned), spending, local loyalty and rivals' pressure. Below a threshold a plaza becomes contested; a contest resolves through PL-0005 heat and the conflict rules (spec).
4. v1 map: one producing region, one transit corridor (northern Mexico border crossings) and one consumer market (US Southwest), at about 20–30 plazas.
5. The map is data (`plazas.yaml`), real geography at the level of regions and crossings; nothing finer than a city district.

**Consequences.** Territory is the league table made visible and the main thing a rival or the agency can take away.

