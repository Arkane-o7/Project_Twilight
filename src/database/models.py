"""
Database Models
SQLAlchemy models for the AI Social Media Writer
"""

import os
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Float, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class SocialMediaPost(Base):
    """Model for storing social media posts"""
    __tablename__ = 'social_media_posts'
    
    id = Column(Integer, primary_key=True)
    platform = Column(String(50), nullable=False)
    platform_post_id = Column(String(255))
    content = Column(Text, nullable=False)
    image_path = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    posted_at = Column(DateTime)
    is_generated = Column(Boolean, default=False)
    generation_strategy = Column(String(100))
    style_score = Column(Float)
    engagement_data = Column(JSON)
    status = Column(String(50), default='draft')  # draft, posted, failed

class WritingStyleProfile(Base):
    """Model for storing user writing style profiles"""
    __tablename__ = 'writing_style_profiles'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(String(100), nullable=False)
    platform = Column(String(50), nullable=False)
    profile_data = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    posts_analyzed = Column(Integer, default=0)

class GeneratedContent(Base):
    """Model for storing AI-generated content"""
    __tablename__ = 'generated_content'
    
    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    prompt = Column(Text)
    generation_method = Column(String(100))
    style_profile_id = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    used_at = Column(DateTime)
    platforms = Column(JSON)  # List of target platforms
    quality_score = Column(Float)
    is_used = Column(Boolean, default=False)

class EngagementActivity(Base):
    """Model for tracking engagement activities"""
    __tablename__ = 'engagement_activities'
    
    id = Column(Integer, primary_key=True)
    platform = Column(String(50), nullable=False)
    target_post_id = Column(String(255), nullable=False)
    action = Column(String(50), nullable=False)  # like, retweet, comment, etc.
    comment_text = Column(Text)
    performed_at = Column(DateTime, default=datetime.utcnow)
    success = Column(Boolean, default=True)
    error_message = Column(Text)

class TrendingTopic(Base):
    """Model for storing trending topics"""
    __tablename__ = 'trending_topics'
    
    id = Column(Integer, primary_key=True)
    topic = Column(String(255), nullable=False)
    platform = Column(String(50), nullable=False)
    trending_score = Column(Float)
    discovered_at = Column(DateTime, default=datetime.utcnow)
    used_count = Column(Integer, default=0)
    last_used = Column(DateTime)

class ContentSchedule(Base):
    """Model for scheduling content posts"""
    __tablename__ = 'content_schedule'
    
    id = Column(Integer, primary_key=True)
    content_id = Column(Integer)
    platform = Column(String(50), nullable=False)
    scheduled_for = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    posted_at = Column(DateTime)
    status = Column(String(50), default='scheduled')  # scheduled, posted, failed, cancelled

class UserSettings(Base):
    """Model for storing user preferences and settings"""
    __tablename__ = 'user_settings'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(String(100), nullable=False, unique=True)
    settings_data = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Database initialization
def init_database(database_url: str = None):
    """Initialize the database"""
    if not database_url:
        database_url = os.getenv('DATABASE_URL', 'sqlite:///./social_ai.db')
    
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    return engine, SessionLocal

# Database session management
def get_db_session(database_url: str = None):
    """Get database session"""
    _, SessionLocal = init_database(database_url)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Utility functions for common database operations
