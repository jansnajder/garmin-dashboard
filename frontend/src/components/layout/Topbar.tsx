import { useState } from 'react';

import { useLogout } from '../../api/auth';
import { useAuthStatus } from '../../api/hooks';
import { useRefresh } from '../../hooks/useRefresh';
import { useTheme } from '../../theme/useTheme';
import styles from './Topbar.module.css';

/** Refresh + theme controls, and a user menu with logout/logout+forget. */
export function Topbar() {
  const { data: status } = useAuthStatus();
  const { theme, toggleTheme } = useTheme();
  const { refresh, isRefreshing } = useRefresh();
  const logout = useLogout();
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <div className={styles.bar}>
      <button className={styles.button} onClick={refresh} disabled={isRefreshing}>
        {isRefreshing ? 'Refreshing...' : 'Refresh'}
      </button>
      <button className={styles.button} onClick={toggleTheme}>
        {theme === 'dark' ? 'Light mode' : 'Dark mode'}
      </button>
      <div className={styles.userMenu}>
        <span className={styles.email}>{status?.active}</span>
        <button className={styles.button} onClick={() => setMenuOpen((v) => !v)}>
          Account
        </button>
        {menuOpen && (
          <div className={styles.menuPanel}>
            <button onClick={() => logout.mutate(false)}>Log out</button>
            <button onClick={() => logout.mutate(true)}>Log out &amp; forget account</button>
          </div>
        )}
      </div>
    </div>
  );
}
