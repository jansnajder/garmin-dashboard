import type { ReactElement } from 'react';

import { TodayView } from './features/today/TodayView';

export interface RouteConfig {
  path: string;
  label: string;
  element: ReactElement;
}

/**
 * Single source of truth for both the sidebar nav and the route table.
 * Sleep, HRV & Training, Activities, Body & Weight and Devices land here in
 * Phase 9, once their specs exist - each is one more entry, no shell changes.
 */
export const routes: RouteConfig[] = [{ path: '/', label: 'Today', element: <TodayView /> }];
