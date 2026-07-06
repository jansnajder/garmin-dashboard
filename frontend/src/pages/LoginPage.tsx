import { useState } from 'react';
import type { FormEvent } from 'react';

import { useLogin, useMfa, useSelectAccount } from '../api/auth';
import { ApiError } from '../api/fetchJSON';
import { useAccounts } from '../api/hooks';
import styles from './LoginPage.module.css';

type Step = 'idle' | 'credentials' | 'mfa';

/**
 * Full-window login screen: remembered accounts (click to select), a
 * credentials form for new/expired accounts, and a conditional MFA step.
 */
export function LoginPage() {
  const accountsQuery = useAccounts();
  const selectAccount = useSelectAccount();
  const login = useLogin();
  const mfa = useMfa();

  const [step, setStep] = useState<Step>('idle');
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
        setEmail(accountEmail);
        setStep('credentials');
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
          </form>
        ) : step === 'credentials' ? (
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
        ) : (
          <>
            {accounts.length > 0 && (
              <ul className={styles.accountList}>
                {accounts.map((a) => (
                  <li key={a.slug}>
                    <button
                      className={styles.accountButton}
                      onClick={() => handleSelect(a.slug, a.email)}
                      disabled={selectAccount.isPending}
                    >
                      {a.display_name || a.email}
                    </button>
                  </li>
                ))}
              </ul>
            )}
            <button className={styles.newAccount} onClick={() => setStep('credentials')}>
              Log in with a different account
            </button>
          </>
        )}
      </div>
    </div>
  );
}
