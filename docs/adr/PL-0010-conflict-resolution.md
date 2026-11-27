## PL-0010: Conflict is resolved abstractly, month by month

- Status: **Accepted** (Reece, 2026-11-26)
- Applies: PL-0004 (contests), PL-0005 (heat), PL-0008 (outcomes, not scenes)

**Decision.**

1. **A war** is a record between two organisations over a set of contested plazas, with an **intensity** the player chooses each month: pressure, open conflict or all-out. Higher intensity shifts control faster and costs more.
2. **Strength** per side and plaza: members assigned, weighted by security skill and morale, plus security spending and allies' committed share. **Intelligence** (counter-surveillance, informants inside the other side) multiplies effective strength. **Money** sets how long a side can sustain its intensity.
3. **Monthly resolution** per contested plaza: control moves toward the stronger side by `k × intensity × (Sa − Sb) / (Sa + Sb)` plus keyed noise (stream `war`). Losses (members arrested or lost) and heat for both sides scale with intensity; press attention rises at all-out.
4. **Ending a war:** a truce at a sit-down; exhaustion (a side's money or morale under a threshold); one side's collapse; or agency pressure making both sides pull back.
5. **Alliances** are pacts that commit a share of strength and carry memory of betrayal; breaking one is a council matter.
6. **Reporting:** outcomes only (plazas changing hands, members lost, heat added), in monthly reports and events. No scenes, no detail of violence.

**Consequences.** Conflict is a resource decision like any other, legible through Explain, and expensive in heat, which keeps the state as the counterweight.

