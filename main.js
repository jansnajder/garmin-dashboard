// @ts-check
'use strict';

const { app, BrowserWindow } = require('electron');
const { spawn } = require('child_process');
const http = require('http');
const path = require('path');

const PORT = 8000;

/** @type {import('child_process').ChildProcess | null} */
let backendProcess = null;

/**
 * Spawn the FastAPI/uvicorn backend as a child process.
 *
 * Uses `uv run` so no separate venv activation is needed. The process
 * inherits stdio so its logs appear in the Electron terminal.
 */
function startBackend() {
  const backendDir = path.join(__dirname, 'garmin-backend');

  backendProcess = spawn('uv', ['run', 'uvicorn', 'main:app', '--port', String(PORT)], {
    cwd: backendDir,
    stdio: 'inherit',
    // On Windows, spawn a detached process group so we can signal the tree.
    // Without this, only the `uv` launcher is killed; uvicorn keeps running.
    detached: false,
  });

  backendProcess.on('error', (err) => {
    console.error('[main] Failed to start backend process:', err.message);
  });

  backendProcess.on('exit', (code, signal) => {
    console.log(`[main] Backend exited (code=${code}, signal=${signal})`);
    backendProcess = null;
  });
}

/**
 * Poll `http://localhost:{PORT}` until the server accepts a connection.
 *
 * @param {number} [timeoutMs=30000] - Give up after this many milliseconds.
 * @returns {Promise<void>}
 * @throws {Error} when the server does not start within the timeout.
 */
function waitForBackend(timeoutMs = 30000) {
  return new Promise((resolve, reject) => {
    const deadline = Date.now() + timeoutMs;

    function probe() {
      const req = http.get(`http://localhost:${PORT}/`, (res) => {
        res.resume();
        resolve();
      });

      req.on('error', () => {
        if (Date.now() >= deadline) {
          reject(new Error(`Backend did not start within ${timeoutMs}ms`));
          return;
        }

        setTimeout(probe, 500);
      });

      req.end();
    }

    probe();
  });
}

/**
 * Create and show the main application window.
 *
 * Security notes:
 *   - nodeIntegration: false  -- renderer cannot call Node APIs directly
 *   - contextIsolation: true  -- renderer's JS and any preload run in separate
 *     contexts; no shared global object between them
 * These are the safe defaults. We load a localhost URL (not a remote one) so
 * the risk is low, but keeping them correct establishes the right habit for
 * Phase 4 when the app is packaged and distributed.
 */
function createWindow() {
  const win = new BrowserWindow({
    width: 1400,
    height: 900,
    title: 'Garmin Dashboard',
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
    },
  });

  win.loadURL(`http://localhost:${PORT}`);
}

app.whenReady().then(async () => {
  startBackend();

  try {
    await waitForBackend();
  } catch (err) {
    console.error('[main] Backend failed to start:', err);
    app.quit();
    return;
  }

  createWindow();
});

// Kill the backend when the app is about to quit.
// Note: on Windows, `backendProcess.kill()` terminates the `uv` launcher but
// may leave the uvicorn subprocess running briefly. This is acceptable for the
// PoC; Phase 4 switches to a PyInstaller binary which is a single process.
app.on('before-quit', () => {
  if (backendProcess) {
    backendProcess.kill();
  }
});

app.on('window-all-closed', () => {
  app.quit();
});
