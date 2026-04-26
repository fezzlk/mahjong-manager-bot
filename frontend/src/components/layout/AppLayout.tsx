import { Outlet, NavLink } from 'react-router-dom'
import { Home, Users, User, Settings, LogOut, Layers } from 'lucide-react'
import { BottomNav } from './BottomNav'
import { useAuth } from '@/hooks/useAuth'

export function AppLayout() {
  const { user, logout } = useAuth()

  const sidebarItems = [
    { to: '/', icon: Home, label: 'ダッシュボード' },
    { to: '/groups', icon: Users, label: 'グループ' },
    { to: '/players/me', icon: User, label: 'マイページ' },
    { to: '/settings', icon: Settings, label: '設定' },
  ]

  return (
    <div className="flex min-h-screen bg-background">
      {/* PC: サイドバー */}
      <aside className="hidden md:flex md:w-64 md:flex-col md:fixed md:inset-y-0 bg-white border-r border-border">
        <div className="flex items-center gap-2 px-6 py-5 border-b border-border">
          <Layers size={24} className="text-primary" />
          <span className="font-bold text-lg">麻雀マネージャー</span>
        </div>
        <nav className="flex-1 px-4 py-4 space-y-1">
          {sidebarItems.map(({ to, icon: Icon, label }) => (
            <NavLink
              key={to}
              to={to}
              end={to === '/'}
              className={({ isActive }) =>
                `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm transition-colors ${
                  isActive
                    ? 'bg-primary/10 text-primary font-medium'
                    : 'text-muted-foreground hover:bg-accent hover:text-foreground'
                }`
              }
            >
              <Icon size={18} />
              {label}
            </NavLink>
          ))}
        </nav>
        {user && (
          <div className="px-4 py-4 border-t border-border">
            <div className="flex items-center gap-3 px-3 py-2">
              <div className="w-8 h-8 rounded-full bg-primary/20 flex items-center justify-center text-primary font-medium text-sm">
                {user.name.charAt(0)}
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium truncate">{user.name}</p>
                <p className="text-xs text-muted-foreground truncate">{user.email}</p>
              </div>
            </div>
            <button
              onClick={logout}
              className="mt-2 flex items-center gap-2 w-full px-3 py-2 text-sm text-muted-foreground hover:text-foreground hover:bg-accent rounded-lg transition-colors"
            >
              <LogOut size={16} />
              ログアウト
            </button>
          </div>
        )}
      </aside>

      {/* メインコンテンツ */}
      <main className="flex-1 md:ml-64 pb-16 md:pb-0">
        <Outlet />
      </main>

      {/* スマホ: ボトムナビ */}
      <BottomNav />
    </div>
  )
}
