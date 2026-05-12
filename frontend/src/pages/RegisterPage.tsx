import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Layers } from 'lucide-react'
import { setToken } from '@/lib/auth'
import api from '@/lib/api'

export function RegisterPage() {
  const navigate = useNavigate()
  const [name, setName] = useState('')
  const [loading, setLoading] = useState(true)
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    api.get<{ line_user_id: string; name: string }>('/register-info')
      .then((res) => {
        setName(res.data.name)
        setLoading(false)
      })
      .catch(() => {
        // セッション切れ or 登録フローを経ていない場合はログインへ
        navigate('/login', { replace: true })
      })
  }, [navigate])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!name.trim()) {
      setError('名前を入力してください')
      return
    }
    setSubmitting(true)
    setError(null)
    try {
      const res = await api.post<{ access_token: string }>('/register', { name: name.trim() })
      setToken(res.data.access_token)
      navigate('/', { replace: true })
    } catch (err: unknown) {
      const msg = (err as { response?: { data?: { error?: string } } })?.response?.data?.error
      setError(msg ?? '登録に失敗しました。もう一度お試しください。')
      setSubmitting(false)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p className="text-muted-foreground">読み込み中...</p>
      </div>
    )
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 px-4">
      <div className="w-full max-w-md">
        <div className="bg-white rounded-2xl shadow-lg p-8">
          <div className="flex flex-col items-center mb-8">
            <div className="w-16 h-16 rounded-2xl bg-primary flex items-center justify-center mb-4">
              <Layers size={32} className="text-white" />
            </div>
            <h1 className="text-2xl font-bold text-foreground">アカウント登録</h1>
            <p className="text-muted-foreground text-sm mt-1">麻雀マネージャーへようこそ</p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label htmlFor="name" className="block text-sm font-medium text-foreground mb-1">
                表示名
              </label>
              <input
                id="name"
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="LINE の表示名"
                className="w-full px-3 py-2 border border-border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary"
                disabled={submitting}
              />
              <p className="text-xs text-muted-foreground mt-1">
                他のメンバーに表示される名前です。後から変更できます。
              </p>
            </div>

            {error && (
              <p className="text-sm text-red-500">{error}</p>
            )}

            <button
              type="submit"
              disabled={submitting}
              className="w-full py-3 rounded-lg font-medium text-white bg-primary hover:bg-primary/90 transition-colors disabled:opacity-50"
            >
              {submitting ? '登録中...' : '登録する'}
            </button>
          </form>
        </div>
      </div>
    </div>
  )
}
