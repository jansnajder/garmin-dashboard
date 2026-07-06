import type { EChartsOption } from 'echarts';

import { useHrv } from '../../api/hooks';
import { Chart } from '../../charts/Chart';
import { colorsFor } from '../../charts/echartsThemes';
import { useTheme } from '../../theme/useTheme';
import type { HrvReading } from '../../api/types';

function buildOption(readings: HrvReading[], weeklyAvg: number | undefined, green: string, textMuted: string) {
  const labels = readings.map((r) => {
    const d = new Date(r.startTimestampGMT ?? r.startTimestampLocal ?? '');

    return Number.isNaN(d.getTime()) ? '' : d.toLocaleDateString(undefined, { month: 'short', day: 'numeric' });
  });

  const option: EChartsOption = {
    xAxis: { type: 'category', data: labels },
    yAxis: { type: 'value', name: 'ms' },
    tooltip: { trigger: 'axis' },
    series: [
      {
        type: 'line',
        data: readings.map((r) => r.hrvValue ?? null),
        itemStyle: { color: green },
        lineStyle: { color: green, width: 2 },
        areaStyle: { color: green, opacity: 0.1 },
        symbolSize: 6,
        markLine:
          weeklyAvg != null
            ? {
                symbol: 'none',
                lineStyle: { type: 'dashed', color: textMuted },
                label: { formatter: '7-day avg', color: textMuted },
                data: [{ yAxis: weeklyAvg }],
              }
            : undefined,
      },
    ],
  };

  return option;
}

/** Nightly HRV readings with a dashed 7-day average reference line. */
export function HrvTrendChart({ date }: { date: string }) {
  const { data, isLoading, error } = useHrv(date);
  const { theme } = useTheme();
  const c = colorsFor(theme);

  if (isLoading) {
    return <p>Loading...</p>;
  }

  if (error) {
    return <p>No data: {error.message}</p>;
  }

  const readings = (data?.hrvReadings ?? []).filter((r) => r.hrvValue != null);

  if (readings.length === 0) {
    return <p>No HRV readings</p>;
  }

  return <Chart option={buildOption(readings, data?.hrvSummary?.weeklyAvg, c.green, c.textMuted)} />;
}
