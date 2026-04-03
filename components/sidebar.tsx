'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import {
  LayoutDashboard,
  Instagram,
  Youtube,
  Twitter,
  TrendingUp,
  Zap,
  BarChart3,
  Settings,
  Sparkles,
} from 'lucide-react'
import { cn } from '@/lib/utils'

const navItems = [
  { icon: LayoutDashboard, label: 'Dashboard', href: '/' },
  { icon: Instagram, label: 'Instagram', href: '/instagram' },
  { icon: Youtube, label: 'YouTube', href: '/youtube' },
  { icon: Twitter, label: 'Twitter/X', href: '/twitter' },
  { icon: TrendingUp, label: 'Trend Explorer', href: '/trends' },
  { icon: Zap, label: 'Content Generator', href: '/generator' },
  { icon: BarChart3, label: 'Analytics', href: '/analytics' },
  { icon: Settings, label: 'Settings', href: '/settings' },
]

export function Sidebar() {
  const pathname = usePathname()

  return (
    <aside className="fixed left-0 top-0 z-40 h-screen w-64 border-r border-sidebar-border bg-sidebar text-sidebar-foreground flex flex-col">
      {/* Logo */}
      <div className="flex items-center gap-3 border-b border-sidebar-border px-6 py-6">
        <div className="flex h-10 w-10 items-center justify-center rounded-lg gradient-accent">
          <Sparkles className="h-6 w-6 text-white" />
        </div>
        <div>
          <h1 className="text-lg font-bold">ViralAI</h1>
          <p className="text-xs text-sidebar-foreground/60">Content Assistant</p>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 space-y-1 overflow-y-auto px-3 py-6">
        {navItems.map((item) => {
          const Icon = item.icon
          const isActive = pathname === item.href
          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                'flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-all duration-200',
                isActive
                  ? 'bg-sidebar-primary text-sidebar-primary-foreground shadow-md'
                  : 'text-sidebar-foreground hover:bg-sidebar-accent hover:text-sidebar-accent-foreground'
              )}
            >
              <Icon className="h-5 w-5" />
              <span>{item.label}</span>
            </Link>
          )
        })}
      </nav>

      {/* Footer */}
      <div className="border-t border-sidebar-border px-6 py-6">
        <p className="text-xs text-sidebar-foreground/50">© 2024 ViralAI</p>
      </div>
    </aside>
  )
}
