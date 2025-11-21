#!/usr/bin/env python3
"""
Free CAPTCHA Solver - Manual solving via browser
Works on Termux by opening browser for user to solve CAPTCHA
"""

import time
import webbrowser
import http.server
import socketserver
import threading
import json
from urllib.parse import urlparse, parse_qs

class CaptchaServer(http.server.SimpleHTTPRequestHandler):
    """HTTP server to receive CAPTCHA solution"""
    captcha_solution = None
    sitekey = None  # Store the sitekey for use in HTML generation
    
    def do_GET(self):
        """Handle GET requests"""
        if self.path.startswith('/captcha?'):
            # Parse CAPTCHA solution from URL
            parsed = urlparse(self.path)
            params = parse_qs(parsed.query)
            
            if 'h-captcha-response' in params:
                CaptchaServer.captcha_solution = params['h-captcha-response'][0]
                
                # Send success response
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                
                html = """
                <html>
                <head>
                    <meta name="viewport" content="width=device-width, initial-scale=1">
                    <style>
                        body {
                            font-family: Arial, sans-serif;
                            display: flex;
                            justify-content: center;
                            align-items: center;
                            height: 100vh;
                            margin: 0;
                            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        }
                        .success {
                            background: white;
                            padding: 40px;
                            border-radius: 10px;
                            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
                            text-align: center;
                        }
                        .checkmark {
                            width: 80px;
                            height: 80px;
                            border-radius: 50%;
                            display: block;
                            stroke-width: 2;
                            stroke: #4bb71b;
                            stroke-miterlimit: 10;
                            margin: 10% auto;
                            box-shadow: inset 0px 0px 0px #4bb71b;
                            animation: fill .4s ease-in-out .4s forwards, scale .3s ease-in-out .9s both;
                        }
                        .checkmark__circle {
                            stroke-dasharray: 166;
                            stroke-dashoffset: 166;
                            stroke-width: 2;
                            stroke-miterlimit: 10;
                            stroke: #4bb71b;
                            fill: none;
                            animation: stroke 0.6s cubic-bezier(0.65, 0, 0.45, 1) forwards;
                        }
                        .checkmark__check {
                            transform-origin: 50% 50%;
                            stroke-dasharray: 48;
                            stroke-dashoffset: 48;
                            animation: stroke 0.3s cubic-bezier(0.65, 0, 0.45, 1) 0.8s forwards;
                        }
                        @keyframes stroke {
                            100% {
                                stroke-dashoffset: 0;
                            }
                        }
                        @keyframes scale {
                            0%, 100% {
                                transform: none;
                            }
                            50% {
                                transform: scale3d(1.1, 1.1, 1);
                            }
                        }
                        @keyframes fill {
                            100% {
                                box-shadow: inset 0px 0px 0px 30px #4bb71b;
                            }
                        }
                        h2 {
                            color: #333;
                            margin-top: 20px;
                        }
                        p {
                            color: #666;
                        }
                    </style>
                </head>
                <body>
                    <div class="success">
                        <svg class="checkmark" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 52 52">
                            <circle class="checkmark__circle" cx="26" cy="26" r="25" fill="none"/>
                            <path class="checkmark__check" fill="none" d="M14.1 27.2l7.1 7.2 16.7-16.8"/>
                        </svg>
                        <h2>CAPTCHA Solved!</h2>
                        <p>You can close this window now.</p>
                        <p style="font-size: 12px; margin-top: 20px;">Return to your terminal...</p>
                    </div>
                </body>
                </html>
                """
                self.wfile.write(html.encode())
                return
        
        # Serve CAPTCHA solving page
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        html = """
        <html>
        <head>
            <title>Solve CAPTCHA</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <script src="https://js.hcaptcha.com/1/api.js" async defer></script>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    min-height: 100vh;
                    margin: 0;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding: 20px;
                }}
                .container {{
                    background: white;
                    padding: 40px;
                    border-radius: 10px;
                    box-shadow: 0 10px 40px rgba(0,0,0,0.2);
                    text-align: center;
                    max-width: 500px;
                    width: 100%;
                }}
                h1 {{
                    color: #333;
                    margin-bottom: 10px;
                }}
                p {{
                    color: #666;
                    margin-bottom: 30px;
                }}
                .captcha-wrapper {{
                    display: flex;
                    justify-content: center;
                    margin: 30px 0;
                }}
                button {{
                    background: #5865F2;
                    color: white;
                    border: none;
                    padding: 12px 30px;
                    border-radius: 5px;
                    font-size: 16px;
                    cursor: pointer;
                    transition: background 0.3s;
                }}
                button:hover {{
                    background: #4752C4;
                }}
                button:disabled {{
                    background: #ccc;
                    cursor: not-allowed;
                }}
                .instructions {{
                    background: #f0f0f0;
                    padding: 15px;
                    border-radius: 5px;
                    margin-bottom: 20px;
                    text-align: left;
                }}
                .instructions ol {{
                    margin: 10px 0;
                    padding-left: 20px;
                }}
                .instructions li {{
                    margin: 5px 0;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🔒 Solve CAPTCHA</h1>
                <p>Please complete the CAPTCHA below to continue</p>
                
                <div class="instructions">
                    <strong>Instructions:</strong>
                    <ol>
                        <li>Click on the CAPTCHA checkbox</li>
                        <li>Complete the challenge if prompted</li>
                        <li>Click "Submit" button</li>
                    </ol>
                </div>
                
                <form id="captcha-form" onsubmit="submitCaptcha(event)">
                    <div class="captcha-wrapper">
                        <div class="h-captcha" data-sitekey="{sitekey}"></div>
                    </div>
                    <button type="submit" id="submit-btn" disabled>Submit</button>
                </form>
                
                <p style="font-size: 12px; margin-top: 20px; color: #999;">
                    This will automatically redirect after solving
                </p>
            </div>
            
            <script>
                // Enable submit button when CAPTCHA is solved
                function onCaptchaSuccess() {{
                    document.getElementById('submit-btn').disabled = false;
                }}
                
                function submitCaptcha(event) {{
                    event.preventDefault();
                    
                    const response = hcaptcha.getResponse();
                    if (response) {{
                        // Redirect with CAPTCHA response
                        window.location.href = '/captcha?h-captcha-response=' + encodeURIComponent(response);
                    }} else {{
                        alert('Please complete the CAPTCHA first!');
                    }}
                }}
                
                // Auto-enable button when CAPTCHA is solved
                setInterval(function() {{
                    const response = hcaptcha.getResponse();
                    if (response) {{
                        document.getElementById('submit-btn').disabled = false;
                    }}
                }}, 500);
            </script>
        </body>
        </html>
        """
        # Replace the sitekey placeholder with the actual sitekey
        if CaptchaServer.sitekey:
            html = html.format(sitekey=CaptchaServer.sitekey)
        else:
            # Fallback to default Discord sitekey if not set
            html = html.format(sitekey='4c672d35-0701-42b2-88c3-78380b0db560')
        
        self.wfile.write(html.encode())
    
    def log_message(self, format, *args):
        """Suppress logging"""
        pass

