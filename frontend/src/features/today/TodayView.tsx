import { useHrv, useSleepData, useSummary } from '../../api/hooks';
import { ActivitiesTable } from './ActivitiesTable';
import { BodyBatteryGauge } from './BodyBatteryGauge';
import { HeartRateChart } from './HeartRateChart';
import { HrvTrendChart } from './HrvTrendChart';
import { SleepStagesChart } from './SleepStagesChart';
import { StatCard } from './StatCard';
import { latestBodyBattery } from './bodyBattery';
import styles from './TodayView.module.css';

function todayISO(): string {
  return new Date().toISOString().slice(0, 10);
}

function formatHrvStatus(status: string | undefined): string {
  if (!status) {
    return '';
  }

  return status.charAt(0).toUpperCase() + status.slice(1).toLowerCase();
}

export function TodayView() {
  const date = todayISO();
  const summary = useSummary(date);
  const sleep = useSleepData(date);
  const hrv = useHrv(date);

  const sleepScore = sleep.data?.dailySleepDTO?.sleepScores?.overall?.value ?? sleep.data?.sleepScore;
  const bodyBattery = latestBodyBattery(summary.data?.body_battery);

  return (
    <div>
      <div className={styles.cardRow}>
        <StatCard
          label="Steps"
          value={summary.data?.stats?.totalSteps?.toLocaleString()}
          sub={
            summary.data?.stats?.dailyStepGoal
              ? `/ ${summary.data.stats.dailyStepGoal.toLocaleString()} goal`
              : undefined
          }
          loading={summary.isLoading}
          error={summary.error?.message}
        />
        <StatCard label="Sleep Score" value={sleepScore} loading={sleep.isLoading} error={sleep.error?.message} />
        <StatCard label="Body Battery" value={bodyBattery} loading={summary.isLoading} error={summary.error?.message} />
        <StatCard
          label="Resting HR"
          value={summary.data?.stats?.restingHeartRate}
          sub="bpm"
          loading={summary.isLoading}
          error={summary.error?.message}
        />
        <StatCard
          label="HRV"
          value={hrv.data?.hrvSummary?.lastNight}
          sub={formatHrvStatus(hrv.data?.hrvSummary?.status)}
          loading={hrv.isLoading}
          error={hrv.error?.message}
        />
      </div>

      <div className={styles.chartRow}>
        <div className={styles.chartCard}>
          <h2>Heart Rate Today</h2>
          <HeartRateChart date={date} />
        </div>
        <div className={styles.chartCard}>
          <h2>Sleep Stages</h2>
          <SleepStagesChart date={date} />
        </div>
        <div className={styles.chartCard}>
          <h2>HRV Trend</h2>
          <HrvTrendChart date={date} />
        </div>
        <div className={styles.chartCard}>
          <h2>Body Battery</h2>
          <BodyBatteryGauge level={bodyBattery} />
        </div>
      </div>

      <ActivitiesTable />
    </div>
  );
}
