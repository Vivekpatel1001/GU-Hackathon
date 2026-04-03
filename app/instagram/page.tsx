'use client'

import { useState } from 'react'
import { Sidebar } from '@/components/sidebar'
import { Navbar } from '@/components/navbar'
import { Button } from '@/components/ui/button'
import { Textarea } from '@/components/ui/textarea'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Copy, Sparkles } from 'lucide-react'

export default function InstagramPage() {
  const [caption, setCaption] = useState('')
  const [generated, setGenerated] = useState(false)

  const handleGenerate = () => {
    if (caption.trim()) {
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
            <h1 className="text-3xl font-bold">Instagram Optimizer</h1>
            <p className="text-muted-foreground mt-2">
              Create viral-worthy Instagram content with AI-powered suggestions
            </p>
          </div>

          {/* Main Content */}
          <div className="grid gap-6 lg:grid-cols-2">
            {/* Input Section */}
            <div className="glass-card">
              <h2 className="text-xl font-bold mb-4">Enter Your Idea</h2>
              <div className="space-y-4">
                <div>
                  <label className="text-sm font-medium">Caption / Reel Idea</label>
                  <Textarea
                    placeholder="Describe your Instagram post idea, reel concept, or caption..."
                    value={caption}
                    onChange={(e) => setCaption(e.target.value)}
                    className="min-h-32 bg-muted resize-none mt-2"
                  />
                </div>

                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="text-sm font-medium">Content Format</label>
                    <select className="w-full h-10 mt-2 px-3 rounded-lg bg-muted border border-border/50">
                      <option>Reel</option>
                      <option>Carousel</option>
                      <option>Story</option>
                      <option>Feed Post</option>
                    </select>
                  </div>
                  <div>
                    <label className="text-sm font-medium">Niche</label>
                    <select className="w-full h-10 mt-2 px-3 rounded-lg bg-muted border border-border/50">
                      <option>Tech</option>
                      <option>Fashion</option>
                      <option>Lifestyle</option>
                      <option>Finance</option>
                    </select>
                  </div>
                </div>

                <Button
                  onClick={handleGenerate}
                  className="w-full h-10 bg-gradient-to-r from-pink-600 to-rose-600 hover:from-pink-700 hover:to-rose-700 text-white border-0"
                >
                  <Sparkles className="mr-2 h-4 w-4" />
                  Generate Suggestions
                </Button>
              </div>
            </div>

            {/* Preview Section */}
            <div className="glass-card">
              <h2 className="text-xl font-bold mb-4">Instagram Preview</h2>
              <div className="rounded-2xl bg-gradient-to-br from-pink-500/20 to-purple-500/20 aspect-square flex items-center justify-center border-2 border-dashed border-border/50">
                <div className="text-center">
                  <p className="text-4xl mb-2">📸</p>
                  <p className="text-sm text-muted-foreground">Post preview appears here</p>
                </div>
              </div>
            </div>
          </div>

          {/* Generated Content */}
          {generated && (
            <div className="glass-card">
              <Tabs defaultValue="captions" className="w-full">
                <TabsList className="grid w-full grid-cols-4">
                  <TabsTrigger value="captions">Captions</TabsTrigger>
                  <TabsTrigger value="hashtags">Hashtags</TabsTrigger>
                  <TabsTrigger value="timing">Best Time</TabsTrigger>
                  <TabsTrigger value="format">Format</TabsTrigger>
                </TabsList>

                {/* Captions */}
                <TabsContent value="captions" className="space-y-4">
                  <p className="text-sm text-muted-foreground mb-4">
                    Generated captions optimized for engagement:
                  </p>
                  {[
                    '🚀 Just launched something incredible! Swipe up to see how we\'re revolutionizing the game. #Innovation #Creator',
                    '✨ Real talk: This is the future. Tap the link in bio to experience it firsthand. #Mindblown #TechLife',
                    '💡 If you\'ve been waiting for the perfect moment, this is it. Double tap if you agree! #GameChanger #Viral',
                  ].map((text, i) => (
                    <div
                      key={i}
                      className="p-4 rounded-lg bg-muted/30 flex items-start justify-between gap-4 hover:bg-muted/50 transition-colors"
                    >
                      <p className="text-sm flex-1">{text}</p>
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

                {/* Hashtags */}
                <TabsContent value="hashtags" className="space-y-4">
                  <p className="text-sm text-muted-foreground mb-4">
                    Trending hashtags for maximum reach:
                  </p>
                  <div className="flex flex-wrap gap-2">
                    {[
                      '#AI',
                      '#Innovation',
                      '#TechTok',
                      '#Creator',
                      '#Viral',
                      '#Trending',
                      '#FYP',
                      '#For You',
                      '#Explore',
                      '#InstagramReels',
                    ].map((tag) => (
                      <button
                        key={tag}
                        className="px-4 py-2 rounded-full bg-primary/10 text-primary hover:bg-primary/20 transition-colors text-sm font-medium"
                      >
                        {tag}
                      </button>
                    ))}
                  </div>
                </TabsContent>

                {/* Best Time */}
                <TabsContent value="timing" className="space-y-4">
                  <p className="text-sm text-muted-foreground mb-4">
                    Post at the optimal time for your audience:
                  </p>
                  <div className="p-4 rounded-lg bg-muted/30">
                    <p className="font-bold text-lg mb-2">Best Posting Time</p>
                    <p className="text-primary font-semibold">Tuesday at 8:30 PM</p>
                    <p className="text-sm text-muted-foreground mt-2">
                      Based on your audience's peak activity. Engagement rate increases by ~35%
                    </p>
                  </div>
                </TabsContent>

                {/* Format */}
                <TabsContent value="format" className="space-y-4">
                  <p className="text-sm text-muted-foreground mb-4">
                    Recommended content format:
                  </p>
                  <div className="space-y-3">
                    {[
                      { format: 'Reel', recommendation: 'Recommended - 15-30 seconds' },
                      { format: 'Carousel', recommendation: 'Good - 5-7 slides' },
                      { format: 'Feed Post', recommendation: 'OK - High-quality image' },
                    ].map((item) => (
                      <div
                        key={item.format}
                        className="p-3 rounded-lg bg-muted/30 flex items-start justify-between"
                      >
                        <div>
                          <p className="font-medium">{item.format}</p>
                          <p className="text-sm text-muted-foreground">
                            {item.recommendation}
                          </p>
                        </div>
                        <span className="text-lg">
                          {item.format === 'Reel' ? '⭐' : '✓'}
                        </span>
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
