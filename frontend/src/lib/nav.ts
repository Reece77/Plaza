// The in-game screens: the left navigation, the 1-9 hotkeys and the command palette all read
// this list (TST's nav.ts pattern). PL-M0 has one in-game screen; each milestone adds its own.

export interface Screen {
  label: string;
  path: string; // under /game/<save>/; '' is the Overview
}

export const SCREENS: readonly Screen[] = [{ label: 'Overview', path: '' }];
