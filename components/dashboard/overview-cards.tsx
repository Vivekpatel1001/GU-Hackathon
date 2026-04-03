'use client'

import { TrendingUp, Zap, Users, Clock } from 'lucide-react'
import { LineChart, Line, ResponsiveContainer } from 'recharts'

const mockData = [
  { value: 40 },
  { value: 45 },
  { value: 38 },
  { value: 52 },
  { value: 48 },
  { value: 61 },
]

const cards = [
  {
    title: 'Trending Topics Today',
    icon: TrendingUp,
    value: '24',
    unit: 'topics',
    change: '+12%',
    positive: true,
    color: 'from-purple-500 to-purple-600',
  },
  {
    title: 'Predicted Viral Score',
    icon: Zap,
    value: '78',
    unit: '/100',
    change: '+5%',
    positive: true,
    color: 'from-blue-500 to-blue-600',
  },
  {
    title: 'Audience Engagement',
    icon: Users,
    value: '4.2K',
    unit: 'interactions',
    change: '+18%',
    positive: true,
    color: 'from-cyan-500 to-cyan-600',
  },
  {
    title: 'Best Posting Time',
    icon: Clock,
    value: '8:30 PM',
    unit: 'peak hour',
    change: 'Updated today',
    positive: false,
    color: 'from-indigo-500 to-indigo-600',
  },
]

export function OverviewCards() {
  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
      {cards.map((card) => {
        const Icon = card.icon
        return (
          <div
            key={card.title}
            className="glass-card group relative overflow-hidden"
          >
            {/* Gradient background */}
            <div
              className={`absolute inset-0 bg-gradient-to-br ${card.color} opacity-0 group-hover:opacity-5 transition-opacity duration-300`}
            />

            {/* Content */}
            <div className="relative flex flex-col gap-4">
              <div className="flex items-start justify-between">
                <div>
                  <p className="text-sm text-muted-foreground">{card.title}</p>
                </div>
                <div className={`rounded-lg bg-gradient-to-br ${card.color} p-2`}>
                  <Icon className="h-4 w-4 text-white" />
                </div>
              </div>

              {/* Value */}
              <div>
                <p className="text-3xl font-bold">{card.value}</p>
                <p className="text-xs text-muted-foreground mt-1">{card.unit}</p>
              </div>

              {/* Chart and Change */}
              <div className="flex items-end justify-between pt-2 border-t border-border/30">
                <div className="w-16 h-8">
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={mockData}>
                      <Line
                        type="monotone"
                        dataKey="value"
                        stroke="currentColor"
                        strokeWidth={2}
                        dot={false}
                        isAnimationActive={false}
                      />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
                <span
                  className={`text-xs font-medium ${
                    card.positive ? 'text-green-500' : 'text-muted-foreground'
                  }`}
                >
                  {card.change}
                </span>
              </div>
            </div>
          </div>
        )
      })}
    </div>
  )
}
