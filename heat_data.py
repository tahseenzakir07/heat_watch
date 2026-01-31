import json
import math
import numpy as np

class HeatDataProcessor:
    """Processes and generates Urban Heat Island data for given coordinates"""
    
    def __init__(self, data_file='data/sample_heat_data.json'):
        with open(data_file, 'r') as f:
            self.data = json.load(f)
        self.heat_zones = self.data['heat_zones']
        self.sample_locations = self.data['sample_locations']
    
    def get_heat_data(self, lat, lng):
        """
        Calculate heat data for given coordinates
        Uses distance-based interpolation from sample locations
        """
        # Find nearest sample location
        min_distance = float('inf')
        nearest_zone = 'suburban'
        
        for location in self.sample_locations:
            distance = self._calculate_distance(
                lat, lng, 
                location['lat'], location['lng']
            )
            if distance < min_distance:
                min_distance = distance
                nearest_zone = location['zone']
        
        # Get zone data
        zone_data = self.heat_zones[nearest_zone]
        
        # Add some randomness for variation
        temp_variation = np.random.uniform(-2, 2)
        
        result = {
            'latitude': lat,
            'longitude': lng,
            'temperature': round(zone_data['base_temp'] + temp_variation, 1),
            'heat_index': zone_data['heat_index'],
            'zone_type': nearest_zone,
            'zone_description': zone_data['description'],
            'risk_level': self._calculate_risk_level(zone_data['heat_index'])
        }
        
        return result
    
    def _calculate_distance(self, lat1, lng1, lat2, lng2):
        """Calculate distance between two coordinates using Haversine formula"""
        R = 6371  # Earth's radius in km
        
        dlat = math.radians(lat2 - lat1)
        dlng = math.radians(lng2 - lng1)
        
        a = (math.sin(dlat / 2) ** 2 + 
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * 
             math.sin(dlng / 2) ** 2)
        
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = R * c
        
        return distance
    
    def _calculate_risk_level(self, heat_index):
        """Determine risk level based on heat index"""
        if heat_index >= 0.75:
            return 'HIGH'
        elif heat_index >= 0.50:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    def generate_heatmap_grid(self, center_lat, center_lng, grid_size=20, radius=0.05):
        """
        Generate a grid of heat values around a center point for visualization
        """
        heatmap_data = []
        
        for i in range(grid_size):
            for j in range(grid_size):
                lat_offset = (i - grid_size/2) * (radius / grid_size) * 2
                lng_offset = (j - grid_size/2) * (radius / grid_size) * 2
                
                lat = center_lat + lat_offset
                lng = center_lng + lng_offset
                
                heat_data = self.get_heat_data(lat, lng)
                
                heatmap_data.append({
                    'lat': lat,
                    'lng': lng,
                    'intensity': heat_data['heat_index']
                })
        
        return heatmap_data