class FreeCaptchaSolver:
    """Free CAPTCHA solver using manual browser solving"""
    
    def __init__(self, port=8888):
        self.port = port
        self.server = None
        self.server_thread = None
        self._find_available_port()
    
    def _find_available_port(self):
        """Find an available port if the default is in use"""
        import socket
        for port in range(self.port, self.port + 10):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind(('', port))
                    self.port = port
                    return
            except OSError:
                continue
        # If no port found in range, keep the original and let it fail gracefully
    
    def start_server(self):
        """Start HTTP server"""
        try:
            self.server = socketserver.TCPServer(("", self.port), CaptchaServer)
            self.server_thread = threading.Thread(target=self.server.serve_forever)
            self.server_thread.daemon = True
            self.server_thread.start()
            return True
        except Exception as e:
            print(f"[-] Failed to start server: {e}")
            return False
    
    def stop_server(self):
        """Stop HTTP server"""
        if self.server:
            self.server.shutdown()
            self.server = None
    
    def solve_captcha(self, sitekey, url, timeout=300):
        """
        Solve CAPTCHA by opening browser for manual solving
        
        Args:
            sitekey: hCaptcha site key
            url: The page URL (not used in manual solving, but kept for API compatibility)
            timeout: Maximum wait time in seconds
        
        Returns:
            CAPTCHA solution or None
        """
        print("\n" + "="*60)
        print("🔒 CAPTCHA Required - Manual Solving")
        print("="*60)
        
        # Reset solution and set sitekey
        CaptchaServer.captcha_solution = None
        CaptchaServer.sitekey = sitekey
        
        # Start server
        if not self.start_server():
            print("[-] Could not start server for CAPTCHA solving")
            return None
        
        # Prepare URL
        url = f"http://localhost:{self.port}/"
        
        print(f"\n[*] Opening browser for CAPTCHA solving...")
        print(f"[*] URL: {url}")
        print(f"[*] If browser doesn't open automatically, open this URL manually:")
        print(f"    {url}")
        
        # Try to open browser (works on Termux with termux-open-url)
        try:
            # For Termux
            import subprocess
            result = subprocess.run(['termux-open-url', url], 
                                  capture_output=True, 
                                  timeout=5)
            if result.returncode == 0:
                print("[✓] Browser opened via termux-open-url")
            else:
                # Fallback to webbrowser
                webbrowser.open(url)
                print("[✓] Browser opened")
        except Exception:
            try:
                # Standard browser opening
                webbrowser.open(url)
                print("[✓] Browser opened")
            except Exception as e:
                print(f"[-] Could not open browser automatically: {e}")
                print(f"[!] Please open this URL manually: {url}")
        
        print(f"\n[*] Waiting for you to solve CAPTCHA...")
        print(f"[*] Instructions:")
        print(f"    1. Complete the CAPTCHA in the browser")
        print(f"    2. Click 'Submit' button")
        print(f"    3. Wait for confirmation message")
        print(f"\n[*] Timeout: {timeout} seconds")
        
        # Wait for solution
        start_time = time.time()
        dots = 0
        
        while time.time() - start_time < timeout:
            if CaptchaServer.captcha_solution:
                print("\n[✓] CAPTCHA solved successfully!")
                solution = CaptchaServer.captcha_solution
                self.stop_server()
                return solution
            
            # Show progress
            elapsed = int(time.time() - start_time)
            remaining = timeout - elapsed
            print(f"\r[*] Waiting for CAPTCHA solution... ({remaining}s remaining) {'.' * (dots % 4)}", end='', flush=True)
            dots += 1
            time.sleep(1)
        
        print("\n[-] CAPTCHA solving timeout")
        self.stop_server()
        return None

def test_solver():
    """Test the CAPTCHA solver"""
    print("Free CAPTCHA Solver Test")
    print("="*60)
    
    solver = FreeCaptchaSolver()
    
    # Example sitekey (Discord's hCaptcha sitekey)
    sitekey = "4c672d35-0701-42b2-88c3-78380b0db560"
    test_url = "https://discord.com/api/oauth2/authorize"
    
    solution = solver.solve_captcha(sitekey, test_url, timeout=120)
    
    if solution:
        print(f"\n[✓] Solution: {solution[:50]}...")
    else:
        print("\n[-] Failed to get solution")

if __name__ == "__main__":
    test_solver()
