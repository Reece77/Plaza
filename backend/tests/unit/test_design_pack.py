"""The design pack is copied into docs/ unchanged (PL-M0 sub-task 1; docs/README.md). A
change to a copied file fails here: change the Claude doc first, copy it again and update
the hash with the reason in CHANGELOG.md."""

from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

DOCS = Path(__file__).resolve().parents[3] / "docs"
PACK = {
    "roadmap.md": "41aedbdda676c3ee98825658388d262f19118794710d1346b18c3e815907518a",
    "reuse-map.md": "c535e92f211b744b121818ecfad57391f51733692105278ada41839692584c86",
    "game-design-spec.md": "aa899beed6bdc0bf290b8a446bfc176c799da23a62381575e9b55bae77bd93ff",
    "questions.md": "8ec2130f5ab270bddf42aaf0965afebf564d8041066e70f65d3e38a484b4a651",
    "research/dossier-v1.md": "1caeb5459e2e750aa0d1e82e86fcfeaa7a02859a021196e8f223577f942bf3df",
}
ADR_PACK = "9529bdcc2f4c8b27e7e5837a482d14abb8f676fe05528eaa68455aba69535c69"
ADR_ORDER = ("0001", "0002", "0003", "0004", "0005", "0006", "0007", "0008", "0011", "0009", "0010")
PREAMBLE = "## The pack's preamble (verbatim)\n\n"
CLOSING = "## The pack's closing section (verbatim)\n\n"


@pytest.mark.parametrize("name", sorted(PACK))
def test_copied_document_unchanged(name: str) -> None:
    digest = hashlib.sha256((DOCS / name).read_bytes()).hexdigest()
    assert digest == PACK[name], f"docs/{name} differs from the design pack's copy"


def test_adr_files_rejoin_to_the_pack_document() -> None:
    readme = (DOCS / "adr" / "README.md").read_text(encoding="utf-8")
    head = readme.split(PREAMBLE, 1)[1].split(CLOSING, 1)[0]
    tail = readme.split(CLOSING, 1)[1]
    adrs = DOCS / "adr"
    body = "".join(next(adrs.glob(f"PL-{n}-*.md")).read_text(encoding="utf-8") for n in ADR_ORDER)
    assert hashlib.sha256((head + body + tail).encode()).hexdigest() == ADR_PACK
