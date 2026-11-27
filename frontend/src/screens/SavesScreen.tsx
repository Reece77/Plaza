import { Anchor, Stack, Text, Title } from '@mantine/core';
import { createColumnHelper, useTable } from '@tanstack/react-table';
import { useMemo } from 'react';
import { Link } from 'react-router';
import { DataTable } from '../components/DataTable';
import { useSaves, type SaveSummary } from '../lib/api';
import { gameTableFeatures, type GameTableFeatures } from '../lib/table';

const helper = createColumnHelper<GameTableFeatures, SaveSummary>();

export function SavesScreen() {
  const saves = useSaves();
  const columns = useMemo(
    () =>
      helper.columns([
        helper.accessor('org_name', {
          header: 'Organisation',
          cell: ({ row, getValue }) => (
            <Anchor component={Link} to={`/game/${row.original.slug}`}>
              {getValue()}
            </Anchor>
          ),
        }),
        helper.accessor('leader_name', { header: 'Leader' }),
        helper.accessor('turn', { header: 'Turn' }),
        helper.accessor('date_label', { header: 'Date', enableSorting: false }),
        helper.accessor('status', {
          header: 'Status',
          cell: ({ getValue }) => getValue().replace('_', ' '),
        }),
      ]),
    [],
  );
  const table = useTable({ features: gameTableFeatures, columns, data: saves.data ?? [] });
  return (
    <Stack maw={720} mx="auto" mt={80} gap="md">
      <Title order={2}>Saves</Title>
      {saves.isPending ? (
        <Text c="dimmed">Loading…</Text>
      ) : (
        <DataTable table={table} label="Saves" rowTestId="save-row" empty="No saves yet." />
      )}
      <Anchor component={Link} to="/">
        Back
      </Anchor>
    </Stack>
  );
}
