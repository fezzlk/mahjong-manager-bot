import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { useParams } from 'react-router-dom'
import { Loader2, Pencil, Trash2 } from 'lucide-react'
import api from '@/lib/api'
import { useAuth } from '@/hooks/useAuth'
import type { Match, Hanchan } from '@/types'

interface MatchDetail extends Match {
  hanchans: Hanchan[]
}

interface EditScoresState {
  hanchanId: string
  scores: Record<string, number>
  userNames: Record<string, string>
}

interface EditChipsState {
  scores: Record<string, number>
  userNames: Record<string, string>
}

export function MatchDetailPage() {
  const { matchId } = useParams<{ id: string; matchId: string }>()
  const queryClient = useQueryClient()
  const { user } = useAuth()

  const [editScores, setEditScores] = useState<EditScoresState | null>(null)
  const [editChips, setEditChips] = useState<EditChipsState | null>(null)
  const [deleteHanchanId, setDeleteHanchanId] = useState<string | null>(null)
  const [deleteMatchConfirm, setDeleteMatchConfirm] = useState(false)
  const [errorMsg, setErrorMsg] = useState<string | null>(null)

  const { data: match, isLoading } = useQuery({
    queryKey: ['matches', matchId],
    queryFn: () => api.get<MatchDetail>(`/matches/${matchId}`).then((r) => r.data),
  })

  const invalidate = () => queryClient.invalidateQueries({ queryKey: ['matches', matchId] })

  const deleteHanchanMutation = useMutation({
    mutationFn: (hanchanId: string) => api.delete(`/hanchans/${hanchanId}`),
    onSuccess: () => { setDeleteHanchanId(null); invalidate() },
    onError: (e: unknown) => setErrorMsg(extractError(e) ?? '削除に失敗しました'),
  })

  const updateScoresMutation = useMutation({
    mutationFn: ({ hanchanId, raw_scores }: { hanchanId: string; raw_scores: Record<string, number> }) =>
      api.put(`/hanchans/${hanchanId}/scores`, { raw_scores }),
    onSuccess: () => { setEditScores(null); invalidate() },
    onError: (e: unknown) => setErrorMsg(extractError(e) ?? '更新に失敗しました'),
  })

  const deleteMatchMutation = useMutation({
    mutationFn: () => api.delete(`/matches/${matchId}`),
    onSuccess: () => { setDeleteMatchConfirm(false); window.history.back() },
    onError: (e: unknown) => setErrorMsg(extractError(e) ?? '削除に失敗しました'),
  })

  const updateChipsMutation = useMutation({
    mutationFn: (chip_scores: Record<string, number>) =>
      api.put(`/matches/${matchId}/chips`, { chip_scores }),
    onSuccess: () => { setEditChips(null); invalidate() },
    onError: (e: unknown) => setErrorMsg(extractError(e) ?? '更新に失敗しました'),
  })

  if (isLoading) {
    return (
      <div className="flex justify-center py-20">
        <Loader2 className="animate-spin text-muted-foreground" size={24} />
      </div>
    )
  }

  const chipParticipants = match ? Object.keys(match.chip_scores ?? {}) : []
  const hasChips = chipParticipants.length > 0

  return (
    <div className="px-4 py-6 max-w-2xl mx-auto">
      {/* ヘッダー */}
      <div className="flex items-start justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold mb-1">
            {match?.date ? formatDate(match.date) : '試合詳細'}
          </h1>
          <p className="text-muted-foreground text-sm">{match?.hanchan_count}半荘</p>
        </div>
        {user && (
          <button
            onClick={() => setDeleteMatchConfirm(true)}
            className="flex items-center gap-1 px-3 py-1.5 text-sm text-red-500 border border-red-200 rounded-lg hover:bg-red-50 transition-colors"
          >
            <Trash2 size={14} />
            対戦削除
          </button>
        )}
      </div>

      {/* エラー表示 */}
      {errorMsg && (
        <div className="mb-4 px-4 py-3 bg-red-50 border border-red-200 rounded-lg text-sm text-red-600">
          {errorMsg}
          <button className="ml-2 underline" onClick={() => setErrorMsg(null)}>閉じる</button>
        </div>
      )}

      {/* チップ */}
      {hasChips && (
        <div className="mb-4 bg-white rounded-xl border border-border overflow-hidden">
          <div className="px-4 py-2 bg-muted/50 border-b border-border flex items-center justify-between">
            <p className="text-sm font-medium text-muted-foreground">チップ</p>
            {user && (
              <button
                onClick={() => {
                  const names: Record<string, string> = {}
                  match?.hanchans.forEach((h) => h.scores.forEach((s) => { names[s.user_id] = s.user_name }))
                  setEditChips({ scores: { ...(match?.chip_scores ?? {}) }, userNames: names })
                }}
                className="text-muted-foreground hover:text-primary"
              >
                <Pencil size={14} />
              </button>
            )}
          </div>
          <div className="px-4 py-3 flex flex-wrap gap-3">
            {chipParticipants.map((uid) => {
              const name = match?.hanchans.flatMap((h) => h.scores).find((s) => s.user_id === uid)?.user_name ?? uid
              const count = match?.chip_scores?.[uid] ?? 0
              return (
                <span key={uid} className="text-sm">
                  <span className="font-medium">{name}</span>
                  <span className={`ml-1 font-semibold ${count >= 0 ? 'text-blue-600' : 'text-red-500'}`}>
                    {count >= 0 ? '+' : ''}{count}
                  </span>
                </span>
              )
            })}
          </div>
        </div>
      )}

      {/* 半荘一覧 */}
      <div className="space-y-4">
        {match?.hanchans.map((hanchan, idx) => (
          <div key={hanchan.id} className="bg-white rounded-xl border border-border overflow-hidden">
            <div className="px-4 py-2 bg-muted/50 border-b border-border flex items-center justify-between">
              <p className="text-sm font-medium text-muted-foreground">{idx + 1}半荘目</p>
              {user && (
                <div className="flex items-center gap-2">
                  <button
                    onClick={() => {
                      const names: Record<string, string> = {}
                      const scores: Record<string, number> = {}
                      hanchan.scores.forEach((s) => { names[s.user_id] = s.user_name; scores[s.user_id] = s.score })
                      setEditScores({ hanchanId: hanchan.id, scores, userNames: names })
                    }}
                    className="text-muted-foreground hover:text-primary"
                  >
                    <Pencil size={14} />
                  </button>
                  <button
                    onClick={() => setDeleteHanchanId(hanchan.id)}
                    className="text-muted-foreground hover:text-red-500"
                  >
                    <Trash2 size={14} />
                  </button>
                </div>
              )}
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

      {/* 素点修正モーダル */}
      {editScores && (
        <Modal title="素点修正" onClose={() => setEditScores(null)}>
          <div className="space-y-3">
            {Object.entries(editScores.scores).map(([uid, score]) => (
              <div key={uid} className="flex items-center gap-3">
                <label className="w-24 text-sm font-medium truncate">
                  {editScores.userNames[uid] ?? uid}
                </label>
                <input
                  type="number"
                  value={score}
                  onChange={(e) =>
                    setEditScores((prev) =>
                      prev ? { ...prev, scores: { ...prev.scores, [uid]: Number(e.target.value) } } : prev,
                    )
                  }
                  className="flex-1 px-3 py-2 border border-border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary"
                />
              </div>
            ))}
          </div>
          <div className="mt-4 flex gap-2 justify-end">
            <button
              onClick={() => setEditScores(null)}
              className="px-4 py-2 text-sm rounded-lg border border-border hover:bg-muted/50"
            >
              キャンセル
            </button>
            <button
              disabled={updateScoresMutation.isPending}
              onClick={() =>
                updateScoresMutation.mutate({
                  hanchanId: editScores.hanchanId,
                  raw_scores: editScores.scores,
                })
              }
              className="px-4 py-2 text-sm rounded-lg bg-primary text-white hover:bg-primary/90 disabled:opacity-50"
            >
              {updateScoresMutation.isPending ? '更新中...' : '更新'}
            </button>
          </div>
        </Modal>
      )}

      {/* チップ修正モーダル */}
      {editChips && (
        <Modal title="チップ修正" onClose={() => setEditChips(null)}>
          <div className="space-y-3">
            {Object.entries(editChips.scores).map(([uid, count]) => (
              <div key={uid} className="flex items-center gap-3">
                <label className="w-24 text-sm font-medium truncate">
                  {editChips.userNames[uid] ?? uid}
                </label>
                <input
                  type="number"
                  value={count}
                  onChange={(e) =>
                    setEditChips((prev) =>
                      prev ? { ...prev, scores: { ...prev.scores, [uid]: Number(e.target.value) } } : prev,
                    )
                  }
                  className="flex-1 px-3 py-2 border border-border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary"
                />
              </div>
            ))}
          </div>
          <div className="mt-4 flex gap-2 justify-end">
            <button
              onClick={() => setEditChips(null)}
              className="px-4 py-2 text-sm rounded-lg border border-border hover:bg-muted/50"
            >
              キャンセル
            </button>
            <button
              disabled={updateChipsMutation.isPending}
              onClick={() => updateChipsMutation.mutate(editChips.scores)}
              className="px-4 py-2 text-sm rounded-lg bg-primary text-white hover:bg-primary/90 disabled:opacity-50"
            >
              {updateChipsMutation.isPending ? '更新中...' : '更新'}
            </button>
          </div>
        </Modal>
      )}

      {/* 半荘削除確認 */}
      {deleteHanchanId && (
        <Modal title="半荘削除" onClose={() => setDeleteHanchanId(null)}>
          <p className="text-sm text-muted-foreground">この半荘を削除します。元に戻せません。</p>
          <div className="mt-4 flex gap-2 justify-end">
            <button
              onClick={() => setDeleteHanchanId(null)}
              className="px-4 py-2 text-sm rounded-lg border border-border hover:bg-muted/50"
            >
              キャンセル
            </button>
            <button
              disabled={deleteHanchanMutation.isPending}
              onClick={() => deleteHanchanMutation.mutate(deleteHanchanId)}
              className="px-4 py-2 text-sm rounded-lg bg-red-500 text-white hover:bg-red-600 disabled:opacity-50"
            >
              {deleteHanchanMutation.isPending ? '削除中...' : '削除'}
            </button>
          </div>
        </Modal>
      )}

      {/* 対戦削除確認 */}
      {deleteMatchConfirm && (
        <Modal title="対戦削除" onClose={() => setDeleteMatchConfirm(false)}>
          <p className="text-sm text-muted-foreground">
            この対戦とすべての半荘データを削除します。元に戻せません。
          </p>
          <div className="mt-4 flex gap-2 justify-end">
            <button
              onClick={() => setDeleteMatchConfirm(false)}
              className="px-4 py-2 text-sm rounded-lg border border-border hover:bg-muted/50"
            >
              キャンセル
            </button>
            <button
              disabled={deleteMatchMutation.isPending}
              onClick={() => deleteMatchMutation.mutate()}
              className="px-4 py-2 text-sm rounded-lg bg-red-500 text-white hover:bg-red-600 disabled:opacity-50"
            >
              {deleteMatchMutation.isPending ? '削除中...' : '削除'}
            </button>
          </div>
        </Modal>
      )}
    </div>
  )
}

function Modal({ title, onClose, children }: { title: string; onClose: () => void; children: React.ReactNode }) {
  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 px-4"
      onClick={onClose}
    >
      <div
        className="w-full max-w-sm bg-white rounded-2xl shadow-xl p-6"
        onClick={(e) => e.stopPropagation()}
      >
        <h2 className="text-base font-bold mb-4">{title}</h2>
        {children}
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

function extractError(e: unknown): string | null {
  return (e as { response?: { data?: { error?: string } } })?.response?.data?.error ?? null
}
