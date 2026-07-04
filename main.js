// @ts-check
'use strict';

const { app, BrowserWindow } = require('electron');
const { spawn, execFileSync } = require('child_process');
const http = require('http');
const path = require('path');

const PORT = 8000;

/** @type {import('child_process').ChildProcess | null} */
let backendProcess = null;

/**
 * Resolve how to launch the backend for the current mode.
 *
 * In dev (`app.isPackaged` false) it runs via `uv run uvicorn`. In a packaged
 * build it runs the PyInstaller-frozen exe shipped under resources/backend.
 *
 * @returns {{cmd: string, args: string[], cwd: string}}
 */
function backendCommand() {
  if (!app.isPackaged) {
    return {
      cmd: 'uv',
      args: ['run', 'uvicorn', 'app.main:app', '--port', String(PORT)],
      cwd: path.join(__dirname, 'backend'),
    };
  }

  const exe = path.join(process.resourcesPath, 'backend', 'backend.exe');

  return { cmd: exe, args: [], cwd: path.dirname(exe) };
}

/**
 * Spawn the FastAPI backend as a child process.
 *
 * The process inherits stdio so its logs appear in the Electron terminal.
 */
function startBackend() {
  const { cmd, args, cwd } = backendCommand();

  backendProcess = spawn(cmd, args, {
    cwd,
    stdio: 'inherit',
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
// On Windows, `kill()` only signals the direct child (the `uv` launcher in dev),
// orphaning uvicorn. `taskkill /T` terminates the whole process tree instead.
app.on('before-quit', () => {
  if (!backendProcess) {
    return;
  }

  const pid = backendProcess.pid;

  if (process.platform === 'win32' && pid) {
    try {
      execFileSync('taskkill', ['/pid', String(pid), '/T', '/F']);
    } catch (_) {
      /* already gone */
    }
  } else {
    backendProcess.kill();
  }

  backendProcess = null;
});

app.on('window-all-closed', () => {
  app.quit();
});
