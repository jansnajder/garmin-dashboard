import { NavLink } from 'react-router-dom';

import { useLogout } from '../../api/auth';
import ChangeAccountIcon from '../../assets/icons/change_account.svg?react';
import CollapseIcon from '../../assets/icons/collapse.svg?react';
import ExpandIcon from '../../assets/icons/expand.svg?react';
import { navItems, profileItem } from '../../routes';
import styles from './Sidebar.module.css';

interface SidebarProps {
  collapsed: boolean;
  onToggle: () => void;
}

/**
 * Left nav: profile avatar on top, the section links, then a bottom group with
 * "Change account" and the collapse/expand toggle. Nav entries come from the
 * shared route config so the sidebar and route table never drift apart.
 *
 * @param collapsed - whether the sidebar is in its icon-only width
 * @param onToggle - flips the collapsed state (owned by Layout)
 */
export function Sidebar({ collapsed, onToggle }: SidebarProps) {
  const logout = useLogout();

  const linkClass = ({ isActive }: { isActive: boolean }) => `${styles.link} ${isActive ? styles.linkActive : ''}`;

  const ProfileIcon = profileItem.icon;

  return (
    <nav className={`${styles.nav} ${collapsed ? styles.collapsed : ''}`}>
      <ul className={styles.list}>
        <li>
          <NavLink to={profileItem.path} className={linkClass} title={profileItem.label}>
            <ProfileIcon className={styles.icon} width={20} height={20} />
            <span className={styles.label}>{profileItem.label}</span>
          </NavLink>
        </li>

        {navItems.map((item) => {
          const Icon = item.icon;

          return (
            <li key={item.path}>
              <NavLink to={item.path} className={linkClass} title={item.label}>
                <Icon className={styles.icon} width={20} height={20} />
                <span className={styles.label}>{item.label}</span>
              </NavLink>
            </li>
          );
        })}
      </ul>

      <button
        type="button"
        className={styles.action}
        onClick={() => logout.mutate(false)}
        disabled={logout.isPending}
        title="Change account"
      >
        <ChangeAccountIcon className={styles.icon} width={20} height={20} />
        <span className={styles.label}>Change account</span>
      </button>

      <button
        type="button"
        className={styles.toggle}
        onClick={onToggle}
        title={collapsed ? 'Expand menu' : 'Collapse menu'}
        aria-label={collapsed ? 'Expand menu' : 'Collapse menu'}
      >
        {collapsed ? (
          <ExpandIcon className={styles.chevron} width={20} height={20} />
        ) : (
          <CollapseIcon className={styles.chevron} width={20} height={20} />
        )}
      </button>
    </nav>
  );
}
