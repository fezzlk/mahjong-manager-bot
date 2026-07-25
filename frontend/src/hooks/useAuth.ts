import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { isAuthenticated, removeToken } from '@/lib/auth'
import api from '@/lib/api'
import type { WebUser } from '@/types'

export function useAuth() {
  const [user, setUser] = useState<WebUser | null>(null)
  const [loading, setLoading] = useState(true)
  const navigate = useNavigate()

  useEffect(() => {
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
  }, [])

  const logout = () => {
    removeToken()
    setUser(null)
    navigate('/login')
  }

  return { user, loading, isAuthenticated: isAuthenticated(), logout }
}
