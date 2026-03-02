import { useQuery } from '@tanstack/react-query'
import { useParams } from 'react-router-dom'
import { Loader2 } from 'lucide-react'
import api from '@/lib/api'
import type { Match, Hanchan } from '@/types'

interface MatchDetail extends Match {
  hanchans: Hanchan[]
}

export function MatchDetailPage() {
  const { matchId } = useParams<{ id: string; matchId: string }>()

  const { data: match, isLoading } = useQuery({
    queryKey: ['matches', matchId],
    queryFn: () => api.get<MatchDetail>(`/matches/${matchId}`).then((r) => r.data),
  })

  if (isLoading) {
    return (
      <div className="flex justify-center py-20">
        <Loader2 className="animate-spin text-muted-foreground" size={24} />
      </div>
    )
  }

  return (
    <div className="px-4 py-6 max-w-2xl mx-auto">
      <h1 className="text-2xl font-bold mb-1">
        {match?.date ? formatDate(match.date) : '試合詳細'}
      </h1>
      <p className="text-muted-foreground text-sm mb-6">{match?.hanchan_count}半荘</p>

      <div className="space-y-4">
        {match?.hanchans.map((hanchan, idx) => (
          <div key={hanchan.id} className="bg-white rounded-xl border border-border overflow-hidden">
            <div className="px-4 py-2 bg-muted/50 border-b border-border">
              <p className="text-sm font-medium text-muted-foreground">{idx + 1}半荘目</p>
            </div>
            <table className="w-full text-sm">
              <thead>
                <tr className="text-muted-foreground border-b border-border">
                  <th className="px-4 py-2 text-left font-medium">順位</th>
                  <th className="px-4 py-2 text-left font-medium">プレイヤー</th>
                  <th className="px-4 py-2 text-right font-medium">素点</th>
                  <th className="px-4 py-2 text-right font-medium">ポイント</th>
                </tr>
              </thead>
              <tbody>
                {hanchan.scores
                  .sort((a, b) => a.rank - b.rank)
                  .map((score) => (
                    <tr key={score.user_id} className="border-t border-border">
                      <td className="px-4 py-3">
                        <span
                          className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold ${
                            score.rank === 1
                              ? 'bg-amber-100 text-amber-600'
                              : score.rank === 2
                              ? 'bg-slate-100 text-slate-600'
                              : score.rank === 3
                              ? 'bg-green-100 text-green-600'
                              : 'bg-red-50 text-red-400'
                          }`}
                        >
                          {score.rank}
                        </span>
                      </td>
                      <td className="px-4 py-3 font-medium">{score.user_name}</td>
                      <td className="px-4 py-3 text-right text-muted-foreground">
                        {score.score.toLocaleString()}
                      </td>
                      <td className="px-4 py-3 text-right">
                        <span
                          className={`font-semibold ${
                            score.point >= 0 ? 'text-blue-600' : 'text-red-500'
                          }`}
                        >
                          {score.point >= 0 ? '+' : ''}{score.point.toFixed(1)}
                        </span>
                      </td>
                    </tr>
                  ))}
              </tbody>
            </table>
          </div>
        ))}
      </div>
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
