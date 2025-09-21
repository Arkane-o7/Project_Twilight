#!/usr/bin/env python3
"""
AI Social Media Writer MVP
==========================

A comprehensive AI-powered social media automation tool that:
1. Analyzes your writing style from previous posts
2. Creates and posts content automatically
3. Engages with your audience (likes, comments, reactions)
4. Generates images for posts
5. Finds viral content and creates trending posts

This MVP uses free and open-source tools to build a production-ready solution.

Usage:
    python mvp_ai_social_media.py --setup    # Initial setup
    python mvp_ai_social_media.py --analyze  # Analyze writing style
    python mvp_ai_social_media.py --generate # Generate content
    python mvp_ai_social_media.py --post     # Auto-post content
    python mvp_ai_social_media.py --engage   # Auto-engage with audience
    python mvp_ai_social_media.py --ui       # Launch web interface

Author: Project Twilight Team
License: MIT
"""

import os
import sys
import argparse
import asyncio
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import json

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.core.config import Config
from src.core.logger import setup_logger
from src.social_media.manager import SocialMediaManager
from src.ai_engine.style_analyzer import StyleAnalyzer
from src.content_generation.generator import ContentGenerator
from src.image_processing.generator import ImageGenerator
from src.database.models import init_database
from src.ui.dashboard import launch_dashboard

# Global logger
logger = setup_logger(__name__)

