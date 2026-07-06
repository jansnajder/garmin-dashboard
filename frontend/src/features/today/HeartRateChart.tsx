import type { EChartsOption } from 'echarts';

import { useHeartRate } from '../../api/hooks';
import { Chart } from '../../charts/Chart';
import type { HeartRateSample } from '../../api/types';

function buildOption(samples: HeartRateSample[]): EChartsOption {
  const points = samples.filter((entry) => Array.isArray(entry) && entry[1] != null && entry[1] > 0);

  return {
    xAxis: { type: 'time' },
    yAxis: { type: 'value' },
    dataZoom: [{ type: 'inside' }, { type: 'slider' }],
    tooltip: { trigger: 'axis', valueFormatter: (v) => `${v} bpm` },
    series: [
      {
        type: 'line',
        data: points,
        showSymbol: false,
        areaStyle: {},
        lineStyle: { width: 1.5 },
      },
    ],
  };
}

/** Intraday heart rate over the day, with a zoom slider for the full-resolution samples. */
export function HeartRateChart({ date }: { date: string }) {
  const { data, isLoading, error } = useHeartRate(date);

  if (isLoading) {
    return <p>Loading...</p>;
  }

  if (error) {
    return <p>No data: {error.message}</p>;
  }

  const samples = data?.heartRateValues ?? data?.heartRateValuesArray ?? [];

  if (samples.filter((s) => s[1] != null && s[1] > 0).length === 0) {
    return <p>No intraday data</p>;
  }

  return <Chart option={buildOption(samples)} />;
}
