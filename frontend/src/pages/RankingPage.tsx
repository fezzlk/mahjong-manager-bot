import { useQuery } from '@tanstack/react-query'
import { useParams } from 'react-router-dom'
import { Trophy, Loader2 } from 'lucide-react'
import api from '@/lib/api'
import type { RankingEntry } from '@/types'

export function RankingPage() {
  const { id } = useParams<{ id: string }>()

  const { data: ranking, isLoading } = useQuery({
    queryKey: ['groups', id, 'ranking'],
    queryFn: () => api.get<RankingEntry[]>(`/groups/${id}/ranking`).then((r) => r.data),
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
      <h1 className="text-2xl font-bold mb-6 flex items-center gap-2">
        <Trophy size={24} className="text-amber-500" />
        ランキング
      </h1>

      <div className="bg-white rounded-xl border border-border overflow-hidden">
        <table className="w-full text-sm">
          <thead>
            <tr className="bg-muted/50 text-muted-foreground">
              <th className="px-4 py-3 text-left font-medium w-10">#</th>
              <th className="px-4 py-3 text-left font-medium">プレイヤー</th>
              <th className="px-4 py-3 text-right font-medium">合計pt</th>
              <th className="px-4 py-3 text-right font-medium hidden sm:table-cell">局数</th>
              <th className="px-4 py-3 text-right font-medium hidden sm:table-cell">平均順位</th>
            </tr>
          </thead>
          <tbody>
            {ranking?.map((entry) => (
              <tr key={entry.user_id} className="border-t border-border hover:bg-muted/30">
                <td className="px-4 py-3">
                  <span
                    className={`w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold ${
                      entry.rank === 1
                        ? 'bg-amber-100 text-amber-600'
                        : entry.rank === 2
                        ? 'bg-slate-100 text-slate-600'
                        : entry.rank === 3
                        ? 'bg-orange-100 text-orange-600'
                        : 'bg-transparent text-muted-foreground'
                    }`}
                  >
                    {entry.rank}
                  </span>
                </td>
                <td className="px-4 py-3">
                  <div>
                    <p className="font-medium">{entry.user_name}</p>
                    <p className="text-xs text-muted-foreground sm:hidden">
                      {entry.hanchan_count}局 / 平均{entry.average_rank.toFixed(2)}位
                    </p>
                  </div>
                </td>
                <td className="px-4 py-3 text-right">
                  <span
                    className={`font-semibold ${
                      entry.total_point >= 0 ? 'text-blue-600' : 'text-red-500'
                    }`}
                  >
                    {entry.total_point >= 0 ? '+' : ''}{entry.total_point.toFixed(1)}
                  </span>
                </td>
                <td className="px-4 py-3 text-right text-muted-foreground hidden sm:table-cell">
                  {entry.hanchan_count}
                </td>
                <td className="px-4 py-3 text-right text-muted-foreground hidden sm:table-cell">
                  {entry.average_rank.toFixed(2)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* 着順分布 */}
      {ranking && ranking.length > 0 && (
        <section className="mt-6">
          <h2 className="text-base font-semibold mb-3">着順分布</h2>
          <div className="space-y-3">
            {ranking.map((entry) => (
              <div key={entry.user_id} className="bg-white rounded-xl border border-border p-4">
                <p className="text-sm font-medium mb-2">{entry.user_name}</p>
                <div className="flex h-5 rounded overflow-hidden">
                  {[
                    { count: entry.first_count, color: 'bg-amber-400' },
                    { count: entry.second_count, color: 'bg-blue-400' },
                    { count: entry.third_count, color: 'bg-green-400' },
                    { count: entry.fourth_count, color: 'bg-red-400' },
                  ].map(({ count, color }, i) => {
                    const pct = entry.hanchan_count > 0 ? (count / entry.hanchan_count) * 100 : 0
                    return pct > 0 ? (
                      <div
                        key={i}
                        className={`${color} h-full`}
                        style={{ width: `${pct}%` }}
                        title={`${['1位', '2位', '3位', '4位'][i]}: ${count}回`}
                      />
                    ) : null
                  })}
                </div>
                <div className="flex gap-3 mt-1 text-xs text-muted-foreground">
                  <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-sm bg-amber-400 inline-block" />1位: {entry.first_count}</span>
                  <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-sm bg-blue-400 inline-block" />2位: {entry.second_count}</span>
                  <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-sm bg-green-400 inline-block" />3位: {entry.third_count}</span>
                  <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-sm bg-red-400 inline-block" />4位: {entry.fourth_count}</span>
                </div>
              </div>
            ))}
          </div>
        </section>
      )}
    </div>
  )
}
