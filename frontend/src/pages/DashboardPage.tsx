import { useQuery } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import { Users, ChevronRight, Loader2 } from 'lucide-react'
import api from '@/lib/api'
import type { Group } from '@/types'

export function DashboardPage() {
  const { data: groups, isLoading } = useQuery({
    queryKey: ['groups'],
    queryFn: () => api.get<Group[]>('/groups').then((r) => r.data),
  })

  return (
    <div className="px-4 py-6 max-w-2xl mx-auto">
      <h1 className="text-2xl font-bold mb-6">ダッシュボード</h1>

      <section>
        <h2 className="text-base font-semibold text-muted-foreground mb-3 flex items-center gap-2">
          <Users size={16} />
          参加中のグループ
        </h2>

        {isLoading && (
          <div className="flex justify-center py-12">
            <Loader2 className="animate-spin text-muted-foreground" size={24} />
          </div>
        )}

        {groups?.length === 0 && (
          <div className="text-center py-12 text-muted-foreground">
            <p>参加中のグループはありません。</p>
            <p className="text-sm mt-1">LINE Bot からグループに参加してください。</p>
          </div>
        )}

        <div className="space-y-3">
          {groups?.map((group) => (
            <Link
              key={group.id}
              to={`/groups/${group.id}`}
              className="flex items-center justify-between p-4 bg-white rounded-xl border border-border hover:border-primary/50 hover:shadow-sm transition-all"
            >
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center text-primary font-bold">
                  {group.name.charAt(0)}
                </div>
                <div>
                  <p className="font-medium">{group.name}</p>
                  {group.member_count !== undefined && (
                    <p className="text-sm text-muted-foreground">
                      {group.member_count} 人のメンバー
                    </p>
                  )}
                </div>
              </div>
              <ChevronRight size={18} className="text-muted-foreground" />
            </Link>
          ))}
        </div>
      </section>
    </div>
  )
}
