#!/usr/bin/env python3
"""
AI Social Media Writer MVP - Demo Version
=========================================

A lightweight demo of the AI-powered social media automation tool.
This version shows the core functionality without requiring external APIs.

Usage:
    python demo_mvp.py --help
    python demo_mvp.py --demo
    python demo_mvp.py --generate
"""

import os
import sys
import argparse
import json
import random
from datetime import datetime
from typing import List, Dict, Any

# Demo data and functionality
class DemoSocialMediaAI:
    """Demo version of the AI Social Media Writer"""
    
    def __init__(self):
        self.demo_posts = [
            {
                'content': 'Just launched my new AI project! Excited to see where this journey takes me 🚀 #AI #startup',
                'platform': 'twitter',
                'engagement': {'likes': 45, 'retweets': 12, 'replies': 8},
                'created_at': '2024-01-15T10:30:00Z'
            },
            {
                'content': 'Working late but loving every minute of it. There\'s something magical about coding in the quiet hours ✨',
                'platform': 'twitter', 
                'engagement': {'likes': 23, 'retweets': 5, 'replies': 3},
                'created_at': '2024-01-14T23:15:00Z'
            },
            {
                'content': 'Coffee + Code + Creativity = Perfect Sunday morning ☕️ What\'s your weekend coding fuel?',
                'platform': 'twitter',
                'engagement': {'likes': 67, 'retweets': 18, 'replies': 15},
                'created_at': '2024-01-14T09:00:00Z'
            },
            {
                'content': 'Reflecting on 2023: built 3 products, learned 5 new technologies, made countless mistakes, and grew tremendously. Here\'s to an even better 2024! 🎯',
                'platform': 'linkedin',
                'engagement': {'likes': 120, 'comments': 25, 'shares': 8},
                'created_at': '2024-01-01T12:00:00Z'
            }
        ]
        
        self.style_profile = None
        self.generated_content = []
    
    def demo_workflow(self):
        """Run a complete demo workflow"""
        print("🤖 AI Social Media Writer MVP - Demo")
        print("=" * 50)
        print()
        
        # Step 1: Analyze writing style
        print("📊 Step 1: Analyzing writing style...")
        self.analyze_writing_style_demo()
        
        # Step 2: Generate content
        print("\n✨ Step 2: Generating content...")
        self.generate_content_demo(3)
        
        # Step 3: Show analytics
        print("\n📈 Step 3: Analytics overview...")
        self.show_analytics_demo()
        
        print("\n🎉 Demo complete! This shows the core functionality of the AI Social Media Writer.")
        print("\nTo get the full version with real APIs, follow the setup instructions in README.md")
    
    def analyze_writing_style_demo(self):
        """Demo writing style analysis"""
        print("  📝 Analyzing your previous posts...")
        
        # Simple analysis
        total_posts = len(self.demo_posts)
        avg_length = sum(len(post['content']) for post in self.demo_posts) / total_posts
        total_engagement = sum(
            sum(post['engagement'].values()) for post in self.demo_posts
        )
        
        # Count emojis and hashtags
        all_content = ' '.join(post['content'] for post in self.demo_posts)
        emoji_count = sum(1 for char in all_content if ord(char) > 127)
        hashtag_count = all_content.count('#')
        
        # Determine dominant tone (simplified)
        positive_words = ['excited', 'amazing', 'love', 'perfect', 'great', 'magical']
        positive_count = sum(all_content.lower().count(word) for word in positive_words)
        
        self.style_profile = {
            'total_posts': total_posts,
            'avg_length': avg_length,
            'total_engagement': total_engagement,
            'avg_engagement': total_engagement / total_posts,
            'emoji_usage': emoji_count / len(all_content),
            'hashtag_usage': hashtag_count / total_posts,
            'dominant_tone': 'positive' if positive_count > 2 else 'neutral',
            'topics': ['AI', 'coding', 'startup', 'technology', 'productivity'],
            'preferred_times': ['morning', 'late_night'],
            'analysis_date': datetime.now().isoformat()
        }
        
        print(f"  ✅ Analyzed {total_posts} posts")
        print(f"  📏 Average length: {avg_length:.0f} characters")
        print(f"  💬 Average engagement: {total_engagement / total_posts:.1f} interactions")
        print(f"  😊 Dominant tone: {self.style_profile['dominant_tone']}")
        print(f"  🔥 Top topics: {', '.join(self.style_profile['topics'][:3])}")
        print(f"  ⏰ Best posting times: {', '.join(self.style_profile['preferred_times'])}")
    
    def generate_content_demo(self, count: int = 3):
        """Demo content generation"""
        if not self.style_profile:
            self.analyze_writing_style_demo()
        
        print(f"  🎯 Generating {count} posts in your style...")
        
        # Content templates that match the analyzed style
        templates = [
            "Just discovered {topic}! This could be a game-changer for {field} 🚀 #innovation",
            "Late night thoughts: {insight} ✨ What do you think?",
            "Weekend project update: Working on {project}. {emotion} to see where this goes! 💪",
            "Coffee fueled coding session: {achievement} ☕️ Small wins count! #coding",
            "Reflecting on {topic}: {lesson}. Growth never stops 🌱",
            "Building in public: {update}. The journey is just as important as the destination 🎯"
        ]
        
        topics = self.style_profile['topics']
        insights = [
            "the best solutions often come from the simplest approaches",
            "consistency beats perfection every time",
            "learning in public accelerates growth",
            "small experiments lead to big breakthroughs"
        ]
        
        emotions = ["Excited", "Thrilled", "Curious", "Motivated"]
        achievements = ["solved a tricky bug", "implemented a new feature", "optimized performance"]
        lessons = [
            "every failure is a learning opportunity",
            "community support makes all the difference", 
            "persistence is the key to breakthrough moments"
        ]
        
        self.generated_content = []
        
        for i in range(count):
            template = random.choice(templates)
            
            # Fill template with appropriate content
            content = template.format(
                topic=random.choice(topics),
                field=random.choice(['developers', 'startups', 'creators', 'entrepreneurs']),
                insight=random.choice(insights),
                emotion=random.choice(emotions),
                project=random.choice(['an AI tool', 'a new app', 'a cool feature']),
                achievement=random.choice(achievements),
                lesson=random.choice(lessons),
                update=random.choice(['made good progress', 'hit a milestone', 'learned something new'])
            )
            
            # Determine platforms
            if len(content) <= 280:
                platforms = ['twitter']
            else:
                platforms = ['linkedin']
            
            if '#' in content or '🚀' in content:
                platforms.append('instagram')
            
            post = {
                'content': content,
                'platforms': platforms,
                'style_score': random.uniform(0.75, 0.95),
                'strategy': random.choice(['trending', 'personal', 'insight']),
                'needs_image': random.choice([True, False]),
                'generated_at': datetime.now().isoformat()
            }
            
            self.generated_content.append(post)
            print(f"  ✅ Generated post {i+1}: {content[:50]}...")
        
        print(f"\n  📋 Generated Content Preview:")
        for i, post in enumerate(self.generated_content, 1):
            print(f"\n  Post {i}:")
            print(f"    Content: {post['content']}")
            print(f"    Platforms: {', '.join(post['platforms'])}")
            print(f"    Style Score: {post['style_score']:.2f}")
            print(f"    Strategy: {post['strategy']}")
    
    def show_analytics_demo(self):
        """Demo analytics display"""
        if not self.style_profile:
            return
        
        print("  📊 Performance Analytics:")
        print(f"    • Total posts analyzed: {self.style_profile['total_posts']}")
        print(f"    • Average engagement rate: {(self.style_profile['avg_engagement'] / 100) * 100:.1f}%")
        print(f"    • Content generated: {len(self.generated_content)}")
        print(f"    • Average style score: {sum(p['style_score'] for p in self.generated_content) / len(self.generated_content):.2f}")
        
        print(f"\n  🎯 Optimization Insights:")
        print(f"    • Your content performs best with {self.style_profile['dominant_tone']} tone")
        print(f"    • Emoji usage: {self.style_profile['emoji_usage']:.1%} - consider {'increasing' if self.style_profile['emoji_usage'] < 0.1 else 'maintaining'}")
        print(f"    • Top performing topics: {', '.join(self.style_profile['topics'][:3])}")
        print(f"    • Best posting times: {', '.join(self.style_profile['preferred_times'])}")

def main():
    """Main demo function"""
    parser = argparse.ArgumentParser(description='AI Social Media Writer MVP Demo')
    parser.add_argument('--demo', action='store_true', help='Run complete demo workflow')
    parser.add_argument('--analyze', action='store_true', help='Demo writing style analysis')
    parser.add_argument('--generate', type=int, default=3, help='Demo content generation')
    parser.add_argument('--analytics', action='store_true', help='Show analytics demo')
    
    args = parser.parse_args()
    
    # Create demo instance
    demo = DemoSocialMediaAI()
    
    if args.demo:
        demo.demo_workflow()
    elif args.analyze:
        demo.analyze_writing_style_demo()
    elif args.generate:
        demo.generate_content_demo(args.generate)
    elif args.analytics:
        demo.analyze_writing_style_demo()  # Need profile first
        demo.show_analytics_demo()
    else:
        parser.print_help()
        print("\n💡 Quick start: python demo_mvp.py --demo")

if __name__ == "__main__":
    main()