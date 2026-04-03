'use client'

import { useState } from 'react'
import { Search, Filter } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'

const trendingData = [
  { hashtag: '#AI', platform: 'Instagram', strength: 'High', count: '2.4M' },
  { hashtag: '#Startup', platform: 'Twitter', strength: 'High', count: '1.8M' },
  { hashtag: '#Viral', platform: 'Instagram', strength: 'Medium', count: '945K' },
  { hashtag: '#TechTrends', platform: 'Twitter', strength: 'High', count: '1.2M' },
  { hashtag: '#Creator', platform: 'YouTube', strength: 'Medium', count: '564K' },
  { hashtag: '#Innovation', platform: 'Instagram', strength: 'High', count: '3.1M' },
]

export function TrendEngine() {
  const [selectedPlatform, setSelectedPlatform] = useState('all')

  const filteredTrends =
    selectedPlatform === 'all'
      ? trendingData
      : trendingData.filter((t) => t.platform === selectedPlatform)

  const strengthColor = (strength: string) => {
    switch (strength) {
      case 'High':
        return 'bg-green-500/20 text-green-600 dark:text-green-400'
      case 'Medium':
        return 'bg-yellow-500/20 text-yellow-600 dark:text-yellow-400'
      default:
        return 'bg-gray-500/20 text-gray-600 dark:text-gray-400'
    }
  }

  return (
    <div className="glass-card">
      <div className="flex flex-col gap-6">
        {/* Header */}
        <div>
          <h2 className="text-xl font-bold mb-2">Trend Detection Engine</h2>
          <p className="text-sm text-muted-foreground">
            Real-time trending hashtags and topics across platforms
          </p>
        </div>

        {/* Controls */}
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
          <Select value={selectedPlatform} onValueChange={setSelectedPlatform}>
            <SelectTrigger className="w-40 h-10 bg-muted">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Platforms</SelectItem>
              <SelectItem value="Instagram">Instagram</SelectItem>
              <SelectItem value="Twitter">Twitter/X</SelectItem>
              <SelectItem value="YouTube">YouTube</SelectItem>
            </SelectContent>
          </Select>
        </div>

        {/* Trends Grid */}
        <div className="grid gap-3">
          {filteredTrends.map((trend, i) => (
            <div
              key={i}
              className="flex items-center justify-between p-3 rounded-lg bg-muted/30 hover:bg-muted/50 transition-colors group cursor-pointer"
            >
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-3 flex-wrap">
                  <code className="text-sm font-semibold text-primary">
                    {trend.hashtag}
                  </code>
                  <span className="text-xs px-2 py-1 rounded-full bg-muted text-muted-foreground">
                    {trend.platform}
                  </span>
                  <span className={`text-xs px-2 py-1 rounded-full font-medium ${strengthColor(trend.strength)}`}>
                    {trend.strength}
                  </span>
                </div>
                <p className="text-xs text-muted-foreground mt-1">
                  {trend.count} posts
                </p>
              </div>
              <Button
                variant="ghost"
                size="sm"
                className="opacity-0 group-hover:opacity-100 transition-opacity"
              >
                Add
              </Button>
            </div>
          ))}
        </div>

        {/* View All */}
        <Button variant="outline" className="w-full">
          View All Trends
        </Button>
      </div>
    </div>
  )
}
