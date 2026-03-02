import { NavLink, useParams } from 'react-router-dom'
import { Home, Users, User, Settings } from 'lucide-react'

export function BottomNav() {
  const { id: groupId } = useParams()

  const items = [
    { to: '/', icon: Home, label: 'ホーム' },
    { to: '/groups', icon: Users, label: 'グループ' },
    { to: groupId ? `/players/me` : '/players/me', icon: User, label: 'マイページ' },
    { to: '/settings', icon: Settings, label: '設定' },
  ]

  return (
    <nav className="fixed bottom-0 left-0 right-0 z-50 flex bg-white border-t border-border h-16 safe-area-pb md:hidden">
      {items.map(({ to, icon: Icon, label }) => (
        <NavLink
          key={to}
          to={to}
          end={to === '/'}
          className={({ isActive }) =>
            `flex flex-1 flex-col items-center justify-center gap-0.5 text-xs transition-colors ${
              isActive
                ? 'text-primary font-medium'
                : 'text-muted-foreground hover:text-foreground'
            }`
          }
        >
          <Icon size={20} />
          <span>{label}</span>
        </NavLink>
      ))}
    </nav>
  )
}
