'use client'

import { useState } from 'react'
import { Sidebar } from '@/components/sidebar'
import { Navbar } from '@/components/navbar'
import { Button } from '@/components/ui/button'
import { Textarea } from '@/components/ui/textarea'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Copy, Sparkles } from 'lucide-react'

export default function YouTubePage() {
  const [topic, setTopic] = useState('')
  const [generated, setGenerated] = useState(false)

  const handleGenerate = () => {
    if (topic.trim()) {
      setGenerated(true)
    }
  }

  return (
    <div className="min-h-screen bg-background">
      <Sidebar />
      <Navbar />

      <main className="ml-64 mt-16 p-6">
        <div className="space-y-8">
          {/* Header */}
          <div>
            <h1 className="text-3xl font-bold">YouTube SEO Optimizer</h1>
            <p className="text-muted-foreground mt-2">
              Get AI-generated titles, descriptions, and SEO optimization for your videos
            </p>
          </div>

          {/* Main Content */}
          <div className="grid gap-6 lg:grid-cols-2">
            {/* Input Section */}
            <div className="glass-card">
              <h2 className="text-xl font-bold mb-4">Video Details</h2>
              <div className="space-y-4">
                <div>
                  <label className="text-sm font-medium">Video Topic / Concept</label>
                  <Textarea
                    placeholder="Describe your video topic, key points, and target audience..."
                    value={topic}
                    onChange={(e) => setTopic(e.target.value)}
                    className="min-h-32 bg-muted resize-none mt-2"
                  />
                </div>

                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="text-sm font-medium">Category</label>
                    <select className="w-full h-10 mt-2 px-3 rounded-lg bg-muted border border-border/50">
                      <option>Technology</option>
                      <option>Entertainment</option>
                      <option>Education</option>
                      <option>Business</option>
                      <option>Lifestyle</option>
                    </select>
                  </div>
                  <div>
                    <label className="text-sm font-medium">Duration</label>
                    <select className="w-full h-10 mt-2 px-3 rounded-lg bg-muted border border-border/50">
                      <option>Under 10 min</option>
                      <option>10-20 min</option>
                      <option>20-30 min</option>
                      <option>30+ min</option>
                    </select>
                  </div>
                </div>

                <Button
                  onClick={handleGenerate}
                  className="w-full h-10 bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 text-white border-0"
                >
                  <Sparkles className="mr-2 h-4 w-4" />
                  Generate SEO Content
                </Button>
              </div>
            </div>

            {/* Thumbnail Preview */}
            <div className="glass-card">
              <h2 className="text-xl font-bold mb-4">Thumbnail Preview</h2>
              <div className="rounded-lg bg-gradient-to-br from-red-500/20 to-orange-500/20 aspect-video flex items-center justify-center border-2 border-dashed border-border/50">
                <div className="text-center">
                  <p className="text-4xl mb-2">🎬</p>
                  <p className="text-sm text-muted-foreground">Thumbnail design appears here</p>
                </div>
              </div>
            </div>
          </div>

          {/* Generated Content */}
          {generated && (
            <div className="glass-card">
              <Tabs defaultValue="title" className="w-full">
                <TabsList className="grid w-full grid-cols-4">
                  <TabsTrigger value="title">Title</TabsTrigger>
                  <TabsTrigger value="description">Description</TabsTrigger>
                  <TabsTrigger value="tags">Tags</TabsTrigger>
                  <TabsTrigger value="metrics">Metrics</TabsTrigger>
                </TabsList>

                {/* Title */}
                <TabsContent value="title" className="space-y-4">
                  <p className="text-sm text-muted-foreground mb-4">
                    SEO-optimized video titles for maximum clicks:
                  </p>
                  {[
                    '🚀 The ULTIMATE Guide to AI in 2024 | Everything You Need to Know',
                    'I Tested 10 AI Tools So You Don\'t Have To (Surprising Results)',
                    'How to Use AI to 10x Your Productivity in 30 Days',
                  ].map((text, i) => (
                    <div
                      key={i}
                      className="p-4 rounded-lg bg-muted/30 flex items-start justify-between gap-4 hover:bg-muted/50 transition-colors"
                    >
                      <p className="text-sm font-medium flex-1">{text}</p>
                      <Button
                        variant="ghost"
                        size="sm"
                        className="shrink-0"
                      >
                        <Copy className="h-4 w-4" />
                      </Button>
                    </div>
                  ))}
                </TabsContent>

                {/* Description */}
                <TabsContent value="description" className="space-y-4">
                  <p className="text-sm text-muted-foreground mb-4">
                    SEO-optimized video description:
                  </p>
                  <div className="p-4 rounded-lg bg-muted/30">
                    <pre className="text-xs whitespace-pre-wrap font-mono">
{`In this video, we explore the latest AI tools and techniques that can transform your workflow. Whether you're a content creator, entrepreneur, or professional, these tools will help you save time and boost productivity.

⏰ Timestamps:
0:00 - Introduction
2:15 - AI Tool #1
5:30 - AI Tool #2
8:45 - Results & Analysis
12:00 - Conclusion

🔗 Resources & Links:
[Tool 1 Link]
[Tool 2 Link]
[Course Link]

📌 Key Takeaways:
✓ AI automation saves 10+ hours weekly
✓ Integration is seamless
✓ Cost-effective solution

#AI #Productivity #Technology`}
                    </pre>
                    <Button
                      variant="ghost"
                      size="sm"
                      className="mt-4"
                    >
                      <Copy className="mr-2 h-4 w-4" />
                      Copy Description
                    </Button>
                  </div>
                </TabsContent>

                {/* Tags */}
                <TabsContent value="tags" className="space-y-4">
                  <p className="text-sm text-muted-foreground mb-4">
                    Recommended hashtags and tags:
                  </p>
                  <div className="flex flex-wrap gap-2">
                    {[
                      '#AI',
                      '#Technology',
                      '#Productivity',
                      '#Tutorial',
                      '#Guide',
                      '#Viral',
                      '#YouTubeOptimization',
                      '#Trending',
                    ].map((tag) => (
                      <button
                        key={tag}
                        className="px-3 py-2 rounded-lg bg-primary/10 text-primary hover:bg-primary/20 transition-colors text-sm font-medium"
                      >
                        {tag}
                      </button>
                    ))}
                  </div>
                </TabsContent>

                {/* Metrics */}
                <TabsContent value="metrics" className="space-y-4">
                  <p className="text-sm text-muted-foreground mb-4">
                    Estimated performance metrics:
                  </p>
                  <div className="grid grid-cols-2 gap-4">
                    {[
                      { label: 'Estimated CTR', value: '8.5%' },
                      { label: 'Avg Watch Time', value: '8:42' },
                      { label: 'Expected Views', value: '50K+' },
                      { label: 'Best Upload Time', value: 'Thursday 2 PM' },
                    ].map((metric) => (
                      <div
                        key={metric.label}
                        className="p-4 rounded-lg bg-muted/30 text-center"
                      >
                        <p className="text-2xl font-bold text-primary">
                          {metric.value}
                        </p>
                        <p className="text-sm text-muted-foreground mt-1">
                          {metric.label}
                        </p>
                      </div>
                    ))}
                  </div>
                </TabsContent>
              </Tabs>
            </div>
          )}
        </div>
      </main>
    </div>
  )
}
