import { useEffect } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { Layers } from 'lucide-react'
import { isAuthenticated, setToken } from '@/lib/auth'

export function LoginPage() {
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()

  useEffect(() => {
    // OAuth コールバック後のトークン受け取り
    const token = searchParams.get('token')
    if (token) {
      setToken(token)
      navigate('/', { replace: true })
      return
    }

    if (isAuthenticated()) {
      navigate('/', { replace: true })
    }
  }, [navigate, searchParams])

  const handleLineLogin = () => {
    window.location.href = '/auth/line/login'
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 px-4">
      <div className="w-full max-w-md">
        <div className="bg-white rounded-2xl shadow-lg p-8">
          <div className="flex flex-col items-center mb-8">
            <div className="w-16 h-16 rounded-2xl bg-primary flex items-center justify-center mb-4">
              <Layers size={32} className="text-white" />
            </div>
            <h1 className="text-2xl font-bold text-foreground">麻雀マネージャー</h1>
            <p className="text-muted-foreground text-sm mt-1">成績・ランキング管理アプリ</p>
          </div>

          <button
            onClick={handleLineLogin}
            className="w-full flex items-center justify-center gap-3 px-4 py-3 rounded-lg transition-colors font-medium text-white"
            style={{ backgroundColor: '#06C755' }}
          >
            <LineIcon />
            LINE でログイン
          </button>

          <p className="mt-6 text-center text-xs text-muted-foreground">
            ログインすると、LINE と連携してグループの成績データを閲覧・管理できます。
          </p>
        </div>
      </div>
    </div>
  )
}

function LineIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="white" xmlns="http://www.w3.org/2000/svg">
      <path d="M24 10.304c0-5.369-5.383-9.738-12-9.738-6.616 0-12 4.369-12 9.738 0 4.814 4.270 8.846 10.036 9.608.391.084.923.258 1.058.592.121.303.079.778.039 1.084 0 0-.141.846-.171 1.027-.053.303-.242 1.188 1.040.648 1.283-.54 6.922-4.077 9.442-6.980C23.218 13.84 24 12.195 24 10.304z" />
    </svg>
  )
}
