# Plaza documents

The design pack (PL-D0, accepted by Reece 2026-11-26) is the source of truth. Each document was written as a Claude doc and copied here unchanged in PL-M0 sub-task 1 (exported as Markdown on 2026-11-27). `backend/tests/unit/test_design_pack.py` fails if a copied file changes; a change to the pack is made in its Claude doc first and copied again.

| Document | Here | Claude doc | sha256 of the copy |
| --- | --- | --- | --- |
| Roadmap v0.1 | [roadmap.md](roadmap.md) | [Plaza Roadmap v0.1](https://claude.ai/artifact/E8fQoN2YVPr9TZHqky2fQQ) | `41aedbdda676c3ee98825658388d262f19118794710d1346b18c3e815907518a` |
| Reuse map v0.1 | [reuse-map.md](reuse-map.md) | [Plaza Reuse Map v0.1](https://claude.ai/artifact/PaqbYADNUKbiuyhpk7D1KN) | `c535e92f211b744b121818ecfad57391f51733692105278ada41839692584c86` |
| ADRs PL-0001 to PL-0011 | [adr/](adr/README.md), one file per ADR | [Plaza ADRs PL-0001 to PL-0008 v0.1](https://claude.ai/artifact/MdRXFLQicghfNuUNrbDvhf) | `9529bdcc2f4c8b27e7e5837a482d14abb8f676fe05528eaa68455aba69535c69` (the files rejoined) |
| Game design spec v0.1 | [game-design-spec.md](game-design-spec.md) | [Plaza Game Design Spec v0.1](https://claude.ai/artifact/Ey3m5EEwojkCxcZUgknXXL) | `aa899beed6bdc0bf290b8a446bfc176c799da23a62381575e9b55bae77bd93ff` |
| Open questions v0.1 | [questions.md](questions.md) | [Plaza Open Questions v0.1](https://claude.ai/artifact/37aheq5Nfp8nSmR1LASQqg) | `8ec2130f5ab270bddf42aaf0965afebf564d8041066e70f65d3e38a484b4a651` |
| Research dossier v1 | [research/dossier-v1.md](research/dossier-v1.md) | [Plaza Research Dossier v1 (2006–2016)](https://claude.ai/artifact/GLeFCi6fwibpCDTvk6yuMK) | `1caeb5459e2e750aa0d1e82e86fcfeaa7a02859a021196e8f223577f942bf3df` |
| Concept and new-project prompt | not copied (superseded by the pack) | [Plaza: Cartel Management Game](https://claude.ai/artifact/QZM26BspysoM2TWQD7RiXD) | — |

Milestone briefs live in [tasks/](tasks/README.md); each is copied from its Claude doc when its session starts and gains a "Decisions made" section as the session works. Column reference for the save schema: [data-dictionary.md](data-dictionary.md).

Precedence (CLAUDE.md section 1): on technical matters sim-core's ADRs and Plaza's ADRs override the spec; any other conflict is a question for Reece.
