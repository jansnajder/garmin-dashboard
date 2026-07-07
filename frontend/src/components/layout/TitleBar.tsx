import { useEffect } from 'react';

import type { TitleBarOverlay } from '../../electron';
import type { Theme } from '../../theme/themeContextObject';
import { useTheme } from '../../theme/useTheme';
import styles from './TitleBar.module.css';

// Row is 32px (see Layout.module.css); overlay height is 2px shorter so our
// own border-bottom shows through along the full width, buttons included.
const TITLEBAR_OVERLAY: Record<Theme, TitleBarOverlay> = {
  dark: { color: '#090a1b', symbolColor: '#a2a2a2', height: 30 },
  light: { color: '#f5f6fa', symbolColor: '#5b6178', height: 30 },
};

/**
 * Draggable strip with the app name, drawn behind the native Windows
 * minimize/maximize/close buttons (`titleBarOverlay` in main.js draws those,
 * not this component). Pushes overlay colors through the `window.electronAPI`
 * preload bridge whenever the app theme changes so the native buttons track
 * light/dark mode. No-ops when opened as a plain web page (no Electron host).
 */
export function TitleBar() {
  const { theme } = useTheme();

  useEffect(() => {
    window.electronAPI?.setTitleBarOverlay(TITLEBAR_OVERLAY[theme]);
  }, [theme]);

  return (
    <div className={styles.bar}>
      <span className={styles.title}>Garmin Dashboard</span>
    </div>
  );
}
