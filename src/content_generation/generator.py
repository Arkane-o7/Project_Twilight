"""
Content Generator
Generates social media content based on user's writing style and trending topics
"""

import os
import logging
import asyncio
import random
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import json
import requests

# AI/ML libraries
from transformers import pipeline, GPT2LMHeadModel, GPT2Tokenizer
import openai

logger = logging.getLogger(__name__)

class ContentGenerator:
    """Generates social media content using AI"""
    
    def __init__(self, config):
        self.config = config
        self.text_generator = None
        self.openai_client = None
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize content generation models"""
        try:
            # Initialize OpenAI client if API key is available
            if self.config.openai_api_key:
                openai.api_key = self.config.openai_api_key
                self.openai_client = openai
                logger.info("OpenAI client initialized")
            
            # Initialize local text generation model as fallback
            self.text_generator = pipeline(
                "text-generation",
                model="gpt2-medium",
                tokenizer="gpt2-medium",
                device=-1  # Use CPU for compatibility
            )
            
            logger.info("Content generator models initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing content generator: {e}")
    
    async def generate_post(self, style_profile: Dict[str, Any], trending_topics: List[str] = None) -> Dict[str, Any]:
        """Generate a single social media post"""
        try:
            # Choose content strategy
            strategies = ['trending', 'personal_style', 'viral_rewrite', 'original']
            strategy = random.choice(strategies)
            
            # Generate content based on strategy
            if strategy == 'trending' and trending_topics:
                content = await self._generate_trending_content(style_profile, trending_topics)
            elif strategy == 'viral_rewrite':
                content = await self._generate_viral_rewrite(style_profile)
            else:
                content = await self._generate_original_content(style_profile)
            
            # Determine if image is needed
            needs_image = self._should_include_image(content, style_profile)
            
            # Select appropriate platforms
            platforms = self._select_platforms(content, style_profile)
            
            result = {
                'content': content,
                'strategy': strategy,
                'needs_image': needs_image,
                'platforms': platforms,
                'generated_at': datetime.now().isoformat(),
                'style_score': self._calculate_style_score(content, style_profile)
            }
            
            logger.info(f"Generated post using '{strategy}' strategy")
            return result
            
        except Exception as e:
            logger.error(f"Error generating post: {e}")
            return {
                'content': "Hello! 👋 Just testing my new AI social media assistant!",
                'strategy': 'fallback',
                'needs_image': False,
                'platforms': ['twitter'],
                'generated_at': datetime.now().isoformat(),
                'style_score': 0.5
            }
    
    async def _generate_trending_content(self, style_profile: Dict[str, Any], trending_topics: List[str]) -> str:
        """Generate content based on trending topics"""
        topic = random.choice(trending_topics)
        
        # Create prompt based on user's style
        prompt = self._create_style_prompt(style_profile, f"Write about {topic}")
        
        # Generate content
        if self.openai_client:
            try:
                response = await self._generate_with_openai(prompt)
                return self._adapt_to_style(response, style_profile)
            except Exception as e:
                logger.warning(f"OpenAI generation failed: {e}")
        
        # Fallback to local model
        return await self._generate_with_local_model(prompt, style_profile)
    
    async def _generate_viral_rewrite(self, style_profile: Dict[str, Any]) -> str:
        """Find and rewrite viral content in user's style"""
        # This would typically fetch viral posts from APIs
        # For now, using predefined viral patterns
        
        viral_patterns = [
            "The biggest lesson I learned this year:",
            "Unpopular opinion:",
            "3 things I wish I knew 5 years ago:",
            "Hot take:",
            "This changed my perspective completely:",
            "Things that make no sense to me:",
            "Why I stopped caring about:",
        ]
        
        pattern = random.choice(viral_patterns)
        topics = style_profile.get('topics', ['life', 'work', 'technology', 'growth'])
        topic = random.choice(topics)
        
        prompt = f"{pattern} {topic}"
        
        if self.openai_client:
            try:
                response = await self._generate_with_openai(prompt)
                return self._adapt_to_style(response, style_profile)
            except Exception as e:
                logger.warning(f"OpenAI generation failed: {e}")
        
        return await self._generate_with_local_model(prompt, style_profile)
    
    async def _generate_original_content(self, style_profile: Dict[str, Any]) -> str:
        """Generate original content based on user's style"""
        topics = style_profile.get('topics', ['life', 'work', 'technology'])
        topic = random.choice(topics)
        
        content_types = [
            f"Share a thought about {topic}",
            f"Give advice about {topic}",
            f"Tell a story about {topic}",
            f"Ask a question about {topic}",
            f"Share an insight about {topic}"
        ]
        
        prompt = random.choice(content_types)
        
        if self.openai_client:
            try:
                response = await self._generate_with_openai(prompt)
                return self._adapt_to_style(response, style_profile)
            except Exception as e:
                logger.warning(f"OpenAI generation failed: {e}")
        
        return await self._generate_with_local_model(prompt, style_profile)
    
    def _create_style_prompt(self, style_profile: Dict[str, Any], base_prompt: str) -> str:
        """Create a prompt that incorporates user's writing style"""
        sentiment = style_profile.get('sentiment_profile', {}).get('dominant_sentiment', 'neutral')
        emotion = style_profile.get('emotion_profile', {}).get('dominant_emotion', 'neutral')
        complexity = style_profile.get('readability', {}).get('complexity_level', 'standard')
        
        style_instructions = f"""
        Write in a {sentiment} tone with {emotion} emotion.
        Keep the complexity level {complexity}.
        Average length should be around {int(style_profile.get('avg_length', 100))} characters.
        """
        
        # Add language patterns
        patterns = style_profile.get('language_patterns', {})
        if patterns.get('exclamation_usage', 0) > 0.1:
            style_instructions += " Use exclamation marks for emphasis!"
        if patterns.get('question_usage', 0) > 0.1:
            style_instructions += " Include questions to engage readers?"
        if patterns.get('emoji_usage', 0) > 0.1:
            style_instructions += " Add relevant emojis 😊"
        
        return f"{style_instructions}\n\n{base_prompt}"
    
    async def _generate_with_openai(self, prompt: str) -> str:
        """Generate content using OpenAI"""
        try:
            response = await asyncio.to_thread(
                openai.ChatCompletion.create,
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a social media content creator. Write engaging, authentic posts."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"OpenAI generation error: {e}")
            raise
    
    async def _generate_with_local_model(self, prompt: str, style_profile: Dict[str, Any]) -> str:
        """Generate content using local model"""
        try:
            # Prepare the prompt
            full_prompt = f"Social media post: {prompt}"
            
            # Generate with local model
            result = self.text_generator(
                full_prompt,
                max_length=len(full_prompt) + 100,
                num_return_sequences=1,
                temperature=0.7,
                do_sample=True,
                pad_token_id=self.text_generator.tokenizer.eos_token_id
            )
            
            generated_text = result[0]['generated_text']
            
            # Extract just the generated part
            content = generated_text[len(full_prompt):].strip()
            
            # Clean up and adapt to style
            content = self._clean_generated_content(content)
            content = self._adapt_to_style(content, style_profile)
            
            return content
            
        except Exception as e:
            logger.error(f"Local model generation error: {e}")
            return self._generate_fallback_content(style_profile)
    
    def _clean_generated_content(self, content: str) -> str:
        """Clean up generated content"""
        # Remove incomplete sentences
        sentences = content.split('.')
        if len(sentences) > 1 and len(sentences[-1].strip()) < 10:
            content = '.'.join(sentences[:-1]) + '.'
        
        # Remove very long content
        if len(content) > 300:
            content = content[:300] + "..."
        
        # Remove unwanted patterns
        content = content.replace('\n', ' ')
        content = ' '.join(content.split())  # Normalize whitespace
        
        return content
    
    def _adapt_to_style(self, content: str, style_profile: Dict[str, Any]) -> str:
        """Adapt content to match user's style"""
        # Adjust length to match user's average
        target_length = int(style_profile.get('avg_length', 150))
        
        if len(content) > target_length * 1.5:
            # Shorten content
            sentences = content.split('.')
            content = '.'.join(sentences[:2]) + '.'
        
        # Add style elements based on patterns
        patterns = style_profile.get('language_patterns', {})
        
        # Add emojis if user uses them
        if patterns.get('emoji_usage', 0) > 0.1 and '😊' not in content:
            emoji_options = ['😊', '💡', '🤔', '🚀', '✨', '👍', '🔥', '💪']
            content += f" {random.choice(emoji_options)}"
        
        # Ensure proper punctuation style
        if patterns.get('exclamation_usage', 0) > 0.2 and '!' not in content:
            content = content.replace('.', '!', 1)
        
        return content
    
    def _generate_fallback_content(self, style_profile: Dict[str, Any]) -> str:
        """Generate simple fallback content"""
        fallback_templates = [
            "Just had an interesting thought about {topic}... 💭",
            "Working on improving my {topic} skills today! 💪",
            "What's your take on {topic}? Would love to hear your thoughts! 🤔",
            "Grateful for the lessons {topic} has taught me. ✨",
            "Today's focus: {topic}. Small steps, big progress! 🚀"
        ]
        
        topics = style_profile.get('topics', ['life', 'growth', 'learning'])
        topic = random.choice(topics)
        template = random.choice(fallback_templates)
        
        return template.format(topic=topic)
    
    def _should_include_image(self, content: str, style_profile: Dict[str, Any]) -> bool:
        """Determine if post should include an image"""
        # Check for image-worthy keywords
        image_keywords = ['beautiful', 'amazing', 'incredible', 'stunning', 'awesome', 
                         'photo', 'picture', 'look', 'see', 'view', 'sunset', 'sunrise']
        
        content_lower = content.lower()
        has_image_keywords = any(keyword in content_lower for keyword in image_keywords)
        
        # Random chance based on user's typical image usage
        random_chance = random.random() < 0.3  # 30% chance
        
        return has_image_keywords or random_chance
    
    def _select_platforms(self, content: str, style_profile: Dict[str, Any]) -> List[str]:
        """Select appropriate platforms for the content"""
        platforms = []
        
        # Twitter - good for short, engaging content
        if len(content) <= 280:
            platforms.append('twitter')
        
        # LinkedIn - good for professional content
        professional_keywords = ['work', 'career', 'business', 'professional', 'industry']
        if any(keyword in content.lower() for keyword in professional_keywords):
            platforms.append('linkedin')
        
        # Facebook - general content
        platforms.append('facebook')
        
        # Instagram - visual content
        if self._should_include_image(content, style_profile):
            platforms.append('instagram')
        
        return platforms if platforms else ['twitter']
    
    def _calculate_style_score(self, content: str, style_profile: Dict[str, Any]) -> float:
        """Calculate how well content matches user's style"""
        score = 0.5  # Base score
        
        # Length similarity
        target_length = style_profile.get('avg_length', 150)
        length_diff = abs(len(content) - target_length) / target_length
        length_score = max(0, 1 - length_diff)
        score += length_score * 0.2
        
        # Pattern matching
        patterns = style_profile.get('language_patterns', {})
        
        # Emoji usage
        content_emoji_usage = sum(1 for char in content if ord(char) > 127) / len(content)
        target_emoji_usage = patterns.get('emoji_usage', 0)
        emoji_similarity = 1 - abs(content_emoji_usage - target_emoji_usage)
        score += emoji_similarity * 0.1
        
        # Exclamation usage
        content_excl_usage = content.count('!') / len(content)
        target_excl_usage = patterns.get('exclamation_usage', 0)
        excl_similarity = 1 - abs(content_excl_usage - target_excl_usage)
        score += excl_similarity * 0.1
        
        return min(1.0, max(0.0, score))
    
    async def get_trending_topics(self) -> List[str]:
        """Get trending topics from various sources"""
        topics = []
        
        try:
            # Try to get trending topics from social media APIs
            # This is a simplified version - in production, you'd use real APIs
            
            # Fallback to predefined trending topics
            trending_topics = [
                "artificial intelligence", "remote work", "sustainability", 
                "mental health", "productivity", "innovation", "technology",
                "leadership", "entrepreneurship", "personal growth",
                "social media", "digital transformation", "creativity",
                "wellness", "learning", "future of work"
            ]
            
            # Return random selection
            topics = random.sample(trending_topics, min(5, len(trending_topics)))
            
        except Exception as e:
            logger.error(f"Error fetching trending topics: {e}")
            topics = ["technology", "innovation", "growth"]
        
        return topics
    
    async def should_engage(self, post: Dict[str, Any]) -> bool:
        """Determine if we should engage with a post"""
        # Simple engagement logic - can be enhanced with ML
        
        content = post.get('content', '').lower()
        engagement = post.get('engagement', {})
        
        # Don't engage with low-quality or spam content
        spam_indicators = ['buy now', 'click here', 'limited time', 'act fast']
        if any(indicator in content for indicator in spam_indicators):
            return False
        
        # Engage with popular posts
        total_engagement = sum([
            engagement.get('likes', 0),
            engagement.get('retweets', 0),
            engagement.get('replies', 0)
        ])
        
        if total_engagement > self.config.min_engagement_threshold:
            return True
        
        # Engage with posts containing interesting keywords
        interesting_keywords = ['AI', 'technology', 'innovation', 'tips', 'advice']
        if any(keyword.lower() in content for keyword in interesting_keywords):
            return True
        
        # Random engagement for diversity
        return random.random() < 0.1  # 10% chance
    
    async def generate_response(self, post: Dict[str, Any], style_profile: Dict[str, Any]) -> Dict[str, str]:
        """Generate an appropriate response to a post"""
        content = post.get('content', '')
        
        # Determine response type
        if '?' in content:
            # It's a question, provide an answer
            action = 'reply'
            comment = await self._generate_reply(content, style_profile)
        elif random.random() < 0.7:
            # Like the post
            action = 'like'
            comment = None
        else:
            # Comment on the post
            action = 'reply'
            comment = await self._generate_comment(content, style_profile)
        
        return {
            'action': action,
            'comment': comment
        }
    
    async def _generate_reply(self, content: str, style_profile: Dict[str, Any]) -> str:
        """Generate a reply to a question or discussion"""
        reply_templates = [
            "Great question! I think {opinion}",
            "Interesting perspective. In my experience, {opinion}",
            "This resonates with me. {opinion}",
            "Thanks for sharing! {opinion}",
            "I've found that {opinion}"
        ]
        
        opinions = [
            "it's all about finding the right balance.",
            "consistency is key to success.",
            "it's important to stay curious and keep learning.",
            "the best approach is to start small and iterate.",
            "mindset makes all the difference."
        ]
        
        template = random.choice(reply_templates)
        opinion = random.choice(opinions)
        
        reply = template.format(opinion=opinion)
        
        # Adapt to user's style
        return self._adapt_to_style(reply, style_profile)
    
    async def _generate_comment(self, content: str, style_profile: Dict[str, Any]) -> str:
        """Generate a general comment"""
        comment_templates = [
            "Love this! 💡",
            "So true! Thanks for sharing ✨",
            "Great insight! 👍",
            "This is exactly what I needed to hear today 🙏",
            "Couldn't agree more! 🔥"
        ]
        
        comment = random.choice(comment_templates)
        return self._adapt_to_style(comment, style_profile)