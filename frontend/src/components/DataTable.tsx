// Ported from Partner Track frontend/src/components/DataTable.tsx @ 0e13dca7 (TST's, without
// the glossary Term on headers); changed: no saved column views yet (they need a settings API).
import type { ReactTable, RowData } from '@tanstack/react-table';
import { useLayoutEffect, useRef, useState, type HTMLAttributes, type UIEvent } from 'react';
import { ROW_PX, VIEW_PX, rowWindow, WINDOW_FROM, type GameTableFeatures } from '../lib/table';

const ARROWS = { asc: ' ▲', desc: ' ▼' } as const;

interface Props<T extends RowData> {
  table: ReactTable<GameTableFeatures, T>;
  label: string;
  rowTestId?: string;
  selectedRowId?: string;
  empty?: string;
  rowProps?: (row: T) => HTMLAttributes<HTMLTableRowElement>; // e.g. draggable rows (Org)
}

/** Table markup for a TanStack table: header click sorts, wide tables scroll in the panel. */
export function DataTable<T extends RowData>({
  table,
  label,
  rowTestId,
  selectedRowId,
  empty,
  rowProps,
}: Props<T>) {
  const rows = table.getRowModel().rows;
  const windowed = rows.length > WINDOW_FROM;
  const wrap = useRef<HTMLDivElement>(null);
  const firstRow = useRef<HTMLTableRowElement>(null);
  const [scrollTop, setScrollTop] = useState(0);
  const [viewport, setViewport] = useState(VIEW_PX);
  const [rowPx, setRowPx] = useState(ROW_PX);
  useLayoutEffect(() => {
    if (!windowed) return;
    const height = wrap.current?.clientHeight ?? 0;
    if (height > 0 && height !== viewport) setViewport(height);
    const row = firstRow.current?.offsetHeight ?? 0;
    if (row > 0 && row !== rowPx) setRowPx(row);
  }, [windowed, viewport, rowPx, rows.length]);
  const span = windowed
    ? rowWindow(rows.length, scrollTop, viewport, rowPx)
    : { start: 0, end: rows.length, before: 0, after: 0 };
  const columns = table.getVisibleLeafColumns().length;
  const onScroll = windowed
    ? (e: UIEvent<HTMLDivElement>) => setScrollTop(e.currentTarget.scrollTop)
    : undefined;
  const body = (
    <div
      ref={wrap}
      className={windowed ? 'tst-table-wrap tst-table-wrap--windowed' : 'tst-table-wrap'}
      onScroll={onScroll}
    >
      <table
        className="tst-table"
        aria-label={label}
        aria-rowcount={windowed ? rows.length + 1 : undefined}
      >
        <thead>
          {table.getHeaderGroups().map((group) => (
            <tr key={group.id}>
              {group.headers.map((header) => {
                if (header.isPlaceholder) return <th key={header.id} />;
                const sorted = header.column.getIsSorted();
                const toggle = header.column.getToggleSortingHandler();
                return (
                  <th
                    key={header.id}
                    aria-sort={
                      sorted === 'asc' ? 'ascending' : sorted === 'desc' ? 'descending' : undefined
                    }
                  >
                    {header.column.getCanSort() && toggle ? (
                      <button type="button" onClick={toggle}>
                        <table.FlexRender header={header} />
                        {sorted ? ARROWS[sorted] : ''}
                      </button>
                    ) : (
                      <table.FlexRender header={header} />
                    )}
                  </th>
                );
              })}
            </tr>
          ))}
        </thead>
        <tbody>
          {rows.length === 0 ? (
            <tr>
              <td className="tst-muted" colSpan={columns}>
                {empty ?? 'Nothing to show.'}
              </td>
            </tr>
          ) : (
            <>
              {span.before > 0 && (
                <tr aria-hidden="true" style={{ height: span.before }}>
                  <td colSpan={columns} />
                </tr>
              )}
              {rows.slice(span.start, span.end).map((row, i) => (
                <tr
                  key={row.id}
                  ref={i === 0 ? firstRow : undefined}
                  aria-rowindex={windowed ? span.start + i + 2 : undefined}
                  data-testid={rowTestId}
                  data-selected={row.id === selectedRowId}
                  {...rowProps?.(row.original)}
                >
                  {row.getVisibleCells().map((cell) => (
                    <td key={cell.id}>
                      <table.FlexRender cell={cell} />
                    </td>
                  ))}
                </tr>
              ))}
              {span.after > 0 && (
                <tr aria-hidden="true" style={{ height: span.after }}>
                  <td colSpan={columns} />
                </tr>
              )}
            </>
          )}
        </tbody>
      </table>
    </div>
  );
  return body;
}
