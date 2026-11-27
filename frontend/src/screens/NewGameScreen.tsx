import { Alert, Button, Select, Stack, Switch, Text, TextInput, Title } from '@mantine/core';
import { useState } from 'react';
import { useNavigate } from 'react-router';
import { toSaveSlug } from '../core/lib/slug';
import { useMeta, useNewGame } from '../lib/api';

export function NewGameScreen() {
  const meta = useMeta();
  const create = useNewGame();
  const navigate = useNavigate();
  const [orgName, setOrgName] = useState('');
  const [leaderName, setLeaderName] = useState('');
  const [background, setBackground] = useState<string | null>(null);
  const [difficulty, setDifficulty] = useState<string | null>(null);
  const [ironman, setIronman] = useState(false);
  const chosenDifficulty = difficulty ?? meta.data?.default_difficulty ?? null;
  const chosenBackground = background ?? meta.data?.backgrounds[0]?.id ?? null;
  const lean = meta.data?.backgrounds.find((b) => b.id === chosenBackground)?.description;
  const ready = orgName.trim() !== '' && leaderName.trim() !== '' && chosenBackground !== null;

  const start = () =>
    create.mutate(
      {
        slug: toSaveSlug(orgName) || 'organisation',
        org_name: orgName.trim(),
        leader_name: leaderName.trim(),
        background: chosenBackground ?? '',
        difficulty: chosenDifficulty ?? undefined,
        ironman,
      },
      { onSuccess: (state) => navigate(`/game/${state.slug}`) },
    );

  return (
    <Stack maw={480} mx="auto" mt={80} gap="md">
      <Title order={2}>New game</Title>
      <TextInput
        label="Organisation name"
        value={orgName}
        onChange={(e) => setOrgName(e.currentTarget.value)}
      />
      <TextInput
        label="Leader name"
        value={leaderName}
        onChange={(e) => setLeaderName(e.currentTarget.value)}
      />
      <Select
        label="Background"
        data={(meta.data?.backgrounds ?? []).map((b) => ({ value: b.id, label: b.name }))}
        value={chosenBackground}
        onChange={setBackground}
        allowDeselect={false}
      />
      {lean && (
        <Text size="sm" c="dimmed" data-testid="background-lean">
          {lean}
        </Text>
      )}
      <Select
        label="Difficulty"
        data={(meta.data?.difficulties ?? []).map((d) => ({ value: d.id, label: d.name }))}
        value={chosenDifficulty}
        onChange={setDifficulty}
        allowDeselect={false}
      />
      <Switch
        label="Ironman (one save; capture or death is final)"
        checked={ironman}
        onChange={(e) => setIronman(e.currentTarget.checked)}
      />
      {create.error && <Alert color="warn">{create.error.message}</Alert>}
      <Button onClick={start} loading={create.isPending} disabled={!ready}>
        Break away
      </Button>
    </Stack>
  );
}
