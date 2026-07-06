import type { EChartsOption } from 'echarts';

import { useSleepData } from '../../api/hooks';
import { Chart } from '../../charts/Chart';
import { colorsFor } from '../../charts/echartsThemes';
import { useTheme } from '../../theme/useTheme';

function toMinutes(seconds: number | undefined): number {
  return Math.round((seconds ?? 0) / 60);
}

function buildOption(stages: { label: string; value: number; color: string }[]): EChartsOption {
  return {
    xAxis: { type: 'value' },
    yAxis: { type: 'category', data: [''] },
    tooltip: { trigger: 'item', valueFormatter: (v) => `${v}m` },
    legend: { bottom: 0 },
    series: stages.map((s) => ({
      name: s.label,
      type: 'bar',
      stack: 'sleep',
      data: [s.value],
      itemStyle: { color: s.color },
    })),
  };
}

/** Horizontal stacked bar of sleep stage durations (Deep/Light/REM/Awake). */
export function SleepStagesChart({ date }: { date: string }) {
  const { data, isLoading, error } = useSleepData(date);
  const { theme } = useTheme();
  const c = colorsFor(theme);

  if (isLoading) {
    return <p>Loading...</p>;
  }

  if (error) {
    return <p>No data: {error.message}</p>;
  }

  const dto = data?.dailySleepDTO;

  const stages = [
    { label: 'Deep', value: toMinutes(dto?.deepSleepSeconds), color: c.blue },
    { label: 'Light', value: toMinutes(dto?.lightSleepSeconds), color: c.textMuted },
    { label: 'REM', value: toMinutes(dto?.remSleepSeconds), color: c.purple },
    { label: 'Awake', value: toMinutes(dto?.awakeSleepSeconds), color: c.red },
  ];

  if (stages.every((s) => s.value === 0)) {
    return <p>No sleep stage data</p>;
  }

  return <Chart option={buildOption(stages)} />;
}
