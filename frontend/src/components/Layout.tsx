import { Outlet, Link, useLocation } from 'react-router-dom'
import { useState } from 'react'
import { 
  HomeIcon, 
  RssIcon, 
  DocumentTextIcon, 
  CogIcon,
  ArrowRightOnRectangleIcon,
  SparklesIcon,
  Bars3Icon,
  XMarkIcon
} from '@heroicons/react/24/outline'
import { useAuth } from '../contexts/AuthContext'

const navigation = [
  { name: 'Dashboard', href: '/dashboard', icon: HomeIcon },
  { name: 'Sources', href: '/sources', icon: RssIcon },
  { name: 'Drafts', href: '/drafts', icon: DocumentTextIcon },
  { name: 'Settings', href: '/settings', icon: CogIcon },
]

export default function Layout() {
  const location = useLocation()
  const { user, signOut } = useAuth()
  const [sidebarOpen, setSidebarOpen] = useState(false)

  return (
    <div className="min-h-screen bg-gray-50 flex">
      {/* Mobile sidebar overlay */}
      {sidebarOpen && (
        <div 
          className="fixed inset-0 z-40 bg-gray-600 bg-opacity-75 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <div className={`fixed inset-y-0 left-0 z-50 w-64 bg-white shadow-sm flex flex-col transform transition-transform duration-300 ease-in-out lg:static lg:inset-0 ${
        sidebarOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
      }`}>
        <div className="flex min-h-0 flex-1 flex-col">
          <div className="flex flex-1 flex-col overflow-y-auto pt-5 pb-4">
            <div className="flex flex-shrink-0 items-center justify-between px-4 gap-2">
              <div className="flex items-center gap-2">
                <SparklesIcon className="h-8 w-8 text-blue-600" />
                <h1 className="text-xl font-bold text-gray-900">EchoWrite</h1>
              </div>
              {/* Close button for mobile */}
              <button
                onClick={() => setSidebarOpen(false)}
                className="lg:hidden p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100"
              >
                <XMarkIcon className="h-6 w-6" />
              </button>
            </div>
            <nav className="mt-8 flex-1 space-y-1 px-2">
              {navigation.map((item) => {
                const isActive = location.pathname === item.href
                return (
                  <Link
                    key={item.name}
                    to={item.href}
                    className={`${
                      isActive
                        ? 'bg-blue-50 border-r-2 border-blue-600 text-blue-700'
                        : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                    } group flex items-center px-2 py-2 text-sm font-medium rounded-md`}
                  >
                    <item.icon
                      className={`${
                        isActive ? 'text-blue-500' : 'text-gray-400 group-hover:text-gray-500'
                      } mr-3 h-5 w-5 flex-shrink-0`}
                    />
                    {item.name}
                  </Link>
                )
              })}
            </nav>
          </div>

          {/* User info & sign out */}
          <div className="border-t border-gray-200 p-4">
            <div className="flex items-center gap-3 mb-3">
              <div className="w-10 h-10 bg-blue-500 rounded-full flex items-center justify-center text-white font-semibold">
                {user?.fullName?.charAt(0).toUpperCase() || user?.email?.charAt(0).toUpperCase() || 'U'}
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-gray-900 truncate">
                  {user?.fullName || 'User'}
                </p>
                <p className="text-xs text-gray-500 truncate">
                  {user?.email}
                </p>
                {user?.userType && (
                  <span className="inline-block mt-1 px-2 py-0.5 bg-blue-100 text-blue-800 text-xs font-medium rounded">
                    {user.userType === 'agency' ? 'Agency' : 'Creator'}
                  </span>
                )}
              </div>
            </div>
            <button
              onClick={signOut}
              className="w-full flex items-center justify-center gap-2 px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 rounded-lg transition-colors"
            >
              <ArrowRightOnRectangleIcon className="h-4 w-4" />
              Sign Out
            </button>
          </div>
        </div>
      </div>

      {/* Main content */}
      <div className="flex-1 flex flex-col lg:ml-0">
        <header className="bg-white border-b border-gray-200 px-4 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              {/* Mobile menu button */}
              <button
                onClick={() => setSidebarOpen(true)}
                className="lg:hidden p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100"
              >
                <Bars3Icon className="h-6 w-6" />
              </button>
              <h2 className="text-xl font-semibold text-gray-800">
                {location.pathname === '/dashboard' && 'Dashboard'}
                {location.pathname === '/sources' && 'Content Sources'}
                {location.pathname === '/drafts' && 'Newsletter Drafts'}
                {location.pathname === '/settings' && 'Settings'}
              </h2>
            </div>
          </div>
        </header>
        
        <main className="flex-1 p-4 lg:p-8 bg-gray-50 overflow-auto">
          <Outlet />
        </main>
      </div>
    </div>
  )
}
