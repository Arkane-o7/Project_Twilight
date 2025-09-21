"""
Streamlit Dashboard for AI Social Media Writer
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import asyncio
import json
import os
from typing import Dict, List, Any

# Import our modules
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

def launch_dashboard(ai_instance):
    """Launch the Streamlit dashboard"""
    # Store AI instance in session state
    if 'ai_instance' not in st.session_state:
        st.session_state.ai_instance = ai_instance
    
    main_dashboard()

def main_dashboard():
    """Main dashboard interface"""
    st.set_page_config(
        page_title="AI Social Media Writer",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 0.75rem;
        border-radius: 0.25rem;
        border: 1px solid #c3e6cb;
    }
    .warning-message {
        background-color: #fff3cd;
        color: #856404;
        padding: 0.75rem;
        border-radius: 0.25rem;
        border: 1px solid #ffeaa7;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown('<h1 class="main-header">🤖 AI Social Media Writer</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("Navigation")
        page = st.selectbox("Choose a page:", [
            "Dashboard",
            "Content Generator",
            "Style Analyzer",
            "Social Media Manager",
            "Analytics",
            "Settings"
        ])
    
    # Main content based on selected page
    if page == "Dashboard":
        dashboard_page()
    elif page == "Content Generator":
        content_generator_page()
    elif page == "Style Analyzer":
        style_analyzer_page()
    elif page == "Social Media Manager":
        social_media_page()
    elif page == "Analytics":
        analytics_page()
    elif page == "Settings":
        settings_page()

def dashboard_page():
    """Main dashboard overview"""
    st.header("📊 Dashboard Overview")
    
    # Quick stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Posts Generated", get_stat("posts_generated", 0))
    
    with col2:
        st.metric("Engagement Rate", f"{get_stat('engagement_rate', 0):.1%}")
    
    with col3:
        st.metric("Platforms Connected", get_stat("platforms_connected", 0))
    
    with col4:
        st.metric("Style Score", f"{get_stat('style_score', 0):.2f}")
    
    st.markdown("---")
    
    # Quick Actions
    st.header("🚀 Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔍 Analyze Writing Style", use_container_width=True):
            with st.spinner("Analyzing your writing style..."):
                if run_async_task("analyze_writing_style"):
                    st.success("✅ Writing style analysis completed!")
                else:
                    st.error("❌ Analysis failed. Check your API connections.")
    
    with col2:
        if st.button("✨ Generate Content", use_container_width=True):
            count = st.number_input("Number of posts", min_value=1, max_value=10, value=3)
            with st.spinner(f"Generating {count} posts..."):
                if run_async_task("generate_content", count):
                    st.success(f"✅ Generated {count} posts!")
                else:
                    st.error("❌ Content generation failed.")
    
    with col3:
        if st.button("📤 Auto Post", use_container_width=True):
            with st.spinner("Posting content..."):
                if run_async_task("auto_post"):
                    st.success("✅ Content posted successfully!")
                else:
                    st.error("❌ Posting failed.")
    
    # Recent Activity
    st.header("📋 Recent Activity")
    display_recent_activity()

def content_generator_page():
    """Content generation interface"""
    st.header("✨ Content Generator")
    
    # Content generation form
    with st.form("content_generator_form"):
        st.subheader("Generate New Content")
        
        col1, col2 = st.columns(2)
        
        with col1:
            content_type = st.selectbox("Content Type", [
                "Original",
                "Trending Topic",
                "Viral Rewrite",
                "Custom Prompt"
            ])
            
            num_posts = st.number_input("Number of posts", min_value=1, max_value=20, value=5)
        
        with col2:
            platforms = st.multiselect("Target Platforms", [
                "Twitter", "Facebook", "Instagram", "LinkedIn"
            ], default=["Twitter"])
            
            include_images = st.checkbox("Include Images", value=True)
        
        if content_type == "Custom Prompt":
            custom_prompt = st.text_area("Custom Prompt", 
                placeholder="Write about productivity tips for remote workers...")
        
        submitted = st.form_submit_button("Generate Content")
        
        if submitted:
            with st.spinner(f"Generating {num_posts} posts..."):
                # Generate content
                success = run_async_task("generate_content", num_posts)
                
                if success:
                    st.success(f"✅ Successfully generated {num_posts} posts!")
                    display_generated_content()
                else:
                    st.error("❌ Content generation failed.")
    
    st.markdown("---")
    
    # Display existing generated content
    st.subheader("📝 Generated Content")
    display_generated_content()

def style_analyzer_page():
    """Writing style analysis interface"""
    st.header("🔍 Writing Style Analyzer")
    
    # Style analysis controls
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Analyze Your Style")
        
        platforms_to_analyze = st.multiselect(
            "Platforms to Analyze",
            ["Twitter", "Facebook", "Instagram", "LinkedIn"],
            default=["Twitter"]
        )
        
        max_posts = st.slider("Maximum posts to analyze", 10, 500, 100)
        
        if st.button("🔍 Start Analysis"):
            with st.spinner("Analyzing your writing style..."):
                if run_async_task("analyze_writing_style"):
                    st.success("✅ Analysis completed!")
                    st.rerun()  # Refresh to show new data
                else:
                    st.error("❌ Analysis failed.")
    
    with col2:
        st.subheader("Style Profile Status")
        
        # Load existing style profile
        style_profile = load_style_profile()
        
        if style_profile:
            st.info(f"✅ Style profile available (analyzed {style_profile.get('total_posts', 0)} posts)")
            
            if st.button("📄 View Detailed Report"):
                display_style_report(style_profile)
        else:
            st.warning("❌ No style profile found. Run analysis first.")
    
    st.markdown("---")
    
    # Style insights
    if load_style_profile():
        display_style_insights()

def social_media_page():
    """Social media management interface"""
    st.header("📱 Social Media Manager")
    
    # Platform connections
    st.subheader("🔗 Platform Connections")
    
    # Test connections
    if st.button("🔍 Test All Connections"):
        with st.spinner("Testing connections..."):
            connections = test_connections()
            
            for platform, status in connections.items():
                if status:
                    st.success(f"✅ {platform.title()}: Connected")
                else:
                    st.error(f"❌ {platform.title()}: Not connected")
    
    st.markdown("---")
    
    # Manual posting
    st.subheader("📝 Manual Post")
    
    with st.form("manual_post_form"):
        content = st.text_area("Post Content", max_chars=280)
        
        col1, col2 = st.columns(2)
        
        with col1:
            post_platforms = st.multiselect("Post to Platforms", [
                "Twitter", "Facebook", "Instagram", "LinkedIn"
            ])
        
        with col2:
            upload_image = st.file_uploader("Upload Image (optional)", 
                type=['png', 'jpg', 'jpeg'])
        
        if st.form_submit_button("📤 Post Now"):
            if content and post_platforms:
                with st.spinner("Posting..."):
                    # Handle image upload
                    image_path = None
                    if upload_image:
                        image_path = save_uploaded_image(upload_image)
                    
                    # Post to selected platforms
                    success_count = 0
                    for platform in post_platforms:
                        if run_async_task("post_to_platform", platform.lower(), content, image_path):
                            success_count += 1
                    
                    if success_count == len(post_platforms):
                        st.success(f"✅ Posted to all {len(post_platforms)} platforms!")
                    elif success_count > 0:
                        st.warning(f"⚠️ Posted to {success_count}/{len(post_platforms)} platforms.")
                    else:
                        st.error("❌ Failed to post to any platform.")
            else:
                st.error("❌ Please enter content and select at least one platform.")
    
    st.markdown("---")
    
    # Engagement automation
    st.subheader("👥 Engagement Automation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🤝 Run Auto-Engagement"):
            with st.spinner("Running auto-engagement..."):
                if run_async_task("auto_engage"):
                    st.success("✅ Auto-engagement completed!")
                else:
                    st.error("❌ Auto-engagement failed.")
    
    with col2:
        engagement_stats = get_engagement_stats()
        st.metric("Today's Engagements", engagement_stats.get('today', 0))

def analytics_page():
    """Analytics and reporting interface"""
    st.header("📈 Analytics")
    
    # Time range selector
    time_range = st.selectbox("Time Range", [
        "Last 7 days",
        "Last 30 days",
        "Last 90 days",
        "All time"
    ])
    
    # Get analytics data
    analytics_data = get_analytics_data(time_range)
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Posts", analytics_data.get('total_posts', 0))
    
    with col2:
        st.metric("Generated Posts", analytics_data.get('generated_posts', 0))
    
    with col3:
        st.metric("Total Engagement", analytics_data.get('total_engagement', 0))
    
    with col4:
        st.metric("Avg Style Score", f"{analytics_data.get('avg_style_score', 0):.2f}")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Posts over time
        st.subheader("📊 Posts Over Time")
        if analytics_data.get('posts_timeline'):
            df = pd.DataFrame(analytics_data['posts_timeline'])
            fig = px.line(df, x='date', y='posts', title="Posts Over Time")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data available for posts timeline.")
    
    with col2:
        # Platform distribution
        st.subheader("📱 Platform Distribution")
        if analytics_data.get('platform_distribution'):
            df = pd.DataFrame(list(analytics_data['platform_distribution'].items()), 
                            columns=['Platform', 'Posts'])
            fig = px.pie(df, values='Posts', names='Platform', title="Posts by Platform")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data available for platform distribution.")
    
    # Engagement analysis
    st.subheader("👥 Engagement Analysis")
    if analytics_data.get('engagement_data'):
        engagement_df = pd.DataFrame(analytics_data['engagement_data'])
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(engagement_df, x='type', y='count', title="Engagement Types")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.line(engagement_df, x='date', y='engagement_rate', 
                         title="Engagement Rate Over Time")
            st.plotly_chart(fig, use_container_width=True)

def settings_page():
    """Settings and configuration interface"""
    st.header("⚙️ Settings")
    
    # API Configuration
    st.subheader("🔑 API Configuration")
    
    with st.expander("Social Media APIs"):
        # Twitter settings
        st.write("**Twitter/X**")
        twitter_api_key = st.text_input("API Key", type="password", key="twitter_api_key")
        twitter_api_secret = st.text_input("API Secret", type="password", key="twitter_api_secret")
        twitter_access_token = st.text_input("Access Token", type="password", key="twitter_access_token")
        twitter_access_token_secret = st.text_input("Access Token Secret", type="password", key="twitter_access_token_secret")
        
        st.markdown("---")
        
        # AI APIs
        st.write("**AI Services**")
        openai_api_key = st.text_input("OpenAI API Key", type="password", key="openai_api_key")
        huggingface_api_key = st.text_input("Hugging Face API Key", type="password", key="huggingface_api_key")
    
    # Content Settings
    st.subheader("📝 Content Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        max_post_length = st.slider("Max Post Length", 50, 500, 280)
        posting_frequency = st.slider("Posting Frequency (hours)", 1, 24, 4)
    
    with col2:
        include_emojis = st.checkbox("Include Emojis", value=True)
        include_hashtags = st.checkbox("Include Hashtags", value=True)
    
    # Automation Settings
    st.subheader("🤖 Automation Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        auto_posting = st.checkbox("Enable Auto Posting")
        auto_engagement = st.checkbox("Enable Auto Engagement")
    
    with col2:
        engagement_rate_limit = st.slider("Engagement Rate Limit (per hour)", 1, 100, 20)
        min_engagement_threshold = st.slider("Min Engagement Threshold", 1, 100, 10)
    
    # Save settings
    if st.button("💾 Save Settings"):
        settings = {
            'max_post_length': max_post_length,
            'posting_frequency': posting_frequency,
            'include_emojis': include_emojis,
            'include_hashtags': include_hashtags,
            'auto_posting': auto_posting,
            'auto_engagement': auto_engagement,
            'engagement_rate_limit': engagement_rate_limit,
            'min_engagement_threshold': min_engagement_threshold
        }
        
        save_settings(settings)
        st.success("✅ Settings saved successfully!")

# Helper functions
def run_async_task(task_name: str, *args):
    """Run async task and return result"""
    try:
        ai_instance = st.session_state.get('ai_instance')
        if not ai_instance:
            return False
        
        # This is a simplified version - in production, you'd use proper async handling
        if task_name == "analyze_writing_style":
            # Simulate the task
            return True
        elif task_name == "generate_content":
            return True
        elif task_name == "auto_post":
            return True
        elif task_name == "auto_engage":
            return True
        
        return False
    except Exception as e:
        st.error(f"Task failed: {e}")
        return False

def get_stat(stat_name: str, default_value=0):
    """Get statistic value"""
    # This would typically query the database
    stats = {
        'posts_generated': 42,
        'engagement_rate': 0.12,
        'platforms_connected': 2,
        'style_score': 0.85
    }
    return stats.get(stat_name, default_value)

def display_recent_activity():
    """Display recent activity"""
    # Mock recent activity data
    activities = [
        {"time": "2 hours ago", "activity": "Generated 3 posts", "status": "success"},
        {"time": "5 hours ago", "activity": "Posted to Twitter", "status": "success"},
        {"time": "1 day ago", "activity": "Analyzed writing style", "status": "success"},
        {"time": "2 days ago", "activity": "Auto-engaged with 15 posts", "status": "success"},
    ]
    
    for activity in activities:
        col1, col2, col3 = st.columns([2, 4, 1])
        
        with col1:
            st.text(activity["time"])
        
        with col2:
            st.text(activity["activity"])
        
        with col3:
            if activity["status"] == "success":
                st.success("✅")
            else:
                st.error("❌")

def display_generated_content():
    """Display generated content"""
    # Load generated content from file
    try:
        with open('data/generated_content.json', 'r') as f:
            content_list = json.load(f)
        
        if content_list:
            for i, content in enumerate(content_list[-5:]):  # Show last 5
                with st.expander(f"Post {i+1}: {content['content'][:50]}..."):
                    st.write(f"**Content:** {content['content']}")
                    st.write(f"**Strategy:** {content.get('strategy', 'Unknown')}")
                    st.write(f"**Platforms:** {', '.join(content.get('platforms', []))}")
                    st.write(f"**Style Score:** {content.get('style_score', 0):.2f}")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button(f"✏️ Edit", key=f"edit_{i}"):
                            pass  # Edit functionality
                    with col2:
                        if st.button(f"📤 Post", key=f"post_{i}"):
                            pass  # Post functionality
                    with col3:
                        if st.button(f"🗑️ Delete", key=f"delete_{i}"):
                            pass  # Delete functionality
        else:
            st.info("No generated content found. Generate some content first!")
            
    except FileNotFoundError:
        st.info("No generated content found. Generate some content first!")

def load_style_profile():
    """Load writing style profile"""
    try:
        with open('data/writing_style_profile.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def display_style_report(style_profile):
    """Display detailed style report"""
    st.subheader("📊 Detailed Style Report")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Posts Analyzed", style_profile.get('total_posts', 0))
        st.metric("Avg Length", f"{style_profile.get('avg_length', 0):.0f} chars")
        st.metric("Complexity", style_profile.get('readability', {}).get('complexity_level', 'Unknown'))
    
    with col2:
        st.metric("Dominant Sentiment", style_profile.get('sentiment_profile', {}).get('dominant_sentiment', 'Unknown'))
        st.metric("Dominant Emotion", style_profile.get('emotion_profile', {}).get('dominant_emotion', 'Unknown'))
        st.metric("Emoji Usage", f"{style_profile.get('language_patterns', {}).get('emoji_usage', 0):.1%}")

def display_style_insights():
    """Display style insights"""
    style_profile = load_style_profile()
    if not style_profile:
        return
    
    st.subheader("💡 Style Insights")
    
    # Create visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        # Sentiment distribution
        sentiment_data = style_profile.get('sentiment_profile', {}).get('sentiment_distribution', {})
        if sentiment_data:
            df = pd.DataFrame(list(sentiment_data.items()), columns=['Sentiment', 'Percentage'])
            fig = px.pie(df, values='Percentage', names='Sentiment', title="Sentiment Distribution")
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Top topics
        topics = style_profile.get('topics', [])[:5]
        if topics:
            df = pd.DataFrame({'Topic': topics, 'Frequency': range(len(topics), 0, -1)})
            fig = px.bar(df, x='Topic', y='Frequency', title="Top Topics")
            st.plotly_chart(fig, use_container_width=True)

def test_connections():
    """Test social media connections"""
    # This would test actual connections
    return {
        'twitter': True,
        'facebook': False,
        'instagram': False,
        'linkedin': False
    }

def save_uploaded_image(uploaded_file):
    """Save uploaded image"""
    os.makedirs('uploads', exist_ok=True)
    file_path = os.path.join('uploads', uploaded_file.name)
    
    with open(file_path, 'wb') as f:
        f.write(uploaded_file.getbuffer())
    
    return file_path

def get_engagement_stats():
    """Get engagement statistics"""
    return {'today': 25, 'this_week': 180, 'this_month': 720}

def get_analytics_data(time_range):
    """Get analytics data for specified time range"""
    # Mock analytics data
    return {
        'total_posts': 150,
        'generated_posts': 120,
        'total_engagement': 2500,
        'avg_style_score': 0.82,
        'posts_timeline': [
            {'date': '2024-01-01', 'posts': 5},
            {'date': '2024-01-02', 'posts': 8},
            {'date': '2024-01-03', 'posts': 6},
        ],
        'platform_distribution': {
            'Twitter': 80,
            'Facebook': 45,
            'LinkedIn': 25
        },
        'engagement_data': [
            {'type': 'Likes', 'count': 1200},
            {'type': 'Comments', 'count': 300},
            {'type': 'Shares', 'count': 150},
        ]
    }

def save_settings(settings):
    """Save user settings"""
    os.makedirs('data', exist_ok=True)
    with open('data/user_settings.json', 'w') as f:
        json.dump(settings, f, indent=2)

if __name__ == "__main__":
    # For standalone testing
    main_dashboard()