import type { EChartsOption } from 'echarts';

import { Chart } from '../../charts/Chart';
import { colorsFor } from '../../charts/echartsThemes';
import { useTheme } from '../../theme/useTheme';

function buildOption(level: number, color: string, textMuted: string): EChartsOption {
  return {
    series: [
      {
        type: 'gauge',
        min: 0,
        max: 100,
        progress: { show: true, itemStyle: { color } },
        axisLine: { lineStyle: { width: 8, color: [[1, textMuted]] } },
        pointer: { show: false },
        axisTick: { show: false },
        splitLine: { show: false },
        axisLabel: { show: false },
        detail: { valueAnimation: true, formatter: '{value}', color, fontSize: 28 },
        data: [{ value: level }],
      },
    ],
  };
}

/** Current body battery level as a 0-100 gauge. */
export function BodyBatteryGauge({ level }: { level: number | null }) {
  const { theme } = useTheme();
  const c = colorsFor(theme);

  if (level == null) {
    return <p>No body battery data</p>;
  }

  return <Chart option={buildOption(level, c.green, c.border)} height={180} />;
}
