import { useActivities } from '../../api/hooks';
import styles from './TodayView.module.css';

function formatDuration(seconds: number): string {
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);

  return h > 0 ? `${h}h ${m}m` : `${m}m`;
}

/** Table of activities from the last 7 days. */
export function ActivitiesTable() {
  const { data, isLoading, error } = useActivities();

  return (
    <section className={styles.activitiesSection}>
      <h2>Recent Activities</h2>
      <table className={styles.table}>
        <thead>
          <tr>
            <th>Date</th>
            <th>Activity</th>
            <th>Duration</th>
            <th>Distance</th>
            <th>Avg HR</th>
            <th>Calories</th>
          </tr>
        </thead>
        <tbody>
          {isLoading ? (
            <tr>
              <td colSpan={6} className={styles.muted}>
                Loading...
              </td>
            </tr>
          ) : error ? (
            <tr>
              <td colSpan={6} className={styles.errorText}>
                {error.message}
              </td>
            </tr>
          ) : !data || data.length === 0 ? (
            <tr>
              <td colSpan={6} className={styles.muted}>
                No activities found.
              </td>
            </tr>
          ) : (
            data.map((a, i) => {
              const dt = new Date(a.startTimeLocal ?? a.startTimeGMT ?? '');
              const dateStr = Number.isNaN(dt.getTime()) ? '--' : dt.toLocaleDateString();
              const name = a.activityName ?? a.name ?? a.typeKey ?? '--';
              const dur = a.duration ? formatDuration(a.duration) : '--';
              const dist = a.distanceMeters ? `${(a.distanceMeters / 1000).toFixed(1)} km` : '--';
              const cal = a.calories ? Math.round(a.calories) : '--';

              return (
                <tr key={i}>
                  <td>{dateStr}</td>
                  <td>{name}</td>
                  <td>{dur}</td>
                  <td>{dist}</td>
                  <td>{a.averageHR ?? '--'}</td>
                  <td>{cal}</td>
                </tr>
              );
            })
          )}
        </tbody>
      </table>
    </section>
  );
}
