import { BrowserRouter, Route, Routes } from 'react-router';
import { GameLayout } from './screens/GameLayout';
import { MainMenu } from './screens/MainMenu';
import { NewGameScreen } from './screens/NewGameScreen';
import { OverviewScreen } from './screens/OverviewScreen';
import { SavesScreen } from './screens/SavesScreen';
import { SettingsScreen } from './screens/SettingsScreen';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<MainMenu />} />
        <Route path="/new" element={<NewGameScreen />} />
        <Route path="/saves" element={<SavesScreen />} />
        <Route path="/settings" element={<SettingsScreen />} />
        <Route path="/game/:slug" element={<GameLayout />}>
          <Route index element={<OverviewScreen />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
