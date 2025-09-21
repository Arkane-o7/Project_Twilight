# AI Social Media Writer MVP

🤖 **An AI-powered social media automation tool that learns your writing style and creates authentic content automatically.**

## Features

✨ **AI Writing Style Analysis** - Analyzes your previous posts to understand your unique voice
📝 **Intelligent Content Generation** - Creates posts that sound like you using advanced AI
🖼️ **AI Image Generation** - Automatically generates images for your posts
📱 **Multi-Platform Support** - Works with Twitter, Facebook, Instagram, and LinkedIn
🔥 **Viral Content Detection** - Finds trending topics and creates engaging content
🤝 **Auto-Engagement** - Automatically likes, comments, and shares relevant content
📊 **Analytics Dashboard** - Track performance and optimize your strategy
⚡ **Real-time Automation** - Schedule and post content automatically

## Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/Arkane-o7/Project_Twilight.git
cd Project_Twilight

# Run setup script
python setup.py

# Or install manually
pip install -r requirements.txt
```

### 2. Configuration

1. Copy `.env.example` to `.env`
2. Add your API keys:
   - **Twitter API**: Get from [Twitter Developer Portal](https://developer.twitter.com/)
   - **OpenAI API**: Get from [OpenAI](https://platform.openai.com/)
   - **Other platforms**: See [API Setup Guide](#api-setup-guide)

### 3. First Run

```bash
# Initial setup and connection testing
python mvp_ai_social_media.py --setup

# Analyze your writing style
python mvp_ai_social_media.py --analyze

# Generate content
python mvp_ai_social_media.py --generate 5

# Launch web interface
python mvp_ai_social_media.py --ui
```

## Usage Examples

### Command Line Interface

```bash
# Analyze writing style from your posts
python mvp_ai_social_media.py --analyze

# Generate 10 pieces of content
python mvp_ai_social_media.py --generate 10

# Auto-post generated content
python mvp_ai_social_media.py --post

# Run auto-engagement
python mvp_ai_social_media.py --engage

