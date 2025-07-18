# 🤖 Friday AI - Your Personal AI Assistant

A Python-based AI assistant inspired by *Jarvis* from Iron Man, featuring a beautiful web interface and voice capabilities.

## ✨ Features

- 🎤 **Voice Assistant** - Natural speech interaction
- 🔍 **Web Search** - Real-time internet search capabilities
- 🌤️ **Weather Updates** - Current weather information
- 📨 **Email Sending** - Send emails through Gmail
- 📷 **Computer Vision** - Screen monitoring and text recognition
- 🗣️ **Multi-language Support** - Hindi and English
- 🌐 **Web Interface** - Beautiful UI with voice animations
- 🎯 **LiveKit Integration** - Real-time voice communication

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- LiveKit Cloud account
- Google API key (for speech and search)
- Gmail account (for email feature)

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/friday-ai-assistant.git
   cd friday-ai-assistant
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   Create a `.env` file with your API keys:
   ```env
   LIVEKIT_URL=your_livekit_url
   LIVEKIT_SECRET=your_livekit_secret
   GOOGLE_API_KEY=your_google_api_key
   GMAIL_EMAIL=your_email@gmail.com
   GMAIL_PASSWORD=your_app_password
   ```

5. **Start the web interface**
   ```bash
   python run.py
   ```

6. **Open your browser**
   Navigate to `http://localhost:5000`

## 🌐 Web Interface

The project includes a beautiful web interface with:

- 🎨 **Modern Design** - Glassmorphism UI with gradients
- 🎤 **Voice Animation** - Pulsing circles when active
- 🟢 **Start/Stop Controls** - Easy agent management
- 🔇 **Mute Functionality** - Audio control
- 📱 **Responsive Design** - Works on mobile and desktop
- ⚡ **Real-time Status** - Live updates

### Web Interface Features

- **Start Button**: Runs the AI assistant
- **Stop Button**: Safely stops the assistant
- **Mute Button**: Controls audio output
- **Voice Animation**: Visual feedback for active state
- **Status Updates**: Real-time connection status

## 🚀 Deployment

### Render Deployment

1. **Fork/Clone** this repository to your GitHub account
2. **Create Render account** at [render.com](https://render.com)
3. **New Web Service** → Connect your GitHub repository
4. **Configure settings**:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Environment**: Python 3
5. **Add environment variables** in Render dashboard
6. **Deploy** and get your live URL

### Environment Variables for Deployment

Add these to your Render environment:

```
LIVEKIT_URL=https://your-livekit-url.livekit.cloud
LIVEKIT_SECRET=your_livekit_secret
GOOGLE_API_KEY=your_google_api_key
GMAIL_EMAIL=your_email@gmail.com
GMAIL_PASSWORD=your_app_password
```

### Alternative Deployment Options

- **Railway**: Better for LiveKit agents
- **DigitalOcean App Platform**: More reliable
- **Google Cloud Run**: Serverless, pay-per-use

## 🛠️ Project Structure

```
friday-ai-assistant/
├── agent.py              # Main AI assistant logic
├── app.py                # Flask web server
├── run.py                # Easy startup script
├── tools.py              # Core tools (weather, search, email)
├── prompts.py            # AI prompts and instructions
├── All_tools/            # Advanced tools (screen monitoring)
├── static/
│   └── index.html        # Web interface
├── requirements.txt       # Python dependencies
├── .env                  # Environment variables (create this)
├── Procfile              # For deployment
├── runtime.txt           # Python version
└── render.yaml           # Render configuration
```

## 🎯 LiveKit Setup

1. **Create LiveKit Cloud account** at [livekit.io](https://livekit.io)
2. **Get your API keys** from the dashboard
3. **Configure your project** with the provided URL and secret
4. **Test the connection** using the web interface

## 🔧 Configuration

### Required API Keys

- **LiveKit**: For real-time voice communication
- **Google API**: For speech recognition and search
- **Gmail**: For email functionality (optional)

### Optional Features

- **Screen Monitoring**: Requires additional permissions
- **Browser Integration**: For web automation
- **Email Sending**: Requires Gmail app password

## 🐛 Troubleshooting

### Common Issues

1. **LiveKit Connection Failed**
   - Check your LiveKit URL and secret
   - Ensure your LiveKit project is active

2. **Voice Not Working**
   - Verify microphone permissions
   - Check browser console for errors

3. **Deployment Issues**
   - Ensure all environment variables are set
   - Check build logs in Render dashboard

### Local Development Issues

- **Port already in use**: Change port in `app.py`
- **Missing dependencies**: Run `pip install -r requirements.txt`
- **Environment variables**: Create `.env` file

## 📚 Tutorial Video

Before you start, **make sure to follow this tutorial to set up the voice agent correctly**:  


## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- **LiveKit** for real-time voice communication
- **Google AI** for speech recognition
- **OpenAI** for language model integration

---

**Made with ❤️ for AI enthusiasts**

> "Sometimes you gotta run before you can walk." - Tony Stark

