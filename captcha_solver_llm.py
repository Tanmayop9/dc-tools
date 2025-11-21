#!/usr/bin/env python3
"""
Free LLM-based CAPTCHA Solver - For Educational Purposes Only
Uses free LLM APIs to solve visual CAPTCHAs automatically
Termux-friendly implementation

⚠️ DISCLAIMER: This tool is for educational purposes only.
Use at your own risk. The authors are not responsible for any misuse.
"""

import requests
import json
import base64
import time
import io
from typing import Optional, Dict, Any
from pathlib import Path

class ColoredOutput:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    @staticmethod
    def print_success(msg):
        print(f"{ColoredOutput.GREEN}[✓] {msg}{ColoredOutput.ENDC}")
    
    @staticmethod
    def print_error(msg):
        print(f"{ColoredOutput.FAIL}[✗] {msg}{ColoredOutput.ENDC}")
    
    @staticmethod
    def print_info(msg):
        print(f"{ColoredOutput.CYAN}[*] {msg}{ColoredOutput.ENDC}")
    
    @staticmethod
    def print_warning(msg):
        print(f"{ColoredOutput.WARNING}[!] {msg}{ColoredOutput.ENDC}")


class LLMCaptchaSolver:
    """
    Free LLM-based CAPTCHA solver using various free APIs
    Supports multiple providers with automatic fallback
    """
    
    # Default User-Agent (can be customized)
    DEFAULT_USER_AGENT = 'Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36'
    
    def __init__(self, user_agent: str = None):
        """
        Initialize the LLM CAPTCHA solver
        
        Args:
            user_agent: Custom User-Agent string (optional)
        """
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': user_agent or self.DEFAULT_USER_AGENT
        })
        
        # Free LLM API endpoints (no API key required)
        self.llm_providers = [
            {
                'name': 'HuggingFace Inference API (Free)',
                'endpoint': 'https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large',
                'type': 'vision',
                'requires_key': False
            },
            {
                'name': 'Local LLM Fallback',
                'endpoint': 'local',
                'type': 'pattern',
                'requires_key': False
            }
        ]
    
    def download_captcha_image(self, captcha_url: str) -> Optional[bytes]:
        """
        Download CAPTCHA image from URL
        
        Args:
            captcha_url: URL of the CAPTCHA image
            
        Returns:
            Image bytes or None if failed
        """
        try:
            ColoredOutput.print_info(f"Downloading CAPTCHA image...")
            response = self.session.get(captcha_url, timeout=10)
            
            if response.status_code == 200:
                ColoredOutput.print_success("CAPTCHA image downloaded")
                return response.content
            else:
                ColoredOutput.print_error(f"Failed to download image: {response.status_code}")
                return None
                
        except Exception as e:
            ColoredOutput.print_error(f"Error downloading CAPTCHA: {str(e)}")
            return None
    
    def solve_with_huggingface(self, image_bytes: bytes) -> Optional[str]:
        """
        Solve CAPTCHA using HuggingFace's free image captioning model
        
        Args:
            image_bytes: CAPTCHA image as bytes
            
        Returns:
            Extracted text or None
        """
        try:
            ColoredOutput.print_info("Using HuggingFace BLIP model (free)...")
            
            # Encode image to base64
            image_b64 = base64.b64encode(image_bytes).decode('utf-8')
            
            # Try HuggingFace Inference API (free, no API key needed)
            response = self.session.post(
                'https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large',
                headers={'Content-Type': 'application/json'},
                json={'inputs': image_b64},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    caption = result[0].get('generated_text', '')
                    ColoredOutput.print_success(f"LLM analysis: {caption}")
                    
                    # Extract text/numbers from caption
                    extracted = self._extract_captcha_from_caption(caption)
                    if extracted:
                        ColoredOutput.print_success(f"Extracted CAPTCHA: {extracted}")
                        return extracted
            
            elif response.status_code == 503:
                ColoredOutput.print_warning("Model is loading, retry in a moment...")
                time.sleep(2)
                return self.solve_with_huggingface(image_bytes)
            
            return None
            
        except Exception as e:
            ColoredOutput.print_error(f"HuggingFace solver error: {str(e)}")
            return None
    
    def solve_with_ollama(self, image_bytes: bytes) -> Optional[str]:
        """
        Solve CAPTCHA using local Ollama (if available)
        
        Args:
            image_bytes: CAPTCHA image as bytes
            
        Returns:
            Extracted text or None
        """
        try:
            ColoredOutput.print_info("Trying local Ollama vision model...")
            
            # Check if Ollama is running locally
            image_b64 = base64.b64encode(image_bytes).decode('utf-8')
            
            response = self.session.post(
                'http://localhost:11434/api/generate',
                json={
                    'model': 'llava',
                    'prompt': 'What text or numbers do you see in this CAPTCHA image? Only return the text/numbers, nothing else.',
                    'images': [image_b64],
                    'stream': False
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                text = result.get('response', '').strip()
                ColoredOutput.print_success(f"Ollama extracted: {text}")
                return text
            
            return None
            
        except requests.exceptions.ConnectionError:
            ColoredOutput.print_info("Ollama not available locally")
            return None
        except Exception as e:
            ColoredOutput.print_error(f"Ollama solver error: {str(e)}")
            return None
    
    def solve_with_pattern_recognition(self, image_bytes: bytes) -> Optional[str]:
        """
        Fallback: Use basic pattern recognition for simple text CAPTCHAs
        
        Args:
            image_bytes: CAPTCHA image as bytes
            
        Returns:
            Extracted text or None
        """
        try:
            ColoredOutput.print_info("Attempting pattern-based recognition...")
            
            # Try using pytesseract if available
            try:
                import pytesseract
                from PIL import Image
                
                image = Image.open(io.BytesIO(image_bytes))
                
                # Preprocess image for better OCR
                image = image.convert('L')  # Convert to grayscale
                
                text = pytesseract.image_to_string(image, config='--psm 7')
                text = ''.join(c for c in text if c.isalnum()).strip()
                
                if text:
                    ColoredOutput.print_success(f"Pattern recognition extracted: {text}")
                    return text
                    
            except ImportError:
                ColoredOutput.print_info("pytesseract not available, skipping...")
            
            return None
            
        except Exception as e:
            ColoredOutput.print_error(f"Pattern recognition error: {str(e)}")
            return None
    
    def _extract_captcha_from_caption(self, caption: str) -> Optional[str]:
        """
        Extract CAPTCHA text from image caption using pattern matching
        
        This method analyzes the LLM-generated caption to find CAPTCHA text.
        It uses regex patterns to identify common CAPTCHA formats:
        - 4-8 character alphanumeric codes (e.g., "ABC123")
        - 4-6 digit numeric codes (e.g., "1234")
        - 4-8 letter sequences (e.g., "ABCDEF")
        
        Args:
            caption: Image caption from LLM (e.g., "a sign with text ABC123")
            
        Returns:
            Extracted CAPTCHA text or None if no pattern matches
        """
        import re
        
        # Look for alphanumeric sequences in the caption
        # Common patterns in CAPTCHA descriptions
        patterns = [
            r'\b[A-Z0-9]{4,8}\b',  # 4-8 uppercase alphanumeric
            r'\b\d{4,6}\b',         # 4-6 digits
            r'\b[a-zA-Z]{4,8}\b',   # 4-8 letters
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, caption.upper())
            if matches:
                return matches[0]
        
        # If no pattern match, try to extract any word that looks like a CAPTCHA
        words = caption.split()
        for word in words:
            clean = ''.join(c for c in word if c.isalnum())
            if 4 <= len(clean) <= 8:
                return clean.upper()
        
        return None
    
    def solve_captcha(self, captcha_url: str = None, image_bytes: bytes = None) -> Optional[str]:
        """
        Solve CAPTCHA using available LLM providers with fallback
        
        Args:
            captcha_url: URL of CAPTCHA image (optional)
            image_bytes: Image bytes directly (optional)
            
        Returns:
            CAPTCHA solution or None
        """
        # Get image bytes
        if image_bytes is None and captcha_url:
            image_bytes = self.download_captcha_image(captcha_url)
        
        if not image_bytes:
            ColoredOutput.print_error("No image data available")
            return None
        
        ColoredOutput.print_info("Starting free LLM-based CAPTCHA solving...")
        
        # Try HuggingFace first (free, no setup required)
        result = self.solve_with_huggingface(image_bytes)
        if result:
            return result
        
        # Try local Ollama if available
        result = self.solve_with_ollama(image_bytes)
        if result:
            return result
        
        # Fallback to pattern recognition
        result = self.solve_with_pattern_recognition(image_bytes)
        if result:
            return result
        
        ColoredOutput.print_error("All LLM solving methods failed")
        return None
    
    def solve_hcaptcha(self, sitekey: str, url: str) -> Optional[str]:
        """
        Solve hCaptcha challenges (Discord uses hCaptcha)
        
        Args:
            sitekey: hCaptcha site key
            url: Page URL where CAPTCHA is shown
            
        Returns:
            hCaptcha response token or None
        """
        ColoredOutput.print_info("hCaptcha detected - attempting free solve...")
        ColoredOutput.print_warning("Note: hCaptcha is more complex, may require manual fallback")
        
        try:
            # Get hCaptcha challenge
            ColoredOutput.print_info("Fetching hCaptcha challenge...")
            
            hsw_response = self._get_hsw(sitekey)
            if not hsw_response:
                ColoredOutput.print_error("Failed to get hCaptcha challenge")
                return None
            
            # For now, return None to trigger manual fallback
            # Full hCaptcha automation would require more complex image processing
            ColoredOutput.print_warning("hCaptcha requires manual solving (opening browser)...")
            return None
            
        except Exception as e:
            ColoredOutput.print_error(f"hCaptcha solve error: {str(e)}")
            return None
    
    def _get_hsw(self, sitekey: str) -> Optional[str]:
        """Get hCaptcha HSW (proof of work)"""
        try:
            response = self.session.get(
                f'https://hcaptcha.com/checksiteconfig?host=discord.com&sitekey={sitekey}&sc=1&swa=1',
                timeout=10
            )
            if response.status_code == 200:
                return response.text
            return None
        except:
            return None


def main():
    """Test the LLM CAPTCHA solver"""
    print("=" * 60)
    print("Free LLM CAPTCHA Solver - Test Mode")
    print("=" * 60)
    print()
    
    ColoredOutput.print_warning("⚠️  For educational purposes only!")
    print()
    
    solver = LLMCaptchaSolver()
    
    # Example usage
    ColoredOutput.print_info("Solver initialized with free LLM providers:")
    for provider in solver.llm_providers:
        print(f"  - {provider['name']} ({provider['type']})")
    
    print()
    ColoredOutput.print_info("Ready to solve CAPTCHAs!")
    ColoredOutput.print_info("Use solve_captcha(captcha_url) or solve_captcha(image_bytes=data)")


if __name__ == "__main__":
    main()
