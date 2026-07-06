import type * as echarts from 'echarts';

import { useECharts } from './useECharts';

interface ChartProps {
  option: echarts.EChartsOption;
  height?: number | string;
  className?: string;
}

/** Renders an ECharts option into a container div; see useECharts for the lifecycle. */
export function Chart({ option, height = 240, className }: ChartProps) {
  const containerRef = useECharts(option);

  return <div ref={containerRef} className={className} style={{ width: '100%', height }} />;
}
