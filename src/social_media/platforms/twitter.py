"""
Twitter/X API Client
Handles all Twitter operations using the official API
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import tweepy
import aiohttp

logger = logging.getLogger(__name__)

class TwitterClient:
    """Twitter API client using Tweepy"""
    
    def __init__(self, config: Dict[str, str]):
        self.config = config
        self.api_v1 = None
        self.api_v2 = None
        self.client = None
        self._initialize_clients()
    
    def _initialize_clients(self):
        """Initialize Twitter API clients"""
        try:
            # Twitter API v1.1 (for some features)
            auth = tweepy.OAuthHandler(
                self.config['api_key'],
                self.config['api_secret']
            )
            auth.set_access_token(
                self.config['access_token'],
                self.config['access_token_secret']
            )
            self.api_v1 = tweepy.API(auth, wait_on_rate_limit=True)
            
            # Twitter API v2 (primary)
            self.client = tweepy.Client(
                bearer_token=self.config.get('bearer_token'),
                consumer_key=self.config['api_key'],
                consumer_secret=self.config['api_secret'],
                access_token=self.config['access_token'],
                access_token_secret=self.config['access_token_secret'],
                wait_on_rate_limit=True
            )
            
            logger.info("Twitter clients initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Twitter clients: {e}")
            raise
    
    async def test_connection(self) -> bool:
        """Test Twitter API connection"""
        try:
            # Test with a simple API call
            user = self.client.get_me()
            if user.data:
                logger.info(f"Twitter connection successful for user: {user.data.username}")
                return True
            return False
        except Exception as e:
            logger.error(f"Twitter connection test failed: {e}")
            return False
    
    async def get_user_posts(self, limit: int = 100) -> List[Dict]:
        """Get user's own tweets"""
        try:
            # Get authenticated user
            me = self.client.get_me()
            user_id = me.data.id
            
            # Fetch user's tweets
            tweets = tweepy.Paginator(
                self.client.get_users_tweets,
                id=user_id,
                tweet_fields=['created_at', 'public_metrics', 'context_annotations'],
                max_results=min(100, limit)
            ).flatten(limit=limit)
            
            posts = []
            for tweet in tweets:
                post = {
                    'id': tweet.id,
                    'content': tweet.text,
                    'created_at': tweet.created_at,
                    'platform': 'twitter',
                    'engagement': {
                        'likes': tweet.public_metrics.get('like_count', 0),
                        'retweets': tweet.public_metrics.get('retweet_count', 0),
                        'replies': tweet.public_metrics.get('reply_count', 0),
                    },
                    'url': f"https://twitter.com/user/status/{tweet.id}"
                }
                posts.append(post)
            
            return posts
            
        except Exception as e:
            logger.error(f"Error fetching user tweets: {e}")
            return []
    
    async def get_feed_posts(self, limit: int = 20) -> List[Dict]:
        """Get posts from user's timeline/feed"""
        try:
            # Get home timeline
            tweets = self.client.get_home_timeline(
                max_results=min(100, limit),
                tweet_fields=['created_at', 'public_metrics', 'author_id']
            )
            
            posts = []
            for tweet in tweets.data or []:
                post = {
                    'id': tweet.id,
                    'content': tweet.text,
                    'created_at': tweet.created_at,
                    'author_id': tweet.author_id,
                    'platform': 'twitter',
                    'engagement': {
                        'likes': tweet.public_metrics.get('like_count', 0),
                        'retweets': tweet.public_metrics.get('retweet_count', 0),
                        'replies': tweet.public_metrics.get('reply_count', 0),
                    },
                    'url': f"https://twitter.com/user/status/{tweet.id}"
                }
                posts.append(post)
            
            return posts
            
        except Exception as e:
            logger.error(f"Error fetching feed posts: {e}")
            return []
    
    async def post_content(self, content: str, image_path: Optional[str] = None) -> bool:
        """Post a tweet"""
        try:
            media_ids = []
            
            # Upload image if provided
            if image_path:
                try:
                    media = self.api_v1.media_upload(image_path)
                    media_ids = [media.media_id]
                except Exception as e:
                    logger.warning(f"Failed to upload image: {e}")
            
            # Post tweet
            response = self.client.create_tweet(
                text=content,
                media_ids=media_ids if media_ids else None
            )
            
            if response.data:
                logger.info(f"Tweet posted successfully: {response.data['id']}")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error posting tweet: {e}")
            return False
    
    async def engage_with_post(self, post_id: str, action: str, comment: Optional[str] = None) -> bool:
        """Engage with a tweet (like, retweet, reply)"""
        try:
            if action == 'like':
                response = self.client.like(post_id)
                return response.data.get('liked', False)
            
            elif action == 'retweet':
                response = self.client.retweet(post_id)
                return response.data.get('retweeted', False)
            
            elif action == 'reply' and comment:
                response = self.client.create_tweet(
                    text=comment,
                    in_reply_to_tweet_id=post_id
                )
                return response.data is not None
            
            elif action == 'quote' and comment:
                # Quote tweet
                quote_url = f"https://twitter.com/user/status/{post_id}"
                tweet_text = f"{comment} {quote_url}"
                response = self.client.create_tweet(text=tweet_text)
                return response.data is not None
            
            return False
            
        except Exception as e:
            logger.error(f"Error engaging with tweet: {e}")
            return False
    
    async def get_trending_topics(self) -> List[str]:
        """Get trending topics on Twitter"""
        try:
            # Get trends for worldwide (WOEID: 1)
            trends = self.api_v1.get_place_trends(1)
            
            if trends:
                trend_names = [trend['name'] for trend in trends[0]['trends'][:10]]
                return trend_names
            
            return []
            
        except Exception as e:
            logger.error(f"Error fetching trending topics: {e}")
            return []
    
    async def search_posts(self, query: str, limit: int = 50) -> List[Dict]:
        """Search for tweets"""
        try:
            tweets = tweepy.Paginator(
                self.client.search_recent_tweets,
                query=query,
                tweet_fields=['created_at', 'public_metrics', 'author_id'],
                max_results=min(100, limit)
            ).flatten(limit=limit)
            
            posts = []
            for tweet in tweets:
                post = {
                    'id': tweet.id,
                    'content': tweet.text,
                    'created_at': tweet.created_at,
                    'author_id': tweet.author_id,
                    'platform': 'twitter',
                    'engagement': {
                        'likes': tweet.public_metrics.get('like_count', 0),
                        'retweets': tweet.public_metrics.get('retweet_count', 0),
                        'replies': tweet.public_metrics.get('reply_count', 0),
                    },
                    'url': f"https://twitter.com/user/status/{tweet.id}"
                }
                posts.append(post)
            
            return posts
            
        except Exception as e:
            logger.error(f"Error searching tweets: {e}")
            return []
    
    def get_stats(self) -> Dict[str, Any]:
        """Get Twitter account statistics"""
        try:
            user = self.client.get_me(user_fields=['public_metrics'])
            
            if user.data:
                return {
                    'platform': 'twitter',
                    'username': user.data.username,
                    'followers': user.data.public_metrics.get('followers_count', 0),
                    'following': user.data.public_metrics.get('following_count', 0),
                    'tweets': user.data.public_metrics.get('tweet_count', 0),
                }
            
            return {}
            
        except Exception as e:
            logger.error(f"Error getting Twitter stats: {e}")
            return {}