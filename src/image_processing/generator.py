"""
Image Generator
Generates images for social media posts using AI
"""

import os
import logging
import requests
import asyncio
from typing import Optional, Dict, Any
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import io
import base64

# For local image generation
try:
    from diffusers import StableDiffusionPipeline
    import torch
    DIFFUSERS_AVAILABLE = True
except ImportError:
    DIFFUSERS_AVAILABLE = False

logger = logging.getLogger(__name__)

class ImageGenerator:
    """Generates images for social media posts"""
    
    def __init__(self, config):
        self.config = config
        self.pipeline = None
        self.output_dir = "generated_images"
        os.makedirs(self.output_dir, exist_ok=True)
        
        self._initialize_generator()
    
    def _initialize_generator(self):
        """Initialize image generation models"""
        try:
            # Try to initialize Stable Diffusion locally
            if DIFFUSERS_AVAILABLE and torch.cuda.is_available():
                logger.info("Initializing local Stable Diffusion...")
                self.pipeline = StableDiffusionPipeline.from_pretrained(
                    "runwayml/stable-diffusion-v1-5",
                    torch_dtype=torch.float16
                )
                self.pipeline = self.pipeline.to("cuda")
                logger.info("Local Stable Diffusion initialized")
            else:
                logger.info("Using API-based image generation (no local GPU available)")
                
        except Exception as e:
            logger.warning(f"Could not initialize local image generation: {e}")
    
    async def generate_image(self, prompt: str, style: str = "realistic") -> Optional[str]:
        """Generate an image based on text prompt"""
        try:
            # Clean and enhance the prompt
            enhanced_prompt = self._enhance_prompt(prompt, style)
            
            # Try different generation methods
            image_path = None
            
            # Method 1: Local Stable Diffusion
            if self.pipeline:
                image_path = await self._generate_local(enhanced_prompt)
            
            # Method 2: External API (Stability AI, etc.)
            if not image_path and self.config.stability_ai_api_key:
                image_path = await self._generate_with_stability_ai(enhanced_prompt)
            
            # Method 3: Fallback to simple text image
            if not image_path:
                image_path = await self._generate_text_image(prompt)
            
            if image_path:
                logger.info(f"Image generated successfully: {image_path}")
            
            return image_path
            
        except Exception as e:
            logger.error(f"Error generating image: {e}")
            return None
    
    def _enhance_prompt(self, prompt: str, style: str) -> str:
        """Enhance the prompt for better image generation"""
        # Extract key concepts from the prompt
        words = prompt.lower().split()
        
        # Remove social media specific words
        filtered_words = [word for word in words if word not in [
            'post', 'tweet', 'share', 'think', 'believe', 'just', 'really',
            'http', 'https', 'www', '#', '@'
        ]]
        
        # Take first meaningful concepts
        key_concepts = ' '.join(filtered_words[:10])
        
        # Add style modifiers
        style_modifiers = {
            'realistic': 'photorealistic, high quality, detailed',
            'artistic': 'digital art, creative, colorful',
            'minimalist': 'clean, simple, minimalist design',
            'professional': 'corporate, professional, clean design',
            'vibrant': 'vibrant colors, energetic, dynamic'
        }
        
        modifier = style_modifiers.get(style, style_modifiers['realistic'])
        
        enhanced_prompt = f"{key_concepts}, {modifier}"
        
        # Add negative prompt elements
        negative_elements = "text, watermark, signature, blurry, low quality"
        
        return f"{enhanced_prompt}, no {negative_elements}"
    
    async def _generate_local(self, prompt: str) -> Optional[str]:
        """Generate image using local Stable Diffusion"""
        try:
            # Generate image
            image = await asyncio.to_thread(
                self.pipeline,
                prompt,
                num_inference_steps=20,
                guidance_scale=7.5,
                width=512,
                height=512
            )
            
            # Save image
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"generated_{timestamp}.png"
            filepath = os.path.join(self.output_dir, filename)
            
            image.images[0].save(filepath)
            
            return filepath
            
        except Exception as e:
            logger.error(f"Local image generation failed: {e}")
            return None
    
    async def _generate_with_stability_ai(self, prompt: str) -> Optional[str]:
        """Generate image using Stability AI API"""
        try:
            url = "https://api.stability.ai/v1/generation/stable-diffusion-v1-6/text-to-image"
            
            headers = {
                "Authorization": f"Bearer {self.config.stability_ai_api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "text_prompts": [{"text": prompt}],
                "cfg_scale": 7,
                "height": 512,
                "width": 512,
                "samples": 1,
                "steps": 20
            }
            
            response = await asyncio.to_thread(
                requests.post, url, headers=headers, json=data
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Save the generated image
                image_data = base64.b64decode(result["artifacts"][0]["base64"])
                
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"generated_{timestamp}.png"
                filepath = os.path.join(self.output_dir, filename)
                
                with open(filepath, "wb") as f:
                    f.write(image_data)
                
                return filepath
            
            else:
                logger.error(f"Stability AI API error: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Stability AI generation failed: {e}")
            return None
    
    async def _generate_text_image(self, text: str) -> str:
        """Generate a simple text-based image as fallback"""
        try:
            # Create a simple image with text
            width, height = 800, 600
            background_color = (64, 128, 255)  # Nice blue
            text_color = (255, 255, 255)  # White
            
            # Create image
            image = Image.new('RGB', (width, height), background_color)
            draw = ImageDraw.Draw(image)
            
            # Prepare text
            display_text = text[:100] + "..." if len(text) > 100 else text
            
            # Try to use a nice font, fallback to default
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
            except:
                try:
                    font = ImageFont.truetype("arial.ttf", 36)
                except:
                    font = ImageFont.load_default()
            
            # Calculate text position
            text_bbox = draw.textbbox((0, 0), display_text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            
            # Handle long text by wrapping
            if text_width > width - 40:  # 40px margin
                words = display_text.split()
                lines = []
                current_line = ""
                
                for word in words:
                    test_line = current_line + " " + word if current_line else word
                    test_bbox = draw.textbbox((0, 0), test_line, font=font)
                    test_width = test_bbox[2] - test_bbox[0]
                    
                    if test_width <= width - 40:
                        current_line = test_line
                    else:
                        if current_line:
                            lines.append(current_line)
                        current_line = word
                
                if current_line:
                    lines.append(current_line)
                
                # Draw multiple lines
                line_height = text_height + 10
                total_height = len(lines) * line_height
                start_y = (height - total_height) // 2
                
                for i, line in enumerate(lines):
                    line_bbox = draw.textbbox((0, 0), line, font=font)
                    line_width = line_bbox[2] - line_bbox[0]
                    x = (width - line_width) // 2
                    y = start_y + i * line_height
                    draw.text((x, y), line, fill=text_color, font=font)
            
            else:
                # Single line
                x = (width - text_width) // 2
                y = (height - text_height) // 2
                draw.text((x, y), display_text, fill=text_color, font=font)
            
            # Add decorative elements
            draw.ellipse([50, 50, 100, 100], fill=(255, 255, 255, 128))
            draw.ellipse([width-100, height-100, width-50, height-50], fill=(255, 255, 255, 128))
            
            # Save image
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"text_image_{timestamp}.png"
            filepath = os.path.join(self.output_dir, filename)
            
            image.save(filepath, "PNG")
            
            return filepath
            
        except Exception as e:
            logger.error(f"Text image generation failed: {e}")
            return None
    
    def optimize_for_platform(self, image_path: str, platform: str) -> str:
        """Optimize image for specific social media platform"""
        try:
            # Platform specific requirements
            sizes = {
                'twitter': (1200, 675),      # 16:9 aspect ratio
                'instagram': (1080, 1080),   # Square
                'facebook': (1200, 630),     # ~1.9:1 aspect ratio
                'linkedin': (1200, 627)      # ~1.9:1 aspect ratio
            }
            
            target_size = sizes.get(platform, (1080, 1080))
            
            # Open and resize image
            with Image.open(image_path) as img:
                # Convert to RGB if necessary
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Resize maintaining aspect ratio
                img.thumbnail(target_size, Image.Resampling.LANCZOS)
                
                # Create new image with exact dimensions
                new_img = Image.new('RGB', target_size, (255, 255, 255))
                
                # Center the resized image
                x = (target_size[0] - img.width) // 2
                y = (target_size[1] - img.height) // 2
                new_img.paste(img, (x, y))
                
                # Save optimized image
                base_name = os.path.splitext(os.path.basename(image_path))[0]
                optimized_filename = f"{base_name}_{platform}.png"
                optimized_path = os.path.join(self.output_dir, optimized_filename)
                
                new_img.save(optimized_path, "PNG", optimize=True)
                
                return optimized_path
                
        except Exception as e:
            logger.error(f"Image optimization failed: {e}")
            return image_path  # Return original if optimization fails
    
    def add_watermark(self, image_path: str, watermark_text: str = None) -> str:
        """Add watermark to image"""
        try:
            if not watermark_text:
                watermark_text = "Generated by AI Social Media Writer"
            
            with Image.open(image_path) as img:
                # Create a transparent overlay
                overlay = Image.new('RGBA', img.size, (255, 255, 255, 0))
                draw = ImageDraw.Draw(overlay)
                
                # Use a small font for watermark
                try:
                    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
                except:
                    font = ImageFont.load_default()
                
                # Position watermark at bottom right
                text_bbox = draw.textbbox((0, 0), watermark_text, font=font)
                text_width = text_bbox[2] - text_bbox[0]
                text_height = text_bbox[3] - text_bbox[1]
                
                x = img.width - text_width - 10
                y = img.height - text_height - 10
                
                # Draw watermark with semi-transparent background
                draw.rectangle([x-5, y-5, x+text_width+5, y+text_height+5], 
                             fill=(0, 0, 0, 128))
                draw.text((x, y), watermark_text, fill=(255, 255, 255, 200), font=font)
                
                # Combine with original image
                watermarked = Image.alpha_composite(img.convert('RGBA'), overlay)
                
                # Save watermarked image
                base_name = os.path.splitext(os.path.basename(image_path))[0]
                watermarked_filename = f"{base_name}_watermarked.png"
                watermarked_path = os.path.join(self.output_dir, watermarked_filename)
                
                watermarked.convert('RGB').save(watermarked_path, "PNG")
                
                return watermarked_path
                
        except Exception as e:
            logger.error(f"Watermarking failed: {e}")
            return image_path
    
    def get_image_stats(self) -> Dict[str, Any]:
        """Get statistics about generated images"""
        try:
            images = [f for f in os.listdir(self.output_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
            
            total_size = sum(
                os.path.getsize(os.path.join(self.output_dir, img)) 
                for img in images
            )
            
            return {
                'total_images': len(images),
                'total_size_mb': total_size / (1024 * 1024),
                'output_directory': self.output_dir,
                'recent_images': images[-5:] if images else []
            }
            
        except Exception as e:
            logger.error(f"Error getting image stats: {e}")
            return {}