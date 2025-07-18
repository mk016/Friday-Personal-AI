#!/usr/bin/env python3
"""
Friday AI Assistant - Web Interface
Run this script to start the web interface for Friday AI
"""

import os
import sys
import subprocess

def check_dependencies():
    """Check if all required dependencies are installed"""
    try:
        import flask
        print("✅ Flask is installed")
    except ImportError:
        print("❌ Flask is not installed. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "flask==2.3.3"])
        print("✅ Flask installed successfully")

def main():
    print("🤖 Friday AI Assistant - Web Interface")
    print("=" * 50)
    
    # Check dependencies
    check_dependencies()
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("⚠️  Warning: .env file not found!")
        print("   Make sure you have configured your environment variables.")
        print("   Required variables: LiveKit URL, LiveKit Secret, etc.")
    
    print("\n🚀 Starting Friday AI Web Interface...")
    print("📱 Open your browser and go to: http://localhost:5000")
    print("🛑 Press Ctrl+C to stop the server")
    print("=" * 50)
    
    # Import and run the Flask app
    try:
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        print("Make sure all dependencies are installed: pip install -r requirements.txt")

if __name__ == "__main__":
    main() 