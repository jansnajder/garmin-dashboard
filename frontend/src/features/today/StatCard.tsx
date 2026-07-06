import styles from './StatCard.module.css';

interface StatCardProps {
  label: string;
  value: string | number | null | undefined;
  sub?: string;
  loading?: boolean;
  error?: string;
}

/** A single labeled stat with an optional sub-line, loading skeleton and error state. */
export function StatCard({ label, value, sub, loading, error }: StatCardProps) {
  return (
    <div className={styles.card}>
      <div className={styles.label}>{label}</div>
      <div className={`${styles.value} ${error ? styles.valueError : ''}`} title={error}>
        {loading ? '…' : error ? '--' : (value ?? '--')}
      </div>
      {sub && !loading && !error && <div className={styles.sub}>{sub}</div>}
    </div>
  );
}
