import type { ComponentType, ReactElement, SVGProps } from 'react';

import ActivitiesIcon from './assets/icons/activities.svg?react';
import HealthIcon from './assets/icons/health.svg?react';
import HomeIcon from './assets/icons/home.svg?react';
import PerformanceIcon from './assets/icons/performance.svg?react';
import ProfileIcon from './assets/icons/profile.svg?react';
import StatisticsIcon from './assets/icons/statistics.svg?react';
import { PlaceholderView } from './pages/PlaceholderView';

export type IconComponent = ComponentType<SVGProps<SVGSVGElement>>;

export interface NavItem {
  path: string;
  label: string;
  icon: IconComponent;
  element: ReactElement;
}

/**
 * Single source of truth for the sidebar nav and the route table.
 *
 * `profileItem` is rendered in the sidebar's own top slot (avatar), `navItems`
 * fill the main nav list; `routes` is the flat list the router mounts. Each
 * section renders an empty placeholder for now - Phase 9 swaps in the real
 * views one entry at a time, no shell changes needed.
 */
export const profileItem: NavItem = {
  path: '/profile',
  label: 'Profile',
  icon: ProfileIcon,
  element: <PlaceholderView title="Profile" />,
};

export const navItems: NavItem[] = [
  { path: '/', label: 'Home', icon: HomeIcon, element: <PlaceholderView title="Home" /> },
  { path: '/activities', label: 'Activities', icon: ActivitiesIcon, element: <PlaceholderView title="Activities" /> },
  { path: '/health', label: 'Health', icon: HealthIcon, element: <PlaceholderView title="Health" /> },
  {
    path: '/performance',
    label: 'Performance',
    icon: PerformanceIcon,
    element: <PlaceholderView title="Performance" />,
  },
  { path: '/statistics', label: 'Statistics', icon: StatisticsIcon, element: <PlaceholderView title="Statistics" /> },
];

export const routes: NavItem[] = [profileItem, ...navItems];
