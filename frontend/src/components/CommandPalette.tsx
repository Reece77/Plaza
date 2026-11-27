// Ported from TST frontend/src/components/CommandPalette.tsx @ 3da2f5b1; changed: screens only
// (people, products and rivals join with their milestones) and no unlock gating yet.
import { Modal, TextInput } from '@mantine/core';
import { useMemo, useState } from 'react';
import { useNavigate } from 'react-router';
import { SCREENS } from '../lib/nav';
import { matchOptions, type Option } from '../lib/palette';
import { pushRecent, readRecent } from '../lib/recent';

// The command palette: Ctrl+K (or Cmd+K) jumps to any screen by name. With nothing typed it
// lists recent items.

const MAX_SHOWN = 12;

export function CommandPalette({
  saveId,
  opened,
  onClose,
}: {
  saveId: string;
  opened: boolean;
  onClose: () => void;
}) {
  return (
    <Modal
      opened={opened}
      onClose={onClose}
      title="Go to"
      size="lg"
      data-testid="command-palette"
      transitionProps={{ duration: 0 }}
    >
      {opened && <PaletteBody saveId={saveId} onClose={onClose} />}
    </Modal>
  );
}

function PaletteBody({ saveId, onClose }: { saveId: string; onClose: () => void }) {
  const navigate = useNavigate();
  const [query, setQuery] = useState('');
  const [index, setIndex] = useState(0);
  const [recent] = useState(() => readRecent(saveId));

  const options = useMemo<Option[]>(
    () =>
      SCREENS.map((s) => ({
        key: `screen-${s.path}`,
        label: s.label,
        detail: 'Screen',
        kind: 'screen',
        path: s.path,
      })),
    [],
  );

  const shown: Option[] = query.trim()
    ? matchOptions(options, query).slice(0, MAX_SHOWN)
    : recent.map((r) => ({ key: `recent-${r.path}`, ...r, detail: 'Screen' }));

  const go = (o: Option) => {
    pushRecent(saveId, { label: o.label, path: o.path, kind: o.kind });
    onClose();
    void navigate(`/game/${saveId}/${o.path}`);
  };

  return (
    <>
      <TextInput
        data-autofocus
        placeholder="A screen"
        value={query}
        aria-label="Search screens"
        data-testid="palette-input"
        onChange={(e) => {
          setQuery(e.currentTarget.value);
          setIndex(0);
        }}
        onKeyDown={(e) => {
          if (e.key === 'ArrowDown') {
            e.preventDefault();
            setIndex((i) => Math.min(i + 1, Math.max(shown.length - 1, 0)));
          } else if (e.key === 'ArrowUp') {
            e.preventDefault();
            setIndex((i) => Math.max(i - 1, 0));
          } else if (e.key === 'Enter' && shown[index]) {
            e.preventDefault();
            go(shown[index]);
          }
        }}
      />
      <div role="listbox" aria-label="Results" style={{ marginTop: 10 }}>
        {!query.trim() && shown.length > 0 && (
          <div className="tst-muted" style={{ fontSize: 12, padding: '4px 8px' }}>
            Recent
          </div>
        )}
        {shown.map((o, i) => (
          <button
            key={o.key}
            type="button"
            role="option"
            aria-selected={i === index}
            className="tst-row"
            data-testid="palette-option"
            onMouseEnter={() => setIndex(i)}
            onClick={() => go(o)}
            style={{
              width: '100%',
              border: 0,
              cursor: 'pointer',
              textAlign: 'left',
              background: i === index ? 'var(--tst-panel-active)' : 'transparent',
              color: 'var(--tst-text)',
              borderRadius: 6,
              padding: '6px 8px',
            }}
          >
            <span>{o.label}</span>
            <span className="tst-muted" style={{ fontSize: 12 }}>
              Screen
            </span>
          </button>
        ))}
        {query.trim() && shown.length === 0 && (
          <p className="tst-muted" style={{ margin: '8px', fontSize: 13 }}>
            Nothing matches.
          </p>
        )}
      </div>
    </>
  );
}
