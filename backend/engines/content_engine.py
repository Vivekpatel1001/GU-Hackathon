"""
Content Generation Engine - AI-powered content creator for captions, 
hashtags, SEO keywords, hooks, and headlines.
"""
import random
import logging
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
from backend.config import PLATFORM_CONFIGS, CONTENT_CATEGORIES, TONES

logger = logging.getLogger(__name__)


class ContentEngine:
    """AI content generation engine for multi-platform optimization."""
    
    # Hook templates by tone
    HOOKS = {
        "viral": [
            "🔥 You won't believe what happened when I tried {topic}...",
            "STOP scrolling! This {topic} hack changes everything 👇",
            "Nobody is talking about this {topic} secret...",
            "I tested {topic} for 30 days and the results are INSANE",
            "POV: You just discovered the best {topic} tip ever",
            "The {topic} industry doesn't want you to know this 🤫"
        ],
        "professional": [
            "Here's what 10 years in {topic} taught me...",
            "The data-driven approach to {topic} that top brands use",
            "3 proven strategies to master {topic} in 2026",
            "{topic}: A comprehensive guide for professionals",
            "Why 90% of {topic} strategies fail (and how to fix yours)",
            "The future of {topic}: Key insights and predictions"
        ],
        "casual": [
            "let's talk about {topic} because why not 😂",
            "ok but can we appreciate how cool {topic} is?",
            "me: I should be productive. also me: *researches {topic}*",
            "that moment when {topic} actually works 🙌",
            "ngl {topic} is my new obsession and here's why",
            "friendly reminder that {topic} exists and it's amazing ✨"
        ],
        "humorous": [
            "My therapist said I need to stop talking about {topic}. So anyway...",
            "{topic} walked so we could run 🏃‍♂️💨",
            "If {topic} was a person, I'd marry them. No cap.",
            "Tell me you love {topic} without telling me 😂",
            "Plot twist: {topic} was the answer all along 🤯",
            "Me explaining {topic} to someone who didn't ask 📢"
        ],
        "inspirational": [
            "Your journey with {topic} starts today. Here's how 🌟",
            "Don't let anyone tell you {topic} isn't possible",
            "Every expert was once a beginner. Master {topic} step by step",
            "The secret to {topic}? Consistency beats perfection every time",
            "Transform your approach to {topic} with these mindset shifts",
            "Believe in your {topic} journey — results are coming 💪"
        ]
    }
    
    # Caption templates
    CAPTIONS = {
        "instagram": {
            "Reel": [
                "✨ {hook}\n\n{body}\n\n💬 Drop a {emoji} if you agree!\n\n{hashtags}",
                "🎬 {hook}\n\n{body}\n\n👉 Save this for later!\n\n{hashtags}",
                "🔥 {hook}\n\n{body}\n\n🔄 Share with someone who needs this\n\n{hashtags}"
            ],
            "Photo": [
                "📸 {hook}\n\n{body}\n\n💡 What are your thoughts? Comment below!\n\n{hashtags}",
                "🌟 {hook}\n\n{body}\n\n❤️ Double tap if this resonates!\n\n{hashtags}"
            ],
            "Carousel": [
                "📚 SWIPE for the full guide 👉\n\n{hook}\n\n{body}\n\n💾 Save & Share!\n\n{hashtags}",
                "1/{total} — {hook}\n\n{body}\n\n📌 Bookmark this carousel!\n\n{hashtags}"
            ],
            "Story": [
                "Quick story time! 📖\n\n{hook}\n\n{body}",
                "🔔 Don't miss this!\n\n{hook}\n\n{body}"
            ],
            "Video": [
                "🎥 New video alert!\n\n{hook}\n\n{body}\n\n🔗 Full video link in bio!\n\n{hashtags}",
                "📹 Watch till the end!\n\n{hook}\n\n{body}\n\n{hashtags}"
            ]
        },
        "youtube": {
            "title": [
                "{hook} | {topic} Guide 2026",
                "How to {topic} Like a Pro (Step-by-Step)",
                "{topic}: Everything You Need to Know in 2026",
                "I Tried {topic} for 30 Days — Here's What Happened",
                "The ULTIMATE {topic} Tutorial (Beginners to Pro)"
            ],
            "description": [
                "🎬 In this video, I'm sharing everything about {topic}.\n\n{body}\n\n⏰ Timestamps:\n0:00 - Introduction\n1:30 - Key Concepts\n5:00 - Practical Tips\n10:00 - Results\n\n📌 Key Takeaways:\n{takeaways}\n\n🔔 Subscribe for more {topic} content!\n\n##{topic_tag} #tutorial #howto"
            ]
        },
        "twitter": {
            "single": [
                "{hook}\n\n{body_short}",
                "🧵 {hook}\n\n{body_short}\n\n♻️ RT to help others!",
                "💡 {hook}\n\n{body_short}\n\nAgree? 🤔"
            ],
            "thread": [
                "🧵 THREAD: {topic} — Everything you need to know\n\n1/ {hook}",
                "🔥 Let me break down {topic} for you\n\n1/ {hook}",
                "📚 {topic} masterclass in tweets:\n\n1/ {hook}"
            ],
            "question": [
                "What's your take on {topic}? 🤔\n\n{body_short}",
                "Hot take: {hook}\n\nAgree or disagree? 👇",
                "If you could change one thing about {topic}, what would it be? 💭"
            ]
        }
    }
    
    HASHTAG_TEMPLATES = {
        "Technology": ["#tech", "#technology", "#innovation", "#digital", "#AI", "#coding", "#startup", "#software", "#gadgets", "#techlife"],
        "Fashion": ["#fashion", "#style", "#ootd", "#fashionista", "#outfit", "#trending", "#streetstyle", "#fashionblogger", "#lookoftheday", "#styleinspo"],
        "Beauty": ["#beauty", "#skincare", "#makeup", "#beautytips", "#glowup", "#selfcare", "#beautyhacks", "#skincareroutine", "#cosmetics", "#beautyreview"],
        "Food": ["#food", "#foodie", "#recipe", "#cooking", "#homemade", "#foodporn", "#healthyfood", "#delicious", "#foodblogger", "#instafood"],
        "Travel": ["#travel", "#wanderlust", "#explore", "#travelgram", "#adventure", "#vacation", "#travelphotography", "#tourist", "#instatravel", "#worldtravel"],
        "Fitness": ["#fitness", "#gym", "#workout", "#fitlife", "#health", "#motivation", "#exercise", "#bodybuilding", "#fitnessmotivation", "#training"],
        "Music": ["#music", "#musician", "#newmusic", "#song", "#artist", "#musiclover", "#singer", "#producer", "#beats", "#musicvideo"],
        "Comedy": ["#comedy", "#funny", "#humor", "#lol", "#memes", "#comedyclub", "#standup", "#funnyvideos", "#laughs", "#hilarious"],
        "Photography": ["#photography", "#photo", "#photooftheday", "#photographer", "#camera", "#nature", "#portrait", "#streetphotography", "#art", "#instagood"],
        "Lifestyle": ["#lifestyle", "#life", "#inspiration", "#motivation", "#daily", "#mindset", "#wellness", "#livingmybestlife", "#positivevibes", "#growth"]
    }
    
    SEO_KEYWORDS = {
        "Technology": ["tech review", "best gadgets 2026", "coding tutorial", "AI tools", "software development", "tech tips", "startup advice"],
        "Fashion": ["fashion trends 2026", "outfit ideas", "style guide", "wardrobe essentials", "fashion haul", "seasonal fashion"],
        "Food": ["easy recipes", "cooking tips", "healthy meals", "meal prep", "food review", "restaurant recommendations"],
        "Fitness": ["workout routine", "fitness tips", "weight loss", "muscle building", "home workout", "gym tutorial"],
        "Travel": ["travel guide", "best destinations 2026", "budget travel", "travel tips", "hidden gems", "travel vlog"],
    }
    
    def generate_content(self, topic: str, platform: str, tone: str = "casual", 
                        content_type: str = None, target_audience: str = None,
                        niche: str = None) -> dict:
        """Generate optimized content for any platform."""
        
        tone = tone.lower() if tone else "casual"
        if tone not in self.HOOKS:
            tone = "casual"
        
        platform = platform.lower()
        hook = random.choice(self.HOOKS[tone]).format(topic=topic)
        
        result = {
            "platform": platform,
            "topic": topic,
            "tone": tone,
            "hook": hook,
        }
        
        if platform == "instagram":
            result.update(self._generate_instagram_content(topic, tone, content_type, niche, hook))
        elif platform == "youtube":
            result.update(self._generate_youtube_content(topic, tone, hook))
        elif platform in ("twitter", "x"):
            result.update(self._generate_twitter_content(topic, tone, content_type, hook))
        else:
            result.update(self._generate_generic_content(topic, tone, hook))
        
        return result
    
    def _generate_instagram_content(self, topic, tone, content_type, niche, hook):
        ct = content_type or "Reel"
        niche = niche or "Lifestyle"
        
        body = self._generate_body(topic, tone, platform="instagram")
        hashtags = self._generate_hashtags(topic, niche)
        emoji = random.choice(["🔥", "💯", "✨", "❤️", "🙌", "👏", "💪", "🎯"])
        
        templates = self.CAPTIONS["instagram"].get(ct, self.CAPTIONS["instagram"]["Reel"])
        caption = random.choice(templates).format(
            hook=hook, body=body, hashtags=hashtags, emoji=emoji, total=5
        )
        
        peak_hours = PLATFORM_CONFIGS["instagram"]["peak_hours"]
        best_time = random.choice(peak_hours)
        
        return {
            "caption": caption,
            "hashtags": hashtags,
            "content_type": ct,
            "best_posting_time": f"{best_time}:00",
            "improvements": [
                f"Use trending audio for {ct}s to boost reach",
                "Add a clear CTA (Call to Action) in caption",
                f"Post at {best_time}:00 for maximum engagement",
                "Use location tags to increase discoverability",
                "Engage with comments within the first 30 minutes"
            ],
            "seo_keywords": self.SEO_KEYWORDS.get(niche, [f"{topic} tips", f"best {topic}", f"{topic} 2026"])
        }
    
    def _generate_youtube_content(self, topic, tone, hook):
        title = random.choice(self.CAPTIONS["youtube"]["title"]).format(hook=hook, topic=topic)
        
        body = self._generate_body(topic, tone, platform="youtube", long=True)
        takeaways = "\n".join([
            f"✅ {topic} fundamentals explained",
            f"✅ Advanced {topic} techniques",
            f"✅ Common mistakes to avoid",
            f"✅ Real-world {topic} examples"
        ])
        topic_tag = topic.lower().replace(" ", "")
        
        description = self.CAPTIONS["youtube"]["description"][0].format(
            topic=topic, body=body, takeaways=takeaways, topic_tag=topic_tag
        )
        
        keywords = [f"{topic} tutorial", f"how to {topic}", f"{topic} 2026", 
                    f"best {topic}", f"{topic} tips", f"{topic} for beginners",
                    f"{topic} guide", f"learn {topic}", f"{topic} explained"]
        
        return {
            "title": title,
            "description": description,
            "tags": keywords,
            "thumbnail_suggestion": f"Bold text '{topic.upper()}' with contrasting colors, expressive face, and arrow pointing to key element",
            "engagement_tips": [
                "Add end screens linking to related videos",
                "Include cards at key moments",
                "Ask viewers to comment their experience",
                "Use chapters/timestamps for SEO",
                "Pin a comment with a question to boost engagement"
            ]
        }
    
    def _generate_twitter_content(self, topic, tone, tweet_type, hook):
        tt = tweet_type or "single"
        body_short = self._generate_body(topic, tone, platform="twitter", short=True)
        
        templates = self.CAPTIONS["twitter"].get(tt, self.CAPTIONS["twitter"]["single"])
        tweet = random.choice(templates).format(
            hook=hook, topic=topic, body_short=body_short
        )
        
        # Generate thread if requested
        thread = None
        if tt == "thread":
            thread = self._generate_thread(topic, tone, hook)
        
        improved = self._improve_tweet(tweet, tone)
        
        return {
            "tweet": tweet,
            "improved_tweet": improved,
            "thread": thread,
            "character_count": len(tweet),
            "engagement_suggestions": [
                "Tweet during 9 AM, 12 PM, or 5 PM for max visibility",
                "Use 1-2 relevant hashtags (not more)",
                "Quote tweet your own post after 4 hours",
                "Reply to comments to boost algorithm ranking",
                "Use polls or questions to increase engagement"
            ]
        }
    
    def _generate_generic_content(self, topic, tone, hook):
        return {
            "caption": f"{hook}\n\n{self._generate_body(topic, tone)}",
            "hashtags": self._generate_hashtags(topic),
            "ideas": [
                f"Create a how-to guide about {topic}",
                f"Share a personal story about {topic}",
                f"Compare top tools/products in {topic}",
                f"Interview an expert in {topic}",
                f"Create a challenge related to {topic}"
            ]
        }
    
    def _generate_body(self, topic, tone, platform="generic", long=False, short=False):
        if short:
            bodies = {
                "viral": f"This {topic} strategy is game-changing. Most people overlook it but the results speak for themselves.",
                "professional": f"After extensive research on {topic}, here are the key findings that every professional should know.",
                "casual": f"Honestly, {topic} has been on my mind lately and I had to share my thoughts with you all.",
                "humorous": f"So I went down the {topic} rabbit hole at 2 AM and now I have opinions. Many opinions.",
                "inspirational": f"Your {topic} journey is unique. Embrace it, learn from it, and watch yourself grow."
            }
            return bodies.get(tone, bodies["casual"])
        
        if long:
            return (
                f"In today's comprehensive guide, we're diving deep into {topic}. "
                f"Whether you're a complete beginner or an experienced professional, "
                f"this content will help you level up your understanding and skills.\n\n"
                f"We'll cover the fundamentals, advanced strategies, common pitfalls to avoid, "
                f"and real-world examples that demonstrate these concepts in action.\n\n"
                f"By the end, you'll have a clear roadmap for mastering {topic} "
                f"and implementing these strategies in your own projects."
            )
        
        bodies = {
            "viral": f"Here's the truth about {topic} that nobody's telling you. I've spent months testing different approaches, and these results completely changed my perspective. Read this carefully — it might just change yours too.",
            "professional": f"After analyzing the latest data and industry trends, here are my key insights on {topic}. These findings are backed by research and real-world application across multiple case studies.",
            "casual": f"So I've been really into {topic} lately and honestly? It's been a game-changer. Here's what I've learned so far and why I think you should give it a shot too.",
            "humorous": f"Okay so {topic} is basically my entire personality now. I'm not sorry about it. Here's my totally unbiased and very professional take on the whole situation.",
            "inspirational": f"The journey of mastering {topic} isn't always easy, but it's always worth it. Every step forward, no matter how small, brings you closer to where you want to be. Here's what I've learned along the way."
        }
        return bodies.get(tone, bodies["casual"])
    
    def _generate_hashtags(self, topic, niche=None):
        base_tags = []
        if niche and niche in self.HASHTAG_TEMPLATES:
            base_tags = self.HASHTAG_TEMPLATES[niche][:7]
        
        topic_tags = [
            f"#{topic.lower().replace(' ', '')}",
            f"#{topic.lower().replace(' ', '')}tips",
            f"#{topic.lower().replace(' ', '')}2026",
            "#trending", "#viral", "#fyp", "#explore",
            "#contentcreator", "#digitalmarketing"
        ]
        
        all_tags = list(set(base_tags + topic_tags))[:15]
        return " ".join(all_tags)
    
    def _generate_thread(self, topic, tone, hook):
        tweets = [
            f"🧵 THREAD: Everything you need to know about {topic}\n\n1/ {hook}",
            f"2/ First, let's understand why {topic} matters in 2026. The landscape has changed dramatically, and those who adapt will thrive.",
            f"3/ The biggest mistake people make with {topic}? Starting without a clear strategy. Here's the framework I use:",
            f"4/ Step 1: Research your audience\nStep 2: Find your unique angle\nStep 3: Create valuable content\nStep 4: Engage consistently",
            f"5/ Here's the data that backs this up:\n• 73% improvement in engagement\n• 2.5x more reach\n• 40% higher retention",
            f"6/ The tools I recommend for {topic}:\n• Tool A for planning\n• Tool B for creation\n• Tool C for analytics",
            f"7/ Final thoughts: {topic} isn't a sprint, it's a marathon. Stay consistent and the results will follow.\n\n♻️ RT the first tweet to help others!\n\nFollow me for more {topic} insights 🔔"
        ]
        return tweets
    
    def _improve_tweet(self, tweet, tone):
        improvements = {
            "viral": "🚨 " + tweet.replace(".", "!"),
            "professional": tweet.replace("!", ".").replace("🔥", "📊"),
            "casual": tweet + " 💭",
            "humorous": tweet + " (and yes, I'm serious 😤)",
            "inspirational": "✨ " + tweet + " 🌟"
        }
        improved = improvements.get(tone, tweet)
        return improved[:280]
    
    def generate_ideas(self, topic: str, platform: str = "all", 
                      tone: str = "casual", target_audience: str = None) -> dict:
        """Generate multi-platform content ideas."""
        ideas = {
            "instagram": [
                f"📸 Before/After transformation of {topic}",
                f"🎬 Day-in-the-life Reel featuring {topic}",
                f"📚 5-slide Carousel: '{topic} 101'",
                f"💡 Quick tip Story about {topic}",
                f"🎯 Challenge: 7 days of {topic}",
                f"🤝 Collaboration post with a {topic} expert"
            ],
            "youtube": [
                f"🎬 Ultimate Beginner's Guide to {topic}",
                f"📊 {topic} in 2026: What's Changed?",
                f"⚡ 10 {topic} Hacks You Didn't Know",
                f"🔴 Live Q&A about {topic}",
                f"📈 {topic} Case Study: Real Results",
                f"🆚 {topic} Method A vs Method B"
            ],
            "twitter": [
                f"🧵 Thread: The complete guide to {topic}",
                f"📊 Poll: What's your biggest challenge with {topic}?",
                f"💡 Daily {topic} tip series",
                f"🎯 Hot take about {topic} trends",
                f"📚 Book recommendations for {topic}",
                f"🤔 Controversial opinion about {topic}"
            ]
        }
        
        strategy = {
            "content_pillars": [
                f"Educational: Teach {topic} concepts and tutorials",
                f"Entertainment: Fun, relatable {topic} content",
                f"Inspirational: Success stories and motivation",
                f"Community: Engage and build around {topic}"
            ],
            "posting_schedule": {
                "instagram": "4-5 times/week (Reels 3x, Carousel 1x, Stories daily)",
                "youtube": "2 videos/week (1 long-form, 1 short)",
                "twitter": "3-5 tweets/day (mix of threads, tips, engagement)"
            },
            "cross_platform": f"Create one {topic} piece, repurpose into 5+ formats across platforms"
        }
        
        return {
            "topic": topic,
            "content_ideas": ideas if platform == "all" else {platform: ideas.get(platform, [])},
            "strategy": strategy,
            "target_audience": target_audience or "General audience interested in " + topic
        }


# Global instance
content_engine = ContentEngine()
