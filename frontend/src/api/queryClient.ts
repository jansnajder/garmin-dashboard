import { QueryCache, QueryClient } from '@tanstack/react-query';

import { ApiError } from './fetchJSON';

/**
 * Shared query client with a global 401 handler: any query that fails with
 * ApiError(401) invalidates the auth status query, which flips AuthGate back
 * to the login screen as a pure consequence of the re-render - no manual
 * navigation call needed.
 */
export const queryClient = new QueryClient({
  queryCache: new QueryCache({
    onError: (error) => {
      if (error instanceof ApiError && error.status === 401) {
        void queryClient.invalidateQueries({ queryKey: ['auth', 'status'] });
      }
    },
  }),
  defaultOptions: {
    queries: {
      retry: (failureCount, error) => !(error instanceof ApiError && error.status === 401) && failureCount < 2,
    },
  },
});
