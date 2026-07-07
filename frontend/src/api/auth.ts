import { useMutation, useQueryClient } from '@tanstack/react-query';

import { fetchJSON } from './fetchJSON';

interface StatusResult {
  status: string;
}

function postJSON<T>(url: string, body: unknown): Promise<T> {
  return fetchJSON<T>(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
}

/** Start a credential login; "needs_mfa" means useMfa() must follow. */
export function useLogin() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (body: { email: string; password: string }) => postJSON<StatusResult>('/api/auth/login', body),
    onSuccess: (result) => {
      if (result.status === 'ok') {
        void queryClient.invalidateQueries({ queryKey: ['auth', 'status'] });
      }
    },
  });
}

/** Complete a pending MFA login started by useLogin(). */
export function useMfa() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (code: string) => postJSON<StatusResult>('/api/auth/mfa', { code }),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ['auth', 'status'] });
    },
  });
}

/** Activate a remembered account; "needs_login" means a fresh credential login is required. */
export function useSelectAccount() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (slug: string) => postJSON<StatusResult>('/api/auth/select', { slug }),
    onSuccess: (result) => {
      if (result.status === 'ok') {
        void queryClient.invalidateQueries({ queryKey: ['auth', 'status'] });
      }
    },
  });
}

/** Log out the active account, optionally forgetting it. */
export function useLogout() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (forget: boolean) => postJSON<StatusResult>('/api/auth/logout', { forget }),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ['auth', 'status'] });
    },
  });
}

/** Delete a remembered account and its stored tokens by slug. */
export function useForgetAccount() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (slug: string) => postJSON<StatusResult>('/api/auth/forget', { slug }),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ['auth', 'accounts'] });
      void queryClient.invalidateQueries({ queryKey: ['auth', 'status'] });
    },
  });
}
