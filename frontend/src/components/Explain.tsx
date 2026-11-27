// Ported from TST frontend/src/components/Explain.tsx @ 3da2f5b1 by way of Partner Track's port
// @ 0e13dca7; changed: a cash KPI's breakdown is every posted line on its account (the API's
// ExplainOut), with no band, trend or Ask why yet.
import { Drawer, Text } from '@mantine/core';
import { createColumnHelper, useTable } from '@tanstack/react-table';
import { useMemo, useState } from 'react';
import { useParams } from 'react-router';
import { formatMoney } from '../core/lib/format';
import { useExplain, type CashKpi, type ExplainData } from '../lib/api';
import { gameTableFeatures, type GameTableFeatures } from '../lib/table';
import { DataTable } from './DataTable';

// Explain this: a number's breakdown as the API built it. Read-only: it never changes the game.

type Line = ExplainData['lines'][number];

/** The Explain affordance: a small button beside a number that opens its panel. */
export function Explain({ kpi, label }: { kpi: CashKpi; label: string }) {
  const { slug = '' } = useParams();
  const [open, setOpen] = useState(false);
  return (
    <>
      <button
        type="button"
        className="tst-explain"
        aria-label={`Explain ${label}`}
        title={`Explain ${label}`}
        data-testid={`explain-${kpi}`}
        onClick={(e) => {
          e.preventDefault();
          e.stopPropagation();
          setOpen(true);
        }}
      >
        ?
      </button>
      {open && <ExplainPanel slug={slug} kpi={kpi} label={label} onClose={() => setOpen(false)} />}
    </>
  );
}

const helper = createColumnHelper<GameTableFeatures, Line>();

function Breakdown({ lines }: { lines: Line[] }) {
  const columns = useMemo(
    () =>
      helper.columns([
        helper.accessor('date_label', { header: 'Month' }),
        helper.accessor('memo', { header: 'Entry' }),
        helper.accessor('book', { header: 'Book' }),
        helper.accessor('amount_cents', {
          header: 'Amount',
          cell: ({ getValue }) => <span className="tst-num">{formatMoney(getValue())}</span>,
        }),
      ]),
    [],
  );
  const table = useTable({ features: gameTableFeatures, columns, data: lines });
  return (
    <DataTable
      table={table}
      label="Breakdown"
      rowTestId="explain-line"
      empty="Nothing has been posted to this account yet."
    />
  );
}

function ExplainPanel({
  slug,
  kpi,
  label,
  onClose,
}: {
  slug: string;
  kpi: CashKpi;
  label: string;
  onClose: () => void;
}) {
  const explain = useExplain(slug, kpi, true);
  const e = explain.data;
  return (
    <Drawer opened onClose={onClose} position="right" size="lg" title={`Explain: ${label}`}>
      {explain.isPending ? (
        <Text c="dimmed">Loading…</Text>
      ) : explain.error || !e ? (
        <Text c="red">Could not explain this number: {explain.error?.message}</Text>
      ) : (
        <div
          style={{ display: 'flex', flexDirection: 'column', gap: 16 }}
          data-testid="explain-panel"
        >
          <div className="tst-num" style={{ fontSize: 22, fontWeight: 600 }}>
            {formatMoney(e.total_cents)}
          </div>
          <Breakdown lines={e.lines} />
        </div>
      )}
    </Drawer>
  );
}
