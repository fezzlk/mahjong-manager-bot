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

  const handleGoogleLogin = () => {
    window.location.href = '/auth/google/login'
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
            onClick={handleGoogleLogin}
            className="w-full flex items-center justify-center gap-3 px-4 py-3 border border-border rounded-lg hover:bg-accent transition-colors font-medium text-foreground"
          >
            <GoogleIcon />
            Google でログイン
          </button>

          <p className="mt-6 text-center text-xs text-muted-foreground">
            ログインすると、LINE と連携してグループの成績データを閲覧・管理できます。
          </p>
        </div>
      </div>
    </div>
  )
}

function GoogleIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 18 18" xmlns="http://www.w3.org/2000/svg">
      <g fill="none" fillRule="evenodd">
        <path
          d="M17.64 9.205c0-.639-.057-1.252-.164-1.841H9v3.481h4.844a4.14 4.14 0 0 1-1.796 2.716v2.259h2.908c1.702-1.567 2.684-3.875 2.684-6.615z"
          fill="#4285F4"
        />
        <path
          d="M9 18c2.43 0 4.467-.806 5.956-2.18l-2.908-2.259c-.806.54-1.837.86-3.048.86-2.344 0-4.328-1.584-5.036-3.711H.957v2.332A8.997 8.997 0 0 0 9 18z"
          fill="#34A853"
        />
        <path
          d="M3.964 10.71A5.41 5.41 0 0 1 3.682 9c0-.593.102-1.17.282-1.71V4.958H.957A8.996 8.996 0 0 0 0 9c0 1.452.348 2.827.957 4.042l3.007-2.332z"
          fill="#FBBC05"
        />
        <path
          d="M9 3.58c1.321 0 2.508.454 3.44 1.345l2.582-2.58C13.463.891 11.426 0 9 0A8.997 8.997 0 0 0 .957 4.958L3.964 7.29C4.672 5.163 6.656 3.58 9 3.58z"
          fill="#EA4335"
        />
      </g>
    </svg>
  )
}
