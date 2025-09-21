# AI Social Media Twin 🤖

An AI-powered social media writing assistant that analyzes your personal writing style and generates authentic content that sounds exactly like you.

## 🚀 Features

- **Style Analysis**: Analyzes your Twitter posts to understand your unique writing style
- **Content Generation**: Creates original posts that match your tone, vocabulary, and patterns
- **Post Variations**: Rewrites existing posts in your personal style
- **Multiple Topics**: Generate content on any topic while maintaining your voice
- **Export Options**: Save generated content as text or JSON files
- **Demo Mode**: Try the app without API keys using sample data

## 🛠 Tech Stack

- **Backend**: Python with OpenAI GPT-3.5-turbo
- **Social Media**: Twitter API v2 (Tweepy)
- **Frontend**: Streamlit for rapid web development
- **Deployment**: Ready for Streamlit Cloud

## ⚡ Quick Start (5 minutes)

### 1. Clone & Setup
```bash
git clone https://github.com/Arkane-o7/Project_Twilight.git
cd Project_Twilight
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure APIs (Optional)
```bash
cp .env.example .env
# Edit .env with your API keys:
# - OpenAI API key from https://platform.openai.com/api-keys
# - Twitter Bearer Token from https://developer.twitter.com/
```

### 3. Run the App
```bash
streamlit run app.py
```

### 4. Try Demo Mode
- Open the app in your browser
- Enable "Demo Mode" in the sidebar
- Click "Analyze Writing Style" to see sample analysis
- Generate posts on any topic!

## 🎯 How It Works

1. **Input**: Enter a Twitter username and topic
2. **Analysis**: AI analyzes recent tweets to create a style profile
3. **Generation**: Creates new content matching the analyzed style
4. **Export**: Copy or download generated posts

## 📋 API Requirements

### Required for Full Features:
- **OpenAI API Key**: For style analysis and content generation
- **Twitter Bearer Token**: For fetching user tweets

### Free Trial Available:
- OpenAI: $5 free credits for new accounts
- Twitter: Free tier includes 500,000 tweets/month

## 🎮 Demo Mode

No API keys? No problem! Enable demo mode to:
- See sample style analysis
- Generate content using sample data
- Test all features without setup

## 📊 Style Analysis Includes

- **Tone**: Casual, professional, humorous, etc.
- **Topics**: Main themes the person writes about
- **Writing Patterns**: Questions, personal stories, advice style
- **Vocabulary Level**: Simple to academic
- **Emoji & Hashtag Usage**: Frequency and patterns
- **Personality Traits**: Observable characteristics
- **Content Structure**: How posts are organized

## 🔧 Advanced Usage

### Batch Content Generation
```python
from style_analyzer import StyleAnalyzer

analyzer = StyleAnalyzer()
tweets = analyzer.get_recent_tweets("username")
style = analyzer.analyze_style(tweets)
posts = analyzer.generate_content(style, "AI trends", count=5)
```

### Custom Style Profiles
You can manually create or modify style profiles for specific use cases.

## 🚀 Deployment

### Streamlit Cloud (Recommended)
1. Fork this repository
2. Connect to Streamlit Cloud
3. Add secrets for API keys
4. Deploy with one click

### Local Production
```bash
streamlit run app.py --server.port 8080
```

## 📈 Roadmap

### Current (MVP)
- ✅ Style analysis from Twitter
- ✅ Content generation
- ✅ Web interface
- ✅ Export functionality

### Phase 2
- [ ] Auto-posting to social media
- [ ] Multi-platform support (Instagram, LinkedIn)
- [ ] Viral content detection
- [ ] Image generation integration
- [ ] Scheduling system

### Phase 3
- [ ] Comments and reactions
- [ ] Team collaboration
- [ ] Analytics dashboard
- [ ] A/B testing for posts

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🆘 Support

- **Issues**: Report bugs or request features
- **Demo**: Try the live demo mode
- **Docs**: Check this README for setup help

## 🎉 Success Stories

This MVP approach focuses on the 80/20 rule - delivering 80% of the value with 20% of the complexity. Perfect for:

- **Content Creators**: Maintain consistent voice across platforms
- **Businesses**: Scale social media with authentic content
- **Individuals**: Never run out of post ideas
- **Agencies**: Create content for multiple clients efficiently

---

**Built with ❤️ for authentic social media content**
