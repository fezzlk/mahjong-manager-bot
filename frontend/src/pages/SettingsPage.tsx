import { useQuery } from '@tanstack/react-query'
import { Link2, LogOut, User } from 'lucide-react'
import api from '@/lib/api'
import { useAuth } from '@/hooks/useAuth'
import type { WebUser } from '@/types'

export function SettingsPage() {
  const { logout } = useAuth()

  const { data: user } = useQuery({
    queryKey: ['me'],
    queryFn: () => api.get<WebUser>('/me').then((r) => r.data),
  })

  return (
    <div className="px-4 py-6 max-w-2xl mx-auto">
      <h1 className="text-2xl font-bold mb-6">設定</h1>

      {/* プロフィール */}
      <section className="mb-6">
        <h2 className="text-sm font-semibold text-muted-foreground mb-2 uppercase tracking-wide">
          アカウント
        </h2>
        <div className="bg-white rounded-xl border border-border divide-y divide-border">
          <div className="flex items-center gap-4 px-4 py-4">
            <div className="w-12 h-12 rounded-full bg-primary/20 flex items-center justify-center text-primary font-bold text-xl flex-shrink-0">
              {user?.name.charAt(0)}
            </div>
            <div>
              <p className="font-medium">{user?.name}</p>
              <p className="text-sm text-muted-foreground">{user?.email}</p>
            </div>
          </div>
          <div className="flex items-center justify-between px-4 py-4">
            <div className="flex items-center gap-3">
              <User size={18} className="text-muted-foreground" />
              <span className="text-sm">プロフィール編集</span>
            </div>
            <span className="text-xs text-muted-foreground">準備中</span>
          </div>
        </div>
      </section>

      {/* LINE 連携 */}
      <section className="mb-6">
        <h2 className="text-sm font-semibold text-muted-foreground mb-2 uppercase tracking-wide">
          連携
        </h2>
        <div className="bg-white rounded-xl border border-border divide-y divide-border">
          <div className="flex items-center justify-between px-4 py-4">
            <div className="flex items-center gap-3">
              <Link2 size={18} className="text-muted-foreground" />
              <div>
                <p className="text-sm font-medium">LINE 連携</p>
                {user?.line_user_id ? (
                  <p className="text-xs text-green-600">連携済み</p>
                ) : (
                  <p className="text-xs text-muted-foreground">未連携 — グループデータを見るには LINE 連携が必要です</p>
                )}
              </div>
            </div>
            {!user?.line_user_id && (
              <button className="text-xs text-primary font-medium">連携する</button>
            )}
          </div>
        </div>
      </section>

      {/* ログアウト */}
      <section>
        <div className="bg-white rounded-xl border border-border">
          <button
            onClick={logout}
            className="flex items-center gap-3 w-full px-4 py-4 text-red-500 hover:bg-red-50 rounded-xl transition-colors"
          >
            <LogOut size={18} />
            <span className="text-sm font-medium">ログアウト</span>
          </button>
        </div>
      </section>
    </div>
  )
}
