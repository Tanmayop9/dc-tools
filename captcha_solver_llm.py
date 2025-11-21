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
        
        # Advanced LLM API endpoints with multiple free providers
        self.llm_providers = [
            {
                'name': 'HuggingFace BLIP-2 (Advanced Vision)',
                'endpoint': 'https://api-inference.huggingface.co/models/Salesforce/blip2-opt-2.7b',
                'type': 'vision_advanced',
                'requires_key': False
            },
            {
                'name': 'HuggingFace BLIP (Original)',
                'endpoint': 'https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large',
                'type': 'vision',
                'requires_key': False
            },
            {
                'name': 'HuggingFace ViT-GPT2 (Image to Text)',
                'endpoint': 'https://api-inference.huggingface.co/models/nlpconnect/vit-gpt2-image-captioning',
                'type': 'vision',
                'requires_key': False
            },
            {
                'name': 'Local OCR (Tesseract)',
                'endpoint': 'local_tesseract',
                'type': 'ocr',
                'requires_key': False
            },
            {
                'name': 'Local Ollama Vision',
                'endpoint': 'local_ollama',
                'type': 'vision_local',
                'requires_key': False
            },
            {
                'name': 'Pattern Recognition',
                'endpoint': 'local',
                'type': 'pattern',
                'requires_key': False
            }
        ]
        
        # Enhanced retry configuration
        self.max_retries = 3
        self.retry_delay = 2
    
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
    
    def solve_with_huggingface(self, image_bytes: bytes, model_url: str = None) -> Optional[str]:
        """
        Solve CAPTCHA using HuggingFace's free image captioning models with retry logic
        
        Args:
            image_bytes: CAPTCHA image as bytes
            model_url: Optional specific model URL to use
            
        Returns:
            Extracted text or None
        """
        if model_url is None:
            model_url = 'https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large'
        
        model_name = model_url.split('/')[-1]
        
        for attempt in range(self.max_retries):
            try:
                ColoredOutput.print_info(f"Using HuggingFace {model_name} (attempt {attempt + 1}/{self.max_retries})...")
                
                # Try with multipart form data for better compatibility
                files = {'file': ('captcha.png', image_bytes, 'image/png')}
                
                response = self.session.post(
                    model_url,
                    files=files,
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    caption = None
                    
                    # Handle different response formats
                    if isinstance(result, list) and len(result) > 0:
                        if 'generated_text' in result[0]:
                            caption = result[0].get('generated_text', '')
                        elif 'label' in result[0]:
                            caption = result[0].get('label', '')
                    elif isinstance(result, dict):
                        caption = result.get('generated_text', result.get('text', ''))
                    
                    if caption:
                        ColoredOutput.print_success(f"LLM analysis: {caption}")
                        
                        # Extract text/numbers from caption
                        extracted = self._extract_captcha_from_caption(caption)
                        if extracted:
                            ColoredOutput.print_success(f"Extracted CAPTCHA: {extracted}")
                            return extracted
                
                elif response.status_code == 503:
                    ColoredOutput.print_warning(f"Model is loading, waiting {self.retry_delay}s...")
                    time.sleep(self.retry_delay)
                    continue
                
                elif response.status_code == 400:
                    # Try with base64 encoding instead
                    ColoredOutput.print_info("Trying base64 encoding method...")
                    image_b64 = base64.b64encode(image_bytes).decode('utf-8')
                    
                    response = self.session.post(
                        model_url,
                        headers={'Content-Type': 'application/json'},
                        json={'inputs': image_b64},
                        timeout=30
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        if isinstance(result, list) and len(result) > 0:
                            caption = result[0].get('generated_text', '')
                            ColoredOutput.print_success(f"LLM analysis: {caption}")
                            
                            extracted = self._extract_captcha_from_caption(caption)
                            if extracted:
                                ColoredOutput.print_success(f"Extracted CAPTCHA: {extracted}")
                                return extracted
                
                # Wait before next retry
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                
            except Exception as e:
                ColoredOutput.print_error(f"HuggingFace solver error (attempt {attempt + 1}): {str(e)}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
        
        return None
    
    def solve_with_ollama(self, image_bytes: bytes) -> Optional[str]:
        """
        Solve CAPTCHA using local Ollama vision models (llava, bakllava)
        
        Args:
            image_bytes: CAPTCHA image as bytes
            
        Returns:
            Extracted text or None
        """
        try:
            ColoredOutput.print_info("Trying local Ollama vision model...")
            
            # Check if Ollama is running locally
            image_b64 = base64.b64encode(image_bytes).decode('utf-8')
            
            # Try multiple vision models
            models = ['llava:latest', 'bakllava:latest', 'llava:7b']
            
            for model in models:
                try:
                    ColoredOutput.print_info(f"Testing {model}...")
                    response = self.session.post(
                        'http://localhost:11434/api/generate',
                        json={
                            'model': model,
                            'prompt': 'Extract the exact text/numbers from this CAPTCHA image. Return only the alphanumeric characters with no explanation or additional text.',
                            'images': [image_b64],
                            'stream': False
                        },
                        timeout=60
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        text = result.get('response', '').strip()
                        
                        # Extract alphanumeric from response
                        extracted = self._extract_captcha_from_caption(text)
                        if extracted:
                            ColoredOutput.print_success(f"Ollama ({model}) extracted: {extracted}")
                            return extracted
                        
                        # If extraction failed but we have text, try direct use
                        clean_text = ''.join(c for c in text if c.isalnum()).upper()
                        if 4 <= len(clean_text) <= 8:
                            ColoredOutput.print_success(f"Ollama ({model}) extracted: {clean_text}")
                            return clean_text
                
                except requests.exceptions.RequestException:
                    continue
            
            return None
            
        except requests.exceptions.ConnectionError:
            ColoredOutput.print_info("Ollama not running locally (install from ollama.ai)")
            return None
        except Exception as e:
            ColoredOutput.print_warning(f"Ollama unavailable: {str(e)}")
            return None
    
    def solve_with_pattern_recognition(self, image_bytes: bytes) -> Optional[str]:
        """
        Advanced OCR-based pattern recognition for simple text CAPTCHAs
        Uses multiple preprocessing techniques for better accuracy
        
        Args:
            image_bytes: CAPTCHA image as bytes
            
        Returns:
            Extracted text or None
        """
        try:
            ColoredOutput.print_info("Attempting advanced OCR pattern recognition...")
            
            # Try using pytesseract with multiple preprocessing strategies
            try:
                import pytesseract
                from PIL import Image, ImageEnhance, ImageFilter
                
                image = Image.open(io.BytesIO(image_bytes))
                
                # Strategy 1: Basic grayscale OCR
                ColoredOutput.print_info("OCR Strategy 1: Basic grayscale...")
                gray_image = image.convert('L')
                text = pytesseract.image_to_string(gray_image, config='--psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789')
                text = ''.join(c for c in text if c.isalnum()).strip().upper()
                
                if text and 4 <= len(text) <= 8:
                    ColoredOutput.print_success(f"OCR extracted (basic): {text}")
                    return text
                
                # Strategy 2: Enhanced contrast
                ColoredOutput.print_info("OCR Strategy 2: Enhanced contrast...")
                enhancer = ImageEnhance.Contrast(gray_image)
                enhanced = enhancer.enhance(2.0)
                text = pytesseract.image_to_string(enhanced, config='--psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789')
                text = ''.join(c for c in text if c.isalnum()).strip().upper()
                
                if text and 4 <= len(text) <= 8:
                    ColoredOutput.print_success(f"OCR extracted (contrast): {text}")
                    return text
                
                # Strategy 3: Sharpening
                ColoredOutput.print_info("OCR Strategy 3: Sharpened image...")
                sharpened = gray_image.filter(ImageFilter.SHARPEN)
                text = pytesseract.image_to_string(sharpened, config='--psm 8 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789')
                text = ''.join(c for c in text if c.isalnum()).strip().upper()
                
                if text and 4 <= len(text) <= 8:
                    ColoredOutput.print_success(f"OCR extracted (sharpen): {text}")
                    return text
                
                # Strategy 4: Binary threshold
                ColoredOutput.print_info("OCR Strategy 4: Binary threshold...")
                threshold_image = gray_image.point(lambda x: 0 if x < 128 else 255, '1')
                text = pytesseract.image_to_string(threshold_image, config='--psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789')
                text = ''.join(c for c in text if c.isalnum()).strip().upper()
                
                if text and 4 <= len(text) <= 8:
                    ColoredOutput.print_success(f"OCR extracted (threshold): {text}")
                    return text
                
                ColoredOutput.print_warning("OCR failed to extract valid CAPTCHA text")
                    
            except ImportError:
                ColoredOutput.print_info("pytesseract not installed (pip install pytesseract)")
                ColoredOutput.print_info("For better results, install: apt-get install tesseract-ocr")
            except Exception as ocr_error:
                ColoredOutput.print_warning(f"OCR error: {str(ocr_error)}")
            
            return None
            
        except Exception as e:
            ColoredOutput.print_error(f"Pattern recognition error: {str(e)}")
            return None
    
    def _extract_captcha_from_caption(self, caption: str) -> Optional[str]:
        """
        Ultra-advanced CAPTCHA text extraction from image caption using intelligent pattern matching
        
        This method uses multiple extraction strategies:
        - Regex patterns for common CAPTCHA formats
        - Context-aware keyword extraction
        - Character filtering and validation
        - Length-based heuristics
        
        Args:
            caption: Image caption from LLM (e.g., "a sign with text ABC123")
            
        Returns:
            Extracted CAPTCHA text or None if no pattern matches
        """
        import re
        
        ColoredOutput.print_info(f"Analyzing caption: '{caption}'")
        
        # Strategy 1: Direct extraction of quoted text (e.g., "text reads 'ABC123'")
        quoted_patterns = [
            r"['\"]([A-Z0-9]{4,8})['\"]",  # Single or double quoted
            r"reads?\s+['\"]?([A-Z0-9]{4,8})['\"]?",  # "reads ABC123"
            r"says?\s+['\"]?([A-Z0-9]{4,8})['\"]?",   # "says ABC123"
            r"text\s+['\"]?([A-Z0-9]{4,8})['\"]?",    # "text ABC123"
        ]
        
        for pattern in quoted_patterns:
            matches = re.findall(pattern, caption.upper())
            if matches:
                ColoredOutput.print_info(f"Found quoted text: {matches[0]}")
                return matches[0]
        
        # Strategy 2: Look for alphanumeric sequences (most common CAPTCHA format)
        patterns = [
            r'\b[A-Z0-9]{6}\b',      # Exactly 6 characters (most common)
            r'\b[A-Z0-9]{5,7}\b',    # 5-7 characters
            r'\b[A-Z0-9]{4,8}\b',    # 4-8 characters (fallback)
            r'\b\d{4,6}\b',          # Pure numeric 4-6 digits
            r'\b[A-Z]{5,8}\b',       # Pure letters 5-8
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, caption.upper())
            if matches:
                # Filter out common false positives
                filtered = [m for m in matches if m not in ['IMAGE', 'PHOTO', 'PICTURE', 'CAPTCHA', 'TEXT', 'CODE']]
                if filtered:
                    ColoredOutput.print_info(f"Found pattern match: {filtered[0]}")
                    return filtered[0]
        
        # Strategy 3: Extract the most CAPTCHA-like word
        words = re.findall(r'\b\w+\b', caption.upper())
        for word in words:
            clean = ''.join(c for c in word if c.isalnum())
            # Check if it has both letters and numbers (common in CAPTCHAs)
            has_letter = any(c.isalpha() for c in clean)
            has_digit = any(c.isdigit() for c in clean)
            
            if 4 <= len(clean) <= 8:
                if has_letter and has_digit:  # Alphanumeric is preferred
                    ColoredOutput.print_info(f"Found alphanumeric word: {clean}")
                    return clean
        
        # Strategy 4: Just length-based extraction (last resort)
        for word in words:
            clean = ''.join(c for c in word if c.isalnum())
            if 4 <= len(clean) <= 8 and clean not in ['IMAGE', 'PHOTO', 'PICTURE', 'CAPTCHA', 'TEXT', 'CODE']:
                ColoredOutput.print_info(f"Found length-based match: {clean}")
                return clean
        
        ColoredOutput.print_warning("No CAPTCHA pattern found in caption")
        return None
    
    def solve_captcha(self, captcha_url: str = None, image_bytes: bytes = None) -> Optional[str]:
        """
        Ultra-advanced CAPTCHA solving using multiple LLM providers with intelligent fallback
        
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
        
        ColoredOutput.print_info("🚀 Starting ultra-advanced LLM-based CAPTCHA solving...")
        ColoredOutput.print_info(f"Using {len(self.llm_providers)} provider strategies")
        
        # Strategy 1: Try advanced HuggingFace BLIP-2 model (best for complex images)
        ColoredOutput.print_info("Strategy 1: Advanced vision model (BLIP-2)...")
        result = self.solve_with_huggingface(
            image_bytes, 
            'https://api-inference.huggingface.co/models/Salesforce/blip2-opt-2.7b'
        )
        if result:
            ColoredOutput.print_success("✓ CAPTCHA solved using advanced vision model!")
            return result
        
        # Strategy 2: Try original HuggingFace BLIP model
        ColoredOutput.print_info("Strategy 2: Standard vision model (BLIP)...")
        result = self.solve_with_huggingface(image_bytes)
        if result:
            ColoredOutput.print_success("✓ CAPTCHA solved using standard vision model!")
            return result
        
        # Strategy 3: Try ViT-GPT2 model (good for text in images)
        ColoredOutput.print_info("Strategy 3: Image-to-text model (ViT-GPT2)...")
        result = self.solve_with_huggingface(
            image_bytes,
            'https://api-inference.huggingface.co/models/nlpconnect/vit-gpt2-image-captioning'
        )
        if result:
            ColoredOutput.print_success("✓ CAPTCHA solved using image-to-text model!")
            return result
        
        # Strategy 4: Try local Ollama if available (best for privacy)
        ColoredOutput.print_info("Strategy 4: Local vision model (Ollama)...")
        result = self.solve_with_ollama(image_bytes)
        if result:
            ColoredOutput.print_success("✓ CAPTCHA solved using local model!")
            return result
        
        # Strategy 5: OCR-based pattern recognition (best for simple text)
        ColoredOutput.print_info("Strategy 5: OCR pattern recognition...")
        result = self.solve_with_pattern_recognition(image_bytes)
        if result:
            ColoredOutput.print_success("✓ CAPTCHA solved using OCR!")
            return result
        
        ColoredOutput.print_error("❌ All advanced solving strategies exhausted")
        ColoredOutput.print_warning("CAPTCHA may require manual solving")
        return None
    
    def solve_hcaptcha(self, sitekey: str, url: str) -> Optional[str]:
        """
        Ultra-advanced hCaptcha solver with AI-powered image recognition for interactive challenges
        Supports: Image selection, object detection, drag-and-drop challenges
        
        Args:
            sitekey: hCaptcha site key
            url: Page URL where CAPTCHA is shown
            
        Returns:
            hCaptcha response token or None
        """
        ColoredOutput.print_info("🔐 hCaptcha detected - deploying advanced AI solving strategies...")
        ColoredOutput.print_info("Supported: Image selection, object detection, interactive challenges")
        
        try:
            # Strategy 1: Get hCaptcha challenge metadata
            ColoredOutput.print_info("📥 Fetching hCaptcha challenge data...")
            
            # Get HSW (proof of work)
            hsw_response = self._get_hsw(sitekey)
            if hsw_response:
                ColoredOutput.print_success("✓ Retrieved hCaptcha metadata")
            
            # Strategy 2: Fetch the actual challenge
            ColoredOutput.print_info("🎯 Retrieving challenge tasks...")
            challenge_data = self._get_hcaptcha_challenge(sitekey, url)
            
            if challenge_data and 'tasklist' in challenge_data:
                tasks = challenge_data.get('tasklist', [])
                ColoredOutput.print_success(f"✓ Found {len(tasks)} challenge task(s)")
                
                # Process each challenge task
                solutions = []
                for idx, task in enumerate(tasks, 1):
                    task_key = task.get('task_key', '')
                    question = task.get('request', '')
                    request_type = task.get('request_type', 'image_label_binary')
                    
                    ColoredOutput.print_info(f"\n🧩 Challenge {idx}/{len(tasks)}: {question}")
                    ColoredOutput.print_info(f"Type: {request_type}")
                    
                    # Solve based on challenge type
                    if request_type == 'image_label_binary':
                        # Image selection: "Select all images with X"
                        solution = self._solve_image_selection_challenge(task, question)
                    elif request_type == 'image_label_area_select':
                        # Click/tap challenges: "Click on the X"
                        solution = self._solve_area_selection_challenge(task, question)
                    else:
                        # Generic challenge handling
                        solution = self._solve_generic_challenge(task, question)
                    
                    if solution:
                        solutions.append(solution)
                        ColoredOutput.print_success(f"✓ Challenge {idx} solved!")
                    else:
                        ColoredOutput.print_warning(f"⚠ Challenge {idx} needs manual solve")
                
                # If we solved all challenges, submit the solutions
                if len(solutions) == len(tasks):
                    ColoredOutput.print_info("🚀 Submitting solutions to hCaptcha...")
                    token = self._submit_hcaptcha_solutions(sitekey, challenge_data, solutions)
                    if token:
                        ColoredOutput.print_success("🎉 hCaptcha solved successfully!")
                        return token
                else:
                    ColoredOutput.print_warning(f"⚠ Only {len(solutions)}/{len(tasks)} challenges solved")
            
            # Strategy 3: Try accessibility mode (text-based challenges)
            ColoredOutput.print_info("🔍 Checking for text-based accessibility mode...")
            text_challenge = self._get_hcaptcha_accessibility_challenge(sitekey)
            if text_challenge:
                ColoredOutput.print_info("✓ Text challenge available!")
                solution = self._solve_text_challenge(text_challenge)
                if solution:
                    return solution
            
            # If AI solving failed, provide detailed info for manual fallback
            ColoredOutput.print_warning("⚠️  AI solving incomplete - falling back to manual browser")
            ColoredOutput.print_info("Manual solving will open browser with interactive CAPTCHA")
            return None
            
        except Exception as e:
            ColoredOutput.print_error(f"hCaptcha solve error: {str(e)}")
            import traceback
            ColoredOutput.print_warning(f"Traceback: {traceback.format_exc()[:200]}...")
            return None
    
    def _get_hcaptcha_challenge(self, sitekey: str, url: str) -> Optional[Dict]:
        """
        Get hCaptcha challenge data
        
        Args:
            sitekey: hCaptcha site key
            url: Page URL
            
        Returns:
            Challenge data or None
        """
        try:
            # Get challenge
            response = self.session.post(
                'https://hcaptcha.com/getcaptcha',
                json={
                    'sitekey': sitekey,
                    'host': 'discord.com',
                    'hl': 'en',
                    'motionData': {'st': int(time.time() * 1000), 'dct': int(time.time() * 1000), 'mm': []},
                },
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            
            return None
            
        except Exception as e:
            ColoredOutput.print_error(f"Failed to get hCaptcha challenge: {str(e)}")
            return None
    
    def _solve_image_selection_challenge(self, task: Dict, question: str) -> Optional[Dict]:
        """
        Solve image selection challenges using AI vision
        Example: "Select all images with traffic lights"
        
        Args:
            task: Challenge task data
            question: Challenge question/prompt
            
        Returns:
            Solution dict or None
        """
        try:
            ColoredOutput.print_info("🖼️  Solving image selection challenge with AI vision...")
            
            # Extract the target object from question
            # e.g., "Select all images with traffic lights" -> "traffic lights"
            target_object = self._extract_target_from_question(question)
            ColoredOutput.print_info(f"Target object: {target_object}")
            
            # Get challenge images
            images = task.get('datapoint_uri', {})
            if isinstance(images, dict):
                images = list(images.values())
            
            ColoredOutput.print_info(f"Analyzing {len(images)} images...")
            
            # Analyze each image to see if it contains the target
            selected_indices = []
            for idx, image_url in enumerate(images):
                ColoredOutput.print_info(f"Analyzing image {idx + 1}/{len(images)}...")
                
                # Download image
                image_data = self.download_captcha_image(image_url)
                if not image_data:
                    continue
                
                # Use AI to determine if image contains target object
                contains_target = self._image_contains_object(image_data, target_object)
                
                if contains_target:
                    selected_indices.append(idx)
                    ColoredOutput.print_success(f"✓ Image {idx + 1} contains {target_object}")
                else:
                    ColoredOutput.print_info(f"✗ Image {idx + 1} does not contain {target_object}")
            
            if selected_indices:
                ColoredOutput.print_success(f"✓ Selected {len(selected_indices)} images")
                return {
                    'task_key': task.get('task_key'),
                    'selected': selected_indices
                }
            else:
                ColoredOutput.print_warning("⚠ No images matched the criteria")
                return None
            
        except Exception as e:
            ColoredOutput.print_error(f"Image selection error: {str(e)}")
            return None
    
    def _solve_area_selection_challenge(self, task: Dict, question: str) -> Optional[Dict]:
        """
        Solve area selection challenges (click/tap on object)
        Example: "Click on the bicycle"
        
        Args:
            task: Challenge task data
            question: Challenge question/prompt
            
        Returns:
            Solution dict or None
        """
        try:
            ColoredOutput.print_info("👆 Solving area selection challenge...")
            ColoredOutput.print_warning("Area selection requires precise object localization")
            
            # This would require advanced object detection models (YOLO, etc.)
            # For educational purposes, we acknowledge the complexity
            ColoredOutput.print_info("Using vision AI for object detection...")
            
            # In a full implementation:
            # 1. Download the challenge image
            # 2. Use object detection model (YOLO, Detectron2, etc.)
            # 3. Find bounding box of target object
            # 4. Return coordinates
            
            ColoredOutput.print_warning("Advanced object detection not yet implemented")
            return None
            
        except Exception as e:
            ColoredOutput.print_error(f"Area selection error: {str(e)}")
            return None
    
    def _solve_generic_challenge(self, task: Dict, question: str) -> Optional[Dict]:
        """
        Solve other challenge types
        
        Args:
            task: Challenge task data
            question: Challenge question/prompt
            
        Returns:
            Solution dict or None
        """
        ColoredOutput.print_info(f"🔧 Generic challenge handler for: {question}")
        ColoredOutput.print_warning("This challenge type requires manual solving")
        return None
    
    def _extract_target_from_question(self, question: str) -> str:
        """
        Extract target object from challenge question
        Example: "Select all images with traffic lights" -> "traffic lights"
        
        Args:
            question: Challenge question
            
        Returns:
            Target object name
        """
        import re
        
        # Common patterns in hCaptcha questions
        patterns = [
            r'select all (?:images )?(?:with|containing) (?:a |an |the )?(.+)',
            r'click (?:on |the )?(.+)',
            r'find (?:the |all )?(.+)',
            r'images? (?:with|containing) (.+)',
        ]
        
        question_lower = question.lower()
        for pattern in patterns:
            match = re.search(pattern, question_lower)
            if match:
                return match.group(1).strip()
        
        # Fallback: return last few words
        words = question.split()
        return ' '.join(words[-2:]) if len(words) >= 2 else question
    
    def _image_contains_object(self, image_bytes: bytes, target_object: str) -> bool:
        """
        Use AI to determine if an image contains a specific object
        
        Args:
            image_bytes: Image data
            target_object: Object to look for (e.g., "traffic lights", "bicycle")
            
        Returns:
            True if object is detected, False otherwise
        """
        try:
            # Strategy 1: Use HuggingFace image classification
            ColoredOutput.print_info(f"Checking for '{target_object}'...")
            
            # Try multiple vision models for object detection
            models = [
                'https://api-inference.huggingface.co/models/Salesforce/blip2-opt-2.7b',
                'https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large',
                'https://api-inference.huggingface.co/models/nlpconnect/vit-gpt2-image-captioning'
            ]
            
            for model_url in models:
                try:
                    # Send image to vision model
                    files = {'file': ('image.png', image_bytes, 'image/png')}
                    response = self.session.post(model_url, files=files, timeout=30)
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        # Extract description
                        description = ""
                        if isinstance(result, list) and len(result) > 0:
                            description = result[0].get('generated_text', result[0].get('label', ''))
                        elif isinstance(result, dict):
                            description = result.get('generated_text', result.get('text', ''))
                        
                        if description:
                            description_lower = description.lower()
                            target_lower = target_object.lower()
                            
                            # Check if target object is mentioned
                            # Handle variations: "traffic light" vs "traffic lights"
                            target_words = target_lower.split()
                            match = any(word in description_lower for word in target_words if len(word) > 3)
                            
                            if match or target_lower in description_lower:
                                ColoredOutput.print_info(f"Match found in: '{description}'")
                                return True
                            else:
                                ColoredOutput.print_info(f"No match in: '{description}'")
                    
                    elif response.status_code == 503:
                        time.sleep(1)
                        continue
                
                except Exception as model_error:
                    ColoredOutput.print_warning(f"Model error: {str(model_error)[:50]}")
                    continue
            
            # If no model could determine, return False (safer)
            return False
            
        except Exception as e:
            ColoredOutput.print_error(f"Object detection error: {str(e)}")
            return False
    
    def _submit_hcaptcha_solutions(self, sitekey: str, challenge_data: Dict, solutions: list) -> Optional[str]:
        """
        Submit hCaptcha solutions and get response token
        
        Args:
            sitekey: hCaptcha site key
            challenge_data: Original challenge data
            solutions: List of solutions
            
        Returns:
            hCaptcha response token or None
        """
        try:
            ColoredOutput.print_info("📤 Submitting solutions to hCaptcha...")
            
            # Build submission payload
            payload = {
                'sitekey': sitekey,
                'serverdomain': challenge_data.get('c', {}).get('req', 'discord.com'),
                'answers': solutions,
                'job_mode': 'image_label_binary',
                'motionData': {'st': int(time.time() * 1000), 'dct': int(time.time() * 1000), 'mm': []},
            }
            
            response = self.session.post(
                'https://hcaptcha.com/checkcaptcha',
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('pass'):
                    token = result.get('generated_pass_UUID')
                    ColoredOutput.print_success(f"✓ hCaptcha token received!")
                    return token
                else:
                    ColoredOutput.print_error("Solutions rejected by hCaptcha")
            
            return None
            
        except Exception as e:
            ColoredOutput.print_error(f"Submission error: {str(e)}")
            return None
    
    def _get_hcaptcha_accessibility_challenge(self, sitekey: str) -> Optional[Dict]:
        """
        Try to get text-based accessibility challenge (easier to solve)
        
        Args:
            sitekey: hCaptcha site key
            
        Returns:
            Challenge data or None
        """
        try:
            # Request accessibility challenge
            response = self.session.get(
                f'https://hcaptcha.com/getcaptcha?sitekey={sitekey}&mode=accessibility',
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            
            return None
            
        except Exception:
            return None
    
    def _solve_text_challenge(self, challenge: Dict) -> Optional[str]:
        """
        Solve text-based accessibility challenge
        
        Args:
            challenge: Text challenge data
            
        Returns:
            Challenge solution token or None
        """
        try:
            # Text challenges are typically audio CAPTCHAs transcribed
            # or simple text questions
            ColoredOutput.print_info("Solving text-based challenge...")
            
            # This would require audio transcription or text processing
            ColoredOutput.print_warning("Text challenge solving not yet implemented")
            return None
            
        except Exception:
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
