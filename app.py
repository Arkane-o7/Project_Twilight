import streamlit as st
import json
import time
from datetime import datetime
from style_analyzer import StyleAnalyzer, create_sample_style_profile, create_sample_tweets

# Page configuration
st.set_page_config(
    page_title="AI Social Media Twin",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1DA1F2;
        margin-bottom: 2rem;
    }
    .feature-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .post-container {
        background-color: #ffffff;
        border: 1px solid #e1e8ed;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'analyzer' not in st.session_state:
    st.session_state.analyzer = StyleAnalyzer()
if 'style_profile' not in st.session_state:
    st.session_state.style_profile = None
if 'generated_posts' not in st.session_state:
    st.session_state.generated_posts = []
if 'tweets_cache' not in st.session_state:
    st.session_state.tweets_cache = {}

def main():
    # Header
    st.markdown('<h1 class="main-header">🤖 AI Social Media Twin</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p style="text-align: center; font-size: 1.2em; color: #666;">Analyze your writing style → Generate content that sounds exactly like YOU</p>',
        unsafe_allow_html=True
    )
    
    # Sidebar with instructions and API status
    with st.sidebar:
        st.markdown("## 🎯 How it works:")
        st.markdown("""
        1. **Enter your Twitter username** (without @)
        2. **Specify topics** for new posts
        3. **AI analyzes** your writing style
        4. **Generate posts** that sound like you!
        """)
        
        # API Status Check
        st.markdown("## 🔧 API Status")
        check_api_status()
        
        # Demo Mode Toggle
        st.markdown("## 🎮 Demo Mode")
        demo_mode = st.checkbox("Use sample data (no API required)", help="Try the app with sample tweets and style analysis")
        
        if demo_mode:
            st.info("Demo mode enabled! Using sample data to showcase features.")
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📊 Style Analysis")
        
        # User input section
        username = st.text_input(
            "Twitter username (without @):",
            placeholder="elonmusk",
            disabled=demo_mode,
            help="Enter any public Twitter username to analyze their writing style"
        )
        
        # Analysis button
        if st.button("🔍 Analyze Writing Style", type="primary"):
            analyze_style(username, demo_mode)
        
        # Display style profile
        display_style_profile()
    
    with col2:
        st.markdown("### ✨ Content Generation")
        
        # Topic input
        topic = st.text_input(
            "What topic should I create posts about?",
            placeholder="AI trends, startup tips, productivity hacks...",
            help="Be specific for better results"
        )
        
        # Number of posts
        num_posts = st.slider("Number of posts to generate:", 1, 5, 3)
        
        # Generation type
        generation_type = st.radio(
            "Generation type:",
            ["Create original posts", "Rewrite existing post"],
            help="Choose whether to create new posts or rewrite an existing one"
        )
        
        # Original post input for rewriting
        if generation_type == "Rewrite existing post":
            original_post = st.text_area(
                "Original post to rewrite:",
                placeholder="Paste the post you want to rewrite in your style...",
                height=100
            )
        
        # Generate button
        generate_disabled = (not st.session_state.style_profile or 
                           not topic or 
                           (generation_type == "Rewrite existing post" and not original_post))
        
        if st.button("🚀 Generate Posts", type="primary", disabled=generate_disabled):
            if generation_type == "Create original posts":
                generate_content(topic, num_posts)
            else:
                generate_variations(original_post, num_posts)
        
        # Display generated content
        display_generated_posts()
    
    # Additional features
    st.markdown("---")
    display_additional_features()

def check_api_status():
    """Check and display API configuration status."""
    import os
    
    openai_configured = bool(os.getenv("OPENAI_API_KEY"))
    twitter_configured = bool(os.getenv("TWITTER_BEARER_TOKEN"))
    
    st.write("**OpenAI API:**", "✅ Configured" if openai_configured else "❌ Not configured")
    st.write("**Twitter API:**", "✅ Configured" if twitter_configured else "❌ Not configured")
    
    if not openai_configured or not twitter_configured:
        st.warning("⚠️ Some APIs not configured. Use demo mode or check .env file.")
        with st.expander("API Setup Instructions"):
            st.markdown("""
            **To use all features:**
            1. Copy `.env.example` to `.env`
            2. Add your OpenAI API key
            3. Add your Twitter Bearer Token
            4. Restart the app
            
            **Get API Keys:**
            - OpenAI: https://platform.openai.com/api-keys
            - Twitter: https://developer.twitter.com/
            """)

def analyze_style(username, demo_mode):
    """Analyze writing style from Twitter posts."""
    if demo_mode:
        # Use sample data
        with st.spinner("Analyzing sample writing style..."):
            time.sleep(2)  # Simulate API call
            st.session_state.style_profile = create_sample_style_profile()
            st.session_state.tweets_cache['demo'] = create_sample_tweets()
        st.success("✅ Sample style analysis complete!")
        return
    
    if not username:
        st.error("Please enter a Twitter username.")
        return
    
    try:
        # Check cache first
        cache_key = f"tweets_{username}"
        if cache_key in st.session_state.tweets_cache:
            tweets = st.session_state.tweets_cache[cache_key]
            st.info(f"Using cached tweets for @{username}")
        else:
            # Fetch tweets
            with st.spinner(f"Fetching recent tweets from @{username}..."):
                tweets = st.session_state.analyzer.get_recent_tweets(username, count=20)
                if tweets:
                    st.session_state.tweets_cache[cache_key] = tweets
        
        if not tweets:
            st.error(f"❌ Couldn't fetch tweets for @{username}. Check username or API limits.")
            return
        
        st.success(f"✅ Found {len(tweets)} recent tweets!")
        
        # Analyze style
        with st.spinner("🧠 Analyzing writing style with AI..."):
            style_profile = st.session_state.analyzer.analyze_style(tweets)
            
        if "error" in style_profile:
            st.error(f"❌ Style analysis failed: {style_profile['error']}")
            return
        
        st.session_state.style_profile = style_profile
        st.success("✅ Writing style analysis complete!")
        
    except Exception as e:
        st.error(f"❌ Analysis failed: {str(e)}")

def display_style_profile():
    """Display the analyzed style profile."""
    if not st.session_state.style_profile:
        st.info("👆 Analyze a Twitter account first to see the writing style profile.")
        return
    
    profile = st.session_state.style_profile
    
    if "error" in profile:
        st.error(f"Analysis error: {profile['error']}")
        return
    
    st.markdown("#### 📈 Style Profile Results")
    
    # Create expandable sections for different aspects
    with st.expander("✨ Writing Style Overview", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            if "tone" in profile:
                st.write(f"**Tone:** {profile['tone']}")
            if "vocabulary_level" in profile:
                st.write(f"**Vocabulary:** {profile['vocabulary_level']}")
            if "avg_length" in profile:
                st.write(f"**Post Length:** {profile['avg_length']}")
        
        with col2:
            if "emoji_usage" in profile:
                st.write(f"**Emoji Usage:** {profile['emoji_usage']}")
            if "hashtag_style" in profile:
                st.write(f"**Hashtags:** {profile['hashtag_style']}")
            if "content_structure" in profile:
                st.write(f"**Structure:** {profile['content_structure']}")
    
    with st.expander("📝 Content Patterns"):
        if "topics" in profile and profile["topics"]:
            st.write("**Common Topics:**")
            for topic in profile["topics"][:5]:  # Show top 5 topics
                st.write(f"• {topic}")
        
        if "writing_patterns" in profile and profile["writing_patterns"]:
            st.write("**Writing Patterns:**")
            for pattern in profile["writing_patterns"][:5]:
                st.write(f"• {pattern}")
    
    with st.expander("🎭 Personality Insights"):
        if "personality_traits" in profile and profile["personality_traits"]:
            st.write("**Personality Traits:**")
            for trait in profile["personality_traits"]:
                st.write(f"• {trait}")
        
        if "punctuation_style" in profile:
            st.write(f"**Punctuation Style:** {profile['punctuation_style']}")
    
    # Analysis metadata
    if "analysis_date" in profile:
        st.caption(f"Analysis completed: {profile['analysis_date']} | Tweets analyzed: {profile.get('tweet_count', 'N/A')}")

def generate_content(topic, num_posts):
    """Generate original content based on style profile."""
    try:
        with st.spinner(f"🎨 Generating {num_posts} posts about '{topic}' in your style..."):
            posts = st.session_state.analyzer.generate_content(
                st.session_state.style_profile,
                topic,
                num_posts
            )
        
        st.session_state.generated_posts = posts
        st.success(f"✅ Generated {len(posts)} posts!")
        
    except Exception as e:
        st.error(f"❌ Content generation failed: {str(e)}")

def generate_variations(original_post, num_posts):
    """Generate variations of an existing post."""
    try:
        with st.spinner(f"🔄 Creating {num_posts} variations in your style..."):
            posts = st.session_state.analyzer.generate_variations(
                original_post,
                st.session_state.style_profile,
                num_posts
            )
        
        st.session_state.generated_posts = posts
        st.success(f"✅ Generated {len(posts)} variations!")
        
    except Exception as e:
        st.error(f"❌ Variation generation failed: {str(e)}")

def display_generated_posts():
    """Display generated posts with copy buttons."""
    if not st.session_state.generated_posts:
        st.info("👆 Generate some posts first to see them here.")
        return
    
    st.markdown("#### 🎯 Generated Posts")
    
    for i, post in enumerate(st.session_state.generated_posts, 1):
        with st.container():
            st.markdown(f'<div class="post-container">', unsafe_allow_html=True)
            st.markdown(f"**Post {i}:**")
            st.write(post)
            
            # Copy button (using code block for easy copying)
            if st.button(f"📋 Copy Post {i}", key=f"copy_{i}"):
                st.code(post, language=None)
                st.info("📋 Post ready to copy!")
            
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown("")

def display_additional_features():
    """Display additional features and export options."""
    if st.session_state.generated_posts:
        st.markdown("### 💾 Export & Save")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📄 Export as Text"):
                export_text = "\n\n---\n\n".join([f"Post {i+1}:\n{post}" for i, post in enumerate(st.session_state.generated_posts)])
                st.download_button(
                    label="Download Text File",
                    data=export_text,
                    file_name=f"generated_posts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )
        
        with col2:
            if st.button("📊 Export as JSON"):
                export_data = {
                    "generated_posts": st.session_state.generated_posts,
                    "style_profile": st.session_state.style_profile,
                    "timestamp": datetime.now().isoformat()
                }
                st.download_button(
                    label="Download JSON File",
                    data=json.dumps(export_data, indent=2),
                    file_name=f"ai_posts_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
        
        with col3:
            if st.button("🔄 Clear All"):
                st.session_state.generated_posts = []
                st.session_state.style_profile = None
                st.rerun()

if __name__ == "__main__":
    main()