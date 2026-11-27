import { expect, test } from '@playwright/test';

// PL-M0: create an organisation, press Continue, see dirty cash on the Overview, Explain it,
// reload the save, find it on the Saves screen, and read the LLM budget meter.
test('break away, press Continue, reload the save', async ({ page }) => {
  await page.goto('/');
  await page.getByRole('link', { name: 'New game' }).click();
  await page.getByLabel('Organisation name').fill('Smoke Test Org');
  await page.getByLabel('Leader name').fill('Smoke Leader');
  await expect(page.getByTestId('background-lean')).toBeVisible();
  await page.getByRole('button', { name: 'Break away' }).click();
  await expect(page.getByTestId('date')).toHaveText('Jan 2006');
  await expect(page.getByTestId('dirty-cash')).toHaveText('$100,000.00');
  await expect(page.getByTestId('clean-cash')).toHaveText('$0.00');
  await page.getByTestId('overview-continue').click();
  await expect(page.getByTestId('date')).toHaveText('Feb 2006');
  await page.keyboard.press('Space');
  await expect(page.getByTestId('date')).toHaveText('Mar 2006');
  await page.getByTestId('explain-dirty_cash_cents').click();
  await expect(page.getByTestId('explain-panel')).toContainText('Starting stake');
  await page.keyboard.press('Escape');
  await page.reload();
  await expect(page.getByTestId('date')).toHaveText('Mar 2006');
  await expect(page.getByTestId('dirty-cash')).toHaveText('$100,000.00');
  await page.keyboard.press('Control+k');
  await expect(page.getByTestId('palette-input')).toBeVisible();
  await page.keyboard.press('Escape');
  await page.goto('/saves');
  await expect(page.getByRole('link', { name: 'Smoke Test Org' })).toBeVisible();
  await page.goto('/settings');
  await expect(page.getByTestId('llm-meter-label')).toContainText('used this month');
});
