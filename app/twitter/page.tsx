'use client'

import { useState } from 'react'
import { Sidebar } from '@/components/sidebar'
import { Navbar } from '@/components/navbar'
import { Button } from '@/components/ui/button'
import { Textarea } from '@/components/ui/textarea'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Copy, Heart, MessageCircle, Share2, Sparkles } from 'lucide-react'

export default function TwitterPage() {
  const [idea, setIdea] = useState('')
  const [generated, setGenerated] = useState(false)

  const handleGenerate = () => {
    if (idea.trim()) {
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
            <h1 className="text-3xl font-bold">Twitter/X Optimizer</h1>
            <p className="text-muted-foreground mt-2">
              Create engaging tweets and threads that drive conversation
            </p>
          </div>

          {/* Main Content */}
          <div className="grid gap-6 lg:grid-cols-2">
            {/* Input Section */}
            <div className="glass-card">
              <h2 className="text-xl font-bold mb-4">Tweet Idea</h2>
              <div className="space-y-4">
                <div>
                  <label className="text-sm font-medium">Tweet or Thread Concept</label>
                  <Textarea
                    placeholder="Share your tweet idea, thread topic, or conversation starter..."
                    value={idea}
                    onChange={(e) => setIdea(e.target.value)}
                    className="min-h-32 bg-muted resize-none mt-2"
                  />
                </div>

                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="text-sm font-medium">Tweet Type</label>
                    <select className="w-full h-10 mt-2 px-3 rounded-lg bg-muted border border-border/50">
                      <option>Single Tweet</option>
                      <option>Thread</option>
                      <option>Question</option>
                      <option>Breaking News</option>
                    </select>
                  </div>
                  <div>
                    <label className="text-sm font-medium">Tone</label>
                    <select className="w-full h-10 mt-2 px-3 rounded-lg bg-muted border border-border/50">
                      <option>Professional</option>
                      <option>Casual</option>
                      <option>Viral</option>
                      <option>Humorous</option>
                    </select>
                  </div>
                </div>

                <Button
                  onClick={handleGenerate}
                  className="w-full h-10 bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-700 hover:to-cyan-700 text-white border-0"
                >
                  <Sparkles className="mr-2 h-4 w-4" />
                  Generate Tweet
                </Button>
              </div>
            </div>

            {/* Tweet Preview */}
            <div className="glass-card">
              <h2 className="text-xl font-bold mb-4">Tweet Preview</h2>
              <div className="rounded-lg bg-muted/30 p-4 border border-border/50 space-y-3">
                <div className="flex gap-3">
                  <div className="h-12 w-12 rounded-full bg-gradient-to-r from-blue-500 to-cyan-500" />
                  <div className="flex-1">
                    <p className="font-bold text-sm">You</p>
                    <p className="text-xs text-muted-foreground">@username</p>
                  </div>
                </div>
                <p className="text-sm text-muted-foreground italic">
                  Tweet content will appear here...
                </p>
                <div className="flex gap-8 text-muted-foreground text-xs">
                  <button className="flex items-center gap-2 hover:text-blue-500 transition-colors">
                    <MessageCircle className="h-4 w-4" />
                    <span>0</span>
                  </button>
                  <button className="flex items-center gap-2 hover:text-green-500 transition-colors">
                    <Share2 className="h-4 w-4" />
                    <span>0</span>
                  </button>
                  <button className="flex items-center gap-2 hover:text-red-500 transition-colors">
                    <Heart className="h-4 w-4" />
                    <span>0</span>
                  </button>
                </div>
              </div>
            </div>
          </div>

          {/* Generated Content */}
          {generated && (
            <div className="glass-card">
              <Tabs defaultValue="tweet" className="w-full">
                <TabsList className="grid w-full grid-cols-4">
                  <TabsTrigger value="tweet">Tweet</TabsTrigger>
                  <TabsTrigger value="thread">Thread</TabsTrigger>
                  <TabsTrigger value="hashtags">Hashtags</TabsTrigger>
                  <TabsTrigger value="timing">Best Time</TabsTrigger>
                </TabsList>

                {/* Tweet */}
                <TabsContent value="tweet" className="space-y-4">
                  <p className="text-sm text-muted-foreground mb-4">
                    Optimized tweets for maximum engagement:
                  </p>
                  {[
                    '🚀 AI is changing everything. The next 10 years will be defined by how well you adopt it. What\'s the one AI tool you can\'t live without anymore?',
                    '💡 If you\'re not using AI to automate your workflow yet, you\'re leaving 10 hours/week on the table. Start here: [link]',
                    '✨ The future isn\'t about having the best ideas. It\'s about executing them 10x faster. AI is the difference maker.',
                  ].map((text, i) => (
                    <div
                      key={i}
                      className="p-4 rounded-lg bg-muted/30 flex items-start justify-between gap-4 hover:bg-muted/50 transition-colors group"
                    >
                      <p className="text-sm flex-1">{text}</p>
                      <Button
                        variant="ghost"
                        size="sm"
                        className="shrink-0 opacity-0 group-hover:opacity-100 transition-opacity"
                      >
                        <Copy className="h-4 w-4" />
                      </Button>
                    </div>
                  ))}
                </TabsContent>

                {/* Thread */}
                <TabsContent value="thread" className="space-y-4">
                  <p className="text-sm text-muted-foreground mb-4">
                    AI-generated thread for deeper engagement:
                  </p>
                  <div className="space-y-3">
                    {[
                      { num: '1/5', text: '🧵 The AI Revolution is here. And if you\'re not paying attention, you\'re already behind. Let me share 5 game-changing insights...' },
                      { num: '2/5', text: 'First: Stop thinking of AI as a threat. It\'s a tool. The question isn\'t "Will AI replace me?" It\'s "How can I use AI to become unstoppable?"' },
                      { num: '3/5', text: 'Second: The barrier to entry is now zero. You can build AI-powered apps without coding. The advantage goes to those who move fast.' },
                      { num: '4/5', text: 'Third: Your content game will 10x. AI helps you ideate, create, optimize & scale faster than ever. This is the future of content.' },
                      { num: '5/5', text: 'Start experimenting today. Try ChatGPT, Claude, or Gemini. The future rewards the curious & punishes the complacent. Which will you be? 🚀' },
                    ].map((item, i) => (
                      <div
                        key={i}
                        className="p-4 rounded-lg bg-muted/30 border-l-4 border-primary"
                      >
                        <p className="text-xs font-semibold text-primary mb-2">
                          {item.num}
                        </p>
                        <p className="text-sm">{item.text}</p>
                      </div>
                    ))}
                  </div>
                </TabsContent>

                {/* Hashtags */}
                <TabsContent value="hashtags" className="space-y-4">
                  <p className="text-sm text-muted-foreground mb-4">
                    Trending hashtags for visibility:
                  </p>
                  <div className="flex flex-wrap gap-2">
                    {[
                      '#AI',
                      '#TechNews',
                      '#Startup',
                      '#Innovation',
                      '#Future',
                      '#Automation',
                      '#Viral',
                      '#XCommunity',
                      '#Trending',
                    ].map((tag) => (
                      <button
                        key={tag}
                        className="px-3 py-2 rounded-full bg-primary/10 text-primary hover:bg-primary/20 transition-colors text-sm font-medium"
                      >
                        {tag}
                      </button>
                    ))}
                  </div>
                </TabsContent>

                {/* Timing */}
                <TabsContent value="timing" className="space-y-4">
                  <p className="text-sm text-muted-foreground mb-4">
                    Post at the optimal time for your audience:
                  </p>
                  <div className="grid grid-cols-2 gap-4">
                    {[
                      { day: 'Weekday', time: '8-10 AM EST' },
                      { day: 'Weekend', time: '9 AM - 1 PM EST' },
                      { day: 'Thread Best', time: 'Tuesday-Thursday' },
                      { day: 'Breaking News', time: 'Immediate' },
                    ].map((item) => (
                      <div
                        key={item.day}
                        className="p-4 rounded-lg bg-muted/30 text-center"
                      >
                        <p className="text-sm text-muted-foreground">{item.day}</p>
                        <p className="font-bold text-primary mt-1">{item.time}</p>
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
