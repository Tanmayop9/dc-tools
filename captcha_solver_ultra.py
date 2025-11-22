#!/usr/bin/env python3
"""
Ultra Advanced Free CAPTCHA Solver - For Educational Purposes Only
Combines multiple free methods for maximum success rate:
- AI Vision Models (HuggingFace, local models)
- Advanced OCR (EasyOCR, Tesseract with preprocessing)
- Browser automation (Playwright, Selenium)
- Pattern recognition and ML
- Hybrid approaches

NO PAID SERVICES - 100% FREE

DISCLAIMER: This tool is for educational purposes only.
Use at your own risk. The authors are not responsible for any misuse.
"""

import requests
import json
import base64
import time
import io
import re
import hashlib
from typing import Optional, Dict, Any, List, Tuple
from pathlib import Path
from urllib.parse import urlparse

class ColoredOutput:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

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


class UltraAdvancedCaptchaSolver:
    """
    Ultra Advanced Free CAPTCHA Solver
    Combines multiple free methods with intelligent fallback chain
    """
    
    def __init__(self, cache_dir: Optional[str] = None):
        """
        Initialize the ultra advanced CAPTCHA solver
        
        Args:
            cache_dir: Directory for caching solved CAPTCHAs (default: ~/captcha_cache)
        """
        if cache_dir is None:
            cache_dir = str(Path.home() / 'captcha_cache')
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True, parents=True)
        
        # Initialize solver methods in priority order (fastest to slowest)
        self.solver_chain = [
            ('Cache Lookup', self._solve_from_cache),
            ('HuggingFace BLIP-2', self._solve_with_hf_blip2),
            ('HuggingFace ViT-GPT2', self._solve_with_hf_vitgpt2),
            ('HuggingFace TrOCR', self._solve_with_hf_trocr),
            ('HuggingFace CLIP', self._solve_with_hf_clip),
            ('HuggingFace Donut', self._solve_with_hf_donut),
            ('Keras OCR', self._solve_with_keras_ocr),
            ('PaddleOCR', self._solve_with_paddle_ocr),
            ('EasyOCR', self._solve_with_easyocr),
            ('Tesseract Advanced', self._solve_with_tesseract_advanced),
            ('Tesseract Multiple Languages', self._solve_with_tesseract_multilang),
            ('OpenCV Template Matching', self._solve_with_opencv_template),
            ('OpenCV Contour Detection', self._solve_with_opencv_contours),
            ('Scikit-Image OCR', self._solve_with_skimage),
            ('PIL Advanced Preprocessing', self._solve_with_pil_advanced),
            ('Pattern Recognition', self._solve_with_pattern_recognition),
            ('ML Character Recognition', self._solve_with_ml_characters),
            ('Local LLM (Ollama)', self._solve_with_ollama),
            ('Local LLM (LLaVA Next)', self._solve_with_ollama_llava_next),
            ('Browser Automation', self._solve_with_browser),
        ]
        
        # Advanced retry configuration
        self.max_retries = 3
        self.retry_delay = 1
        
        # Performance metrics
        self.metrics = {
            'attempts': 0,
            'successes': 0,
            'failures': 0,
            'cache_hits': 0,
            'solver_stats': {}
        }
        
        ColoredOutput.print_success("Ultra Advanced Free CAPTCHA Solver initialized!")
        ColoredOutput.print_info(f"Solver chain: {len(self.solver_chain)} methods available")
    
    def _get_cache_key(self, image_bytes: bytes) -> str:
        """Generate cache key from image hash"""
        return hashlib.sha256(image_bytes).hexdigest()
    
    def _solve_from_cache(self, image_bytes: bytes, **kwargs) -> Optional[str]:
        """Check if we've solved this CAPTCHA before"""
        try:
            cache_key = self._get_cache_key(image_bytes)
            cache_file = self.cache_dir / f"{cache_key}.txt"
            
            if cache_file.exists():
                with open(cache_file, 'r') as f:
                    solution = f.read().strip()
                    if solution:
                        ColoredOutput.print_success(f"Cache hit! Solution: {solution}")
                        self.metrics['cache_hits'] += 1
                        return solution
        except Exception as e:
            ColoredOutput.print_warning(f"Cache lookup error: {str(e)}")
        return None
    
    def _cache_solution(self, image_bytes: bytes, solution: str):
        """Cache a solved CAPTCHA"""
        try:
            cache_key = self._get_cache_key(image_bytes)
            cache_file = self.cache_dir / f"{cache_key}.txt"
            with open(cache_file, 'w') as f:
                f.write(solution)
        except Exception as e:
            ColoredOutput.print_warning(f"Failed to cache solution: {str(e)}")
    
    def _solve_with_hf_blip2(self, image_bytes: bytes, **kwargs) -> Optional[str]:
        """Solve using HuggingFace BLIP-2 (advanced vision model)"""
        try:
            ColoredOutput.print_info("Trying HuggingFace BLIP-2 (advanced vision)...")
            
            for attempt in range(self.max_retries):
                try:
                    response = self.session.post(
                        'https://api-inference.huggingface.co/models/Salesforce/blip2-opt-2.7b',
                        data=image_bytes,
                        headers={'Content-Type': 'application/octet-stream'},
                        timeout=30
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        if isinstance(result, list) and len(result) > 0:
                            caption = result[0].get('generated_text', '')
                            if caption:
                                ColoredOutput.print_info(f"BLIP-2 caption: {caption}")
                                extracted = self._extract_text_from_caption(caption)
                                if extracted:
                                    ColoredOutput.print_success(f"BLIP-2 extracted: {extracted}")
                                    return extracted
                    
                    elif response.status_code == 503:
                        ColoredOutput.print_warning(f"Model loading, retry {attempt+1}/{self.max_retries}...")
                        time.sleep(self.retry_delay * (attempt + 1))
                        continue
                
                except Exception as e:
                    if attempt < self.max_retries - 1:
                        time.sleep(self.retry_delay)
                    
        except Exception as e:
            ColoredOutput.print_warning(f"BLIP-2 solver failed: {str(e)}")
        return None
    
    def _solve_with_hf_vitgpt2(self, image_bytes: bytes, **kwargs) -> Optional[str]:
        """Solve using HuggingFace ViT-GPT2"""
        try:
            ColoredOutput.print_info("Trying HuggingFace ViT-GPT2...")
            
            response = self.session.post(
                'https://api-inference.huggingface.co/models/nlpconnect/vit-gpt2-image-captioning',
                data=image_bytes,
                headers={'Content-Type': 'application/octet-stream'},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    caption = result[0].get('generated_text', '')
                    if caption:
                        ColoredOutput.print_info(f"ViT-GPT2 caption: {caption}")
                        extracted = self._extract_text_from_caption(caption)
                        if extracted:
                            ColoredOutput.print_success(f"ViT-GPT2 extracted: {extracted}")
                            return extracted
        
        except Exception as e:
            ColoredOutput.print_warning(f"ViT-GPT2 solver failed: {str(e)}")
        return None
    
    def _solve_with_easyocr(self, image_bytes: bytes, **kwargs) -> Optional[str]:
        """Solve using EasyOCR (advanced multi-language OCR)"""
        try:
            import easyocr
            import numpy as np
            from PIL import Image
            
            ColoredOutput.print_info("Trying EasyOCR (advanced OCR)...")
            
            # Initialize reader (cached after first use)
            if not hasattr(self, '_easyocr_reader'):
                self._easyocr_reader = easyocr.Reader(['en'], gpu=False)
            
            # Convert bytes to numpy array
            image = Image.open(io.BytesIO(image_bytes))
            image_np = np.array(image)
            
            # Read text
            results = self._easyocr_reader.readtext(image_np)
            
            if results:
                # Extract text from results
                texts = [text for (bbox, text, prob) in results if prob > 0.3]
                combined = ''.join(texts).strip()
                
                # Clean and extract alphanumeric
                extracted = ''.join(c for c in combined if c.isalnum())
                if extracted and 3 <= len(extracted) <= 10:
                    ColoredOutput.print_success(f"EasyOCR extracted: {extracted}")
                    return extracted
        
        except ImportError:
            ColoredOutput.print_warning("EasyOCR not installed (pip install easyocr)")
        except Exception as e:
            ColoredOutput.print_warning(f"EasyOCR solver failed: {str(e)}")
        return None
    
    def _solve_with_tesseract_advanced(self, image_bytes: bytes, **kwargs) -> Optional[str]:
        """Solve using Tesseract with advanced preprocessing"""
        try:
            import pytesseract
            from PIL import Image, ImageEnhance, ImageFilter
            import cv2
            import numpy as np
            
            ColoredOutput.print_info("Trying Tesseract with advanced preprocessing...")
            
            # Load image
            image = Image.open(io.BytesIO(image_bytes))
            
            # Try multiple preprocessing techniques
            preprocessing_methods = [
                ('Original', lambda img: img),
                ('Grayscale + Threshold', self._preprocess_threshold),
                ('Denoise + Sharpen', self._preprocess_denoise),
                ('Contrast Enhancement', self._preprocess_contrast),
                ('Edge Enhancement', self._preprocess_edges),
            ]
            
            for method_name, preprocess_func in preprocessing_methods:
                try:
                    processed = preprocess_func(image.copy())
                    
                    # Extract text with multiple configs
                    configs = [
                        '--psm 7 --oem 3',  # Single line
                        '--psm 8 --oem 3',  # Single word
                        '--psm 13 --oem 3', # Raw line
                    ]
                    
                    for config in configs:
                        text = pytesseract.image_to_string(processed, config=config).strip()
                        extracted = ''.join(c for c in text if c.isalnum())
                        
                        if extracted and 3 <= len(extracted) <= 10:
                            ColoredOutput.print_success(f"Tesseract ({method_name}) extracted: {extracted}")
                            return extracted
                
                except Exception:
                    continue
        
        except ImportError:
            ColoredOutput.print_warning("Tesseract not installed (install tesseract-ocr)")
        except Exception as e:
            ColoredOutput.print_warning(f"Tesseract solver failed: {str(e)}")
        return None
    
    def _preprocess_threshold(self, image):
        """Apply threshold preprocessing"""
        import cv2
        import numpy as np
        
        img_array = np.array(image.convert('L'))
        _, thresh = cv2.threshold(img_array, 127, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return Image.fromarray(thresh)
    
    def _preprocess_denoise(self, image):
        """Apply denoising and sharpening"""
        from PIL import ImageFilter, ImageEnhance
        
        image = image.filter(ImageFilter.MedianFilter(size=3))
        enhancer = ImageEnhance.Sharpness(image)
        return enhancer.enhance(2.0)
    
    def _preprocess_contrast(self, image):
        """Enhance contrast"""
        from PIL import ImageEnhance
        
        enhancer = ImageEnhance.Contrast(image)
        return enhancer.enhance(2.5)
    
    def _preprocess_edges(self, image):
        """Edge enhancement"""
        from PIL import ImageFilter
        
        return image.filter(ImageFilter.EDGE_ENHANCE_MORE)
    
    def _solve_with_pattern_recognition(self, image_bytes: bytes, **kwargs) -> Optional[str]:
        """Advanced pattern recognition and ML"""
        try:
            ColoredOutput.print_info("Trying pattern recognition...")
            
            from PIL import Image
            import numpy as np
            
            image = Image.open(io.BytesIO(image_bytes))
            
            # Convert to grayscale and analyze patterns
            gray = image.convert('L')
            pixels = np.array(gray)
            
            # Basic pattern matching for common CAPTCHA formats
            # This is a simplified example - can be extended with ML models
            
            # Look for high-contrast regions (potential text)
            threshold = pixels.mean()
            binary = (pixels > threshold).astype(np.uint8) * 255
            
            # Count connected components (potential characters)
            # This is a basic heuristic
            
            ColoredOutput.print_info("Pattern analysis complete (no text extracted)")
            
        except Exception as e:
            ColoredOutput.print_warning(f"Pattern recognition failed: {str(e)}")
        return None
    
    def _solve_with_ollama(self, image_bytes: bytes, **kwargs) -> Optional[str]:
        """Solve using local Ollama vision models"""
        try:
            ColoredOutput.print_info("Trying local Ollama vision model...")
            
            image_b64 = base64.b64encode(image_bytes).decode('utf-8')
            
            # Try multiple vision models
            models = ['llava:latest', 'llava:13b', 'bakllava:latest', 'llava:7b']
            
            for model in models:
                try:
                    response = self.session.post(
                        'http://localhost:11434/api/generate',
                        json={
                            'model': model,
                            'prompt': 'Extract ONLY the text/numbers from this CAPTCHA. Return just the alphanumeric characters with no explanation.',
                            'images': [image_b64],
                            'stream': False
                        },
                        timeout=60
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        text = result.get('response', '').strip()
                        extracted = self._extract_text_from_caption(text)
                        
                        if extracted:
                            ColoredOutput.print_success(f"Ollama ({model}) extracted: {extracted}")
                            return extracted
                
                except requests.exceptions.RequestException:
                    continue
        
        except Exception as e:
            ColoredOutput.print_info("Ollama not available (install from ollama.ai)")
        return None
    
    def _solve_with_browser(self, sitekey: str, url: str, **kwargs) -> Optional[str]:
        """Solve using browser automation (manual solving)"""
        try:
            # Import from existing free solver
            from captcha_solver_free import FreeCaptchaSolver
            
            ColoredOutput.print_info("Opening browser for manual solving...")
            ColoredOutput.print_warning("Please solve the CAPTCHA in your browser")
            
            solver = FreeCaptchaSolver()
            solution = solver.solve_captcha(sitekey, url)
            
            if solution:
                ColoredOutput.print_success("Browser manual solve successful!")
                return solution
        
        except ImportError:
            ColoredOutput.print_error("FreeCaptchaSolver not available")
        except Exception as e:
            ColoredOutput.print_warning(f"Browser solver failed: {str(e)}")
        return None
    
    def _solve_with_hf_trocr(self, image_bytes: bytes, **kwargs) -> Optional[str]:
        """Solve using HuggingFace TrOCR (Transformer-based OCR)"""
        try:
            ColoredOutput.print_info("Trying HuggingFace TrOCR...")
            
            response = self.session.post(
                'https://api-inference.huggingface.co/models/microsoft/trocr-base-printed',
                data=image_bytes,
                headers={'Content-Type': 'application/octet-stream'},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    text = result[0].get('generated_text', '')
                    if text:
                        extracted = ''.join(c for c in text if c.isalnum())
                        if extracted and 3 <= len(extracted) <= 10:
                            ColoredOutput.print_success(f"TrOCR extracted: {extracted}")
                            return extracted
        
        except Exception as e:
            ColoredOutput.print_warning(f"TrOCR solver failed: {str(e)}")
        return None
    
    def _solve_with_hf_clip(self, image_bytes: bytes, **kwargs) -> Optional[str]:
        """Solve using HuggingFace CLIP with text prompts
        
        Note: CLIP is primarily for image classification. This method serves as a
        framework for future implementation with candidate text matching.
        """
        try:
            ColoredOutput.print_info("Trying HuggingFace CLIP...")
            
            # CLIP for zero-shot image classification
            response = self.session.post(
                'https://api-inference.huggingface.co/models/openai/clip-vit-large-patch14',
                data=image_bytes,
                headers={'Content-Type': 'application/octet-stream'},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if result:
                    ColoredOutput.print_info(f"CLIP analysis complete")
                    # TODO: Implement custom logic for text extraction
                    # CLIP returns classification scores, would need to compare
                    # image against candidate alphanumeric strings
        
        except Exception as e:
            ColoredOutput.print_warning(f"CLIP solver failed: {str(e)}")
        return None
    
    def _solve_with_hf_donut(self, image_bytes: bytes, **kwargs) -> Optional[str]:
        """Solve using HuggingFace Donut (Document understanding)"""
        try:
            ColoredOutput.print_info("Trying HuggingFace Donut...")
            
            response = self.session.post(
                'https://api-inference.huggingface.co/models/naver-clova-ix/donut-base',
                data=image_bytes,
                headers={'Content-Type': 'application/octet-stream'},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    text = result[0].get('generated_text', '')
                    if text:
                        extracted = self._extract_text_from_caption(text)
                        if extracted:
                            ColoredOutput.print_success(f"Donut extracted: {extracted}")
                            return extracted
        
        except Exception as e:
            ColoredOutput.print_warning(f"Donut solver failed: {str(e)}")
        return None
    
    def _solve_with_keras_ocr(self, image_bytes: bytes, **kwargs) -> Optional[str]:
        """Solve using Keras-OCR"""
        try:
            import keras_ocr
            from PIL import Image
            import numpy as np
            
            ColoredOutput.print_info("Trying Keras-OCR...")
            
            # Initialize pipeline (cached after first use)
            if not hasattr(self, '_keras_ocr_pipeline'):
                self._keras_ocr_pipeline = keras_ocr.pipeline.Pipeline()
            
            # Load image
            image = Image.open(io.BytesIO(image_bytes))
            image_np = np.array(image)
            
            # Recognize text
            prediction_groups = self._keras_ocr_pipeline.recognize([image_np])
            
            if prediction_groups and len(prediction_groups) > 0:
                predictions = prediction_groups[0]
                texts = [text for text, box in predictions]
                combined = ''.join(texts).strip()
                extracted = ''.join(c for c in combined if c.isalnum())
                
                if extracted and 3 <= len(extracted) <= 10:
                    ColoredOutput.print_success(f"Keras-OCR extracted: {extracted}")
                    return extracted
        
        except ImportError:
            ColoredOutput.print_warning("Keras-OCR not installed (pip install keras-ocr)")
        except Exception as e:
            ColoredOutput.print_warning(f"Keras-OCR solver failed: {str(e)}")
        return None
    
    def _solve_with_paddle_ocr(self, image_bytes: bytes, **kwargs) -> Optional[str]:
        """Solve using PaddleOCR (Baidu's OCR)"""
        try:
            from paddleocr import PaddleOCR
            from PIL import Image
            import numpy as np
            
            ColoredOutput.print_info("Trying PaddleOCR...")
            
            # Initialize OCR (cached after first use)
            if not hasattr(self, '_paddle_ocr'):
                self._paddle_ocr = PaddleOCR(use_angle_cls=True, lang='en', show_log=False)
            
            # Load image
            image = Image.open(io.BytesIO(image_bytes))
            image_np = np.array(image)
            
            # Run OCR
            results = self._paddle_ocr.ocr(image_np, cls=True)
            
            if results and len(results) > 0 and results[0]:
                texts = []
                for line in results[0]:
                    if len(line) >= 2:
                        text = line[1][0]  # Get the text part
                        texts.append(text)
                
                combined = ''.join(texts).strip()
                extracted = ''.join(c for c in combined if c.isalnum())
                
                if extracted and 3 <= len(extracted) <= 10:
                    ColoredOutput.print_success(f"PaddleOCR extracted: {extracted}")
                    return extracted
        
        except ImportError:
            ColoredOutput.print_warning("PaddleOCR not installed (pip install paddleocr)")
        except Exception as e:
            ColoredOutput.print_warning(f"PaddleOCR solver failed: {str(e)}")
        return None
    
    def _solve_with_tesseract_multilang(self, image_bytes: bytes, **kwargs) -> Optional[str]:
        """Solve using Tesseract with multiple language support"""
        try:
            import pytesseract
            from PIL import Image
            
            ColoredOutput.print_info("Trying Tesseract with multiple languages...")
            
            # Load image
            image = Image.open(io.BytesIO(image_bytes))
            
            # Try different language combinations
            lang_configs = [
                'eng+fra',  # English + French
                'eng+deu',  # English + German
                'eng+spa',  # English + Spanish
                'eng+chi_sim',  # English + Simplified Chinese
            ]
            
            for lang in lang_configs:
                try:
                    text = pytesseract.image_to_string(image, lang=lang, config='--psm 7').strip()
                    extracted = ''.join(c for c in text if c.isalnum())
                    
                    if extracted and 3 <= len(extracted) <= 10:
                        ColoredOutput.print_success(f"Tesseract ({lang}) extracted: {extracted}")
                        return extracted
                except Exception:
                    continue
        
        except ImportError:
            ColoredOutput.print_warning("Tesseract not installed")
        except Exception as e:
            ColoredOutput.print_warning(f"Tesseract multilang solver failed: {str(e)}")
        return None
    
    def _solve_with_opencv_template(self, image_bytes: bytes, **kwargs) -> Optional[str]:
        """Solve using OpenCV template matching"""
        try:
            import cv2
            import numpy as np
            from PIL import Image
            
            ColoredOutput.print_info("Trying OpenCV template matching...")
            
            # Load image
            image = Image.open(io.BytesIO(image_bytes))
            image_np = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
            
            # Apply preprocessing
            _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
            
            # Find contours which might represent characters
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if contours:
                ColoredOutput.print_info(f"Found {len(contours)} potential character regions")
                # Template matching would require pre-stored character templates
                # This is a placeholder for the actual template matching logic
        
        except ImportError:
            ColoredOutput.print_warning("OpenCV not installed")
        except Exception as e:
            ColoredOutput.print_warning(f"OpenCV template matching failed: {str(e)}")
        return None
    
    def _solve_with_opencv_contours(self, image_bytes: bytes, **kwargs) -> Optional[str]:
        """Solve using OpenCV contour detection and analysis"""
        try:
            import cv2
            import numpy as np
            from PIL import Image
            import pytesseract
            
            ColoredOutput.print_info("Trying OpenCV contour detection...")
            
            # Load image
            image = Image.open(io.BytesIO(image_bytes))
            image_np = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
            
            # Apply multiple preprocessing techniques
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
            
            # Morphological operations
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
            morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
            
            # Convert back to PIL for Tesseract
            result_image = Image.fromarray(morph)
            text = pytesseract.image_to_string(result_image, config='--psm 7').strip()
            extracted = ''.join(c for c in text if c.isalnum())
            
            if extracted and 3 <= len(extracted) <= 10:
                ColoredOutput.print_success(f"OpenCV contours extracted: {extracted}")
                return extracted
        
        except ImportError:
            ColoredOutput.print_warning("OpenCV or Tesseract not installed")
        except Exception as e:
            ColoredOutput.print_warning(f"OpenCV contours solver failed: {str(e)}")
        return None
    
    def _solve_with_skimage(self, image_bytes: bytes, **kwargs) -> Optional[str]:
        """Solve using scikit-image preprocessing and OCR"""
        try:
            from skimage import filters, morphology, exposure
            from skimage.io import imread
            from PIL import Image
            import numpy as np
            import pytesseract
            
            ColoredOutput.print_info("Trying scikit-image preprocessing...")
            
            # Load image
            image = Image.open(io.BytesIO(image_bytes))
            image_np = np.array(image.convert('L'))
            
            # Apply various preprocessing techniques
            # Adaptive histogram equalization
            equalized = exposure.equalize_adapthist(image_np)
            
            # Apply Otsu thresholding
            thresh = filters.threshold_otsu(equalized)
            binary = equalized > thresh
            
            # Morphological operations
            cleaned = morphology.remove_small_objects(binary, min_size=50)
            
            # Convert to PIL for OCR
            result_image = Image.fromarray((cleaned * 255).astype(np.uint8))
            text = pytesseract.image_to_string(result_image, config='--psm 7').strip()
            extracted = ''.join(c for c in text if c.isalnum())
            
            if extracted and 3 <= len(extracted) <= 10:
                ColoredOutput.print_success(f"Scikit-image extracted: {extracted}")
                return extracted
        
        except ImportError:
            ColoredOutput.print_warning("Scikit-image not installed (pip install scikit-image)")
        except Exception as e:
            ColoredOutput.print_warning(f"Scikit-image solver failed: {str(e)}")
        return None
    
    def _solve_with_pil_advanced(self, image_bytes: bytes, **kwargs) -> Optional[str]:
        """Solve using advanced PIL preprocessing techniques"""
        try:
            from PIL import Image, ImageEnhance, ImageFilter, ImageOps
            import pytesseract
            
            ColoredOutput.print_info("Trying PIL advanced preprocessing...")
            
            # Load image
            image = Image.open(io.BytesIO(image_bytes))
            
            # Try multiple PIL preprocessing pipelines
            pipelines = [
                # Pipeline 1: Invert + Enhance
                lambda img: ImageEnhance.Contrast(ImageOps.invert(img.convert('L'))).enhance(3.0),
                # Pipeline 2: AutoContrast + Sharpen
                lambda img: ImageOps.autocontrast(img.convert('L')).filter(ImageFilter.SHARPEN),
                # Pipeline 3: Equalize + Enhance
                lambda img: ImageEnhance.Sharpness(ImageOps.equalize(img.convert('L'))).enhance(2.0),
                # Pipeline 4: Solarize + Contrast
                lambda img: ImageEnhance.Contrast(ImageOps.solarize(img.convert('L'), threshold=128)).enhance(2.5),
            ]
            
            for i, pipeline in enumerate(pipelines):
                try:
                    processed = pipeline(image.copy())
                    text = pytesseract.image_to_string(processed, config='--psm 7').strip()
                    extracted = ''.join(c for c in text if c.isalnum())
                    
                    if extracted and 3 <= len(extracted) <= 10:
                        ColoredOutput.print_success(f"PIL advanced (pipeline {i+1}) extracted: {extracted}")
                        return extracted
                except Exception:
                    continue
        
        except ImportError:
            ColoredOutput.print_warning("PIL or Tesseract not installed")
        except Exception as e:
            ColoredOutput.print_warning(f"PIL advanced solver failed: {str(e)}")
        return None
    
    def _solve_with_ml_characters(self, image_bytes: bytes, **kwargs) -> Optional[str]:
        """Solve using ML-based character recognition
        
        Note: This is a framework method for custom ML model integration.
        Users can implement their own models here.
        """
        try:
            from PIL import Image
            import numpy as np
            
            ColoredOutput.print_info("Trying ML character recognition...")
            
            # Load image
            image = Image.open(io.BytesIO(image_bytes))
            image_np = np.array(image.convert('L'))
            
            # TODO: Implement ML model loading and inference
            # Framework for custom ML model implementation:
            # 1. Load pre-trained CNN model (custom trained on CAPTCHA datasets)
            # 2. Use transfer learning from MNIST/EMNIST
            # 3. Implement character segmentation + individual recognition
            # 4. Try ensemble methods with multiple models
            #
            # Example implementation:
            # if hasattr(self, '_ml_model'):
            #     predictions = self._ml_model.predict(image_np)
            #     return self._decode_predictions(predictions)
            
            ColoredOutput.print_info("ML character recognition - no custom model loaded")
        
        except Exception as e:
            ColoredOutput.print_warning(f"ML character recognition failed: {str(e)}")
        return None
    
    def _solve_with_ollama_llava_next(self, image_bytes: bytes, **kwargs) -> Optional[str]:
        """Solve using Ollama with LLaVA-Next (improved vision model)"""
        try:
            ColoredOutput.print_info("Trying Ollama LLaVA-Next...")
            
            image_b64 = base64.b64encode(image_bytes).decode('utf-8')
            
            # Try LLaVA-Next variants
            models = ['llava-next:latest', 'llava-phi3:latest', 'llava-v1.6:latest']
            
            for model in models:
                try:
                    response = self.session.post(
                        'http://localhost:11434/api/generate',
                        json={
                            'model': model,
                            'prompt': 'What text or alphanumeric code is shown in this CAPTCHA image? Reply with ONLY the characters, no explanation.',
                            'images': [image_b64],
                            'stream': False
                        },
                        timeout=60
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        text = result.get('response', '').strip()
                        extracted = self._extract_text_from_caption(text)
                        
                        if extracted:
                            ColoredOutput.print_success(f"Ollama LLaVA-Next ({model}) extracted: {extracted}")
                            return extracted
                
                except requests.exceptions.RequestException:
                    continue
        
        except Exception as e:
            ColoredOutput.print_info("Ollama LLaVA-Next not available")
        return None
    
    def _extract_text_from_caption(self, caption: str) -> Optional[str]:
        """Extract alphanumeric text from caption"""
        if not caption:
            return None
        
        # Remove common words and phrases
        caption = caption.lower()
        noise_words = ['captcha', 'text', 'image', 'says', 'shows', 'reads', 'contains', 'displays']
        for word in noise_words:
            caption = caption.replace(word, ' ')
        
        # Extract alphanumeric sequences
        alphanumeric = re.findall(r'[a-zA-Z0-9]+', caption)
        
        # Filter valid CAPTCHA patterns (typically 4-8 characters)
        candidates = [s for s in alphanumeric if 3 <= len(s) <= 10]
        
        if candidates:
            # Return the longest candidate (most likely to be CAPTCHA)
            return max(candidates, key=len).upper()
        
        return None
    
    def solve_hcaptcha(self, sitekey: str, url: str) -> Optional[str]:
        """
        Solve hCaptcha using the solver chain
        
        Args:
            sitekey: hCaptcha site key
            url: Page URL where CAPTCHA appears
            
        Returns:
            CAPTCHA solution token or None
        """
        ColoredOutput.print_info("=" * 60)
        ColoredOutput.print_info("Starting Ultra Advanced Free hCaptcha Solver")
        ColoredOutput.print_info("=" * 60)
        
        self.metrics['attempts'] += 1
        
        # Try to get CAPTCHA challenge
        try:
            # Get hCaptcha config
            config_url = f"https://hcaptcha.com/getcaptcha/{sitekey}"
            response = self.session.post(config_url, json={
                'sitekey': sitekey,
                'host': urlparse(url).netloc,
                'v': '1',
                'motionData': '{}',
            })
            
            if response.status_code != 200:
                ColoredOutput.print_warning("Could not fetch CAPTCHA challenge via API")
                # Fall back to browser method
                return self._solve_with_browser(sitekey, url)
            
            data = response.json()
            
            # If we have image challenges, try to solve them
            if 'requester_question' in data and 'tasklist' in data:
                ColoredOutput.print_info(f"Challenge: {data.get('requester_question', {}).get('en', 'Unknown')}")
                
                # Get challenge images
                tasks = data.get('tasklist', [])
                if not tasks:
                    ColoredOutput.print_warning("No challenge tasks found")
                    return self._solve_with_browser(sitekey, url)
                
                # Try to solve each challenge image with all methods
                solutions = []
                for task in tasks:
                    image_url = task.get('datapoint_uri')
                    if not image_url:
                        continue
                    
                    # Download image
                    img_response = self.session.get(image_url)
                    if img_response.status_code == 200:
                        image_bytes = img_response.content
                        
                        # Try all solvers in chain
                        solution = self._solve_with_chain(image_bytes, sitekey=sitekey, url=url)
                        if solution:
                            solutions.append(solution)
                
                if solutions:
                    # Submit solutions (this is simplified - real implementation needs proper hCaptcha protocol)
                    ColoredOutput.print_success(f"Solved {len(solutions)} challenges!")
                    self.metrics['successes'] += 1
                    return solutions[0]  # Return first solution for now
        
        except Exception as e:
            ColoredOutput.print_error(f"Error in hCaptcha solve: {str(e)}")
        
        # Fallback to browser method
        ColoredOutput.print_info("Falling back to browser manual solve...")
        solution = self._solve_with_browser(sitekey, url)
        
        if solution:
            self.metrics['successes'] += 1
        else:
            self.metrics['failures'] += 1
        
        return solution
    
    def _solve_with_chain(self, image_bytes: bytes, **kwargs) -> Optional[str]:
        """
        Try all solvers in chain until one succeeds
        
        Args:
            image_bytes: CAPTCHA image bytes
            **kwargs: Additional arguments for specific solvers
            
        Returns:
            Solution or None
        """
        for solver_name, solver_func in self.solver_chain:
            try:
                ColoredOutput.print_info(f"Trying {solver_name}...")
                
                # Track solver stats
                if solver_name not in self.metrics['solver_stats']:
                    self.metrics['solver_stats'][solver_name] = {'attempts': 0, 'successes': 0}
                
                self.metrics['solver_stats'][solver_name]['attempts'] += 1
                
                solution = solver_func(image_bytes, **kwargs)
                
                if solution:
                    self.metrics['solver_stats'][solver_name]['successes'] += 1
                    self._cache_solution(image_bytes, solution)
                    ColoredOutput.print_success(f"{solver_name} succeeded!")
                    return solution
                else:
                    ColoredOutput.print_warning(f"{solver_name} failed, trying next...")
            
            except Exception as e:
                ColoredOutput.print_warning(f"{solver_name} error: {str(e)}")
                continue
        
        return None
    
    def get_stats(self) -> Dict:
        """Get performance statistics"""
        stats = self.metrics.copy()
        if stats['attempts'] > 0:
            stats['success_rate'] = (stats['successes'] / stats['attempts']) * 100
        else:
            stats['success_rate'] = 0.0
        
        return stats
    
    def print_stats(self):
        """Print performance statistics"""
        stats = self.get_stats()
        
        ColoredOutput.print_info("=" * 60)
        ColoredOutput.print_info("Ultra Advanced Solver Statistics")
        ColoredOutput.print_info("=" * 60)
        ColoredOutput.print_info(f"Total attempts: {stats['attempts']}")
        ColoredOutput.print_success(f"Successes: {stats['successes']}")
        ColoredOutput.print_error(f"Failures: {stats['failures']}")
        ColoredOutput.print_info(f"Success rate: {stats['success_rate']:.1f}%")
        ColoredOutput.print_info(f"Cache hits: {stats['cache_hits']}")
        
        ColoredOutput.print_info("\nSolver performance:")
        for solver, solver_stats in stats['solver_stats'].items():
            attempts = solver_stats['attempts']
            successes = solver_stats['successes']
            rate = (successes / attempts * 100) if attempts > 0 else 0
            ColoredOutput.print_info(f"  {solver}: {successes}/{attempts} ({rate:.1f}%)")


# Backward compatibility - provide same interface as LLMCaptchaSolver
class LLMCaptchaSolver(UltraAdvancedCaptchaSolver):
    """Alias for backward compatibility"""
    pass
