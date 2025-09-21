#!/usr/bin/env python3
"""
Setup script for AI Social Media Writer MVP
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def print_banner():
    """Print setup banner"""
    print("=" * 60)
    print("🤖 AI Social Media Writer MVP Setup")
    print("=" * 60)
    print()

def check_python_version():
    """Check Python version"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    print(f"✅ Python {sys.version.split()[0]} detected")

def install_requirements():
    """Install required packages"""
    print("\n📦 Installing required packages...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully")
    except subprocess.CalledProcessError:
        print("❌ Failed to install requirements")
        return False
    
    return True

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directories...")
    
    directories = [
        "data",
        "logs",
        "generated_images",
        "uploads",
        "models"
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created {directory}/")

def setup_environment():
    """Setup environment file"""
    print("\n🔧 Setting up environment...")
    
    if not os.path.exists('.env'):
        shutil.copy('.env.example', '.env')
        print("✅ Created .env file from template")
        print("⚠️  Please edit .env file with your API keys")
    else:
        print("✅ .env file already exists")

def download_models():
    """Download required AI models"""
    print("\n🤖 Checking AI models...")
    
    try:
        import nltk
        print("📥 Downloading NLTK data...")
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        nltk.download('vader_lexicon', quiet=True)
        print("✅ NLTK data downloaded")
    except ImportError:
        print("⚠️  NLTK not installed, will download during first run")

def test_installation():
    """Test the installation"""
    print("\n🧪 Testing installation...")
    
    try:
        # Test imports
        import streamlit
        import transformers
        import pandas
        import plotly
        print("✅ All core packages imported successfully")
        
        # Test MVP script
        result = subprocess.run([sys.executable, "mvp_ai_social_media.py", "--help"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ MVP script is working")
        else:
            print("⚠️  MVP script test failed")
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    
    return True

def print_next_steps():
    """Print next steps"""
    print("\n" + "=" * 60)
    print("🎉 Setup Complete!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Edit .env file with your API keys")
    print("2. Run: python mvp_ai_social_media.py --setup")
    print("3. Start generating content: python mvp_ai_social_media.py --analyze")
    print("4. Launch web interface: python mvp_ai_social_media.py --ui")
    print()
    print("For help: python mvp_ai_social_media.py --help")
    print()

def main():
    """Main setup function"""
    print_banner()
    
    # Check requirements
    check_python_version()
    
    # Setup steps
    if not install_requirements():
        sys.exit(1)
    
    create_directories()
    setup_environment()
    download_models()
    
    if test_installation():
        print_next_steps()
    else:
        print("\n❌ Setup completed with errors. Please check the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main()