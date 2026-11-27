import {
  Anchor,
  Button,
  Group,
  NumberInput,
  Progress,
  Select,
  Stack,
  Text,
  Title,
} from '@mantine/core';
import { useState } from 'react';
import { Link } from 'react-router';
import { formatMoney } from '../core/lib/format';
import { useLlmSettings, useSaveLlmSettings } from '../lib/api';

// The LLM budget meter (TST ADR-0005 section 6): real spend this calendar month against the
// player's budget. The template adapter is the default; no text is generated before PL-M8.
export function SettingsScreen() {
  const settings = useLlmSettings();
  const save = useSaveLlmSettings();
  const [adapter, setAdapter] = useState<string | null>(null);
  const [budget, setBudget] = useState<number | null>(null);
  const s = settings.data;
  const chosenAdapter = adapter ?? (s && s.adapter !== 'mock' ? s.adapter : 'templates');
  const budgetDollars = budget ?? (s ? s.monthly_budget_cents / 100 : 0);
  const used = s && s.monthly_budget_cents > 0 ? (100 * s.spent_cents) / s.monthly_budget_cents : 0;

  return (
    <Stack maw={560} mx="auto" mt={80} gap="md">
      <Title order={2}>Settings</Title>
      <Title order={4}>Story text (LLM)</Title>
      {s && (
        <>
          <Text size="sm" data-testid="llm-meter-label">
            {formatMoney(Math.round(s.spent_cents))} of {formatMoney(s.monthly_budget_cents)} used
            this month ({s.calls} calls); resets {s.resets_on}.
          </Text>
          <Progress value={Math.min(used, 100)} data-testid="llm-meter" />
          <Select
            label="Writer"
            data={[
              { value: 'templates', label: 'Templates (offline)' },
              { value: 'claude', label: s.has_key ? 'Claude' : 'Claude (no API key found)' },
            ]}
            value={chosenAdapter}
            onChange={setAdapter}
            allowDeselect={false}
          />
          <NumberInput
            label="Monthly budget (USD)"
            min={0}
            max={10000}
            value={budgetDollars}
            onChange={(v) => setBudget(typeof v === 'number' ? v : Number(v) || 0)}
          />
          <Group>
            <Button
              onClick={() =>
                save.mutate({
                  adapter: chosenAdapter === 'claude' ? 'claude' : 'templates',
                  monthly_budget_cents: Math.round(budgetDollars * 100),
                })
              }
              loading={save.isPending}
            >
              Save
            </Button>
          </Group>
        </>
      )}
      <Anchor component={Link} to="/">
        Back
      </Anchor>
    </Stack>
  );
}
