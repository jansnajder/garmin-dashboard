import { QueryClientProvider } from '@tanstack/react-query';
import { BrowserRouter, Route, Routes } from 'react-router-dom';

import { queryClient } from './api/queryClient';
import { AuthGate } from './auth/AuthGate';
import { Layout } from './components/layout/Layout';
import { routes } from './routes';
import { ThemeProvider } from './theme/ThemeContext';

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider>
        <BrowserRouter>
          <AuthGate>
            <Routes>
              <Route element={<Layout />}>
                {routes.map((r) => (
                  <Route key={r.path} path={r.path} element={r.element} />
                ))}
              </Route>
            </Routes>
          </AuthGate>
        </BrowserRouter>
      </ThemeProvider>
    </QueryClientProvider>
  );
}

export default App;
