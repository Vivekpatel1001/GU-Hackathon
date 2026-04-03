'use client'

import { useState } from 'react'
import { Sidebar } from '@/components/sidebar'
import { Navbar } from '@/components/navbar'
import { Button } from '@/components/ui/button'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import {
  Lock,
  Bell,
  Shield,
  LogOut,
  Zap,
  Instagram,
  Youtube,
  Twitter,
  AlertCircle,
} from 'lucide-react'

export default function SettingsPage() {
  const [connected, setConnected] = useState({
    instagram: false,
    twitter: false,
    youtube: false,
  })

  const toggleConnect = (platform: string) => {
    setConnected((prev) => ({
      ...prev,
      [platform]: !prev[platform],
    }))
  }

  return (
    <div className="min-h-screen bg-background">
      <Sidebar />
      <Navbar />

      <main className="ml-64 mt-16 p-6">
        <div className="space-y-8">
          {/* Header */}
          <div>
            <h1 className="text-3xl font-bold">Settings</h1>
            <p className="text-muted-foreground mt-2">
              Manage your account, preferences, and integrations
            </p>
          </div>

          {/* Settings Tabs */}
          <Tabs defaultValue="integrations" className="w-full">
            <TabsList className="grid w-full grid-cols-4">
              <TabsTrigger value="integrations">Integrations</TabsTrigger>
              <TabsTrigger value="preferences">Preferences</TabsTrigger>
              <TabsTrigger value="notifications">Notifications</TabsTrigger>
              <TabsTrigger value="account">Account</TabsTrigger>
            </TabsList>

            {/* Integrations Tab */}
            <TabsContent value="integrations" className="space-y-6 mt-6">
              <div className="glass-card">
                <div className="flex items-center justify-between mb-6">
                  <div>
                    <h3 className="text-lg font-bold">Connected Platforms</h3>
                    <p className="text-sm text-muted-foreground mt-1">
                      Connect your social media accounts to get analytics and insights
                    </p>
                  </div>
                </div>

                <div className="space-y-4">
                  {[
                    {
                      name: 'Instagram',
                      icon: Instagram,
                      description: 'Get insights and post optimization tips',
                      key: 'instagram',
                    },
                    {
                      name: 'Twitter/X',
                      icon: Twitter,
                      description: 'Analyze tweet performance and trends',
                      key: 'twitter',
                    },
                    {
                      name: 'YouTube',
                      icon: Youtube,
                      description: 'Get video analytics and SEO recommendations',
                      key: 'youtube',
                    },
                  ].map((platform) => {
                    const Icon = platform.icon
                    const isConnected = connected[platform.key as keyof typeof connected]

                    return (
                      <div
                        key={platform.key}
                        className="p-4 rounded-lg bg-muted/30 flex items-center justify-between hover:bg-muted/50 transition-colors"
                      >
                        <div className="flex items-center gap-4">
                          <div className="h-12 w-12 rounded-lg bg-primary/20 flex items-center justify-center">
                            <Icon className="h-6 w-6 text-primary" />
                          </div>
                          <div>
                            <p className="font-semibold">{platform.name}</p>
                            <p className="text-sm text-muted-foreground">
                              {platform.description}
                            </p>
                          </div>
                        </div>
                        <Button
                          onClick={() => toggleConnect(platform.key)}
                          className={
                            isConnected
                              ? 'bg-green-600 hover:bg-green-700'
                              : 'bg-muted text-foreground hover:bg-muted'
                          }
                        >
                          {isConnected ? 'Connected' : 'Connect'}
                        </Button>
                      </div>
                    )
                  })}
                </div>
              </div>

              {/* API Keys */}
              <div className="glass-card">
                <div className="flex items-center gap-2 mb-4">
                  <Zap className="h-5 w-5" />
                  <h3 className="text-lg font-bold">API Keys</h3>
                </div>
                <p className="text-sm text-muted-foreground mb-4">
                  Manage your API keys for advanced integrations
                </p>

                <div className="space-y-3">
                  {['Trend API', 'Analytics API', 'Generation API'].map((api) => (
                    <div
                      key={api}
                      className="p-3 rounded-lg bg-muted/30 flex items-center justify-between"
                    >
                      <div>
                        <p className="font-medium text-sm">{api}</p>
                        <code className="text-xs text-muted-foreground">
                          sk_live_••••••••••••
                        </code>
                      </div>
                      <Button variant="ghost" size="sm">
                        Regenerate
                      </Button>
                    </div>
                  ))}
                </div>
              </div>
            </TabsContent>

            {/* Preferences Tab */}
            <TabsContent value="preferences" className="space-y-6 mt-6">
              <div className="glass-card">
                <h3 className="text-lg font-bold mb-6">Content Preferences</h3>

                <div className="space-y-4">
                  {/* Niche */}
                  <div>
                    <label className="text-sm font-medium block mb-2">
                      Primary Content Niche
                    </label>
                    <select className="w-full h-10 px-3 rounded-lg bg-muted border border-border/50">
                      <option>Technology</option>
                      <option>Fashion</option>
                      <option>Finance</option>
                      <option>Lifestyle</option>
                      <option>Entertainment</option>
                      <option>Other</option>
                    </select>
                  </div>

                  {/* Language */}
                  <div>
                    <label className="text-sm font-medium block mb-2">
                      Preferred Language
                    </label>
                    <select className="w-full h-10 px-3 rounded-lg bg-muted border border-border/50">
                      <option>English</option>
                      <option>Spanish</option>
                      <option>French</option>
                      <option>German</option>
                      <option>Chinese</option>
                    </select>
                  </div>

                  {/* Content Safety */}
                  <div>
                    <label className="text-sm font-medium block mb-2">
                      Content Safety Filter
                    </label>
                    <div className="flex items-center gap-3">
                      <select className="flex-1 h-10 px-3 rounded-lg bg-muted border border-border/50">
                        <option>Moderate</option>
                        <option>Strict</option>
                        <option>Relaxed</option>
                      </select>
                      <Button variant="outline">Learn more</Button>
                    </div>
                  </div>

                  {/* Default Tone */}
                  <div>
                    <label className="text-sm font-medium block mb-2">
                      Default Content Tone
                    </label>
                    <select className="w-full h-10 px-3 rounded-lg bg-muted border border-border/50">
                      <option>Professional</option>
                      <option>Casual</option>
                      <option>Viral</option>
                      <option>Educational</option>
                      <option>Humorous</option>
                    </select>
                  </div>
                </div>

                <div className="mt-6 pt-6 border-t border-border/50">
                  <Button className="w-full">Save Preferences</Button>
                </div>
              </div>
            </TabsContent>

            {/* Notifications Tab */}
            <TabsContent value="notifications" className="space-y-6 mt-6">
              <div className="glass-card">
                <div className="flex items-center gap-2 mb-6">
                  <Bell className="h-5 w-5" />
                  <h3 className="text-lg font-bold">Notification Settings</h3>
                </div>

                <div className="space-y-4">
                  {[
                    {
                      title: 'Trending Topics',
                      description: 'Get notified when new trends are detected',
                    },
                    {
                      title: 'Performance Alerts',
                      description: 'Alerts when your content gets high engagement',
                    },
                    {
                      title: 'Weekly Digest',
                      description: 'Receive weekly analytics summary',
                    },
                    {
                      title: 'Best Posting Times',
                      description: 'Reminders to post at optimal times',
                    },
                    {
                      title: 'Tool Updates',
                      description: 'New features and improvements notifications',
                    },
                  ].map((notif) => (
                    <div
                      key={notif.title}
                      className="p-3 rounded-lg bg-muted/30 flex items-center justify-between"
                    >
                      <div>
                        <p className="font-medium text-sm">{notif.title}</p>
                        <p className="text-xs text-muted-foreground">
                          {notif.description}
                        </p>
                      </div>
                      <input
                        type="checkbox"
                        defaultChecked
                        className="h-4 w-4 rounded"
                      />
                    </div>
                  ))}
                </div>

                <div className="mt-6 pt-6 border-t border-border/50">
                  <Button className="w-full">Save Notification Settings</Button>
                </div>
              </div>
            </TabsContent>

            {/* Account Tab */}
            <TabsContent value="account" className="space-y-6 mt-6">
              {/* Profile */}
              <div className="glass-card">
                <h3 className="text-lg font-bold mb-6">Profile Information</h3>

                <div className="space-y-4">
                  <div>
                    <label className="text-sm font-medium block mb-2">Email</label>
                    <input
                      type="email"
                      defaultValue="john@example.com"
                      className="w-full h-10 px-3 rounded-lg bg-muted border border-border/50"
                      readOnly
                    />
                  </div>

                  <div>
                    <label className="text-sm font-medium block mb-2">
                      Full Name
                    </label>
                    <input
                      type="text"
                      defaultValue="John Doe"
                      className="w-full h-10 px-3 rounded-lg bg-muted border border-border/50"
                    />
                  </div>

                  <div>
                    <label className="text-sm font-medium block mb-2">
                      Username
                    </label>
                    <input
                      type="text"
                      defaultValue="johndoe"
                      className="w-full h-10 px-3 rounded-lg bg-muted border border-border/50"
                    />
                  </div>
                </div>

                <div className="mt-6 pt-6 border-t border-border/50">
                  <Button className="w-full">Update Profile</Button>
                </div>
              </div>

              {/* Password */}
              <div className="glass-card">
                <div className="flex items-center gap-2 mb-6">
                  <Lock className="h-5 w-5" />
                  <h3 className="text-lg font-bold">Password & Security</h3>
                </div>

                <div className="space-y-4">
                  <Button variant="outline" className="w-full justify-start">
                    <Lock className="mr-2 h-4 w-4" />
                    Change Password
                  </Button>
                  <Button variant="outline" className="w-full justify-start">
                    <Shield className="mr-2 h-4 w-4" />
                    Enable Two-Factor Authentication
                  </Button>
                </div>
              </div>

              {/* Danger Zone */}
              <div className="glass-card border-red-500/20">
                <div className="flex items-center gap-2 mb-6">
                  <AlertCircle className="h-5 w-5 text-red-500" />
                  <h3 className="text-lg font-bold text-red-500">Danger Zone</h3>
                </div>

                <p className="text-sm text-muted-foreground mb-4">
                  Once you delete your account, there is no going back. Please be
                  certain.
                </p>

                <Button variant="destructive" className="w-full">
                  Delete Account
                </Button>
              </div>

              {/* Sign Out */}
              <Button
                variant="outline"
                className="w-full justify-center gap-2"
              >
                <LogOut className="h-4 w-4" />
                Sign Out
              </Button>
            </TabsContent>
          </Tabs>
        </div>
      </main>
    </div>
  )
}
