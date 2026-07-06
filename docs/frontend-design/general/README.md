The SVG files in this folder sketch the general visuals of the application. The implemented shell lives
in `frontend/src/components/layout/` (Layout, Sidebar, Topbar).

The left menu is full-height on the left. From the top:

- Profile
- Home
- Activities
- Health
- Performance
- Statistics

- Change account
- Arrow that expands/collapses the menu

The top bar sits beside the menu (not above it) and contains:

- Back button (cycles to the previous view)
- Refresh button (icon only, with tooltip)
- Theme button (icon only, with tooltip)

Each light blue element in the SVGs is a placeholder for an icon; the app renders `lucide-react` icons.

## Behavior

- **Collapse / expand:** the bottom arrow toggles the menu between icon-only (collapsed) and icon + label
  (expanded), and the state persists across restarts. The width animates with a simple eased (non-linear)
  movement and the labels fade with it; the arrow icon itself swaps instantly (no fade).
- **Change account:** logs out without forgetting and drops to the login screen. The login screen and the
  account picker are the same view: an email/password form with the remembered accounts listed beneath it
  (click an account to switch, the trash icon to delete one, and a Back button escapes the MFA step).
- **Refresh:** clears the volatile cache and refetches everything; the icon spins while fetching.
- **Theme:** toggles dark/light and persists across restarts.

Wired so far: Change account, Collapse/expand, Refresh, Theme. The Back button, Profile, and the section
views are placeholders - the nav items route and highlight the active item but render an empty view until
Phase 9 fills them in.
