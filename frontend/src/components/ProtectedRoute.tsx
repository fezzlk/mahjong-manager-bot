import { Navigate, useLocation } from 'react-router-dom'
import { isAuthenticated } from '@/lib/auth'

interface Props {
  children: React.ReactNode
}

export function ProtectedRoute({ children }: Props) {
  const location = useLocation()

  if (!isAuthenticated()) {
    return <Navigate to="/login" state={{ from: location }} replace />
  }

  return <>{children}</>
}
