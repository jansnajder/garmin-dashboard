import { useEffect, useState } from 'react';
import { Outlet } from 'react-router-dom';

import { Sidebar } from './Sidebar';
import { TitleBar } from './TitleBar';
import { Topbar } from './Topbar';
import styles from './Layout.module.css';

const STORAGE_KEY = 'garmin-dashboard:sidebar-collapsed';

function initialCollapsed(): boolean {
  return localStorage.getItem(STORAGE_KEY) === 'true';
}

/**
 * CSS-grid app shell: the sidebar spans the full height on the left, with the
 * topbar beside it over the content ('nav topbar' / 'nav content'). Owns the
 * sidebar collapsed state (persisted to localStorage) so the grid column width
 * and the sidebar's own contents stay in sync.
 */
export function Layout() {
  const [collapsed, setCollapsed] = useState(initialCollapsed);

  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, String(collapsed));
  }, [collapsed]);

  return (
    <div className={`${styles.shell} ${collapsed ? styles.collapsed : ''}`}>
      <div className={styles.titlebar}>
        <TitleBar />
      </div>
      <div className={styles.topbar}>
        <Topbar />
      </div>
      <div className={styles.sidebar}>
        <Sidebar collapsed={collapsed} onToggle={() => setCollapsed((c) => !c)} />
      </div>
      <main className={styles.content}>
        <Outlet />
      </main>
    </div>
  );
}
