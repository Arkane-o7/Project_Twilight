"""
LinkedIn API Client
Handles LinkedIn operations using the LinkedIn API
"""

import logging
from typing import Dict, List, Optional, Any
import requests

logger = logging.getLogger(__name__)

class LinkedInClient:
    """LinkedIn API client"""
    
    def __init__(self, config: Dict[str, str]):
        self.config = config
        self.base_url = "https://api.linkedin.com/v2"
        self.access_token = config.get('access_token')
    
    async def test_connection(self) -> bool:
        """Test LinkedIn API connection"""
        try:
            url = f"{self.base_url}/me"
            headers = {'Authorization': f'Bearer {self.access_token}'}
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"LinkedIn connection successful for user: {data.get('localizedFirstName')} {data.get('localizedLastName')}")
                return True
            return False
        except Exception as e:
            logger.error(f"LinkedIn connection test failed: {e}")
            return False
    
    async def get_user_posts(self, limit: int = 100) -> List[Dict]:
        """Get user's LinkedIn posts"""
        try:
            # Get user's person ID first
            me_url = f"{self.base_url}/me"
            headers = {'Authorization': f'Bearer {self.access_token}'}
            me_response = requests.get(me_url, headers=headers)
            
            if me_response.status_code != 200:
                return []
            
            person_id = me_response.json().get('id')
            
            # Get posts
            url = f"{self.base_url}/shares"
            params = {
                'q': 'owners',
                'owners': f'urn:li:person:{person_id}',
                'count': min(50, limit)  # API limit
            }
            
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                data = response.json()
                posts = []
                
                for item in data.get('elements', []):
                    content = ''
                    if 'text' in item.get('text', {}):
                        content = item['text']['text']
                    
                    post = {
                        'id': item.get('id'),
                        'content': content,
                        'created_at': item.get('created', {}).get('time'),
                        'platform': 'linkedin'
                    }
                    posts.append(post)
                
                return posts
            
            return []
        except Exception as e:
            logger.error(f"Error fetching LinkedIn posts: {e}")
            return []
    
    async def get_feed_posts(self, limit: int = 20) -> List[Dict]:
        """Get posts from user's LinkedIn feed (limited access)"""
        logger.warning("LinkedIn feed access requires special permissions")
        return []
    
    async def post_content(self, content: str, image_path: Optional[str] = None) -> bool:
        """Post content to LinkedIn"""
        try:
            # Get user's person ID first
            me_url = f"{self.base_url}/me"
            headers = {'Authorization': f'Bearer {self.access_token}'}
            me_response = requests.get(me_url, headers=headers)
            
            if me_response.status_code != 200:
                return False
            
            person_id = me_response.json().get('id')
            
            # Create share
            url = f"{self.base_url}/shares"
            headers['Content-Type'] = 'application/json'
            
            post_data = {
                "content": {
                    "contentEntities": [],
                    "title": content[:100] + "..." if len(content) > 100 else content
                },
                "distribution": {
                    "linkedInDistributionTarget": {}
                },
                "owner": f"urn:li:person:{person_id}",
                "text": {
                    "text": content
                }
            }
            
            response = requests.post(url, headers=headers, json=post_data)
            if response.status_code == 201:
                logger.info("LinkedIn post successful")
                return True
            
            return False
        except Exception as e:
            logger.error(f"Error posting to LinkedIn: {e}")
            return False
    
    async def engage_with_post(self, post_id: str, action: str, comment: Optional[str] = None) -> bool:
        """Engage with LinkedIn post (limited functionality)"""
        logger.warning("LinkedIn engagement requires special permissions")
        return False
    
    async def get_trending_topics(self) -> List[str]:
        """Get trending topics (not available in LinkedIn API)"""
        logger.warning("LinkedIn trending topics not available via API")
        return []
    
    async def search_posts(self, query: str, limit: int = 50) -> List[Dict]:
        """Search LinkedIn posts (limited access)"""
        logger.warning("LinkedIn search requires special permissions")
        return []
    
    def get_stats(self) -> Dict[str, Any]:
        """Get LinkedIn account statistics"""
        try:
            url = f"{self.base_url}/me"
            headers = {'Authorization': f'Bearer {self.access_token}'}
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'platform': 'linkedin',
                    'name': f"{data.get('localizedFirstName', '')} {data.get('localizedLastName', '')}".strip(),
                    'id': data.get('id')
                }
            
            return {}
        except Exception as e:
            logger.error(f"Error getting LinkedIn stats: {e}")
            return {}