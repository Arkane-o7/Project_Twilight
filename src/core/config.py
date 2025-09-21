"""
Configuration management for the AI Social Media Writer
"""

import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import Field

# Load environment variables
load_dotenv()

class Config(BaseSettings):
    """Configuration class using Pydantic for validation"""
    
    # Application settings
    debug: bool = Field(default=False, env='DEBUG')
    log_level: str = Field(default='INFO', env='LOG_LEVEL')
    secret_key: str = Field(default='dev-secret-key', env='SECRET_KEY')
    
    # Database
    database_url: str = Field(default='sqlite:///./social_ai.db', env='DATABASE_URL')
    
    # Social Media API Keys
    # Twitter/X
    twitter_api_key: Optional[str] = Field(default=None, env='TWITTER_API_KEY')
    twitter_api_secret: Optional[str] = Field(default=None, env='TWITTER_API_SECRET')
    twitter_access_token: Optional[str] = Field(default=None, env='TWITTER_ACCESS_TOKEN')
    twitter_access_token_secret: Optional[str] = Field(default=None, env='TWITTER_ACCESS_TOKEN_SECRET')
    twitter_bearer_token: Optional[str] = Field(default=None, env='TWITTER_BEARER_TOKEN')
    
    # Instagram
    instagram_access_token: Optional[str] = Field(default=None, env='INSTAGRAM_ACCESS_TOKEN')
    instagram_client_id: Optional[str] = Field(default=None, env='INSTAGRAM_CLIENT_ID')
    instagram_client_secret: Optional[str] = Field(default=None, env='INSTAGRAM_CLIENT_SECRET')
    
    # Facebook
    facebook_access_token: Optional[str] = Field(default=None, env='FACEBOOK_ACCESS_TOKEN')
    facebook_app_id: Optional[str] = Field(default=None, env='FACEBOOK_APP_ID')
    facebook_app_secret: Optional[str] = Field(default=None, env='FACEBOOK_APP_SECRET')
    
    # LinkedIn
    linkedin_client_id: Optional[str] = Field(default=None, env='LINKEDIN_CLIENT_ID')
    linkedin_client_secret: Optional[str] = Field(default=None, env='LINKEDIN_CLIENT_SECRET')
    linkedin_access_token: Optional[str] = Field(default=None, env='LINKEDIN_ACCESS_TOKEN')
    
    # AI/ML API Keys
    openai_api_key: Optional[str] = Field(default=None, env='OPENAI_API_KEY')
    huggingface_api_key: Optional[str] = Field(default=None, env='HUGGINGFACE_API_KEY')
    stability_ai_api_key: Optional[str] = Field(default=None, env='STABILITY_AI_API_KEY')
    
    # Content Generation Settings
    max_post_length: int = Field(default=280, env='MAX_POST_LENGTH')
    min_engagement_threshold: int = Field(default=10, env='MIN_ENGAGEMENT_THRESHOLD')
    viral_threshold: int = Field(default=1000, env='VIRAL_THRESHOLD')
    posting_frequency_hours: int = Field(default=4, env='POSTING_FREQUENCY_HOURS')
    
    # Image Generation
    image_style: str = Field(default='realistic', env='IMAGE_STYLE')
    image_size: str = Field(default='1024x1024', env='IMAGE_SIZE')
    max_images_per_post: int = Field(default=4, env='MAX_IMAGES_PER_POST')
    
    # Redis
    redis_url: str = Field(default='redis://localhost:6379/0', env='REDIS_URL')
    
    # Security
    allowed_hosts: str = Field(default='localhost,127.0.0.1', env='ALLOWED_HOSTS')
    
    class Config:
        env_file = '.env'
        case_sensitive = False
    
    def get_social_media_config(self, platform: str) -> Dict[str, Any]:
        """Get configuration for a specific social media platform"""
        configs = {
            'twitter': {
                'api_key': self.twitter_api_key,
                'api_secret': self.twitter_api_secret,
                'access_token': self.twitter_access_token,
                'access_token_secret': self.twitter_access_token_secret,
                'bearer_token': self.twitter_bearer_token,
            },
            'instagram': {
                'access_token': self.instagram_access_token,
                'client_id': self.instagram_client_id,
                'client_secret': self.instagram_client_secret,
            },
            'facebook': {
                'access_token': self.facebook_access_token,
                'app_id': self.facebook_app_id,
                'app_secret': self.facebook_app_secret,
            },
            'linkedin': {
                'client_id': self.linkedin_client_id,
                'client_secret': self.linkedin_client_secret,
                'access_token': self.linkedin_access_token,
            }
        }
        
        return configs.get(platform, {})
    
    def is_platform_configured(self, platform: str) -> bool:
        """Check if a platform is properly configured"""
        config = self.get_social_media_config(platform)
        
        # Check required fields for each platform
        requirements = {
            'twitter': ['api_key', 'api_secret', 'access_token', 'access_token_secret'],
            'instagram': ['access_token'],
            'facebook': ['access_token'],
            'linkedin': ['access_token']
        }
        
        required_fields = requirements.get(platform, [])
        return all(config.get(field) for field in required_fields)
    
    def get_configured_platforms(self) -> list:
        """Get list of properly configured platforms"""
        platforms = ['twitter', 'instagram', 'facebook', 'linkedin']
        return [platform for platform in platforms if self.is_platform_configured(platform)]

# Global config instance
config = Config()