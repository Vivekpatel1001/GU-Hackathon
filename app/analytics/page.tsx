'use client'

import { useState } from 'react'
import { Sidebar } from '@/components/sidebar'
import { Navbar } from '@/components/navbar'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { Button } from '@/components/ui/button'
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts'
import { Download, Calendar } from 'lucide-react'

const engagementData = [
  { date: 'Jan 1', likes: 400, comments: 240, shares: 120 },
  { date: 'Jan 8', likes: 520, comments: 320, shares: 180 },
  { date: 'Jan 15', likes: 680, comments: 420, shares: 280 },
  { date: 'Jan 22', likes: 850, comments: 580, shares: 350 },
  { date: 'Jan 29', likes: 1200, comments: 720, shares: 420 },
]

const platformData = [
  { name: 'Instagram', value: 45, color: '#E4405F' },
  { name: 'Twitter', value: 30, color: '#1DA1F2' },
  { name: 'YouTube', value: 20, color: '#FF0000' },
  { name: 'TikTok', value: 5, color: '#000000' },
]

const topPosts = [
  {
    title: 'How AI Will Change Content Creation',
    platform: 'Instagram',
    likes: 2400,
    comments: 520,
    shares: 840,
  },
  {
    title: 'The Future of Social Media',
    platform: 'Twitter',
    likes: 1800,
    comments: 380,
    shares: 520,
  },
  {
    title: 'Content Creator Tips & Tricks',
    platform: 'YouTube',
    likes: 5200,
    comments: 1200,
    shares: 2100,
  },
]

