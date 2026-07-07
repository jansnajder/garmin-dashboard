import { useIsFetching, useMutation, useQueryClient } from '@tanstack/react-query';

import { fetchJSON } from '../api/fetchJSON';

/**
 * Clears the volatile cache server-side, then refetches every mounted query
 * regardless of outcome - a failed cache-clear still triggers a refetch,
 * matching the PoC's "clear is best-effort, reload happens anyway" behavior.
 */
export function useRefresh() {
  const queryClient = useQueryClient();
  const isFetching = useIsFetching();

  const mutation = useMutation({
    mutationFn: () => fetchJSON('/api/cache/clear?scope=volatile', { method: 'POST' }),
    onSettled: () => {
      void queryClient.invalidateQueries();
    },
  });

  return {
    refresh: () => mutation.mutate(),
    isRefreshing: mutation.isPending || isFetching > 0,
  };
}
