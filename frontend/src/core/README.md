# sim-core UI shell (UI-VENDORED, plan section 3)

The canonical copy of the front-end pieces both games share. Taken from TST's
`frontend/src` at `3da2f5b` unchanged: `lib/format.ts` (`formatMoney` and the other display
formatters; money arrives as integer cents), `lib/attr.ts` (attribute ranges and tiers),
`lib/slug.ts`, their tests, and four components (`AttributeRange`, `MoraleBar`,
`ScreenState`, `ScreenErrorBoundary`; React and Mantine, as in both games).

Games copy this folder into `frontend/src/core/` and check it against the `MANIFEST.json` of
the tag they pin: `python tools/ui_manifest.py --check frontend/src/core` (run from a
sim-core checkout at that tag). Never edit a copy: change it here and release.

The Explain, help, inbox, Holiday, saves and settings screens named in the plan import each
game's generated API client, so they wait for a client-neutral shape (a follow-up).
