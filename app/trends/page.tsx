'use client'

import { useState } from 'react'
import { Sidebar } from '@/components/sidebar'
import { Navbar } from '@/components/navbar'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Search, TrendingUp, Filter, BookmarkPlus } from 'lucide-react'
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts'

const trendChartData = [
  { day: 'Mon', volume: 400 },
  { day: 'Tue', volume: 520 },
  { day: 'Wed', volume: 680 },
  { day: 'Thu', volume: 750 },
  { day: 'Fri', volume: 890 },
  { day: 'Sat', volume: 1200 },
  { day: 'Sun', volume: 950 },
]

const trendTopics = [
  {
    rank: 1,
    hashtag: '#AI',
    platform: 'Twitter',
    volume: '2.4M',
    growth: '+45%',
    momentum: 'High',
  },
  {
    rank: 2,
    hashtag: '#Startup',
    platform: 'Instagram',
    volume: '1.8M',
    growth: '+32%',
    momentum: 'High',
  },
  {
    rank: 3,
    hashtag: '#Innovation',
    platform: 'Twitter',
    volume: '1.2M',
    growth: '+18%',
    momentum: 'Medium',
  },
  {
    rank: 4,
    hashtag: '#Creator',
    platform: 'YouTube',
    volume: '945K',
    growth: '+12%',
    momentum: 'Medium',
  },
  {
    rank: 5,
    hashtag: '#TechTrends',
    platform: 'Twitter',
    volume: '754K',
    growth: '+8%',
    momentum: 'Low',
  },
  {
    rank: 6,
    hashtag: '#SocialMedia',
    platform: 'Instagram',
    volume: '632K',
    growth: '+5%',
    momentum: 'Stable',
  },
]

