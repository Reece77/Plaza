import { Button, Card, Group, Text, Title } from '@mantine/core';
import { useParams } from 'react-router';
import { Explain } from '../components/Explain';
import { LoadError, Loading } from '../core/components/ScreenState';
import { formatMoney } from '../core/lib/format';
import { useAdvance, useGameState } from '../lib/api';

export function OverviewScreen() {
  const { slug = '' } = useParams();
  const game = useGameState(slug);
  const advance = useAdvance(slug);
  if (game.isPending) return <Loading />;
  if (!game.data) return <LoadError title="Overview" error={game.error} />;
  const g = game.data;
  const ended = g.status !== 'active';
  return (
    <>
      <Title order={2} mb="md">
        Overview
      </Title>
      <Group align="stretch">
        <Card withBorder miw={200}>
          <Text c="dimmed" size="sm">
            Date
          </Text>
          <Text size="xl" fw={600} data-testid="overview-date">
            {ended ? g.last_date_label : g.date_label}
          </Text>
          <Text c="dimmed" size="xs">
            {ended ? 'Campaign complete' : `Campaign ends ${g.last_date_label}`}
          </Text>
        </Card>
        <Card withBorder miw={200}>
          <Text c="dimmed" size="sm">
            Dirty cash <Explain kpi="dirty_cash_cents" label="dirty cash" />
          </Text>
          <Text size="xl" fw={600} className="tst-num" data-testid="dirty-cash">
            {formatMoney(g.dirty_cash_cents)}
          </Text>
        </Card>
        <Card withBorder miw={200}>
          <Text c="dimmed" size="sm">
            Clean cash <Explain kpi="clean_cash_cents" label="clean cash" />
          </Text>
          <Text size="xl" fw={600} className="tst-num" data-testid="clean-cash">
            {formatMoney(g.clean_cash_cents)}
          </Text>
        </Card>
      </Group>
      <Group mt="lg">
        <Button
          onClick={() => advance.mutate()}
          loading={advance.isPending}
          disabled={ended}
          data-testid="overview-continue"
        >
          {ended ? 'Campaign complete' : 'Continue'}
        </Button>
      </Group>
    </>
  );
}
