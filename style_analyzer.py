import openai
import tweepy
import os
import json
import time
from dotenv import load_dotenv
from typing import List, Dict, Optional

# Load environment variables
load_dotenv()

class StyleAnalyzer:
    """
    AI-powered social media style analyzer and content generator.
    Analyzes user's writing style from Twitter posts and generates matching content.
    """
    
    def __init__(self):
        """Initialize the StyleAnalyzer with API credentials."""
        # Initialize OpenAI
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key:
            self.openai_client = openai.OpenAI(api_key=openai_key)
        else:
            self.openai_client = None
        
        # Initialize Twitter API
        bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
        if bearer_token:
            self.twitter_api = tweepy.Client(bearer_token=bearer_token)
        else:
            self.twitter_api = None
    
    def get_recent_tweets(self, username: str, count: int = 20) -> List[str]:
        """
        Fetch recent tweets from a Twitter user.
        
        Args:
            username: Twitter username (without @)
            count: Number of tweets to fetch (max 100)
            
        Returns:
            List of tweet texts
        """
        if not self.twitter_api:
            raise ValueError("Twitter API not configured. Please set TWITTER_BEARER_TOKEN.")
        
        try:
            # Get user by username
            user = self.twitter_api.get_user(username=username)
            if not user.data:
                return []
            
            # Get user's tweets
            tweets = self.twitter_api.get_users_tweets(
                user.data.id, 
                max_results=min(count, 100),
                tweet_fields=['created_at', 'public_metrics'],
                exclude=['retweets', 'replies']  # Focus on original content
            )
            
            if not tweets.data:
                return []
            
            # Extract tweet texts
            tweet_texts = []
            for tweet in tweets.data:
                # Clean up tweet text (remove URLs, mentions for style analysis)
                text = tweet.text
                # Keep original text for now - AI can handle cleanup
                tweet_texts.append(text)
            
            return tweet_texts
            
        except Exception as e:
            print(f"Error fetching tweets: {e}")
            return []
    
    def analyze_style(self, tweets: List[str]) -> Dict:
        """
        Analyze writing style from a collection of tweets using AI.
        
        Args:
            tweets: List of tweet texts
            
        Returns:
            Dictionary containing style analysis
        """
        if not tweets:
            return {"error": "No tweets provided for analysis"}
        
        if not self.openai_client:
            return {"error": "OpenAI API not configured. Please set OPENAI_API_KEY environment variable."}
        
        # Prepare tweets for analysis
        tweets_text = "\n---\n".join(tweets[:15])  # Limit to avoid token limits
        
        prompt = f"""Analyze these social media posts and create a comprehensive writing style profile:

Posts:
{tweets_text}

Create a detailed style profile in JSON format with these categories:

1. tone: (casual/professional/humorous/sarcastic/inspirational/etc.)
2. topics: [list of main topics/themes the person writes about]
3. avg_length: (short/medium/long - typical post length)
4. emoji_usage: (none/minimal/moderate/heavy + common emoji patterns)
5. hashtag_style: (none/minimal/strategic/heavy + typical hashtag patterns)
6. writing_patterns: [specific patterns like "uses questions", "starts with quotes", "uses all caps", etc.]
7. vocabulary_level: (simple/conversational/professional/academic)
8. punctuation_style: (minimal/standard/excessive/creative)
9. personality_traits: [observable personality traits from writing]
10. content_structure: (stream-of-consciousness/structured/bullet-points/storytelling/etc.)

Return ONLY a valid JSON object, no other text."""

        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=800,
                temperature=0.3  # Lower temperature for more consistent analysis
            )
            
            content = response.choices[0].message.content.strip()
            
            # Try to parse as JSON
            try:
                style_profile = json.loads(content)
                style_profile["analysis_date"] = time.strftime("%Y-%m-%d %H:%M:%S")
                style_profile["tweet_count"] = len(tweets)
                return style_profile
            except json.JSONDecodeError:
                # If JSON parsing fails, return raw content
                return {
                    "raw_analysis": content,
                    "analysis_date": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "tweet_count": len(tweets)
                }
                
        except Exception as e:
            return {"error": f"Style analysis failed: {str(e)}"}
    
    def generate_content(self, style_profile: Dict, topic: str, count: int = 3) -> List[str]:
        """
        Generate social media content matching the analyzed style.
        
        Args:
            style_profile: Style analysis from analyze_style()
            topic: Topic to write about
            count: Number of posts to generate
            
        Returns:
            List of generated posts
        """
        if not self.openai_client:
            return [f"Content generation failed: OpenAI API not configured. Please set OPENAI_API_KEY environment variable."]
        
        # Convert style profile to text description
        if "raw_analysis" in style_profile:
            style_description = style_profile["raw_analysis"]
        else:
            style_description = json.dumps(style_profile, indent=2)
        
        prompt = f"""Based on this writing style profile, create {count} social media posts about "{topic}":

Style Profile:
{style_description}

Requirements:
- Match the tone, vocabulary, and writing patterns exactly
- Use similar emoji and hashtag patterns
- Keep similar post length
- Stay true to the personality traits
- Make posts engaging and authentic
- Focus on the topic: {topic}

Return {count} posts as a JSON array of strings. Each post should be ready to publish."""

        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=600,
                temperature=0.7  # Higher temperature for more creative content
            )
            
            content = response.choices[0].message.content.strip()
            
            # Try to parse as JSON array
            try:
                posts = json.loads(content)
                if isinstance(posts, list):
                    return posts
                else:
                    return [str(posts)]
            except json.JSONDecodeError:
                # If JSON parsing fails, split by lines or return as single post
                lines = [line.strip() for line in content.split('\n') if line.strip()]
                return lines[:count] if lines else [content]
                
        except Exception as e:
            return [f"Content generation failed: {str(e)}"]
    
    def generate_variations(self, original_post: str, style_profile: Dict, count: int = 3) -> List[str]:
        """
        Generate variations of an existing post in the user's style.
        
        Args:
            original_post: Original post to rewrite
            style_profile: Style analysis from analyze_style()
            count: Number of variations to generate
            
        Returns:
            List of post variations
        """
        if not self.openai_client:
            return [f"Variation generation failed: OpenAI API not configured. Please set OPENAI_API_KEY environment variable."]
        
        style_description = json.dumps(style_profile, indent=2) if "raw_analysis" not in style_profile else style_profile["raw_analysis"]
        
        prompt = f"""Rewrite this post {count} times to match this writing style:

Original Post: "{original_post}"

Style Profile:
{style_description}

Create {count} variations that:
- Keep the same core message/meaning
- Match the style profile exactly
- Sound like they were written by the same person
- Are engaging and natural

Return as a JSON array of {count} strings."""

        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.8
            )
            
            content = response.choices[0].message.content.strip()
            
            try:
                variations = json.loads(content)
                return variations if isinstance(variations, list) else [str(variations)]
            except json.JSONDecodeError:
                lines = [line.strip() for line in content.split('\n') if line.strip()]
                return lines[:count] if lines else [content]
                
        except Exception as e:
            return [f"Variation generation failed: {str(e)}"]

