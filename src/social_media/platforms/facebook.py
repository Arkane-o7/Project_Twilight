"""
Facebook API Client
Handles Facebook operations using the Graph API
"""

import logging
from typing import Dict, List, Optional, Any
import requests

logger = logging.getLogger(__name__)

class FacebookClient:
    """Facebook API client"""
    
    def __init__(self, config: Dict[str, str]):
        self.config = config
        self.base_url = "https://graph.facebook.com/v18.0"
        self.access_token = config.get('access_token')
    
    async def test_connection(self) -> bool:
        """Test Facebook API connection"""
        try:
            url = f"{self.base_url}/me"
            params = {'access_token': self.access_token, 'fields': 'id,name'}
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"Facebook connection successful for user: {data.get('name')}")
                return True
            return False
        except Exception as e:
            logger.error(f"Facebook connection test failed: {e}")
            return False
    
    async def get_user_posts(self, limit: int = 100) -> List[Dict]:
        """Get user's Facebook posts"""
        try:
            url = f"{self.base_url}/me/posts"
            params = {
                'access_token': self.access_token,
                'fields': 'id,message,created_time,permalink_url',
                'limit': min(100, limit)
            }
            
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                posts = []
                
                for item in data.get('data', []):
                    post = {
                        'id': item.get('id'),
                        'content': item.get('message', ''),
                        'created_at': item.get('created_time'),
                        'platform': 'facebook',
                        'url': item.get('permalink_url')
                    }
                    posts.append(post)
                
                return posts
            
            return []
        except Exception as e:
            logger.error(f"Error fetching Facebook posts: {e}")
            return []
    
    async def get_feed_posts(self, limit: int = 20) -> List[Dict]:
        """Get posts from user's Facebook feed"""
        try:
            url = f"{self.base_url}/me/feed"
            params = {
                'access_token': self.access_token,
                'fields': 'id,message,created_time,from',
                'limit': min(25, limit)
            }
            
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                posts = []
                
                for item in data.get('data', []):
                    post = {
                        'id': item.get('id'),
                        'content': item.get('message', ''),
                        'created_at': item.get('created_time'),
                        'author': item.get('from', {}).get('name'),
                        'platform': 'facebook'
                    }
                    posts.append(post)
                
                return posts
            
            return []
        except Exception as e:
            logger.error(f"Error fetching Facebook feed: {e}")
            return []
    
    async def post_content(self, content: str, image_path: Optional[str] = None) -> bool:
        """Post content to Facebook"""
        try:
            url = f"{self.base_url}/me/feed"
            data = {
                'access_token': self.access_token,
                'message': content
            }
            
            # Handle image upload if provided
            if image_path:
                # This is simplified - proper image upload requires additional steps
                logger.warning("Image upload to Facebook requires additional implementation")
            
            response = requests.post(url, data=data)
            if response.status_code == 200:
                result = response.json()
                logger.info(f"Facebook post successful: {result.get('id')}")
                return True
            
            return False
        except Exception as e:
            logger.error(f"Error posting to Facebook: {e}")
            return False
    
    async def engage_with_post(self, post_id: str, action: str, comment: Optional[str] = None) -> bool:
        """Engage with Facebook post"""
        try:
            if action == 'like':
                url = f"{self.base_url}/{post_id}/likes"
                data = {'access_token': self.access_token}
                response = requests.post(url, data=data)
                return response.status_code == 200
            
            elif action == 'comment' and comment:
                url = f"{self.base_url}/{post_id}/comments"
                data = {
                    'access_token': self.access_token,
                    'message': comment
                }
                response = requests.post(url, data=data)
                return response.status_code == 200
            
            return False
        except Exception as e:
            logger.error(f"Error engaging with Facebook post: {e}")
            return False
    
    async def get_trending_topics(self) -> List[str]:
        """Get trending topics (limited in Facebook API)"""
        logger.warning("Facebook trending topics require special permissions")
        return []
    
    async def search_posts(self, query: str, limit: int = 50) -> List[Dict]:
        """Search Facebook posts (limited access)"""
        logger.warning("Facebook search requires special permissions")
        return []
    
    def get_stats(self) -> Dict[str, Any]:
        """Get Facebook account statistics"""
        try:
            url = f"{self.base_url}/me"
            params = {'access_token': self.access_token, 'fields': 'id,name'}
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'platform': 'facebook',
                    'name': data.get('name'),
                    'id': data.get('id')
                }
            
            return {}
        except Exception as e:
            logger.error(f"Error getting Facebook stats: {e}")
            return {}