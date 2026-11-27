# Plaza

A single-player, turn-based management game on the shared [sim-core](https://github.com/Reece77/sim-core) engine: a breakaway organisation from January 2006 to December 2035, told through reports, ledgers and briefings. Personal use.

- Play: double-click `Plaza.cmd` (Windows; needs `uv` and Node.js once), or `make dev` and open http://localhost:5173.
- Headless: `cd backend && uv run plaza new-game --name dev && uv run plaza advance --save dev --turns 12`.
- Read first: [CLAUDE.md](CLAUDE.md), [docs/README.md](docs/README.md) (the design pack) and [docs/adr/](docs/adr/README.md).
- Check: `make check` (and `make e2e`).
