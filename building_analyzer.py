from PIL import Image
import numpy as np

class BuildingAnalyzer:
    """Analyzes building images to extract characteristics"""
    
    def analyze_image(self, image_path):
        """
        Analyze building image to extract features
        For demo purposes, uses simple image analysis
        """
        try:
            img = Image.open(image_path)
            
            # Convert to RGB if needed
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Get image statistics
            img_array = np.array(img)
            
            # Analyze image characteristics
            characteristics = {
                'image_size': img.size,
                'width': img.size[0],
                'height': img.size[1],
                'aspect_ratio': round(img.size[0] / img.size[1], 2),
                'average_brightness': self._calculate_brightness(img_array),
                'complexity': self._estimate_complexity(img_array),
                'dominant_colors': self._get_dominant_colors(img_array)
            }
            
            # Infer building characteristics
            building_features = self._infer_building_features(characteristics)
            
            return {
                'success': True,
                'image_info': characteristics,
                'building_features': building_features
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _calculate_brightness(self, img_array):
        """Calculate average brightness of image"""
        grayscale = np.mean(img_array, axis=2)
        avg_brightness = np.mean(grayscale)
        return round(avg_brightness / 255, 2)
    
    def _estimate_complexity(self, img_array):
        """Estimate image complexity (proxy for building detail)"""
        # Calculate standard deviation as a measure of complexity
        std_dev = np.std(img_array)
        
        if std_dev > 60:
            return 'complex'
        elif std_dev > 30:
            return 'moderate'
        else:
            return 'simple'
    
    def _get_dominant_colors(self, img_array):
        """Get dominant color categories"""
        avg_r = np.mean(img_array[:, :, 0])
        avg_g = np.mean(img_array[:, :, 1])
        avg_b = np.mean(img_array[:, :, 2])
        
        # Classify based on RGB values
        if avg_r > 180 and avg_g > 180 and avg_b > 180:
            return 'light_colors'
        elif avg_r < 80 and avg_g < 80 and avg_b < 80:
            return 'dark_colors'
        else:
            return 'mixed_colors'
    
    def _infer_building_features(self, characteristics):
        """Infer building features from image characteristics"""
        features = {}
        
        # Estimate building size from image dimensions
        total_pixels = characteristics['width'] * characteristics['height']
        if total_pixels > 1000000:
            features['estimated_size'] = 'large'
            features['size_factor'] = 1.3
        elif total_pixels > 400000:
            features['estimated_size'] = 'medium'
            features['size_factor'] = 1.0
        else:
            features['estimated_size'] = 'small'
            features['size_factor'] = 0.8
        
        # Estimate heat vulnerability based on colors (dark = more heat absorption)
        if characteristics['dominant_colors'] == 'dark_colors':
            features['heat_absorption'] = 'high'
            features['absorption_factor'] = 1.4
        elif characteristics['dominant_colors'] == 'light_colors':
            features['heat_absorption'] = 'low'
            features['absorption_factor'] = 0.7
        else:
            features['heat_absorption'] = 'medium'
            features['absorption_factor'] = 1.0
        
        # Estimate based on complexity (more complex = better ventilation design)
        if characteristics['complexity'] == 'complex':
            features['design_quality'] = 'advanced'
            features['design_factor'] = 0.8
        elif characteristics['complexity'] == 'moderate':
            features['design_quality'] = 'standard'
            features['design_factor'] = 1.0
        else:
            features['design_quality'] = 'basic'
            features['design_factor'] = 1.2
        
        return features
