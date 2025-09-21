"""
Instagram API Client
Handles Instagram operations using the Basic Display API
"""

import logging
from typing import Dict, List, Optional, Any
import requests

logger = logging.getLogger(__name__)

class InstagramClient:
    """Instagram API client"""
    
    def __init__(self, config: Dict[str, str]):
        self.config = config
        self.base_url = "https://graph.instagram.com"
        self.access_token = config.get('access_token')
    
    async def test_connection(self) -> bool:
        """Test Instagram API connection"""
        try:
            url = f"{self.base_url}/me"
            params = {'access_token': self.access_token, 'fields': 'id,username'}
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"Instagram connection successful for user: {data.get('username')}")
                return True
            return False
        except Exception as e:
            logger.error(f"Instagram connection test failed: {e}")
            return False
    
    async def get_user_posts(self, limit: int = 100) -> List[Dict]:
        """Get user's Instagram posts"""
        try:
            # Note: Instagram Basic Display API has limited functionality
            # For full posting capabilities, you need Instagram Graph API (business accounts)
            url = f"{self.base_url}/me/media"
            params = {
                'access_token': self.access_token,
                'fields': 'id,caption,media_type,media_url,permalink,timestamp',
                'limit': min(25, limit)  # API limit
            }
            
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                posts = []
                
                for item in data.get('data', []):
                    post = {
                        'id': item.get('id'),
                        'content': item.get('caption', ''),
                        'media_url': item.get('media_url'),
                        'created_at': item.get('timestamp'),
                        'platform': 'instagram',
                        'url': item.get('permalink'),
                        'media_type': item.get('media_type')
                    }
                    posts.append(post)
                
                return posts
            
            return []
        except Exception as e:
            logger.error(f"Error fetching Instagram posts: {e}")
            return []
    
    async def get_feed_posts(self, limit: int = 20) -> List[Dict]:
        """Get posts from user's Instagram feed (limited in Basic Display API)"""
        # Instagram Basic Display API doesn't provide feed access
        # This would require Instagram Graph API with proper permissions
        logger.warning("Instagram feed access requires Graph API")
        return []
    
    async def post_content(self, content: str, image_path: Optional[str] = None) -> bool:
        """Post content to Instagram (requires Graph API for businesses)"""
        # Instagram Basic Display API doesn't support posting
        # This requires Instagram Graph API with a business account
        logger.warning("Instagram posting requires Graph API and business account")
        return False
    
    async def engage_with_post(self, post_id: str, action: str, comment: Optional[str] = None) -> bool:
        """Engage with Instagram post (limited in Basic Display API)"""
        logger.warning("Instagram engagement requires Graph API")
        return False
    
    async def get_trending_topics(self) -> List[str]:
        """Get trending hashtags (not available in Basic Display API)"""
        logger.warning("Instagram trending topics require Graph API")
        return []
    
    async def search_posts(self, query: str, limit: int = 50) -> List[Dict]:
        """Search Instagram posts (not available in Basic Display API)"""
        logger.warning("Instagram search requires Graph API")
        return []
    
    def get_stats(self) -> Dict[str, Any]:
        """Get Instagram account statistics"""
        try:
            url = f"{self.base_url}/me"
            params = {'access_token': self.access_token, 'fields': 'id,username,media_count'}
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'platform': 'instagram',
                    'username': data.get('username'),
                    'media_count': data.get('media_count', 0),
                }
            
            return {}
        except Exception as e:
            logger.error(f"Error getting Instagram stats: {e}")
            return {}