export default function TrendsPage() {
  const [platform, setPlatform] = useState('all')
  const [savedTrends, setSavedTrends] = useState<string[]>([])

  const toggleSave = (hashtag: string) => {
    setSavedTrends((prev) =>
      prev.includes(hashtag)
        ? prev.filter((h) => h !== hashtag)
        : [...prev, hashtag]
    )
  }

  return (
    <div className="min-h-screen bg-background">
      <Sidebar />
      <Navbar />

      <main className="ml-64 mt-16 p-6">
        <div className="space-y-8">
          {/* Header */}
          <div>
            <h1 className="text-3xl font-bold">Trend Explorer</h1>
            <p className="text-muted-foreground mt-2">
              Discover and analyze trending topics across all social platforms
            </p>
          </div>

          {/* Filters */}
          <div className="flex gap-3 flex-wrap">
            <div className="flex-1 min-w-64">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
                <Input
                  placeholder="Search trends..."
                  className="pl-10 h-10 bg-muted"
                />
              </div>
            </div>
            <Select value={platform} onValueChange={setPlatform}>
              <SelectTrigger className="w-48 h-10 bg-muted">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Platforms</SelectItem>
                <SelectItem value="instagram">Instagram</SelectItem>
                <SelectItem value="twitter">Twitter/X</SelectItem>
                <SelectItem value="youtube">YouTube</SelectItem>
              </SelectContent>
            </Select>
            <Button variant="outline" className="h-10">
              <Filter className="mr-2 h-4 w-4" />
              More Filters
            </Button>
          </div>

          {/* Charts */}
          <div className="grid gap-6 lg:grid-cols-2">
            {/* Trend Volume */}
            <div className="glass-card">
              <h3 className="text-lg font-bold mb-4">Trend Volume (This Week)</h3>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={trendChartData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
                  <XAxis dataKey="day" stroke="var(--muted-foreground)" />
                  <YAxis stroke="var(--muted-foreground)" />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: 'var(--card)',
                      border: `1px solid var(--border)`,
                    }}
                  />
                  <Line
                    type="monotone"
                    dataKey="volume"
                    stroke="var(--primary)"
                    strokeWidth={2}
                    dot={{ fill: 'var(--primary)' }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>

            {/* Platform Distribution */}
            <div className="glass-card">
              <h3 className="text-lg font-bold mb-4">Trends by Platform</h3>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={trendChartData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
                  <XAxis dataKey="day" stroke="var(--muted-foreground)" />
                  <YAxis stroke="var(--muted-foreground)" />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: 'var(--card)',
                      border: `1px solid var(--border)`,
                    }}
                  />
                  <Bar dataKey="volume" fill="var(--primary)" radius={[8, 8, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Trending Table */}
          <div className="glass-card">
            <Tabs defaultValue="trending" className="w-full">
              <TabsList className="grid w-full grid-cols-3">
                <TabsTrigger value="trending">Trending Now</TabsTrigger>
                <TabsTrigger value="rising">Rising</TabsTrigger>
                <TabsTrigger value="saved">Saved ({savedTrends.length})</TabsTrigger>
              </TabsList>

              <TabsContent value="trending" className="space-y-3 mt-6">
                <div className="overflow-x-auto">
                  <table className="w-full text-sm">
                    <thead>
                      <tr className="border-b border-border/50">
                        <th className="text-left py-3 px-4 font-semibold">Rank</th>
                        <th className="text-left py-3 px-4 font-semibold">Hashtag</th>
                        <th className="text-left py-3 px-4 font-semibold">Platform</th>
                        <th className="text-left py-3 px-4 font-semibold">Volume</th>
                        <th className="text-left py-3 px-4 font-semibold">Growth</th>
                        <th className="text-left py-3 px-4 font-semibold">Momentum</th>
                        <th className="text-left py-3 px-4 font-semibold">Action</th>
                      </tr>
                    </thead>
                    <tbody>
                      {trendTopics.map((topic) => (
                        <tr
                          key={topic.rank}
                          className="border-b border-border/30 hover:bg-muted/30 transition-colors"
                        >
                          <td className="py-3 px-4">
                            <span className="font-bold text-primary">
                              #{topic.rank}
                            </span>
                          </td>
                          <td className="py-3 px-4 font-semibold">
                            {topic.hashtag}
                          </td>
                          <td className="py-3 px-4">
                            <span className="px-2 py-1 rounded-full bg-muted/50 text-xs">
                              {topic.platform}
                            </span>
                          </td>
                          <td className="py-3 px-4">{topic.volume}</td>
                          <td className="py-3 px-4">
                            <span className="text-green-500 font-medium">
                              {topic.growth}
                            </span>
                          </td>
                          <td className="py-3 px-4">
                            <span
                              className={`px-2 py-1 rounded text-xs font-medium ${
                                topic.momentum === 'High'
                                  ? 'bg-green-500/20 text-green-600 dark:text-green-400'
                                  : topic.momentum === 'Medium'
                                    ? 'bg-yellow-500/20 text-yellow-600 dark:text-yellow-400'
                                    : 'bg-gray-500/20 text-gray-600 dark:text-gray-400'
                              }`}
                            >
                              {topic.momentum}
                            </span>
                          </td>
                          <td className="py-3 px-4">
                            <Button
                              variant="ghost"
                              size="sm"
                              onClick={() => toggleSave(topic.hashtag)}
                              className={
                                savedTrends.includes(topic.hashtag)
                                  ? 'text-yellow-500'
                                  : ''
                              }
                            >
                              <BookmarkPlus className="h-4 w-4" />
                            </Button>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </TabsContent>

              <TabsContent value="rising" className="space-y-3 mt-6">
                <div className="text-center py-8">
                  <TrendingUp className="h-12 w-12 mx-auto text-muted-foreground mb-3" />
                  <p className="text-muted-foreground">
                    Rising trends will appear here
                  </p>
                </div>
              </TabsContent>

              <TabsContent value="saved" className="space-y-3 mt-6">
                {savedTrends.length > 0 ? (
                  <div className="grid gap-3">
                    {savedTrends.map((trend) => (
                      <div
                        key={trend}
                        className="p-3 rounded-lg bg-muted/30 flex items-center justify-between"
                      >
                        <code className="font-semibold">{trend}</code>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => toggleSave(trend)}
                        >
                          Remove
                        </Button>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="text-center py-8">
                    <BookmarkPlus className="h-12 w-12 mx-auto text-muted-foreground mb-3" />
                    <p className="text-muted-foreground">
                      No saved trends yet. Start bookmarking!
                    </p>
                  </div>
                )}
              </TabsContent>
            </Tabs>
          </div>
        </div>
      </main>
    </div>
  )
}
