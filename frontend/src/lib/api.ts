// Server-state hooks over the generated client (TST ADR-0009). No game logic here: every
// number comes from the API; the front end only formats it.
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { api, type Schemas } from '../api/client';

export type GameState = Schemas['StateOut'];
export type SaveSummary = Schemas['SaveOut'];
export type Meta = Schemas['MetaOut'];
export type NewGameBody = Schemas['NewGameIn'];
export type ExplainData = Schemas['ExplainOut'];
export type LlmSettings = Schemas['LlmSettingsOut'];
export type CashKpi = 'dirty_cash_cents' | 'clean_cash_cents';

export class ApiError extends Error {
  code: string;

  constructor(code: string, message: string) {
    super(message);
    this.code = code;
  }
}

function unwrap<T>(result: { data?: T; error?: unknown }): T {
  if (result.error !== undefined || result.data === undefined) {
    const body = (result.error ?? {}) as { code?: string; message?: string };
    throw new ApiError(body.code ?? 'error', body.message ?? 'The request failed');
  }
  return result.data;
}

export const useMeta = () =>
  useQuery({ queryKey: ['meta'], queryFn: async () => unwrap(await api.GET('/api/meta')) });

export const useSaves = () =>
  useQuery({ queryKey: ['saves'], queryFn: async () => unwrap(await api.GET('/api/saves')) });

export const useGameState = (slug: string) =>
  useQuery({
    queryKey: ['state', slug],
    queryFn: async () =>
      unwrap(await api.GET('/api/saves/{slug}/state', { params: { path: { slug } } })),
  });

export function useNewGame() {
  const client = useQueryClient();
  return useMutation({
    mutationFn: async (body: NewGameBody) => unwrap(await api.POST('/api/saves', { body })),
    onSuccess: () => client.invalidateQueries({ queryKey: ['saves'] }),
  });
}

export function useAdvance(slug: string) {
  const client = useQueryClient();
  return useMutation({
    mutationFn: async () =>
      unwrap(await api.POST('/api/saves/{slug}/advance', { params: { path: { slug } } })),
    onSuccess: (state) => {
      client.setQueryData(['state', slug], state);
      void client.invalidateQueries({ queryKey: ['explain', slug] });
      void client.invalidateQueries({ queryKey: ['saves'] });
    },
  });
}

export const useExplain = (slug: string, kpi: CashKpi, enabled: boolean) =>
  useQuery({
    queryKey: ['explain', slug, kpi],
    enabled,
    queryFn: async () =>
      unwrap(await api.GET('/api/saves/{slug}/explain/{kpi}', { params: { path: { slug, kpi } } })),
  });

export const useLlmSettings = () =>
  useQuery({
    queryKey: ['llm'],
    queryFn: async () => unwrap(await api.GET('/api/settings/llm')),
  });

export function useSaveLlmSettings() {
  const client = useQueryClient();
  return useMutation({
    mutationFn: async (body: Schemas['LlmSettingsIn']) =>
      unwrap(await api.PUT('/api/settings/llm', { body })),
    onSuccess: (settings) => client.setQueryData(['llm'], settings),
  });
}
