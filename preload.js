// @ts-check
'use strict';

const { contextBridge, ipcRenderer } = require('electron');

/**
 * Bridge the renderer's title bar to the main-process window overlay controls.
 *
 * Exposed as `window.electronAPI`; `contextIsolation: true` means this is the
 * only way for the renderer to reach these IPC channels (see main.js).
 */
contextBridge.exposeInMainWorld('electronAPI', {
  /**
   * Restyle the native titlebar overlay buttons (minimize/maximize/close) to
   * match the app's current theme.
   *
   * @param {{color: string, symbolColor: string, height?: number}} overlay - overlay colors
   */
  setTitleBarOverlay: (overlay) => ipcRenderer.send('window:set-titlebar-overlay', overlay),
});
