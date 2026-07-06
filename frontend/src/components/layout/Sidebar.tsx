import { NavLink } from 'react-router-dom';

import { routes } from '../../routes';
import styles from './Sidebar.module.css';

/** Left nav, rendered from the shared route config so it stays in sync with the route table. */
export function Sidebar() {
  return (
    <nav className={styles.nav}>
      {routes.map((r) => (
        <NavLink
          key={r.path}
          to={r.path}
          className={({ isActive }) => `${styles.link} ${isActive ? styles.linkActive : ''}`}
        >
          {r.label}
        </NavLink>
      ))}
    </nav>
  );
}
