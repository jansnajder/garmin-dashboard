import { useEffect, useState } from 'react';
import type { ReactNode } from 'react';

import { ThemeContext } from './themeContextObject';
import type { Theme } from './themeContextObject';

const STORAGE_KEY = 'garmin-dashboard:theme';

function initialTheme(): Theme {
  const stored = localStorage.getItem(STORAGE_KEY);

  if (stored === 'light' || stored === 'dark') {
    return stored;
  }

  return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
}

export function ThemeProvider({ children }: { children: ReactNode }) {
  const [theme, setTheme] = useState<Theme>(initialTheme);

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem(STORAGE_KEY, theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme((t) => (t === 'dark' ? 'light' : 'dark'));
  };

  return <ThemeContext.Provider value={{ theme, toggleTheme }}>{children}</ThemeContext.Provider>;
}
