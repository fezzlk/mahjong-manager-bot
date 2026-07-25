import { useEffect, useState } from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { Loader2 } from 'lucide-react'
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
import { TermsOfServicePage } from '@/pages/TermsOfServicePage'
import { setToken } from '@/lib/auth'
import api from '@/lib/api'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5,
      retry: 1,
    },
  },
})

function App() {
  // LINE Login コールバック直後、一度だけ httpOnly Cookie に橋渡しされた JWT を
  // 受け取る。ProtectedRoute の認証判定より先に完了させる必要があるため、
  // Routes のレンダリングをこの処理の完了までブロックする。
  const [bootstrapped, setBootstrapped] = useState(false)

  useEffect(() => {
    api.get<{ access_token: string }>('/auth/exchange')
      .then((res) => {
        if (res.status === 200 && res.data.access_token) {
          setToken(res.data.access_token)
        }
      })
      .catch(() => {
        // ネットワークエラー等: 未認証のまま続行
      })
      .finally(() => setBootstrapped(true))
  }, [])

  if (!bootstrapped) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <Loader2 className="animate-spin text-muted-foreground" size={24} />
      </div>
    )
  }

  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/privacy" element={<PrivacyPolicyPage />} />
          <Route path="/terms" element={<TermsOfServicePage />} />

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
