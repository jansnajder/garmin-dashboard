export interface TitleBarOverlay {
  color: string;
  symbolColor: string;
  height?: number;
}

export interface ElectronAPI {
  setTitleBarOverlay: (overlay: TitleBarOverlay) => void;
}

declare global {
  interface Window {
    /** Bridge to the Electron main process, injected by preload.js. Undefined when opened as a plain web page. */
    electronAPI?: ElectronAPI;
  }
}
