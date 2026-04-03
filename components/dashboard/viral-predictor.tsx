'use client'

import { useState } from 'react'
import { Sparkles, Send } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Textarea } from '@/components/ui/textarea'
import { Progress } from '@/components/ui/progress'

export function ViralPredictor() {
  const [input, setInput] = useState('')
  const [analyzed, setAnalyzed] = useState(false)

  const handleAnalyze = () => {
    if (input.trim()) {
      setAnalyzed(true)
    }
  }

  return (
    <div className="glass-card lg:col-span-2">
      <div className="flex flex-col gap-6">
        {/* Header */}
        <div>
          <h2 className="text-xl font-bold mb-2">Viral Prediction Panel</h2>
          <p className="text-sm text-muted-foreground">
            Get AI-powered insights on your content's viral potential
          </p>
        </div>

        {!analyzed ? (
          <>
            {/* Input */}
            <div className="space-y-3">
              <label className="text-sm font-medium">Enter your content idea</label>
              <Textarea
                placeholder="Share your post idea, caption, video topic, or content concept..."
                value={input}
                onChange={(e) => setInput(e.target.value)}
                className="min-h-24 bg-muted resize-none"
              />
            </div>

            {/* Analyze Button */}
            <Button
              onClick={handleAnalyze}
              className="w-full h-10 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white border-0"
            >
              <Sparkles className="mr-2 h-4 w-4" />
              Analyze Content
            </Button>
          </>
        ) : (
          <div className="space-y-6">
            {/* Viral Score */}
            <div>
              <div className="flex items-center justify-between mb-2">
                <span className="font-semibold text-lg">Viral Score</span>
                <span className="text-2xl font-bold text-primary">78/100</span>
              </div>
              <Progress value={78} className="h-2" />
              <p className="text-xs text-muted-foreground mt-2">
                High potential for engagement
              </p>
            </div>

            {/* Engagement Prediction */}
            <div>
              <p className="font-semibold mb-3">Engagement Prediction</p>
              <div className="grid grid-cols-3 gap-3">
                {[
                  { label: 'Likes', value: '2.4K', icon: '👍' },
                  { label: 'Comments', value: '520', icon: '💬' },
                  { label: 'Shares', value: '840', icon: '🔄' },
                ].map((item) => (
                  <div key={item.label} className="p-3 rounded-lg bg-muted/50">
                    <p className="text-2xl mb-1">{item.icon}</p>
                    <p className="text-xs text-muted-foreground">{item.label}</p>
                    <p className="font-semibold text-sm">{item.value}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* Suggestions */}
            <div>
              <p className="font-semibold mb-3">AI Suggestions</p>
              <ul className="space-y-2">
                {[
                  '✓ Strong hook in the first 3 seconds',
                  '✓ Add trending sounds/music',
                  '→ Include call-to-action (Ask a question)',
                ].map((suggestion, i) => (
                  <li
                    key={i}
                    className="text-sm text-muted-foreground flex items-start gap-2"
                  >
                    <span>{suggestion}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* Reset Button */}
            <Button
              onClick={() => {
                setAnalyzed(false)
                setInput('')
              }}
              variant="outline"
              className="w-full"
            >
              Analyze Another
            </Button>
          </div>
        )}
      </div>
    </div>
  )
}
