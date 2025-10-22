import { createClient } from '@supabase/supabase-js'

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL || ''
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY || ''

export const supabase = createClient(supabaseUrl, supabaseAnonKey)

export interface SignUpData {
  email: string
  password: string
  fullName: string
  userType: 'creator' | 'agency'
  agencyName?: string
}

export interface SignInData {
  email: string
  password: string
}

export interface User {
  id: string
  email: string
  fullName?: string
  userType?: 'creator' | 'agency'
  voiceTraits?: string[]
}

class AuthService {
  /**
   * Sign up a new user
   */
  async signUp(data: SignUpData) {
    try {
      // Create auth user with metadata
      // The database trigger will automatically create the user profile
      const { data: authData, error: authError } = await supabase.auth.signUp({
        email: data.email,
        password: data.password,
        options: {
          data: {
            full_name: data.fullName,
            user_type: data.userType,
            agency_name: data.agencyName,
          },
        },
      })

      if (authError) throw authError
      if (!authData.user) throw new Error('No user returned from sign up')

      return { user: authData.user, session: authData.session }
    } catch (error: any) {
      console.error('Sign up error:', error)
      throw new Error(error.message || 'Failed to sign up')
    }
  }

  /**
   * Sign in existing user
   */
  async signIn(data: SignInData) {
    console.log('🔵 [AuthService] signIn START', { email: data.email })
    try {
      console.log('🔵 [AuthService] Calling supabase.auth.signInWithPassword...')
      const { data: authData, error } = await supabase.auth.signInWithPassword({
        email: data.email,
        password: data.password,
      })

      console.log('🔵 [AuthService] Supabase response:', { 
        hasUser: !!authData.user, 
        hasSession: !!authData.session, 
        error: error 
      })

      if (error) {
        console.error('🔴 [AuthService] Supabase error:', error)
        throw error
      }

      console.log('🟢 [AuthService] signIn SUCCESS')
      return { user: authData.user, session: authData.session }
    } catch (error: any) {
      console.error('🔴 [AuthService] Sign in error:', error)
      throw new Error(error.message || 'Failed to sign in')
    }
  }

  /**
   * Sign out current user
   */
  async signOut() {
    try {
      const { error } = await supabase.auth.signOut()
      if (error) throw error
    } catch (error: any) {
      console.error('Sign out error:', error)
      throw new Error(error.message || 'Failed to sign out')
    }
  }

  /**
   * Get current session
   */
  async getSession() {
    try {
      const { data: { session }, error } = await supabase.auth.getSession()
      if (error) throw error
      return session
    } catch (error: any) {
      console.error('Get session error:', error)
      return null
    }
  }

  /**
   * Get current user
   */
  async getCurrentUser(): Promise<User | null> {
    console.log('🔵 [AuthService] getCurrentUser START')
    try {
      console.log('🔵 [AuthService] Calling supabase.auth.getUser...')
      
      // Add timeout to prevent hanging
      const getUserPromise = supabase.auth.getUser()
      const timeoutPromise = new Promise((_, reject) => 
        setTimeout(() => reject(new Error('getUser timeout')), 5000)
      )
      
      const { data: { user } } = await Promise.race([getUserPromise, timeoutPromise]) as any
      console.log('🟢 [AuthService] Auth user retrieved:', { hasUser: !!user, userId: user?.id })
      
      if (!user) {
        console.log('🟡 [AuthService] No user found, returning null')
        return null
      }

      // Return user with metadata immediately (don't wait for profile)
      const immediateUser = {
        id: user.id,
        email: user.email || '',
        fullName: user.user_metadata?.full_name || '',
        userType: user.user_metadata?.user_type || 'creator',
        voiceTraits: [],
      }
      console.log('🟢 [AuthService] Returning immediate user:', immediateUser)
      return immediateUser

      // TODO: Fetch profile in background later if needed
    } catch (error: any) {
      console.error('🔴 [AuthService] Get current user error:', error)
      console.log('🔴 [AuthService] Returning null')
      return null
    }
  }

  /**
   * Reset password
   */
  async resetPassword(email: string) {
    try {
      const { error } = await supabase.auth.resetPasswordForEmail(email, {
        redirectTo: `${window.location.origin}/reset-password`,
      })
      if (error) throw error
    } catch (error: any) {
      console.error('Reset password error:', error)
      throw new Error(error.message || 'Failed to reset password')
    }
  }

  /**
   * Update password
   */
  async updatePassword(newPassword: string) {
    try {
      const { error } = await supabase.auth.updateUser({
        password: newPassword,
      })
      if (error) throw error
    } catch (error: any) {
      console.error('Update password error:', error)
      throw new Error(error.message || 'Failed to update password')
    }
  }

  /**
   * Listen to auth state changes
   */
  onAuthStateChange(callback: (user: User | null) => void) {
    return supabase.auth.onAuthStateChange(async (event, session) => {
      console.log('🔵 [AuthService] onAuthStateChange triggered', { event, hasSession: !!session })
      if (session?.user) {
        console.log('🔵 [AuthService] Session exists, creating user from session...')
        // Create user directly from session to avoid hanging
        const user = {
          id: session.user.id,
          email: session.user.email || '',
          fullName: session.user.user_metadata?.full_name || '',
          userType: session.user.user_metadata?.user_type || 'creator',
          voiceTraits: [],
        }
        console.log('🟢 [AuthService] Calling callback with session user:', user)
        callback(user)
      } else {
        console.log('🔵 [AuthService] No session, calling callback with null')
        callback(null)
      }
    })
  }
}

export const authService = new AuthService()
export default authService

