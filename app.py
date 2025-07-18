from flask import Flask, render_template, jsonify, request
import subprocess
import threading
import os
import signal
import time

app = Flask(__name__)

# Global variable to store the agent process
agent_process = None
is_running = False

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/start_agent', methods=['POST'])
def start_agent():
    global agent_process, is_running
    
    if is_running:
        return jsonify({'status': 'error', 'message': 'Agent is already running'})
    
    try:
        # Start the agent in a separate thread
        def run_agent():
            global agent_process, is_running
            try:
                # Run agent.py
                agent_process = subprocess.Popen(
                    ['python', 'agent.py'],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                is_running = True
                print(f"Agent started with PID: {agent_process.pid}")
                
                # Wait for the process to complete
                agent_process.wait()
            except Exception as e:
                print(f"Error running agent: {e}")
            finally:
                is_running = False
                agent_process = None
        
        # Start the agent in a background thread
        thread = threading.Thread(target=run_agent, daemon=True)
        thread.start()
        
        # Wait a moment to ensure the process starts
        time.sleep(1)
        
        if is_running:
            return jsonify({'status': 'success', 'message': 'Agent started successfully'})
        else:
            return jsonify({'status': 'error', 'message': 'Failed to start agent'})
            
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Error: {str(e)}'})

@app.route('/stop_agent', methods=['POST'])
def stop_agent():
    global agent_process, is_running
    
    if not is_running or agent_process is None:
        return jsonify({'status': 'error', 'message': 'Agent is not running'})
    
    try:
        # Terminate the agent process
        agent_process.terminate()
        
        # Wait for a moment for graceful shutdown
        try:
            agent_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            # Force kill if it doesn't terminate gracefully
            agent_process.kill()
        
        is_running = False
        agent_process = None
        
        return jsonify({'status': 'success', 'message': 'Agent stopped successfully'})
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Error stopping agent: {str(e)}'})

@app.route('/status')
def get_status():
    global is_running
    return jsonify({'running': is_running})

if __name__ == '__main__':
    # Create static folder if it doesn't exist
    if not os.path.exists('static'):
        os.makedirs('static')
    
    # Move index.html to static folder if it exists in root
    if os.path.exists('index.html'):
        import shutil
        shutil.move('index.html', 'static/index.html')
    
    # Get port from environment variable (for Render)
    port = int(os.environ.get('PORT', 5000))
    
    print("Starting Flask server...")
    print(f"Open http://localhost:{port} in your browser")
    app.run(debug=False, host='0.0.0.0', port=port) 