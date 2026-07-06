import { useState } from 'react';
import type { FormEvent } from 'react';

import { useForgetAccount, useLogin, useMfa, useSelectAccount } from '../api/auth';
import { ApiError } from '../api/fetchJSON';
import { useAccounts } from '../api/hooks';
import DeleteIcon from '../assets/icons/delete.svg?react';
import styles from './LoginPage.module.css';

type Step = 'login' | 'mfa';

/**
 * Full-window login screen: a credentials form with the remembered accounts
 * listed beneath it (click to select, trash to forget), plus a conditional
 * MFA step reached when Garmin challenges a fresh credential login.
 */
export function LoginPage() {
  const accountsQuery = useAccounts();
  const selectAccount = useSelectAccount();
  const forgetAccount = useForgetAccount();
  const login = useLogin();
  const mfa = useMfa();

  const [step, setStep] = useState<Step>('login');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [mfaCode, setMfaCode] = useState('');
  const [error, setError] = useState<string | null>(null);

  const accounts = accountsQuery.data ?? [];

  async function handleSelect(slug: string, accountEmail: string) {
    setError(null);

    try {
      const result = await selectAccount.mutateAsync(slug);

      if (result.status === 'needs_login') {
        // Token expired: prefill the email so only the password is left to enter.
        setEmail(accountEmail);
      }
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e));
    }
  }

  async function handleCredentialsSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);

    try {
      const result = await login.mutateAsync({ email, password });

      if (result.status === 'needs_mfa') {
        setStep('mfa');
      }
    } catch (e) {
      setError(e instanceof ApiError ? e.message : String(e));
    }
  }

  async function handleMfaSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);

    try {
      await mfa.mutateAsync(mfaCode);
    } catch (e) {
      setError(e instanceof ApiError ? e.message : String(e));
    }
  }

  /** Leave the MFA step back to the login screen so a wrong password can be corrected. */
  function backToLogin() {
    setStep('login');
    setMfaCode('');
    setPassword('');
    setError(null);
  }

  return (
    <div className={styles.page}>
      <div className={styles.card}>
        <h1 className={styles.title}>Garmin Dashboard</h1>

        {error && <p className={styles.error}>{error}</p>}

        {step === 'mfa' ? (
          <form onSubmit={handleMfaSubmit}>
            <label className={styles.label}>
              MFA code
              <input className={styles.input} value={mfaCode} onChange={(e) => setMfaCode(e.target.value)} autoFocus />
            </label>
            <button className={styles.submit} type="submit" disabled={mfa.isPending}>
              {mfa.isPending ? 'Verifying...' : 'Verify'}
            </button>
            <button type="button" className={styles.back} onClick={backToLogin}>
              Back
            </button>
          </form>
        ) : (
          <>
            <form onSubmit={handleCredentialsSubmit}>
              <label className={styles.label}>
                Email
                <input className={styles.input} type="email" value={email} onChange={(e) => setEmail(e.target.value)} />
              </label>
              <label className={styles.label}>
                Password
                <input
                  className={styles.input}
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
              </label>
              <button className={styles.submit} type="submit" disabled={login.isPending}>
                {login.isPending ? 'Logging in...' : 'Log in'}
              </button>
            </form>

            {accounts.length > 0 && (
              <>
                <p className={styles.accountsHeading}>Remembered accounts</p>
                <ul className={styles.accountList}>
                  {accounts.map((a) => (
                    <li key={a.slug} className={styles.accountRow}>
                      <button
                        className={styles.accountButton}
                        onClick={() => handleSelect(a.slug, a.email)}
                        disabled={selectAccount.isPending}
                      >
                        {a.display_name || a.email}
                      </button>
                      <button
                        className={styles.deleteAccount}
                        onClick={() => forgetAccount.mutate(a.slug)}
                        disabled={forgetAccount.isPending}
                        title="Delete account"
                        aria-label={`Delete account ${a.display_name || a.email}`}
                      >
                        <DeleteIcon width={16} height={16} />
                      </button>
                    </li>
                  ))}
                </ul>
              </>
            )}
          </>
        )}
      </div>
    </div>
  );
}
