"""
Writing Style Analyzer
Analyzes user's writing style from their social media posts
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import pickle
import numpy as np
from collections import Counter

# NLP libraries
import nltk
from textstat import flesch_reading_ease, flesch_kincaid_grade
from transformers import pipeline, AutoTokenizer, AutoModel
import torch

logger = logging.getLogger(__name__)

class StyleAnalyzer:
    """Analyzes and profiles user's writing style"""
    
    def __init__(self, config):
        self.config = config
        self.sentiment_analyzer = None
        self.emotion_analyzer = None
        self.tokenizer = None
        self.model = None
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize NLP models"""
        try:
            # Download required NLTK data
            nltk.download('punkt', quiet=True)
            nltk.download('stopwords', quiet=True)
            nltk.download('vader_lexicon', quiet=True)
            
            # Initialize sentiment analysis
            self.sentiment_analyzer = pipeline(
                "sentiment-analysis",
                model="cardiffnlp/twitter-roberta-base-sentiment-latest",
                return_all_scores=True
            )
            
            # Initialize emotion analysis
            self.emotion_analyzer = pipeline(
                "text-classification",
                model="j-hartmann/emotion-english-distilroberta-base",
                return_all_scores=True
            )
            
            # Initialize text encoder for style similarity
            self.tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
            
            logger.info("Style analyzer models initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing style analyzer models: {e}")
    
    async def analyze_posts(self, posts: List[Dict]) -> Dict[str, Any]:
        """Analyze writing style from a list of posts"""
        if not posts:
            return {}
        
        logger.info(f"Analyzing writing style from {len(posts)} posts...")
        
        # Extract text content
        texts = [post.get('content', '') for post in posts if post.get('content')]
        
        if not texts:
            return {}
        
        # Basic metrics
        style_profile = {
            'analyzed_at': datetime.now().isoformat(),
            'total_posts': len(posts),
            'avg_length': np.mean([len(text) for text in texts]),
            'median_length': np.median([len(text) for text in texts]),
            'max_length': max([len(text) for text in texts]),
            'min_length': min([len(text) for text in texts]),
        }
        
        # Readability analysis
        readability_scores = []
        for text in texts:
            if len(text.strip()) > 10:  # Skip very short texts
                try:
                    score = flesch_reading_ease(text)
                    readability_scores.append(score)
                except:
                    pass
        
        if readability_scores:
            style_profile['readability'] = {
                'flesch_ease_avg': np.mean(readability_scores),
                'complexity_level': self._get_complexity_level(np.mean(readability_scores))
            }
        
        # Sentiment analysis
        try:
            sentiment_results = []
            for text in texts[:50]:  # Limit for performance
                if len(text.strip()) > 5:
                    result = self.sentiment_analyzer(text[:512])  # Truncate for model limit
                    sentiment_results.append(result)
            
            if sentiment_results:
                style_profile['sentiment_profile'] = self._analyze_sentiment_pattern(sentiment_results)
        except Exception as e:
            logger.warning(f"Sentiment analysis failed: {e}")
        
        # Emotion analysis
        try:
            emotion_results = []
            for text in texts[:30]:  # Limit for performance
                if len(text.strip()) > 5:
                    result = self.emotion_analyzer(text[:512])
                    emotion_results.append(result)
            
            if emotion_results:
                style_profile['emotion_profile'] = self._analyze_emotion_pattern(emotion_results)
        except Exception as e:
            logger.warning(f"Emotion analysis failed: {e}")
        
        # Language patterns
        style_profile['language_patterns'] = self._analyze_language_patterns(texts)
        
        # Topics and keywords
        style_profile['topics'] = self._extract_topics(texts)
        
        # Engagement style (based on post metadata)
        style_profile['engagement_style'] = self._analyze_engagement_style(posts)
        
        # Posting patterns
        style_profile['posting_patterns'] = self._analyze_posting_patterns(posts)
        
        logger.info("Writing style analysis completed")
        return style_profile
    
    def _get_complexity_level(self, flesch_score: float) -> str:
        """Determine complexity level from Flesch score"""
        if flesch_score >= 90:
            return "very_easy"
        elif flesch_score >= 80:
            return "easy"
        elif flesch_score >= 70:
            return "fairly_easy"
        elif flesch_score >= 60:
            return "standard"
        elif flesch_score >= 50:
            return "fairly_difficult"
        elif flesch_score >= 30:
            return "difficult"
        else:
            return "very_difficult"
    
    def _analyze_sentiment_pattern(self, sentiment_results: List) -> Dict[str, Any]:
        """Analyze overall sentiment patterns"""
        all_sentiments = []
        
        for result in sentiment_results:
            if result and len(result[0]) > 0:
                # Get the sentiment with highest score
                top_sentiment = max(result[0], key=lambda x: x['score'])
                all_sentiments.append(top_sentiment['label'])
        
        sentiment_counts = Counter(all_sentiments)
        total = len(all_sentiments)
        
        return {
            'dominant_sentiment': sentiment_counts.most_common(1)[0][0] if sentiment_counts else 'neutral',
            'sentiment_distribution': {
                sentiment: count/total for sentiment, count in sentiment_counts.items()
            },
            'sentiment_consistency': sentiment_counts.most_common(1)[0][1]/total if sentiment_counts else 0
        }
    
    def _analyze_emotion_pattern(self, emotion_results: List) -> Dict[str, Any]:
        """Analyze emotional patterns"""
        all_emotions = []
        
        for result in emotion_results:
            if result and len(result[0]) > 0:
                # Get the emotion with highest score
                top_emotion = max(result[0], key=lambda x: x['score'])
                all_emotions.append(top_emotion['label'])
        
        emotion_counts = Counter(all_emotions)
        total = len(all_emotions)
        
        return {
            'dominant_emotion': emotion_counts.most_common(1)[0][0] if emotion_counts else 'neutral',
            'emotion_distribution': {
                emotion: count/total for emotion, count in emotion_counts.items()
            },
            'emotional_range': len(emotion_counts),
            'top_emotions': [emotion for emotion, _ in emotion_counts.most_common(3)]
        }
    
    def _analyze_language_patterns(self, texts: List[str]) -> Dict[str, Any]:
        """Analyze language usage patterns"""
        all_text = ' '.join(texts).lower()
        
        # Count common patterns
        patterns = {
            'exclamation_usage': all_text.count('!') / len(texts),
            'question_usage': all_text.count('?') / len(texts),
            'emoji_usage': sum(1 for char in all_text if ord(char) > 127) / len(texts),
            'hashtag_usage': all_text.count('#') / len(texts),
            'mention_usage': all_text.count('@') / len(texts),
            'link_usage': all_text.count('http') / len(texts),
        }
        
        # Word patterns
        words = all_text.split()
        word_lengths = [len(word) for word in words]
        
        patterns.update({
            'avg_word_length': np.mean(word_lengths) if word_lengths else 0,
            'vocabulary_richness': len(set(words)) / len(words) if words else 0,
            'sentence_count': sum(text.count('.') + text.count('!') + text.count('?') for text in texts),
        })
        
        return patterns
    
    def _extract_topics(self, texts: List[str]) -> List[str]:
        """Extract common topics/themes from texts"""
        all_text = ' '.join(texts).lower()
        
        # Simple keyword extraction (can be enhanced with more sophisticated methods)
        from nltk.corpus import stopwords
        from nltk.tokenize import word_tokenize
        
        try:
            stop_words = set(stopwords.words('english'))
            words = word_tokenize(all_text)
            
            # Filter meaningful words
            meaningful_words = [
                word for word in words 
                if word.isalpha() and len(word) > 3 and word not in stop_words
            ]
            
            # Get most common words as topics
            word_counts = Counter(meaningful_words)
            return [word for word, _ in word_counts.most_common(10)]
            
        except Exception as e:
            logger.warning(f"Topic extraction failed: {e}")
            return []
    
    def _analyze_engagement_style(self, posts: List[Dict]) -> Dict[str, Any]:
        """Analyze how user engages (based on post performance)"""
        if not posts:
            return {}
        
        # Calculate engagement metrics
        engagements = []
        for post in posts:
            engagement = post.get('engagement', {})
            total_engagement = sum([
                engagement.get('likes', 0),
                engagement.get('retweets', 0),
                engagement.get('replies', 0),
                engagement.get('shares', 0)
            ])
            engagements.append(total_engagement)
        
        if not engagements:
            return {}
        
        return {
            'avg_engagement': np.mean(engagements),
            'max_engagement': max(engagements),
            'engagement_consistency': np.std(engagements),
            'high_performing_threshold': np.percentile(engagements, 75) if len(engagements) > 4 else max(engagements)
        }
    
    def _analyze_posting_patterns(self, posts: List[Dict]) -> Dict[str, Any]:
        """Analyze when and how often user posts"""
        if not posts:
            return {}
        
        # Extract posting times
        posting_hours = []
        posting_days = []
        
        for post in posts:
            created_at = post.get('created_at')
            if created_at:
                try:
                    if isinstance(created_at, str):
                        dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                    else:
                        dt = created_at
                    
                    posting_hours.append(dt.hour)
                    posting_days.append(dt.weekday())
                except:
                    pass
        
        patterns = {}
        
        if posting_hours:
            hour_counts = Counter(posting_hours)
            patterns['preferred_hours'] = [hour for hour, _ in hour_counts.most_common(3)]
            patterns['peak_hour'] = hour_counts.most_common(1)[0][0]
        
        if posting_days:
            day_counts = Counter(posting_days)
            day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            patterns['preferred_days'] = [day_names[day] for day, _ in day_counts.most_common(3)]
            patterns['peak_day'] = day_names[day_counts.most_common(1)[0][0]]
        
        return patterns
    
    def save_profile(self, profile: Dict[str, Any], filename: str = "writing_style_profile.json"):
        """Save writing style profile to file"""
        os.makedirs('data', exist_ok=True)
        filepath = os.path.join('data', filename)
        
        with open(filepath, 'w') as f:
            json.dump(profile, f, indent=2, default=str)
        
        logger.info(f"Writing style profile saved to {filepath}")
    
    def load_profile(self, filename: str = "writing_style_profile.json") -> Optional[Dict[str, Any]]:
        """Load writing style profile from file"""
        filepath = os.path.join('data', filename)
        
        try:
            with open(filepath, 'r') as f:
                profile = json.load(f)
            
            logger.info(f"Writing style profile loaded from {filepath}")
            return profile
        except FileNotFoundError:
            logger.warning(f"Writing style profile not found at {filepath}")
            return None
        except Exception as e:
            logger.error(f"Error loading writing style profile: {e}")
            return None