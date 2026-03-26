import { useEffect, useState } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { isAuthenticated, removeToken, setToken } from '@/lib/auth'
import api from '@/lib/api'
import type { WebUser } from '@/types'

export function useAuth() {
  const [user, setUser] = useState<WebUser | null>(null)
  const [loading, setLoading] = useState(true)
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()

  useEffect(() => {
    // OAuth コールバック後の token 受け取り
    const token = searchParams.get('token')
    if (token) {
      setToken(token)
      navigate('/', { replace: true })
      return
    }

    if (!isAuthenticated()) {
      setLoading(false)
      return
    }

    api.get<WebUser>('/me')
      .then((res) => setUser(res.data))
      .catch(() => {
        removeToken()
      })
      .finally(() => setLoading(false))
  }, [navigate, searchParams])

  const logout = () => {
    removeToken()
    setUser(null)
    navigate('/login')
  }

  return { user, loading, isAuthenticated: isAuthenticated(), logout }
}

export function useTokenFromUrl() {
  const [searchParams, setSearchParams] = useSearchParams()

  useEffect(() => {
    const token = searchParams.get('token')
    if (token) {
      setToken(token)
      const newParams = new URLSearchParams(searchParams)
      newParams.delete('token')
      setSearchParams(newParams, { replace: true })
    }
  }, [searchParams, setSearchParams])
}
