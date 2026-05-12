import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { AppLayout } from '@/components/layout/AppLayout'
import { ProtectedRoute } from '@/components/ProtectedRoute'
import { LoginPage } from '@/pages/LoginPage'
import { DashboardPage } from '@/pages/DashboardPage'
import { GroupListPage } from '@/pages/GroupListPage'
import { GroupDetailPage } from '@/pages/GroupDetailPage'
import { MatchListPage } from '@/pages/MatchListPage'
import { MatchDetailPage } from '@/pages/MatchDetailPage'
import { RankingPage } from '@/pages/RankingPage'
import { StatsPage } from '@/pages/StatsPage'
import { PlayerPage } from '@/pages/PlayerPage'
import { SettingsPage } from '@/pages/SettingsPage'
import { PrivacyPolicyPage } from '@/pages/PrivacyPolicyPage'
import { RegisterPage } from '@/pages/RegisterPage'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5,
      retry: 1,
    },
  },
})

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/privacy" element={<PrivacyPolicyPage />} />

          <Route
            element={
              <ProtectedRoute>
                <AppLayout />
              </ProtectedRoute>
            }
          >
            <Route index element={<DashboardPage />} />
            <Route path="/groups" element={<GroupListPage />} />
            <Route path="/groups/:id" element={<GroupDetailPage />} />
            <Route path="/groups/:id/matches" element={<MatchListPage />} />
            <Route path="/groups/:id/matches/:matchId" element={<MatchDetailPage />} />
            <Route path="/groups/:id/ranking" element={<RankingPage />} />
            <Route path="/groups/:id/stats" element={<StatsPage />} />
            <Route path="/players/:id" element={<PlayerPage />} />
            <Route path="/settings" element={<SettingsPage />} />
          </Route>

          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  )
}

export default App
