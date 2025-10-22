import { createContext, useContext, useState, useEffect, ReactNode } from 'react'
import authService, { User, SignUpData, SignInData } from '../services/auth'
import { useNavigate } from 'react-router-dom'
import toast from 'react-hot-toast'

interface AuthContextType {
  user: User | null
  loading: boolean
  signUp: (data: SignUpData) => Promise<void>
  signIn: (data: SignInData) => Promise<void>
  signOut: () => Promise<void>
  resetPassword: (email: string) => Promise<void>
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)
  const navigate = useNavigate()

  useEffect(() => {
    console.log('🔵 [AuthContext] useEffect mounting')
    // Check current session on mount
    checkSession()

    // Listen to auth state changes
    const { data: { subscription } } = authService.onAuthStateChange((user) => {
      console.log('🔵 [AuthContext] Auth state change callback triggered', { hasUser: !!user, user })
      setUser(user)
      setLoading(false)
      console.log('🟢 [AuthContext] User state updated from listener')
    })

    return () => {
      console.log('🔵 [AuthContext] useEffect cleanup')
      subscription?.unsubscribe()
    }
  }, [])

  async function checkSession() {
    console.log('🔵 [AuthContext] checkSession START')
    try {
      const user = await authService.getCurrentUser()
      console.log('🔵 [AuthContext] checkSession got user:', user)
      setUser(user)
      console.log('🟢 [AuthContext] User state set in checkSession')
    } catch (error) {
      console.error('🔴 [AuthContext] Session check error:', error)
    } finally {
      setLoading(false)
      console.log('🟢 [AuthContext] checkSession COMPLETE, loading = false')
    }
  }

  async function signUp(data: SignUpData) {
    try {
      setLoading(true)
      await authService.signUp(data)
      toast.success('Account created successfully! Please check your email to verify.')
      navigate('/dashboard')
    } catch (error: any) {
      console.error('Sign up error:', error)
      toast.error(error.message || 'Failed to create account')
      throw error
    } finally {
      setLoading(false)
    }
  }

  async function signIn(data: SignInData) {
    console.log('🔵 [AuthContext] signIn START')
    try {
      console.log('🔵 [AuthContext] Calling authService.signIn...')
      await authService.signIn(data)
      console.log('🟢 [AuthContext] authService.signIn SUCCESS')
      
      // Auth state listener will handle setting the user
      toast.success('Signed in successfully!')
      navigate('/dashboard')
      console.log('🟢 [AuthContext] Navigation called - DONE')
    } catch (error: any) {
      console.error('🔴 [AuthContext] Sign in error:', error)
      setLoading(false)
      toast.error(error.message || 'Failed to sign in')
      throw error
    }
  }

  async function signOut() {
    try {
      await authService.signOut()
      setUser(null)
      toast.success('Signed out successfully')
      navigate('/')
    } catch (error: any) {
      console.error('Sign out error:', error)
      toast.error(error.message || 'Failed to sign out')
    }
  }

  async function resetPassword(email: string) {
    try {
      await authService.resetPassword(email)
      toast.success('Password reset email sent! Check your inbox.')
    } catch (error: any) {
      console.error('Reset password error:', error)
      toast.error(error.message || 'Failed to send reset email')
      throw error
    }
  }

  const value = {
    user,
    loading,
    signUp,
    signIn,
    signOut,
    resetPassword,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}

