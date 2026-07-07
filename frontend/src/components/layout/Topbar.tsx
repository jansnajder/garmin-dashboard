import { useRefresh } from '../../hooks/useRefresh';
import BackIcon from '../../assets/icons/back.svg?react';
import DarkModeIcon from '../../assets/icons/dark_mode.svg?react';
import LightModeIcon from '../../assets/icons/light_mode.svg?react';
import RefreshIcon from '../../assets/icons/refresh.svg?react';
import { useTheme } from '../../theme/useTheme';
import styles from './Topbar.module.css';

/** Back button (left) plus icon-only refresh and theme controls (right). */
export function Topbar() {
  const { theme, toggleTheme } = useTheme();
  const { refresh, isRefreshing } = useRefresh();

  return (
    <div className={styles.bar}>
      <button type="button" className={styles.button} title="Back">
        <BackIcon width={20} height={20} />
      </button>

      <div className={styles.controls}>
        <button type="button" className={styles.button} onClick={refresh} disabled={isRefreshing} title="Refresh">
          <RefreshIcon className={isRefreshing ? styles.spin : ''} width={20} height={20} />
        </button>
        <button
          type="button"
          className={styles.button}
          onClick={toggleTheme}
          title={theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'}
        >
          {theme === 'dark' ? <LightModeIcon width={20} height={20} /> : <DarkModeIcon width={20} height={20} />}
        </button>
      </div>
    </div>
  );
}
