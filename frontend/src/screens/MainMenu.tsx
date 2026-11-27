import { Button, Stack, Text, Title } from '@mantine/core';
import { Link } from 'react-router';

export function MainMenu() {
  return (
    <Stack maw={420} mx="auto" mt={120} gap="md">
      <Title order={1}>Plaza</Title>
      <Text c="dimmed">
        Break away in January 2006 with a small crew. Thirty years, to December 2035.
      </Text>
      <Button component={Link} to="/new">
        New game
      </Button>
      <Button component={Link} to="/saves" variant="default">
        Saves
      </Button>
      <Button component={Link} to="/settings" variant="subtle">
        Settings
      </Button>
    </Stack>
  );
}