# Utility functions for testing without API keys
def create_sample_style_profile() -> Dict:
    """Create a sample style profile for testing purposes."""
    return {
        "tone": "casual and humorous",
        "topics": ["technology", "startups", "productivity", "life hacks"],
        "avg_length": "medium",
        "emoji_usage": "moderate",
        "hashtag_style": "minimal and strategic",
        "writing_patterns": ["uses questions", "shares personal experiences", "includes actionable advice"],
        "vocabulary_level": "conversational",
        "punctuation_style": "standard with occasional ellipses",
        "personality_traits": ["optimistic", "helpful", "slightly sarcastic"],
        "content_structure": "storytelling with insights",
        "analysis_date": time.strftime("%Y-%m-%d %H:%M:%S"),
        "tweet_count": 15
    }

def create_sample_tweets() -> List[str]:
    """Create sample tweets for testing purposes."""
    return [
        "Just spent 2 hours debugging a one-line fix... why is programming like this? 😅 #devlife",
        "Hot take: The best productivity hack is actually getting enough sleep. Revolutionary, I know.",
        "Building a startup is 10% inspiration, 90% caffeine, and 100% math doesn't work anymore",
        "Anyone else feel like they're just googling their way through life? Asking for a friend... 🤔",
        "Pro tip: If your code works on the first try, you probably wrote it wrong. #programming",
        "That moment when you realize the bug was in the code you wrote 5 minutes ago... classic me",
        "Why do we call it 'user-friendly' when users are clearly the enemy? 😂 #UXstruggles",
        "Today's mood: Optimistically debugging with the confidence of someone who definitely didn't break it",
        "Reminder: Your side project doesn't need to be perfect to be valuable. Ship it! 🚀",
        "The three stages of learning to code: 1) It works! 2) Why does it work? 3) It stopped working..."
    ]