import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { useParams } from 'react-router-dom'
import { Loader2 } from 'lucide-react'
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts'
import api from '@/lib/api'
import type { WebUser, UserStats, Group } from '@/types'

export function PlayerPage() {
  const { id } = useParams<{ id: string }>()
  const userId = id === 'me' ? 'me' : id
  const [selectedLineGroupId, setSelectedLineGroupId] = useState<string | null>(null)

  const { data: user, isLoading: userLoading } = useQuery({
    queryKey: ['users', userId],
    queryFn: () =>
      userId === 'me'
        ? api.get<WebUser>('/me').then((r) => r.data)
        : api.get<WebUser>(`/users/${userId}`).then((r) => r.data),
  })

  const { data: groups } = useQuery({
    queryKey: ['groups'],
    queryFn: () => api.get<Group[]>('/groups').then((r) => r.data),
    enabled: userId === 'me',
  })

  const statsUrl = selectedLineGroupId
    ? `/users/${userId}/stats?group_id=${selectedLineGroupId}`
    : `/users/${userId}/stats`

  const { data: stats, isLoading: statsLoading } = useQuery({
    queryKey: ['users', userId, 'stats', selectedLineGroupId],
    queryFn: () => api.get<UserStats>(statsUrl).then((r) => r.data),
    enabled: !!userId,
  })

  if (userLoading || statsLoading) {
    return (
      <div className="flex justify-center py-20">
        <Loader2 className="animate-spin text-muted-foreground" size={24} />
      </div>
    )
  }

  const dist = stats?.rank_distribution
  const total = dist ? dist.first + dist.second + dist.third + dist.fourth : 0

  return (
    <div className="px-4 py-6 max-w-2xl mx-auto">
      {/* ヘッダー */}
      <div className="flex items-center gap-4 mb-6">
        <div className="w-16 h-16 rounded-full bg-primary/20 flex items-center justify-center text-primary font-bold text-2xl">
          {user?.name.charAt(0)}
        </div>
        <div>
          <h1 className="text-xl font-bold">{user?.name}</h1>
          <p className="text-sm text-muted-foreground">{user?.email}</p>
        </div>
      </div>

      {/* グループセレクタ（2グループ以上のとき表示） */}
      {groups && groups.length >= 2 && (
        <div className="flex gap-2 mb-6 overflow-x-auto pb-1">
          <button
            onClick={() => setSelectedLineGroupId(null)}
            className={`shrink-0 px-3 py-1.5 rounded-full text-sm font-medium transition-colors ${
              selectedLineGroupId === null
                ? 'bg-primary text-primary-foreground'
                : 'bg-muted text-muted-foreground hover:bg-muted/80'
            }`}
          >
            全グループ
          </button>
          {groups.map((g) => (
            <button
              key={g.id}
              onClick={() => setSelectedLineGroupId(g.line_group_id)}
              className={`shrink-0 px-3 py-1.5 rounded-full text-sm font-medium transition-colors ${
                selectedLineGroupId === g.line_group_id
                  ? 'bg-primary text-primary-foreground'
                  : 'bg-muted text-muted-foreground hover:bg-muted/80'
              }`}
            >
              {g.name}
            </button>
          ))}
        </div>
      )}

      {/* サマリーカード */}
      {stats && (
        <div className="grid grid-cols-3 gap-3 mb-6">
          <div className="bg-white rounded-xl border border-border p-3 text-center">
            <p className="text-xs text-muted-foreground mb-1">総局数</p>
            <p className="text-xl font-bold">{stats.total_hanchan}</p>
          </div>
          <div className="bg-white rounded-xl border border-border p-3 text-center">
            <p className="text-xs text-muted-foreground mb-1">合計pt</p>
            <p className={`text-xl font-bold ${stats.total_point >= 0 ? 'text-blue-600' : 'text-red-500'}`}>
              {stats.total_point >= 0 ? '+' : ''}{stats.total_point.toFixed(1)}
            </p>
          </div>
          <div className="bg-white rounded-xl border border-border p-3 text-center">
            <p className="text-xs text-muted-foreground mb-1">平均順位</p>
            <p className="text-xl font-bold">{stats.average_rank.toFixed(2)}</p>
          </div>
        </div>
      )}

      {/* 着順分布 */}
      {dist && total > 0 && (
        <section className="mb-6">
          <h2 className="text-base font-semibold mb-3">着順分布</h2>
          <div className="bg-white rounded-xl border border-border p-4">
            <div className="flex h-6 rounded overflow-hidden mb-3">
              {[
                { count: dist.first, color: 'bg-amber-400', label: '1位' },
                { count: dist.second, color: 'bg-blue-400', label: '2位' },
                { count: dist.third, color: 'bg-green-400', label: '3位' },
                { count: dist.fourth, color: 'bg-red-400', label: '4位' },
              ].map(({ count, color }, i) => {
                const pct = total > 0 ? (count / total) * 100 : 0
                return pct > 0 ? (
                  <div key={i} className={`${color} h-full`} style={{ width: `${pct}%` }} />
                ) : null
              })}
            </div>
            <div className="flex gap-4 text-xs text-muted-foreground">
              <span className="flex items-center gap-1"><span className="w-2.5 h-2.5 rounded-sm bg-amber-400 inline-block" />1位: {dist.first}回 ({total > 0 ? ((dist.first / total) * 100).toFixed(0) : 0}%)</span>
              <span className="flex items-center gap-1"><span className="w-2.5 h-2.5 rounded-sm bg-blue-400 inline-block" />2位: {dist.second}回</span>
              <span className="flex items-center gap-1"><span className="w-2.5 h-2.5 rounded-sm bg-green-400 inline-block" />3位: {dist.third}回</span>
              <span className="flex items-center gap-1"><span className="w-2.5 h-2.5 rounded-sm bg-red-400 inline-block" />4位: {dist.fourth}回</span>
            </div>
          </div>
        </section>
      )}

      {/* ポイント推移グラフ */}
      {stats?.point_history && stats.point_history.length > 0 && (
        <section>
          <h2 className="text-base font-semibold mb-3">ポイント推移</h2>
          <div className="bg-white rounded-xl border border-border p-4">
            <ResponsiveContainer width="100%" height={200}>
              <LineChart data={stats.point_history} margin={{ top: 5, right: 10, left: -20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                <XAxis dataKey="date" tick={{ fontSize: 10 }} tickLine={false} />
                <YAxis tick={{ fontSize: 10 }} tickLine={false} axisLine={false} />
                <Tooltip
                  contentStyle={{ borderRadius: '8px', border: '1px solid #e2e8f0', fontSize: '12px' }}
                />
                <Line type="monotone" dataKey="point" stroke="#3b82f6" strokeWidth={2} dot={false} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </section>
      )}
    </div>
  )
}