export default function AnalyticsPage() {
  const [platform, setPlatform] = useState('all')
  const [period, setPeriod] = useState('month')

  return (
    <div className="min-h-screen bg-background">
      <Sidebar />
      <Navbar />

      <main className="ml-64 mt-16 p-6">
        <div className="space-y-8">
          {/* Header */}
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold">Analytics Dashboard</h1>
              <p className="text-muted-foreground mt-2">
                Track performance across all your content
              </p>
            </div>
            <Button className="gap-2">
              <Download className="h-4 w-4" />
              Export Report
            </Button>
          </div>

          {/* Filters */}
          <div className="flex gap-3 flex-wrap">
            <Select value={platform} onValueChange={setPlatform}>
              <SelectTrigger className="w-40 h-10 bg-muted">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Platforms</SelectItem>
                <SelectItem value="instagram">Instagram</SelectItem>
                <SelectItem value="twitter">Twitter/X</SelectItem>
                <SelectItem value="youtube">YouTube</SelectItem>
              </SelectContent>
            </Select>

            <Select value={period} onValueChange={setPeriod}>
              <SelectTrigger className="w-40 h-10 bg-muted">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="week">Last Week</SelectItem>
                <SelectItem value="month">Last Month</SelectItem>
                <SelectItem value="quarter">Last Quarter</SelectItem>
                <SelectItem value="year">Last Year</SelectItem>
              </SelectContent>
            </Select>

            <Button variant="outline" className="gap-2">
              <Calendar className="h-4 w-4" />
              Custom Date
            </Button>
          </div>

          {/* Key Metrics */}
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
            {[
              { label: 'Total Likes', value: '24,580', change: '+12%' },
              { label: 'Total Comments', value: '8,240', change: '+8%' },
              { label: 'Total Shares', value: '5,320', change: '+18%' },
              { label: 'Avg Engagement', value: '4.2%', change: '+2.1%' },
            ].map((metric) => (
              <div key={metric.label} className="glass-card">
                <p className="text-sm text-muted-foreground mb-2">
                  {metric.label}
                </p>
                <p className="text-3xl font-bold">{metric.value}</p>
                <p className="text-xs text-green-500 font-medium mt-2">
                  {metric.change} from last period
                </p>
              </div>
            ))}
          </div>

          {/* Charts */}
          <div className="grid gap-6 lg:grid-cols-3">
            {/* Engagement Over Time */}
            <div className="lg:col-span-2 glass-card">
              <h3 className="text-lg font-bold mb-4">Engagement Over Time</h3>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={engagementData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
                  <XAxis dataKey="date" stroke="var(--muted-foreground)" />
                  <YAxis stroke="var(--muted-foreground)" />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: 'var(--card)',
                      border: `1px solid var(--border)`,
                    }}
                  />
                  <Legend />
                  <Line
                    type="monotone"
                    dataKey="likes"
                    stroke="var(--primary)"
                    strokeWidth={2}
                    dot={{ fill: 'var(--primary)' }}
                  />
                  <Line
                    type="monotone"
                    dataKey="comments"
                    stroke="var(--secondary)"
                    strokeWidth={2}
                    dot={{ fill: 'var(--secondary)' }}
                  />
                  <Line
                    type="monotone"
                    dataKey="shares"
                    stroke="var(--accent)"
                    strokeWidth={2}
                    dot={{ fill: 'var(--accent)' }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>

            {/* Platform Distribution */}
            <div className="glass-card">
              <h3 className="text-lg font-bold mb-4">Platform Distribution</h3>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={platformData}
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={90}
                    paddingAngle={2}
                    dataKey="value"
                  >
                    {platformData.map((entry) => (
                      <Cell key={`cell-${entry.name}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip
                    contentStyle={{
                      backgroundColor: 'var(--card)',
                      border: `1px solid var(--border)`,
                    }}
                  />
                </PieChart>
              </ResponsiveContainer>

              {/* Legend */}
              <div className="grid grid-cols-2 gap-2 mt-4 text-xs">
                {platformData.map((item) => (
                  <div key={item.name} className="flex items-center gap-2">
                    <div
                      className="h-3 w-3 rounded-full"
                      style={{ backgroundColor: item.color }}
                    />
                    <span>{item.name}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Performance by Content Type */}
          <div className="glass-card">
            <h3 className="text-lg font-bold mb-4">Performance by Content Type</h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart
                data={[
                  { type: 'Reels', engagement: 8500, reach: 45000 },
                  { type: 'Carousel', engagement: 5200, reach: 28000 },
                  { type: 'Stories', engagement: 3200, reach: 18000 },
                  { type: 'Feed Posts', engagement: 4100, reach: 22000 },
                  { type: 'Videos', engagement: 7200, reach: 38000 },
                ]}
              >
                <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
                <XAxis dataKey="type" stroke="var(--muted-foreground)" />
                <YAxis stroke="var(--muted-foreground)" />
                <Tooltip
                  contentStyle={{
                    backgroundColor: 'var(--card)',
                    border: `1px solid var(--border)`,
                  }}
                />
                <Legend />
                <Bar dataKey="engagement" fill="var(--primary)" radius={[8, 8, 0, 0]} />
                <Bar dataKey="reach" fill="var(--secondary)" radius={[8, 8, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* Top Performing Posts */}
          <div className="glass-card">
            <h3 className="text-lg font-bold mb-4">Top Performing Posts</h3>
            <div className="space-y-3">
              {topPosts.map((post, i) => (
                <div
                  key={i}
                  className="p-4 rounded-lg bg-muted/30 hover:bg-muted/50 transition-colors"
                >
                  <div className="flex items-start justify-between gap-4">
                    <div className="flex-1 min-w-0">
                      <p className="font-semibold truncate">{post.title}</p>
                      <p className="text-xs text-muted-foreground mt-1">
                        {post.platform}
                      </p>
                    </div>
                    <div className="text-right text-sm">
                      <p className="font-semibold">{post.likes.toLocaleString()}</p>
                      <p className="text-xs text-muted-foreground">Likes</p>
                    </div>
                  </div>
                  <div className="flex gap-8 mt-3 text-xs text-muted-foreground">
                    <div>
                      <p className="font-medium text-foreground">
                        {post.comments}
                      </p>
                      <p>Comments</p>
                    </div>
                    <div>
                      <p className="font-medium text-foreground">
                        {post.shares}
                      </p>
                      <p>Shares</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}
