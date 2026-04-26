import { useQuery } from '@tanstack/react-query'
import { Link, useParams } from 'react-router-dom'
import { Trophy, History, BarChart2, Loader2, ChevronRight } from 'lucide-react'
import api from '@/lib/api'
import type { Group, RankingEntry } from '@/types'

export function GroupDetailPage() {
  const { id } = useParams<{ id: string }>()

  const { data: group, isLoading: groupLoading } = useQuery({
    queryKey: ['groups', id],
    queryFn: () => api.get<Group>(`/groups/${id}`).then((r) => r.data),
  })

  const { data: ranking, isLoading: rankingLoading } = useQuery({
    queryKey: ['groups', id, 'ranking'],
    queryFn: () => api.get<RankingEntry[]>(`/groups/${id}/ranking`).then((r) => r.data),
  })

  const isLoading = groupLoading || rankingLoading

  if (isLoading) {
    return (
      <div className="flex justify-center py-20">
        <Loader2 className="animate-spin text-muted-foreground" size={24} />
      </div>
    )
  }

  return (
    <div className="px-4 py-6 max-w-2xl mx-auto">
      <h1 className="text-2xl font-bold mb-1">{group?.name}</h1>
      {group?.description && (
        <p className="text-muted-foreground text-sm mb-6">{group.description}</p>
      )}

      {/* ナビゲーションカード */}
      <div className="grid grid-cols-3 gap-3 mb-8">
        <Link
          to={`/groups/${id}/ranking`}
          className="flex flex-col items-center gap-2 p-4 bg-white rounded-xl border border-border hover:border-primary/50 hover:shadow-sm transition-all"
        >
          <Trophy size={22} className="text-primary" />
          <span className="text-xs font-medium">ランキング</span>
        </Link>
        <Link
          to={`/groups/${id}/matches`}
          className="flex flex-col items-center gap-2 p-4 bg-white rounded-xl border border-border hover:border-primary/50 hover:shadow-sm transition-all"
        >
          <History size={22} className="text-primary" />
          <span className="text-xs font-medium">対局履歴</span>
        </Link>
        <Link
          to={`/groups/${id}/stats`}
          className="flex flex-col items-center gap-2 p-4 bg-white rounded-xl border border-border hover:border-primary/50 hover:shadow-sm transition-all"
        >
          <BarChart2 size={22} className="text-primary" />
          <span className="text-xs font-medium">統計</span>
        </Link>
      </div>

      {/* ランキングプレビュー */}
      <section>
        <div className="flex items-center justify-between mb-3">
          <h2 className="text-base font-semibold flex items-center gap-2">
            <Trophy size={16} className="text-amber-500" />
            ランキング
          </h2>
          <Link
            to={`/groups/${id}/ranking`}
            className="text-sm text-primary flex items-center gap-1"
          >
            すべて見る <ChevronRight size={14} />
          </Link>
        </div>

        <div className="bg-white rounded-xl border border-border overflow-hidden">
          {ranking?.slice(0, 5).map((entry) => (
            <div
              key={entry.user_id}
              className="flex items-center px-4 py-3 border-b border-border last:border-b-0"
            >
              <span
                className={`w-7 h-7 rounded-full flex items-center justify-center text-sm font-bold mr-3 flex-shrink-0 ${
                  entry.rank === 1
                    ? 'bg-amber-100 text-amber-600'
                    : entry.rank === 2
                    ? 'bg-slate-100 text-slate-600'
                    : entry.rank === 3
                    ? 'bg-orange-100 text-orange-600'
                    : 'bg-muted text-muted-foreground'
                }`}
              >
                {entry.rank}
              </span>
              <div className="flex-1 min-w-0">
                <p className="font-medium truncate">{entry.user_name}</p>
                <p className="text-xs text-muted-foreground">
                  {entry.hanchan_count}局 / 平均{entry.average_rank.toFixed(2)}位
                </p>
              </div>
              <span
                className={`text-sm font-semibold ml-2 ${
                  entry.total_point >= 0 ? 'text-blue-600' : 'text-red-500'
                }`}
              >
                {entry.total_point >= 0 ? '+' : ''}{entry.total_point.toFixed(1)}pt
              </span>
            </div>
          ))}
        </div>
      </section>
    </div>
  )
}
