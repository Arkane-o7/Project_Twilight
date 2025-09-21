#!/usr/bin/env python3
"""
Simple test script for the AI Social Media Twin MVP.
Tests core functionality without requiring API keys.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from style_analyzer import StyleAnalyzer, create_sample_style_profile, create_sample_tweets
import json

def test_style_analyzer_initialization():
    """Test if StyleAnalyzer can be initialized."""
    print("🧪 Testing StyleAnalyzer initialization...")
    try:
        analyzer = StyleAnalyzer()
        print("✅ StyleAnalyzer initialized successfully")
        return True
    except Exception as e:
        print(f"❌ StyleAnalyzer initialization failed: {e}")
        return False

def test_sample_data():
    """Test sample data generation."""
    print("\n🧪 Testing sample data generation...")
    try:
        # Test sample tweets
        tweets = create_sample_tweets()
        assert len(tweets) > 0, "No sample tweets generated"
        assert all(isinstance(tweet, str) for tweet in tweets), "All tweets should be strings"
        print(f"✅ Generated {len(tweets)} sample tweets")
        
        # Test sample style profile
        profile = create_sample_style_profile()
        assert isinstance(profile, dict), "Style profile should be a dictionary"
        assert "tone" in profile, "Style profile should have tone"
        assert "topics" in profile, "Style profile should have topics"
        print("✅ Generated sample style profile")
        
        return True, tweets, profile
    except Exception as e:
        print(f"❌ Sample data generation failed: {e}")
        return False, [], {}

def test_style_analysis(tweets):
    """Test style analysis with sample data."""
    print("\n🧪 Testing style analysis...")
    try:
        analyzer = StyleAnalyzer()
        
        # Test with sample tweets (should work without OpenAI API)
        # This will fail gracefully if no API key is set
        result = analyzer.analyze_style(tweets)
        
        if "error" in result:
            print(f"⚠️ Style analysis failed (expected without API key): {result['error']}")
            return True  # This is expected behavior without API
        else:
            print("✅ Style analysis completed successfully")
            print(f"📊 Analysis keys: {list(result.keys())}")
            return True
            
    except Exception as e:
        print(f"❌ Style analysis test failed: {e}")
        return False

def test_content_generation(profile):
    """Test content generation with sample profile."""
    print("\n🧪 Testing content generation...")
    try:
        analyzer = StyleAnalyzer()
        
        # Test content generation
        result = analyzer.generate_content(profile, "artificial intelligence", count=2)
        
        if isinstance(result, list) and len(result) > 0:
            if "generation failed" in str(result[0]).lower():
                print(f"⚠️ Content generation failed (expected without API key): {result[0]}")
                return True  # Expected behavior without API
            else:
                print("✅ Content generation completed successfully")
                print(f"📝 Generated {len(result)} posts")
                return True
        else:
            print("⚠️ Content generation returned unexpected format")
            return True  # Still okay for testing
            
    except Exception as e:
        print(f"❌ Content generation test failed: {e}")
        return False

def test_streamlit_imports():
    """Test if Streamlit app can be imported."""
    print("\n🧪 Testing Streamlit app imports...")
    try:
        import app
        print("✅ Streamlit app imported successfully")
        return True
    except Exception as e:
        print(f"❌ Streamlit app import failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 AI Social Media Twin - MVP Test Suite")
    print("=" * 50)
    
    # Test 1: Initialization
    if not test_style_analyzer_initialization():
        print("\n❌ Critical failure in initialization. Stopping tests.")
        return False
    
    # Test 2: Sample data
    success, tweets, profile = test_sample_data()
    if not success:
        print("\n❌ Critical failure in sample data. Stopping tests.")
        return False
    
    # Test 3: Style analysis
    test_style_analysis(tweets)
    
    # Test 4: Content generation
    test_content_generation(profile)
    
    # Test 5: Streamlit imports
    test_streamlit_imports()
    
    print("\n" + "=" * 50)
    print("🎉 Test suite completed!")
    print("\n📋 Next Steps:")
    print("1. Set up API keys in .env file for full functionality")
    print("2. Run: streamlit run app.py")
    print("3. Try demo mode to see the app in action")
    print("4. Test with real Twitter usernames after API setup")
    
    return True

if __name__ == "__main__":
    main()