class DatabaseManager:
    """Database operations manager"""
    
    def __init__(self, database_url: str = None):
        self.engine, self.SessionLocal = init_database(database_url)
    
    def get_session(self):
        """Get a database session"""
        return self.SessionLocal()
    
    def save_post(self, platform: str, content: str, image_path: str = None, 
                  is_generated: bool = False, **kwargs):
        """Save a social media post"""
        with self.get_session() as session:
            post = SocialMediaPost(
                platform=platform,
                content=content,
                image_path=image_path,
                is_generated=is_generated,
                **kwargs
            )
            session.add(post)
            session.commit()
            return post.id
    
    def save_style_profile(self, user_id: str, platform: str, profile_data: dict, posts_analyzed: int = 0):
        """Save or update writing style profile"""
        with self.get_session() as session:
            # Check if profile exists
            existing = session.query(WritingStyleProfile).filter_by(
                user_id=user_id, platform=platform
            ).first()
            
            if existing:
                existing.profile_data = profile_data
                existing.posts_analyzed = posts_analyzed
                existing.updated_at = datetime.utcnow()
            else:
                profile = WritingStyleProfile(
                    user_id=user_id,
                    platform=platform,
                    profile_data=profile_data,
                    posts_analyzed=posts_analyzed
                )
                session.add(profile)
            
            session.commit()
    
    def get_style_profile(self, user_id: str, platform: str = None):
        """Get writing style profile"""
        with self.get_session() as session:
            query = session.query(WritingStyleProfile).filter_by(user_id=user_id)
            
            if platform:
                query = query.filter_by(platform=platform)
            
            return query.first()
    
    def save_generated_content(self, content: str, prompt: str = None, 
                             method: str = None, platforms: list = None, **kwargs):
        """Save generated content"""
        with self.get_session() as session:
            generated = GeneratedContent(
                content=content,
                prompt=prompt,
                generation_method=method,
                platforms=platforms,
                **kwargs
            )
            session.add(generated)
            session.commit()
            return generated.id
    
    def get_unused_content(self, platform: str = None, limit: int = 10):
        """Get unused generated content"""
        with self.get_session() as session:
            query = session.query(GeneratedContent).filter_by(is_used=False)
            
            if platform:
                query = query.filter(GeneratedContent.platforms.contains([platform]))
            
            return query.limit(limit).all()
    
    def mark_content_used(self, content_id: int):
        """Mark content as used"""
        with self.get_session() as session:
            content = session.query(GeneratedContent).get(content_id)
            if content:
                content.is_used = True
                content.used_at = datetime.utcnow()
                session.commit()
    
    def log_engagement(self, platform: str, target_post_id: str, action: str, 
                      comment_text: str = None, success: bool = True, error_message: str = None):
        """Log engagement activity"""
        with self.get_session() as session:
            activity = EngagementActivity(
                platform=platform,
                target_post_id=target_post_id,
                action=action,
                comment_text=comment_text,
                success=success,
                error_message=error_message
            )
            session.add(activity)
            session.commit()
    
    def save_trending_topics(self, topics: list, platform: str):
        """Save trending topics"""
        with self.get_session() as session:
            for topic_data in topics:
                if isinstance(topic_data, str):
                    topic_text = topic_data
                    score = 1.0
                else:
                    topic_text = topic_data.get('topic', '')
                    score = topic_data.get('score', 1.0)
                
                # Check if topic already exists
                existing = session.query(TrendingTopic).filter_by(
                    topic=topic_text, platform=platform
                ).first()
                
                if existing:
                    existing.trending_score = score
                    existing.discovered_at = datetime.utcnow()
                else:
                    trending = TrendingTopic(
                        topic=topic_text,
                        platform=platform,
                        trending_score=score
                    )
                    session.add(trending)
            
            session.commit()
    
    def get_trending_topics(self, platform: str = None, limit: int = 10):
        """Get trending topics"""
        with self.get_session() as session:
            query = session.query(TrendingTopic).order_by(TrendingTopic.trending_score.desc())
            
            if platform:
                query = query.filter_by(platform=platform)
            
            return query.limit(limit).all()
    
    def schedule_content(self, content_id: int, platform: str, scheduled_for: datetime):
        """Schedule content for posting"""
        with self.get_session() as session:
            schedule = ContentSchedule(
                content_id=content_id,
                platform=platform,
                scheduled_for=scheduled_for
            )
            session.add(schedule)
            session.commit()
            return schedule.id
    
    def get_scheduled_content(self, due_before: datetime = None):
        """Get content scheduled for posting"""
        with self.get_session() as session:
            query = session.query(ContentSchedule).filter_by(status='scheduled')
            
            if due_before:
                query = query.filter(ContentSchedule.scheduled_for <= due_before)
            
            return query.all()
    
    def get_analytics_data(self, days: int = 30):
        """Get analytics data for the last N days"""
        with self.get_session() as session:
            start_date = datetime.utcnow() - timedelta(days=days)
            
            # Posts analytics
            posts = session.query(SocialMediaPost).filter(
                SocialMediaPost.created_at >= start_date
            ).all()
            
            # Engagement analytics
            engagements = session.query(EngagementActivity).filter(
                EngagementActivity.performed_at >= start_date
            ).all()
            
            return {
                'posts': len(posts),
                'generated_posts': len([p for p in posts if p.is_generated]),
                'engagements': len(engagements),
                'successful_engagements': len([e for e in engagements if e.success]),
                'platforms': list(set([p.platform for p in posts])),
                'avg_style_score': sum([p.style_score or 0 for p in posts]) / len(posts) if posts else 0
            }