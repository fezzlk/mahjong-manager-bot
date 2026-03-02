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
  Legend,
  BarChart,
  Bar,
  ResponsiveContainer,
} from 'recharts'
import api from '@/lib/api'
import type { GroupStats } from '@/types'

const COLORS = ['#3b82f6', '#f59e0b', '#10b981', '#ef4444', '#8b5cf6', '#ec4899']

export function StatsPage() {
  const { id } = useParams<{ id: string }>()

  const { data: stats, isLoading } = useQuery({
    queryKey: ['groups', id, 'stats'],
    queryFn: () => api.get<GroupStats>(`/groups/${id}/stats`).then((r) => r.data),
  })

  if (isLoading) {
    return (
      <div className="flex justify-center py-20">
        <Loader2 className="animate-spin text-muted-foreground" size={24} />
      </div>
    )
  }

  const playerNames = stats?.point_history.length
    ? Array.from(
        new Set(
          stats.point_history.flatMap((row) =>
            Object.keys(row).filter((k) => k !== 'date'),
          ),
        ),
      )
    : []

  return (
    <div className="px-4 py-6 max-w-2xl mx-auto">
      <h1 className="text-2xl font-bold mb-6">グループ統計</h1>

      {stats?.point_history && stats.point_history.length > 0 && (
        <section className="mb-8">
          <h2 className="text-base font-semibold mb-4">ポイント推移</h2>
          <div className="bg-white rounded-xl border border-border p-4">
            <ResponsiveContainer width="100%" height={280}>
              <LineChart data={stats.point_history} margin={{ top: 5, right: 10, left: -20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                <XAxis dataKey="date" tick={{ fontSize: 11 }} tickLine={false} />
                <YAxis tick={{ fontSize: 11 }} tickLine={false} axisLine={false} />
                <Tooltip
                  contentStyle={{
                    borderRadius: '8px',
                    border: '1px solid #e2e8f0',
                    fontSize: '12px',
                  }}
                />
                <Legend wrapperStyle={{ fontSize: '12px' }} />
                {playerNames.map((name, i) => (
                  <Line
                    key={name}
                    type="monotone"
                    dataKey={name}
                    stroke={COLORS[i % COLORS.length]}
                    strokeWidth={2}
                    dot={false}
                    activeDot={{ r: 4 }}
                  />
                ))}
              </LineChart>
            </ResponsiveContainer>
          </div>
        </section>
      )}

      {stats?.rank_distribution && stats.rank_distribution.length > 0 && (
        <section>
          <h2 className="text-base font-semibold mb-4">着順分布</h2>
          <div className="bg-white rounded-xl border border-border p-4">
            <ResponsiveContainer width="100%" height={240}>
              <BarChart data={stats.rank_distribution} margin={{ top: 5, right: 10, left: -20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                <XAxis dataKey="user_name" tick={{ fontSize: 11 }} tickLine={false} />
                <YAxis tick={{ fontSize: 11 }} tickLine={false} axisLine={false} />
                <Tooltip
                  contentStyle={{
                    borderRadius: '8px',
                    border: '1px solid #e2e8f0',
                    fontSize: '12px',
                  }}
                />
                <Legend wrapperStyle={{ fontSize: '12px' }} />
                <Bar dataKey="first" name="1位" stackId="a" fill="#f59e0b" />
                <Bar dataKey="second" name="2位" stackId="a" fill="#3b82f6" />
                <Bar dataKey="third" name="3位" stackId="a" fill="#10b981" />
                <Bar dataKey="fourth" name="4位" stackId="a" fill="#ef4444" radius={[2, 2, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </section>
      )}
    </div>
  )
}
