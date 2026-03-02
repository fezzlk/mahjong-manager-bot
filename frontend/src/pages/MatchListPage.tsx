import { useQuery } from '@tanstack/react-query'
import { Link, useParams } from 'react-router-dom'
import { CalendarDays, ChevronRight, Loader2 } from 'lucide-react'
import api from '@/lib/api'
import type { Match } from '@/types'

export function MatchListPage() {
  const { id } = useParams<{ id: string }>()

  const { data: matches, isLoading } = useQuery({
    queryKey: ['groups', id, 'matches'],
    queryFn: () => api.get<Match[]>(`/groups/${id}/matches`).then((r) => r.data),
  })

  return (
    <div className="px-4 py-6 max-w-2xl mx-auto">
      <h1 className="text-2xl font-bold mb-6 flex items-center gap-2">
        <CalendarDays size={24} />
        対局履歴
      </h1>

      {isLoading && (
        <div className="flex justify-center py-12">
          <Loader2 className="animate-spin text-muted-foreground" size={24} />
        </div>
      )}

      <div className="space-y-3">
        {matches?.map((match) => (
          <Link
            key={match.id}
            to={`/groups/${id}/matches/${match.id}`}
            className="flex items-center justify-between p-4 bg-white rounded-xl border border-border hover:border-primary/50 hover:shadow-sm transition-all"
          >
            <div>
              <p className="font-medium">{formatDate(match.date)}</p>
              <p className="text-sm text-muted-foreground">{match.hanchan_count}半荘</p>
            </div>
            <ChevronRight size={18} className="text-muted-foreground" />
          </Link>
        ))}
      </div>

      {matches?.length === 0 && !isLoading && (
        <div className="text-center py-12 text-muted-foreground">
          <p>対局履歴がありません。</p>
        </div>
      )}
    </div>
  )
}

function formatDate(dateStr: string): string {
  const d = new Date(dateStr)
  return d.toLocaleDateString('ja-JP', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    weekday: 'short',
  })
}
