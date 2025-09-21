"""
Social Media Platform Manager
Handles all social media integrations and operations
"""

import asyncio
from typing import Dict, List, Optional, Any
import logging
from datetime import datetime, timedelta

from .platforms.twitter import TwitterClient
from .platforms.instagram import InstagramClient
from .platforms.facebook import FacebookClient
from .platforms.linkedin import LinkedInClient

logger = logging.getLogger(__name__)

class SocialMediaManager:
    """Manages all social media platform integrations"""
    
    def __init__(self, config):
        self.config = config
        self.clients = {}
        self._initialize_clients()
    
    def _initialize_clients(self):
        """Initialize social media clients for configured platforms"""
        
        # Twitter
        if self.config.is_platform_configured('twitter'):
            try:
                self.clients['twitter'] = TwitterClient(self.config.get_social_media_config('twitter'))
                logger.info("Twitter client initialized")
            except Exception as e:
                logger.error(f"Failed to initialize Twitter client: {e}")
        
        # Instagram
        if self.config.is_platform_configured('instagram'):
            try:
                self.clients['instagram'] = InstagramClient(self.config.get_social_media_config('instagram'))
                logger.info("Instagram client initialized")
            except Exception as e:
                logger.error(f"Failed to initialize Instagram client: {e}")
        
        # Facebook
        if self.config.is_platform_configured('facebook'):
            try:
                self.clients['facebook'] = FacebookClient(self.config.get_social_media_config('facebook'))
                logger.info("Facebook client initialized")
            except Exception as e:
                logger.error(f"Failed to initialize Facebook client: {e}")
        
        # LinkedIn
        if self.config.is_platform_configured('linkedin'):
            try:
                self.clients['linkedin'] = LinkedInClient(self.config.get_social_media_config('linkedin'))
                logger.info("LinkedIn client initialized")
            except Exception as e:
                logger.error(f"Failed to initialize LinkedIn client: {e}")
    
    async def test_connections(self) -> Dict[str, bool]:
        """Test connections to all configured platforms"""
        results = {}
        
        for platform, client in self.clients.items():
            try:
                result = await client.test_connection()
                results[platform] = result
                logger.info(f"{platform.title()} connection: {'✅' if result else '❌'}")
            except Exception as e:
                logger.error(f"Error testing {platform} connection: {e}")
                results[platform] = False
        
        return results
    
    async def fetch_user_posts(self, platform: str, limit: int = 100) -> List[Dict]:
        """Fetch user's posts from a specific platform"""
        if platform not in self.clients:
            logger.warning(f"Platform {platform} not configured")
            return []
        
        try:
            posts = await self.clients[platform].get_user_posts(limit=limit)
            logger.info(f"Fetched {len(posts)} posts from {platform}")
            return posts
        except Exception as e:
            logger.error(f"Error fetching posts from {platform}: {e}")
            return []
    
    async def get_feed_posts(self, platform: str, limit: int = 20) -> List[Dict]:
        """Get posts from user's feed/timeline"""
        if platform not in self.clients:
            logger.warning(f"Platform {platform} not configured")
            return []
        
        try:
            posts = await self.clients[platform].get_feed_posts(limit=limit)
            logger.info(f"Fetched {len(posts)} feed posts from {platform}")
            return posts
        except Exception as e:
            logger.error(f"Error fetching feed from {platform}: {e}")
            return []
    
    async def post_content(self, platform: str, content: str, image_path: Optional[str] = None) -> bool:
        """Post content to a specific platform"""
        if platform not in self.clients:
            logger.warning(f"Platform {platform} not configured")
            return False
        
        try:
            result = await self.clients[platform].post_content(
                content=content,
                image_path=image_path
            )
            
            if result:
                logger.info(f"Successfully posted to {platform}")
            else:
                logger.error(f"Failed to post to {platform}")
            
            return result
        except Exception as e:
            logger.error(f"Error posting to {platform}: {e}")
            return False
    
    async def engage_with_post(self, platform: str, post_id: str, action: str, comment: Optional[str] = None) -> bool:
        """Engage with a post (like, comment, retweet, etc.)"""
        if platform not in self.clients:
            logger.warning(f"Platform {platform} not configured")
            return False
        
        try:
            result = await self.clients[platform].engage_with_post(
                post_id=post_id,
                action=action,
                comment=comment
            )
            
            if result:
                logger.info(f"Successfully engaged with post on {platform}")
            else:
                logger.error(f"Failed to engage with post on {platform}")
            
            return result
        except Exception as e:
            logger.error(f"Error engaging with post on {platform}: {e}")
            return False
    
    async def get_trending_topics(self, platform: str) -> List[str]:
        """Get trending topics from a platform"""
        if platform not in self.clients:
            logger.warning(f"Platform {platform} not configured")
            return []
        
        try:
            topics = await self.clients[platform].get_trending_topics()
            logger.info(f"Fetched {len(topics)} trending topics from {platform}")
            return topics
        except Exception as e:
            logger.error(f"Error fetching trending topics from {platform}: {e}")
            return []
    
    async def search_posts(self, platform: str, query: str, limit: int = 50) -> List[Dict]:
        """Search for posts on a platform"""
        if platform not in self.clients:
            logger.warning(f"Platform {platform} not configured")
            return []
        
        try:
            posts = await self.clients[platform].search_posts(query=query, limit=limit)
            logger.info(f"Found {len(posts)} posts for query '{query}' on {platform}")
            return posts
        except Exception as e:
            logger.error(f"Error searching posts on {platform}: {e}")
            return []
    
    def get_platform_stats(self, platform: str) -> Dict[str, Any]:
        """Get statistics for a platform"""
        if platform not in self.clients:
            return {}
        
        try:
            return self.clients[platform].get_stats()
        except Exception as e:
            logger.error(f"Error getting stats for {platform}: {e}")
            return {}
    
    def get_configured_platforms(self) -> List[str]:
        """Get list of configured platforms"""
        return list(self.clients.keys())