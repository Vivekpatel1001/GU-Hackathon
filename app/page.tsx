import { Sidebar } from '@/components/sidebar'
import { Navbar } from '@/components/navbar'
import { OverviewCards } from '@/components/dashboard/overview-cards'
import { TrendEngine } from '@/components/dashboard/trend-engine'
import { ViralPredictor } from '@/components/dashboard/viral-predictor'

export default function DashboardPage() {
  return (
    <div className="min-h-screen bg-background">
      {/* Sidebar */}
      <Sidebar />

      {/* Navbar */}
      <Navbar />

      {/* Main Content */}
      <main className="ml-64 mt-16 p-6">
        <div className="space-y-8">
          {/* Header */}
          <div>
            <h1 className="text-3xl font-bold">Welcome to ViralAI</h1>
            <p className="text-muted-foreground mt-2">
              Optimize your content and maximize your social media impact
            </p>
          </div>

          {/* Overview Cards */}
          <section>
            <OverviewCards />
          </section>

          {/* Main Content Grid */}
          <section className="grid gap-6 lg:grid-cols-3">
            {/* Left Column - Trend Engine */}
            <div className="lg:col-span-1">
              <TrendEngine />
            </div>

            {/* Right Column - Viral Predictor */}
            <div className="lg:col-span-2">
              <ViralPredictor />
            </div>
          </section>

          {/* Recent Activity / Quick Start */}
          <section>
            <div className="glass-card">
              <h2 className="text-xl font-bold mb-4">Quick Start Guides</h2>
              <div className="grid md:grid-cols-3 gap-4">
                {[
                  {
                    title: 'Instagram Optimization',
                    description: 'Create viral-worthy Instagram posts with AI suggestions',
                    icon: '📸',
                  },
                  {
                    title: 'YouTube SEO',
                    description: 'Generate optimized titles, descriptions, and hashtags',
                    icon: '🎬',
                  },
                  {
                    title: 'Twitter Threads',
                    description: 'Craft engaging Twitter threads that drive engagement',
                    icon: '𝕏',
                  },
                ].map((guide) => (
                  <div
                    key={guide.title}
                    className="p-4 rounded-lg bg-muted/30 hover:bg-muted/50 transition-colors cursor-pointer"
                  >
                    <p className="text-2xl mb-2">{guide.icon}</p>
                    <h3 className="font-semibold">{guide.title}</h3>
                    <p className="text-sm text-muted-foreground mt-1">
                      {guide.description}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          </section>
        </div>
      </main>
    </div>
  )
}