class SocialMediaAI:
    """Main class for the AI Social Media Writer MVP"""
    
    def __init__(self):
        """Initialize the AI Social Media Writer"""
        self.config = Config()
        self.social_manager = SocialMediaManager(self.config)
        self.style_analyzer = StyleAnalyzer(self.config)
        self.content_generator = ContentGenerator(self.config)
        self.image_generator = ImageGenerator(self.config)
        
        # Initialize database
        init_database()
        logger.info("AI Social Media Writer initialized successfully")
    
    async def setup(self):
        """Initial setup and configuration"""
        logger.info("Starting initial setup...")
        
        print("🚀 Welcome to AI Social Media Writer MVP!")
        print("=" * 50)
        
        # Check API keys
        missing_keys = self._check_api_keys()
        if missing_keys:
            print("⚠️  Missing API keys:")
            for key in missing_keys:
                print(f"   - {key}")
            print("\nPlease add these to your .env file")
            return False
        
        # Test social media connections
        print("🔗 Testing social media connections...")
        connections = await self.social_manager.test_connections()
        
        for platform, status in connections.items():
            status_icon = "✅" if status else "❌"
            print(f"   {status_icon} {platform.title()}")
        
        print("\n✨ Setup complete! You can now:")
        print("   1. Analyze your writing style: --analyze")
        print("   2. Generate content: --generate")
        print("   3. Launch web interface: --ui")
        
        return True
    
    async def analyze_writing_style(self):
        """Analyze user's writing style from previous posts"""
        logger.info("Starting writing style analysis...")
        
        print("🔍 Analyzing your writing style...")
        
        # Fetch posts from all connected platforms
        all_posts = []
        for platform in ['twitter', 'instagram', 'facebook', 'linkedin']:
            try:
                posts = await self.social_manager.fetch_user_posts(platform, limit=100)
                all_posts.extend(posts)
                print(f"   📝 Fetched {len(posts)} posts from {platform.title()}")
            except Exception as e:
                logger.warning(f"Could not fetch posts from {platform}: {e}")
        
        if not all_posts:
            print("❌ No posts found. Please check your API connections.")
            return
        
        # Analyze writing style
        style_profile = await self.style_analyzer.analyze_posts(all_posts)
        
        print(f"\n📊 Analysis Results:")
        print(f"   • Posts analyzed: {len(all_posts)}")
        print(f"   • Average length: {style_profile.get('avg_length', 0)} characters")
        print(f"   • Tone: {style_profile.get('tone', 'Unknown')}")
        print(f"   • Top topics: {', '.join(style_profile.get('topics', [])[:3])}")
        print(f"   • Engagement style: {style_profile.get('engagement_style', 'Unknown')}")
        
        # Save profile
        self.style_analyzer.save_profile(style_profile)
        print("✅ Writing style profile saved!")
        
        return style_profile
    
    async def generate_content(self, count: int = 5):
        """Generate content based on analyzed style"""
        logger.info(f"Generating {count} pieces of content...")
        
        print(f"✨ Generating {count} pieces of content...")
        
        # Load style profile
        style_profile = self.style_analyzer.load_profile()
        if not style_profile:
            print("❌ No style profile found. Run --analyze first.")
            return
        
        # Find trending topics
        print("🔥 Finding trending topics...")
        trending_topics = await self.content_generator.get_trending_topics()
        
        generated_content = []
        for i in range(count):
            print(f"   📝 Generating post {i+1}/{count}...")
            
            # Generate text content
            content = await self.content_generator.generate_post(
                style_profile=style_profile,
                trending_topics=trending_topics
            )
            
            # Generate image if needed
            if content.get('needs_image'):
                print(f"   🖼️  Generating image for post {i+1}...")
                image_path = await self.image_generator.generate_image(
                    prompt=content['content'],
                    style=style_profile.get('visual_style', 'realistic')
                )
                content['image_path'] = image_path
            
            generated_content.append(content)
            print(f"   ✅ Post {i+1} generated")
        
        # Save generated content
        self._save_generated_content(generated_content)
        
        print(f"\n🎉 Generated {len(generated_content)} posts!")
        print("   Use --post to publish them or --ui to review and edit")
        
        return generated_content
    
    async def auto_post(self):
        """Automatically post generated content"""
        logger.info("Starting auto-posting...")
        
        print("📤 Starting auto-posting...")
        
        # Load generated content
        content_list = self._load_generated_content()
        if not content_list:
            print("❌ No generated content found. Run --generate first.")
            return
        
        posted_count = 0
        for content in content_list:
            if content.get('posted'):
                continue
            
            try:
                # Post to selected platforms
                platforms = content.get('platforms', ['twitter'])
                for platform in platforms:
                    result = await self.social_manager.post_content(
                        platform=platform,
                        content=content['content'],
                        image_path=content.get('image_path')
                    )
                    
                    if result:
                        print(f"   ✅ Posted to {platform.title()}")
                        content['posted'] = True
                        posted_count += 1
                    else:
                        print(f"   ❌ Failed to post to {platform.title()}")
                        
            except Exception as e:
                logger.error(f"Error posting content: {e}")
                print(f"   ❌ Error: {e}")
        
        # Save updated content
        self._save_generated_content(content_list)
        
        print(f"\n🎉 Posted {posted_count} pieces of content!")
    
    async def auto_engage(self):
        """Automatically engage with audience"""
        logger.info("Starting auto-engagement...")
        
        print("👥 Starting auto-engagement...")
        
        engagement_count = 0
        for platform in ['twitter', 'instagram', 'facebook', 'linkedin']:
            try:
                print(f"   🔍 Engaging on {platform.title()}...")
                
                # Get feed posts
                feed_posts = await self.social_manager.get_feed_posts(platform, limit=20)
                
                for post in feed_posts:
                    # Analyze if we should engage
                    should_engage = await self.content_generator.should_engage(post)
                    
                    if should_engage:
                        # Generate appropriate response
                        response = await self.content_generator.generate_response(
                            post=post,
                            style_profile=self.style_analyzer.load_profile()
                        )
                        
                        # Engage (like, comment, etc.)
                        result = await self.social_manager.engage_with_post(
                            platform=platform,
                            post_id=post['id'],
                            action=response['action'],
                            comment=response.get('comment')
                        )
                        
                        if result:
                            engagement_count += 1
                            print(f"   ✅ Engaged with post on {platform.title()}")
                
            except Exception as e:
                logger.warning(f"Error engaging on {platform}: {e}")
        
        print(f"\n🎉 Engaged with {engagement_count} posts!")
    
    def launch_ui(self):
        """Launch the web interface"""
        logger.info("Launching web interface...")
        
        print("🌐 Launching web interface...")
        print("   Opening dashboard at http://localhost:8501")
        
        # Launch Streamlit dashboard
        launch_dashboard(self)
    
    def _check_api_keys(self) -> List[str]:
        """Check for missing API keys"""
        required_keys = [
            'TWITTER_API_KEY',
            'OPENAI_API_KEY',
            'HUGGINGFACE_API_KEY'
        ]
        
        missing = []
        for key in required_keys:
            if not os.getenv(key):
                missing.append(key)
        
        return missing
    
    def _save_generated_content(self, content_list: List[Dict]):
        """Save generated content to file"""
        os.makedirs('data', exist_ok=True)
        with open('data/generated_content.json', 'w') as f:
            json.dump(content_list, f, indent=2, default=str)
    
    def _load_generated_content(self) -> List[Dict]:
        """Load generated content from file"""
        try:
            with open('data/generated_content.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

async def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='AI Social Media Writer MVP')
    parser.add_argument('--setup', action='store_true', help='Initial setup')
    parser.add_argument('--analyze', action='store_true', help='Analyze writing style')
    parser.add_argument('--generate', type=int, default=5, help='Generate content (default: 5 posts)')
    parser.add_argument('--post', action='store_true', help='Auto-post content')
    parser.add_argument('--engage', action='store_true', help='Auto-engage with audience')
    parser.add_argument('--ui', action='store_true', help='Launch web interface')
    parser.add_argument('--all', action='store_true', help='Run full automation cycle')
    
    args = parser.parse_args()
    
    # Initialize the AI
    ai = SocialMediaAI()
    
    if args.setup:
        await ai.setup()
    elif args.analyze:
        await ai.analyze_writing_style()
    elif args.generate:
        await ai.generate_content(args.generate)
    elif args.post:
        await ai.auto_post()
    elif args.engage:
        await ai.auto_engage()
    elif args.ui:
        ai.launch_ui()
    elif args.all:
        print("🤖 Running full automation cycle...")
        await ai.analyze_writing_style()
        await ai.generate_content(3)
        await ai.auto_post()
        await ai.auto_engage()
    else:
        parser.print_help()

if __name__ == "__main__":
    # Handle event loop for Windows compatibility
    if sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print(f"❌ Error: {e}")