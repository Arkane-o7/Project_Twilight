#!/usr/bin/env python3
"""
Demo script for AI Social Media Twin
Showcases functionality with sample data
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from style_analyzer import StyleAnalyzer, create_sample_style_profile, create_sample_tweets
import json

def main():
    print("🤖 AI Social Media Twin - Demo")
    print("=" * 50)
    
    # Create sample data
    print("\n📊 Sample Tweet Analysis")
    print("-" * 30)
    
    tweets = create_sample_tweets()
    print(f"Sample tweets from a developer's profile ({len(tweets)} tweets):\n")
    
    for i, tweet in enumerate(tweets[:3], 1):
        print(f"{i}. {tweet}")
    
    print(f"\n... and {len(tweets) - 3} more tweets")
    
    # Show style analysis
    print("\n🧠 AI Style Analysis")
    print("-" * 30)
    
    style_profile = create_sample_style_profile()
    
    print("Writing Style Profile:")
    print(f"• Tone: {style_profile['tone']}")
    print(f"• Topics: {', '.join(style_profile['topics'][:3])}")
    print(f"• Vocabulary: {style_profile['vocabulary_level']}")
    print(f"• Emoji Usage: {style_profile['emoji_usage']}")
    print(f"• Writing Patterns: {', '.join(style_profile['writing_patterns'][:2])}")
    
    # Show content generation (simulated)
    print("\n✨ Generated Content (Simulated)")
    print("-" * 30)
    
    sample_generated_posts = [
        "Building an MVP? Skip the perfect code and focus on solving the real problem. Your users don't care about your clean architecture if it doesn't work 😅 #startup #mvp",
        
        "Hot take: Documentation is just future you being kind to present you. Write it like you're explaining to someone who'll be debugging at 2 AM... because you will be 🌙 #devlife",
        
        "Three stages of startup life: 1) This will change everything! 2) Why isn't this working? 3) Oh wait, now it's working... but differently than planned 🚀 #entrepreneurship"
    ]
    
    print("Generated posts matching the analyzed style:")
    print("Topic: 'startup advice'\n")
    
    for i, post in enumerate(sample_generated_posts, 1):
        print(f"{i}. {post}")
        print()
    
    print("\n🎯 Key Features Demonstrated:")
    print("✅ Style analysis from social media posts")
    print("✅ Writing pattern recognition")
    print("✅ Content generation matching personal voice")
    print("✅ Topic-based content creation")
    
    print("\n🚀 To try with real data:")
    print("1. Set up API keys in .env file")
    print("2. Run: streamlit run app.py")
    print("3. Enter any Twitter username")
    print("4. Generate authentic content!")
    
    print("\n💡 Business Value:")
    print("• Content creators: Maintain consistent voice")
    print("• Businesses: Scale authentic social media")
    print("• Agencies: Create content for multiple clients")
    print("• Individuals: Never run out of post ideas")

if __name__ == "__main__":
    main()