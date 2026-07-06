import { useQuery } from '@tanstack/react-query';

import { fetchJSON } from './fetchJSON';
import type {
  AccountSummary,
  ActivitiesResponse,
  AuthStatus,
  HeartRateResponse,
  HrvResponse,
  SleepResponse,
  SummaryResponse,
} from './types';

/** Today's steps, calories, resting HR and body battery for a date. */
export function useSummary(date: string) {
  return useQuery({
    queryKey: ['summary', date],
    queryFn: () => fetchJSON<SummaryResponse>(`/api/summary?date=${date}`),
  });
}

/** Sleep score and stage breakdown for a date. */
export function useSleepData(date: string) {
  return useQuery({
    queryKey: ['sleep-data', date],
    queryFn: () => fetchJSON<SleepResponse>(`/api/sleep-data?date=${date}`),
  });
}

/** Resting heart rate and intraday HR samples for a date. */
export function useHeartRate(date: string) {
  return useQuery({
    queryKey: ['heart-rate', date],
    queryFn: () => fetchJSON<HeartRateResponse>(`/api/heart-rate?date=${date}`),
  });
}

/** HRV status for a date. */
export function useHrv(date: string) {
  return useQuery({
    queryKey: ['hrv', date],
    queryFn: () => fetchJSON<HrvResponse>(`/api/hrv?date=${date}`),
  });
}

/** Activities between start and end date (inclusive); defaults to the last 7 days. */
export function useActivities(start?: string, end?: string) {
  return useQuery({
    queryKey: ['activities', start, end],
    queryFn: () => {
      const params = new URLSearchParams();

      if (start) {
        params.set('start', start);
      }

      if (end) {
        params.set('end', end);
      }

      const qs = params.toString();

      return fetchJSON<ActivitiesResponse>(`/api/activities${qs ? `?${qs}` : ''}`);
    },
  });
}

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
