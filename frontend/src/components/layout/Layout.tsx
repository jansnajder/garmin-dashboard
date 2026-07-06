import { Outlet } from 'react-router-dom';

import { Sidebar } from './Sidebar';
import { Topbar } from './Topbar';
import styles from './Layout.module.css';

/** CSS-grid app shell: topbar spans the top, sidebar+content fill the rest. */
export function Layout() {
  return (
    <div className={styles.shell}>
      <div className={styles.topbar}>
        <Topbar />
      </div>
      <div className={styles.sidebar}>
        <Sidebar />
      </div>
      <main className={styles.content}>
        <Outlet />
      </main>
    </div>
  );
}
