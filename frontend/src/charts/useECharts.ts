import * as echarts from 'echarts';
import { useEffect, useRef } from 'react';

import { useTheme } from '../theme/useTheme';
import './echartsThemes';

/**
 * Own an ECharts instance over a container div, re-initializing it whenever
 * the theme changes (ECharts binds its theme at init() time only, so a plain
 * setOption() cannot restyle an existing instance) and updating its option
 * otherwise via setOption(). Resize follows the container via ResizeObserver
 * rather than a window resize listener, so it also reacts to layout changes
 * that don't resize the window (e.g. a future collapsible sidebar).
 *
 * @param option - ECharts option object to render
 * @returns ref to attach to the chart's container div
 */
export function useECharts(option: echarts.EChartsOption) {
  const containerRef = useRef<HTMLDivElement>(null);
  const chartRef = useRef<echarts.ECharts | null>(null);
  const { theme } = useTheme();

  // Read during render (not the effect below) so re-init always paints the
  // option current as of this render, even for a widget whose own props/theme
  // usage didn't change and therefore won't re-run the setOption effect.
  const optionRef = useRef(option);
  optionRef.current = option;

  useEffect(() => {
    const el = containerRef.current;

    if (!el) {
      return;
    }

    const themeName = theme === 'dark' ? 'gd-dark' : 'gd-light';
    const chart = echarts.init(el, themeName);
    chartRef.current = chart;
    chart.setOption(optionRef.current, true);

    const resizeObserver = new ResizeObserver(() => chart.resize());
    resizeObserver.observe(el);

    return () => {
      resizeObserver.disconnect();
      chart.dispose();
      chartRef.current = null;
    };
  }, [theme]);

  useEffect(() => {
    chartRef.current?.setOption(option, true);
  }, [option]);

  return containerRef;
}
