import * as echarts from 'echarts';

/**
 * ECharts theme color values, duplicated from theme.css's CSS custom
 * properties - ECharts themes are plain JSON and can't reference CSS
 * variables, so this is a known, accepted duplication of truth. If the
 * palette in theme.css changes, update the matching values here too.
 */
export const darkColors = {
  bg: '#0f1117',
  surface: '#1c1f2b',
  border: '#2e3347',
  text: '#e8eaf0',
  textMuted: '#7b82a0',
  green: '#4caf7d',
  blue: '#4d9de0',
  orange: '#f4a261',
  red: '#e07070',
  purple: '#9b59b6',
};

export const lightColors = {
  bg: '#f5f6fa',
  surface: '#ffffff',
  border: '#d8dce6',
  text: '#1a1d29',
  textMuted: '#5b6178',
  green: '#2f8f5f',
  blue: '#2a6fb0',
  orange: '#c97a2e',
  red: '#c94747',
  purple: '#7d4a97',
};

function buildTheme(c: typeof darkColors) {
  return {
    color: [c.blue, c.green, c.orange, c.red, c.purple],
    backgroundColor: 'transparent',
    textStyle: { color: c.text },
    title: { textStyle: { color: c.text } },
    legend: { textStyle: { color: c.text } },
    tooltip: { textStyle: { color: c.text } },
    categoryAxis: {
      axisLine: { lineStyle: { color: c.border } },
      axisLabel: { color: c.textMuted },
      splitLine: { lineStyle: { color: c.border } },
    },
    valueAxis: {
      axisLine: { lineStyle: { color: c.border } },
      axisLabel: { color: c.textMuted },
      splitLine: { lineStyle: { color: c.border } },
    },
    timeAxis: {
      axisLine: { lineStyle: { color: c.border } },
      axisLabel: { color: c.textMuted },
      splitLine: { lineStyle: { color: c.border } },
    },
  };
}

echarts.registerTheme('gd-dark', buildTheme(darkColors));
echarts.registerTheme('gd-light', buildTheme(lightColors));

/** The literal color set for a theme name, for series that need an explicit semantic color. */
export function colorsFor(theme: 'light' | 'dark') {
  return theme === 'dark' ? darkColors : lightColors;
}
