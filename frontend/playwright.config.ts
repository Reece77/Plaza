import { defineConfig, devices } from '@playwright/test';
import { mkdtempSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

// The smoke test runs its own API (fresh save folder) and Vite server on spare ports, so it
// never touches saves/ or a running `make dev`.
const API_PORT = Number(process.env.PLAZA_E2E_API_PORT ?? 8785);
const WEB_PORT = Number(process.env.PLAZA_E2E_WEB_PORT ?? 5185);
process.env.PLAZA_E2E_SAVE_DIR ??= mkdtempSync(join(tmpdir(), 'plaza-e2e-'));
const saveDir = process.env.PLAZA_E2E_SAVE_DIR;
// PLAYWRIGHT_CHROMIUM_PATH points at an installed Chromium or Chrome (cloud sessions).
const executablePath = process.env.PLAYWRIGHT_CHROMIUM_PATH;

export default defineConfig({
  testDir: 'e2e',
  fullyParallel: false,
  workers: 1,
  reporter: 'list',
  use: { baseURL: `http://127.0.0.1:${WEB_PORT}`, trace: 'retain-on-failure' },
  projects: [
    {
      name: 'chromium',
      use: {
        ...devices['Desktop Chrome'],
        launchOptions: executablePath ? { executablePath } : {},
      },
    },
  ],
  webServer: [
    {
      command: `uv run uvicorn plaza.api.app:app --port ${API_PORT}`,
      cwd: '../backend',
      url: `http://127.0.0.1:${API_PORT}/api/meta`,
      env: { PLAZA_SAVE_DIR: saveDir, PLAZA_LLM_ADAPTER: 'mock', PLAZA_SQLITE_SYNC: 'OFF' },
      reuseExistingServer: false,
      timeout: 120_000,
    },
    {
      command: `pnpm exec vite --port ${WEB_PORT} --strictPort --host 127.0.0.1`,
      url: `http://127.0.0.1:${WEB_PORT}`,
      env: { PLAZA_API_URL: `http://127.0.0.1:${API_PORT}` },
      reuseExistingServer: false,
      timeout: 120_000,
    },
  ],
});