# Full automation cycle
python mvp_ai_social_media.py --all
```

### Web Interface

```bash
# Launch the dashboard
python mvp_ai_social_media.py --ui
```

Then open http://localhost:8501 in your browser.

## API Setup Guide

### Twitter/X API

1. Go to [Twitter Developer Portal](https://developer.twitter.com/)
2. Create a new app
3. Generate API keys and tokens
4. Add to `.env`:
   ```
   TWITTER_API_KEY=your_api_key
   TWITTER_API_SECRET=your_api_secret
   TWITTER_ACCESS_TOKEN=your_access_token
   TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret
   TWITTER_BEARER_TOKEN=your_bearer_token
   ```

### OpenAI API

1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Create an API key
3. Add to `.env`:
   ```
   OPENAI_API_KEY=your_openai_api_key
   ```

### Instagram API

1. Go to [Facebook Developers](https://developers.facebook.com/)
2. Create an app and get Instagram Basic Display API access
3. Add to `.env`:
   ```
   INSTAGRAM_ACCESS_TOKEN=your_access_token
   ```

### Facebook API

1. Use the same app from Instagram setup
2. Add to `.env`:
   ```
   FACEBOOK_ACCESS_TOKEN=your_access_token
   ```

### LinkedIn API

1. Go to [LinkedIn Developers](https://www.linkedin.com/developers/)
2. Create an app and get API access
3. Add to `.env`:
   ```
   LINKEDIN_ACCESS_TOKEN=your_access_token
   ```

## Architecture

```
src/
├── core/                 # Core configuration and utilities
├── social_media/         # Social media platform integrations
├── ai_engine/           # AI and ML components
├── content_generation/  # Content generation logic
├── image_processing/    # Image generation and processing
├── database/           # Database models and operations
└── ui/                 # Web interface
```

## Free & Open Source Stack

- **Backend**: Python, FastAPI, SQLAlchemy
- **AI/ML**: Transformers, Hugging Face, OpenAI API
- **Frontend**: Streamlit
- **Database**: SQLite (default), PostgreSQL support
- **Image Generation**: Stable Diffusion, Pillow
- **Social APIs**: Official platform APIs
- **Deployment**: Docker, Railway/Render free tiers

## Features in Detail

### 🔍 AI Writing Style Analysis

- Analyzes sentiment, emotion, and tone
- Measures readability and complexity
- Identifies language patterns and preferences
- Tracks posting frequency and timing
- Creates personalized style profiles

### ✨ Intelligent Content Generation

- **Trending Topics**: Creates content based on what's viral
- **Original Content**: Generates unique posts in your style
- **Viral Rewrites**: Adapts popular content to your voice
- **Custom Prompts**: Generate content from your ideas

### 🖼️ AI Image Generation

- Automatic image generation for posts
- Multiple styles: realistic, artistic, minimalist
- Platform optimization (square for Instagram, etc.)
- Text-to-image fallback for any content

### 📱 Multi-Platform Automation

- **Twitter**: Full posting and engagement
- **Facebook**: Post sharing and basic engagement
- **Instagram**: Image posts (requires business account)
- **LinkedIn**: Professional content sharing

### 🤝 Smart Engagement

- Analyzes posts for engagement worthiness
- Generates contextual comments and replies
- Rate limiting and safety measures
- Authentic interaction patterns

### 📊 Analytics & Insights

- Performance tracking across platforms
- Style consistency scoring
- Engagement rate analysis
- Content optimization suggestions

## Advanced Configuration

### Custom AI Models

```python
# Use your own fine-tuned models
CUSTOM_TEXT_MODEL=path/to/your/model
CUSTOM_IMAGE_MODEL=path/to/your/model
```

### Content Scheduling

```python
# Schedule posts for optimal times
POSTING_SCHEDULE=9,12,15,18  # Hours
TIMEZONE=America/New_York
```

### Engagement Rules

```python
# Customize engagement behavior
MIN_ENGAGEMENT_THRESHOLD=10
MAX_ENGAGEMENTS_PER_HOUR=20
ENGAGEMENT_KEYWORDS=AI,tech,startup
```

## Deployment

### Local Development

```bash
python mvp_ai_social_media.py --ui
```

### Docker Deployment

```bash
docker build -t ai-social-media .
docker run -p 8501:8501 ai-social-media
```

### Cloud Deployment

Deploy to Railway, Render, or Heroku using the included configuration files.

## Safety & Ethics

- **Rate Limiting**: Respects platform rate limits
- **Content Filtering**: Avoids spam and inappropriate content
- **Human Oversight**: All content can be reviewed before posting
- **Transparency**: Clear attribution of AI-generated content
- **Privacy**: Your data stays with you

## Troubleshooting

### Common Issues

1. **API Connection Errors**
   - Check your API keys in `.env`
   - Verify API permissions and quotas

2. **Import Errors**
   - Run `pip install -r requirements.txt`
   - Check Python version (3.8+ required)

3. **Image Generation Issues**
   - Ensure sufficient disk space
   - Check GPU availability for local models

4. **Database Errors**
   - Delete `social_ai.db` to reset database
   - Check file permissions

### Getting Help

- Check the [Issues](https://github.com/Arkane-o7/Project_Twilight/issues) page
- Read the [Documentation](https://github.com/Arkane-o7/Project_Twilight/wiki)
- Join our [Discord](https://discord.gg/project-twilight)

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

## Roadmap

- [ ] **Video Content Generation**
- [ ] **TikTok Integration**
- [ ] **Advanced Analytics**
- [ ] **Team Collaboration Features**
- [ ] **Custom Model Training**
- [ ] **API Access for Developers**
- [ ] **Mobile App**

## Credits

Built with ❤️ by the Project Twilight team using:
- [Transformers](https://huggingface.co/transformers/)
- [Streamlit](https://streamlit.io/)
- [OpenAI](https://openai.com/)
- [Stable Diffusion](https://stability.ai/)

---

**⭐ Star this repo if you find it useful!**

**💰 Building a startup with this? We'd love to hear about it!**
