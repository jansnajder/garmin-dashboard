import type { ReactNode } from 'react';

import { useAuthStatus } from '../api/hooks';
import { LoginPage } from '../pages/LoginPage';

/**
 * Single top-level auth check: renders the login screen when nobody is
 * active, otherwise renders the routed app. A single-account desktop app
 * has no per-page auth surface worth guarding individually.
 */
export function AuthGate({ children }: { children: ReactNode }) {
  const { data, isLoading } = useAuthStatus();

  if (isLoading) {
    return null;
  }

  if (!data?.active) {
    return <LoginPage />;
  }

  return <>{children}</>;
}
