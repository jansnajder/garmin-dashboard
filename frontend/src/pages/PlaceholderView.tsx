import styles from './PlaceholderView.module.css';

/**
 * Empty section view used by every route in Phase 8.5. Renders the section
 * name faintly so navigating between sections gives visible feedback while the
 * real content is built out in Phase 9.
 *
 * @param title - the section name to display
 */
export function PlaceholderView({ title }: { title: string }) {
  return (
    <div className={styles.placeholder}>
      <span className={styles.title}>{title}</span>
    </div>
  );
}
