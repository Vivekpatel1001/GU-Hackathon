'use client'

import { useState } from 'react'
import { Sidebar } from '@/components/sidebar'
import { Navbar } from '@/components/navbar'
import { Button } from '@/components/ui/button'
import { Textarea } from '@/components/ui/textarea'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Copy, RefreshCw, Sparkles } from 'lucide-react'

export default function GeneratorPage() {
  const [topic, setTopic] = useState('')
  const [tone, setTone] = useState('professional')
  const [platform, setPlatform] = useState('general')
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
            <h1 className="text-3xl font-bold">Content Generator</h1>
            <p className="text-muted-foreground mt-2">
              Generate hooks, headlines, CTAs, and captions with AI
            </p>
          </div>

          {/* Input Section */}
          <div className="glass-card">
            <h2 className="text-xl font-bold mb-6">Content Configuration</h2>

            <div className="space-y-6">
              {/* Topic Input */}
              <div>
                <label className="text-sm font-medium block mb-2">
                  Content Topic / Idea
                </label>
                <Textarea
                  placeholder="Describe your content topic, product, or idea..."
                  value={topic}
                  onChange={(e) => setTopic(e.target.value)}
                  className="min-h-24 bg-muted resize-none"
                />
              </div>

              {/* Configuration Grid */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {/* Tone */}
                <div>
                  <label className="text-sm font-medium block mb-2">Tone</label>
                  <select
                    value={tone}
                    onChange={(e) => setTone(e.target.value)}
                    className="w-full h-10 px-3 rounded-lg bg-muted border border-border/50"
                  >
                    <option value="professional">Professional</option>
                    <option value="casual">Casual</option>
                    <option value="viral">Viral</option>
                    <option value="educational">Educational</option>
                    <option value="humorous">Humorous</option>
                  </select>
                </div>

                {/* Platform */}
                <div>
                  <label className="text-sm font-medium block mb-2">
                    Primary Platform
                  </label>
                  <select
                    value={platform}
                    onChange={(e) => setPlatform(e.target.value)}
                    className="w-full h-10 px-3 rounded-lg bg-muted border border-border/50"
                  >
                    <option value="general">General/Multi-Platform</option>
                    <option value="instagram">Instagram</option>
                    <option value="twitter">Twitter/X</option>
                    <option value="youtube">YouTube</option>
                    <option value="linkedin">LinkedIn</option>
                  </select>
                </div>

                {/* Target Audience */}
                <div>
                  <label className="text-sm font-medium block mb-2">
                    Target Audience
                  </label>
                  <select className="w-full h-10 px-3 rounded-lg bg-muted border border-border/50">
                    <option>Tech Professionals</option>
                    <option>Entrepreneurs</option>
                    <option>Students</option>
                    <option>Content Creators</option>
                    <option>General Audience</option>
                  </select>
                </div>
              </div>

              {/* Generate Button */}
              <Button
                onClick={handleGenerate}
                className="w-full h-10 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white border-0"
              >
                <Sparkles className="mr-2 h-4 w-4" />
                Generate Content Ideas
              </Button>
            </div>
          </div>

          {/* Generated Content */}
          {generated && (
            <div className="glass-card">
              <Tabs defaultValue="hooks" className="w-full">
                <TabsList className="grid w-full grid-cols-4">
                  <TabsTrigger value="hooks">Hooks</TabsTrigger>
                  <TabsTrigger value="headlines">Headlines</TabsTrigger>
                  <TabsTrigger value="ctas">CTAs</TabsTrigger>
                  <TabsTrigger value="captions">Captions</TabsTrigger>
                </TabsList>

                {/* Hooks */}
                <TabsContent value="hooks" className="space-y-4 mt-6">
                  <div className="flex items-center justify-between mb-4">
                    <p className="text-sm text-muted-foreground">
                      Attention-grabbing hooks to start your content:
                    </p>
                    <Button variant="ghost" size="sm">
                      <RefreshCw className="h-4 w-4 mr-1" />
                      Regenerate
                    </Button>
                  </div>

                  {[
                    'Wait until the end...',
                    'This changed everything for me...',
                    'Nobody talks about this but...',
                    'Most people get this wrong...',
                    'Here\'s what they don\'t want you to know...',
                  ].map((hook, i) => (
                    <div
                      key={i}
                      className="p-4 rounded-lg bg-muted/30 flex items-start justify-between gap-4 hover:bg-muted/50 transition-colors group"
                    >
                      <p className="text-sm font-medium flex-1">{hook}</p>
                      <Button
                        variant="ghost"
                        size="sm"
                        className="opacity-0 group-hover:opacity-100 transition-opacity shrink-0"
                      >
                        <Copy className="h-4 w-4" />
                      </Button>
                    </div>
                  ))}
                </TabsContent>

                {/* Headlines */}
                <TabsContent value="headlines" className="space-y-4 mt-6">
                  <div className="flex items-center justify-between mb-4">
                    <p className="text-sm text-muted-foreground">
                      Compelling headlines for your posts:
                    </p>
                    <Button variant="ghost" size="sm">
                      <RefreshCw className="h-4 w-4 mr-1" />
                      Regenerate
                    </Button>
                  </div>

                  {[
                    '🚀 The Ultimate Guide to Viral Content',
                    '5 Secrets Top Creators Don\'t Want You to Know',
                    'How I Grew From 0 to 100K in 90 Days',
                    'The Truth About Success Nobody Tells You',
                    'Stop Wasting Time: The Shortcut Guide',
                  ].map((headline, i) => (
                    <div
                      key={i}
                      className="p-4 rounded-lg bg-muted/30 flex items-start justify-between gap-4 hover:bg-muted/50 transition-colors group"
                    >
                      <p className="text-sm font-medium flex-1">{headline}</p>
                      <Button
                        variant="ghost"
                        size="sm"
                        className="opacity-0 group-hover:opacity-100 transition-opacity shrink-0"
                      >
                        <Copy className="h-4 w-4" />
                      </Button>
                    </div>
                  ))}
                </TabsContent>

                {/* CTAs */}
                <TabsContent value="ctas" className="space-y-4 mt-6">
                  <div className="flex items-center justify-between mb-4">
                    <p className="text-sm text-muted-foreground">
                      Call-to-action prompts to drive engagement:
                    </p>
                    <Button variant="ghost" size="sm">
                      <RefreshCw className="h-4 w-4 mr-1" />
                      Regenerate
                    </Button>
                  </div>

                  {[
                    'Drop a 🔥 if you agree!',
                    'Comment your biggest takeaway below 👇',
                    'Tap the link in bio to learn more',
                    'Who do you want to see this content?',
                    'Save this post for later!',
                  ].map((cta, i) => (
                    <div
                      key={i}
                      className="p-4 rounded-lg bg-muted/30 flex items-start justify-between gap-4 hover:bg-muted/50 transition-colors group"
                    >
                      <p className="text-sm flex-1">{cta}</p>
                      <Button
                        variant="ghost"
                        size="sm"
                        className="opacity-0 group-hover:opacity-100 transition-opacity shrink-0"
                      >
                        <Copy className="h-4 w-4" />
                      </Button>
                    </div>
                  ))}
                </TabsContent>

                {/* Captions */}
                <TabsContent value="captions" className="space-y-4 mt-6">
                  <div className="flex items-center justify-between mb-4">
                    <p className="text-sm text-muted-foreground">
                      Full captions ready to post:
                    </p>
                    <Button variant="ghost" size="sm">
                      <RefreshCw className="h-4 w-4 mr-1" />
                      Regenerate
                    </Button>
                  </div>

                  {[1, 2, 3].map((i) => (
                    <div
                      key={i}
                      className="p-4 rounded-lg bg-muted/30 hover:bg-muted/50 transition-colors group"
                    >
                      <div className="flex items-start justify-between gap-4 mb-3">
                        <p className="text-xs font-semibold text-primary">
                          Option {i}
                        </p>
                        <Button
                          variant="ghost"
                          size="sm"
                          className="opacity-0 group-hover:opacity-100 transition-opacity"
                        >
                          <Copy className="h-4 w-4" />
                        </Button>
                      </div>
                      <p className="text-sm leading-relaxed">
                        Here&apos;s a complete caption with hooks, value prop, and CTA. This
                        engaging copy is designed to maximize reach and engagement based on
                        platform algorithms and current trending patterns...
                      </p>
                      <div className="mt-3 flex gap-2 flex-wrap">
                        {['#AI', '#Creator', '#Viral'].map((tag) => (
                          <span
                            key={tag}
                            className="text-xs px-2 py-1 rounded-full bg-primary/10 text-primary"
                          >
                            {tag}
                          </span>
                        ))}
                      </div>
                    </div>
                  ))}
                </TabsContent>
              </Tabs>
            </div>
          )}
        </div>
      </main>
    </div>
  )
}
