"""
Tests for the AI Social Media Writer MVP
"""

import pytest
import asyncio
import os
import sys
from unittest.mock import Mock, patch

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.core.config import Config
from src.social_media.platforms.twitter import TwitterClient
from src.ai_engine.style_analyzer import StyleAnalyzer
from src.content_generation.generator import ContentGenerator

class TestConfig:
    """Test configuration management"""
    
    def test_config_initialization(self):
        """Test config initialization"""
        config = Config()
        assert config.debug in [True, False]
        assert config.log_level in ['DEBUG', 'INFO', 'WARNING', 'ERROR']
    
    def test_platform_configuration(self):
        """Test platform configuration detection"""
        config = Config()
        
        # Test with mock API keys
        with patch.dict(os.environ, {
            'TWITTER_API_KEY': 'test_key',
            'TWITTER_API_SECRET': 'test_secret',
            'TWITTER_ACCESS_TOKEN': 'test_token',
            'TWITTER_ACCESS_TOKEN_SECRET': 'test_token_secret'
        }):
            config = Config()
            assert config.is_platform_configured('twitter')

class TestStyleAnalyzer:
    """Test writing style analyzer"""
    
    @pytest.fixture
    def analyzer(self):
        """Create style analyzer instance"""
        config = Config()
        return StyleAnalyzer(config)
    
    @pytest.fixture
    def sample_posts(self):
        """Sample posts for testing"""
        return [
            {
                'content': 'Just had an amazing day! Really excited about the new project 🚀',
                'created_at': '2024-01-01T10:00:00Z',
                'engagement': {'likes': 50, 'retweets': 10}
            },
            {
                'content': 'Working on some interesting AI projects. The future is exciting!',
                'created_at': '2024-01-02T15:00:00Z',
                'engagement': {'likes': 30, 'retweets': 5}
            },
            {
                'content': 'Coffee and code. Perfect combination for productivity ☕',
                'created_at': '2024-01-03T09:00:00Z',
                'engagement': {'likes': 25, 'retweets': 3}
            }
        ]
    
    @pytest.mark.asyncio
    async def test_analyze_posts(self, analyzer, sample_posts):
        """Test post analysis"""
        # Skip if models not available
        if not analyzer.sentiment_analyzer:
            pytest.skip("Sentiment analyzer not available")
        
        profile = await analyzer.analyze_posts(sample_posts)
        
        assert 'total_posts' in profile
        assert profile['total_posts'] == 3
        assert 'avg_length' in profile
        assert profile['avg_length'] > 0

class TestContentGenerator:
    """Test content generator"""
    
    @pytest.fixture
    def generator(self):
        """Create content generator instance"""
        config = Config()
        return ContentGenerator(config)
    
    @pytest.fixture
    def sample_style_profile(self):
        """Sample style profile for testing"""
        return {
            'avg_length': 120,
            'sentiment_profile': {'dominant_sentiment': 'positive'},
            'emotion_profile': {'dominant_emotion': 'joy'},
            'topics': ['AI', 'technology', 'productivity'],
            'language_patterns': {
                'emoji_usage': 0.2,
                'exclamation_usage': 0.1
            }
        }
    
    @pytest.mark.asyncio
    async def test_generate_post(self, generator, sample_style_profile):
        """Test post generation"""
        post = await generator.generate_post(sample_style_profile)
        
        assert 'content' in post
        assert 'strategy' in post
        assert 'platforms' in post
        assert len(post['content']) > 0

    @pytest.mark.asyncio
    async def test_get_trending_topics(self, generator):
        """Test trending topics retrieval"""
        topics = await generator.get_trending_topics()
        
        assert isinstance(topics, list)
        assert len(topics) > 0

class TestTwitterClient:
    """Test Twitter client (mocked)"""
    
    @pytest.fixture
    def twitter_config(self):
        """Twitter configuration for testing"""
        return {
            'api_key': 'test_key',
            'api_secret': 'test_secret',
            'access_token': 'test_token',
            'access_token_secret': 'test_token_secret',
            'bearer_token': 'test_bearer'
        }
    
    def test_client_initialization(self, twitter_config):
        """Test Twitter client initialization"""
        with patch('tweepy.Client'), patch('tweepy.API'):
            client = TwitterClient(twitter_config)
            assert client.config == twitter_config

class TestEndToEnd:
    """End-to-end integration tests"""
    
    @pytest.mark.asyncio
    async def test_mvp_workflow(self):
        """Test basic MVP workflow"""
        # This would test the full workflow in a controlled environment
        # For now, just test that imports work
        
        from mvp_ai_social_media import SocialMediaAI
        
        # Mock the config to avoid API calls
        with patch('src.core.config.Config') as mock_config:
            mock_config.return_value.get_configured_platforms.return_value = []
            
            ai = SocialMediaAI()
            assert ai is not None

def test_requirements_installed():
    """Test that required packages are installed"""
    try:
        import streamlit
        import transformers
        import pandas
        import plotly
        import PIL
        import tweepy
        assert True
    except ImportError as e:
        pytest.fail(f"Required package not installed: {e}")

if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])