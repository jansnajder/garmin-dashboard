import { useQuery } from '@tanstack/react-query';

import { fetchJSON } from './fetchJSON';
import type { AccountSummary, AuthStatus } from './types';

/** The active account's email, or null when nobody is logged in. */
export function useAuthStatus() {
  return useQuery({
    queryKey: ['auth', 'status'],
    queryFn: () => fetchJSON<AuthStatus>('/api/auth/status'),
  });
}

/** Remembered accounts, shown on the login screen. */
export function useAccounts() {
  return useQuery({
    queryKey: ['auth', 'accounts'],
    queryFn: () => fetchJSON<AccountSummary[]>('/api/auth/accounts'),
  });
}
