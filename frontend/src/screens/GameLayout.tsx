import { AppShell, Button, Group, NavLink, Text } from '@mantine/core';
import { useCallback, useState } from 'react';
import { Link, Outlet, useNavigate, useParams } from 'react-router';
import { CommandPalette } from '../components/CommandPalette';
import { ScreenErrorBoundary } from '../core/components/ScreenErrorBoundary';
import { useGameHotkeys } from '../hooks/useGameHotkeys';
import { useAdvance, useGameState } from '../lib/api';
import { SCREENS } from '../lib/nav';
import { usePaletteHotkey } from '../lib/palette';

export function GameLayout() {
  const { slug = '' } = useParams();
  const navigate = useNavigate();
  const game = useGameState(slug);
  const advance = useAdvance(slug);
  const [palette, setPalette] = useState(false);
  const ended = game.data !== undefined && game.data.status !== 'active';
  const canContinue = !!game.data && !ended && !advance.isPending;

  const onContinue = useCallback(() => {
    if (canContinue) advance.mutate();
  }, [advance, canContinue]);
  useGameHotkeys(onContinue, (index) => {
    const screen = SCREENS[index];
    if (screen) void navigate(`/game/${slug}/${screen.path}`);
  });
  usePaletteHotkey(useCallback(() => setPalette(true), []));

  return (
    <AppShell header={{ height: 52 }} navbar={{ width: 200, breakpoint: 'sm' }} padding="md">
      <AppShell.Header>
        <Group h="100%" px="md" justify="space-between">
          <Text fw={600}>{game.data?.org_name ?? 'Plaza'}</Text>
          <Group>
            <Text data-testid="date">
              {ended ? game.data?.last_date_label : (game.data?.date_label ?? '')}
            </Text>
            <Button onClick={onContinue} loading={advance.isPending} disabled={!canContinue}>
              {ended ? 'Campaign complete' : 'Continue'}
            </Button>
          </Group>
        </Group>
      </AppShell.Header>
      <AppShell.Navbar p="xs">
        {SCREENS.map((s) => (
          <NavLink key={s.path} component={Link} to={`/game/${slug}/${s.path}`} label={s.label} />
        ))}
        <NavLink component={Link} to="/saves" label="Saves" />
        <NavLink component={Link} to="/" label="Main menu" />
      </AppShell.Navbar>
      <AppShell.Main>
        <ScreenErrorBoundary>
          <Outlet />
        </ScreenErrorBoundary>
      </AppShell.Main>
      <CommandPalette saveId={slug} opened={palette} onClose={() => setPalette(false)} />
    </AppShell>
  );
}
