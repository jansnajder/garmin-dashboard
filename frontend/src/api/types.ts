/**
 * Hand-written response shapes for the auth endpoints the shell consumes.
 *
 * Phase 9 adds view response types generated from typed Pydantic models via
 * openapi-typescript; these two stay hand-written since they back the shell,
 * not a data view.
 */

export interface AccountSummary {
  slug: string;
  email: string;
  display_name: string;
  last_used: string | null;
}

export interface AuthStatus {
  active: string | null;
}
