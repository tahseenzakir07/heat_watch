class RecommendationEngine:
    """Generates building recommendations based on heat data and building analysis"""
    
    def generate_recommendations(self, heat_data, building_features):
        """
        Generate comprehensive recommendations for building construction
        """
        # Calculate overall suitability score
        suitability_score = self._calculate_suitability(heat_data, building_features)
        
        # Generate specific recommendations
        recommendations = self._generate_specific_recommendations(
            heat_data, building_features, suitability_score
        )
        
        # Determine if construction is advisable
        is_advisable = suitability_score >= 60
        
        # Generate expert insight (rationale)
        expert_insight = self._generate_expert_insight(heat_data, building_features, suitability_score)
        
        result = {
            'suitability_score': suitability_score,
            'is_advisable': is_advisable,
            'verdict': self._get_verdict(suitability_score),
            'expert_insight': expert_insight,
            'heat_risk_level': heat_data['risk_level'],
            'recommendations': recommendations,
            'mitigation_strategies': self._get_mitigation_strategies(heat_data, building_features)
        }
        
        return result
    
    def _calculate_suitability(self, heat_data, building_features):
        """Calculate overall suitability score (0-100)"""
        base_score = 100
        
        # Deduct based on heat index
        heat_penalty = heat_data['heat_index'] * 40
        base_score -= heat_penalty
        
        # Adjust based on building characteristics
        if building_features:
            # Size factor
            size_penalty = (building_features.get('size_factor', 1.0) - 1.0) * 10
            base_score -= size_penalty
            
            # Heat absorption factor
            absorption_penalty = (building_features.get('absorption_factor', 1.0) - 1.0) * 15
            base_score -= absorption_penalty
            
            # Design quality factor (positive adjustment)
            design_bonus = (1.0 - building_features.get('design_factor', 1.0)) * 10
            base_score += design_bonus
        
        # Ensure score is within 0-100
        return max(0, min(100, round(base_score, 1)))
    
    def _get_verdict(self, score):
        """Get verdict text based on suitability score"""
        if score >= 80:
            return "Excellent location for construction"
        elif score >= 60:
            return "Good location with minor heat considerations"
        elif score >= 40:
            return "Moderate location - significant heat mitigation required"
        else:
            return "Not recommended - high heat stress area"
    
    def _generate_specific_recommendations(self, heat_data, building_features, score):
        """Generate specific actionable recommendations"""
        recs = []
        
        # Heat-based recommendations
        if heat_data['heat_index'] >= 0.75:
            recs.append({
                'category': 'Critical',
                'title': 'High Heat Zone',
                'description': 'This area experiences severe urban heat island effect. Cooling systems will require significant capacity.',
                'priority': 'high'
            })
        elif heat_data['heat_index'] >= 0.50:
            recs.append({
                'category': 'Important',
                'title': 'Moderate Heat Zone',
                'description': 'Moderate heat island effect detected. Plan for enhanced ventilation and cooling.',
                'priority': 'medium'
            })
        
        # Building-specific recommendations
        if building_features:
            if building_features.get('heat_absorption') == 'high':
                recs.append({
                    'category': 'Material Selection',
                    'title': 'Use Reflective Materials',
                    'description': 'Current design shows dark colors. Use light-colored, reflective roofing and exterior materials to reduce heat absorption.',
                    'priority': 'high'
                })
            
            if building_features.get('estimated_size') == 'large':
                recs.append({
                    'category': 'Design',
                    'title': 'Enhanced Cooling System',
                    'description': 'Large building footprint requires robust HVAC system designed for high ambient temperatures.',
                    'priority': 'medium'
                })
            
            if building_features.get('design_quality') == 'basic':
                recs.append({
                    'category': 'Design',
                    'title': 'Improve Ventilation Design',
                    'description': 'Consider adding cross-ventilation features, ventilation shafts, or green spaces to improve natural cooling.',
                    'priority': 'medium'
                })
        
        # Temperature-based recommendations
        if heat_data['temperature'] > 36:
            recs.append({
                'category': 'Climate Adaptation',
                'title': 'Heat-Resilient Construction',
                'description': f'Area temperature ({heat_data["temperature"]}°C) requires heat-resistant materials and superior insulation.',
                'priority': 'high'
            })
        
        return recs
    
    def _generate_expert_insight(self, heat_data, building_features, score):
        """Generate a concise expert analysis justifying the score"""
        insights = []
        
        # Risk levels
        if heat_data['heat_index'] > 0.8:
            insights.append("At this heat level, building traditional high-rises can create a 'vertical oven' effect where upper floors trap heat from the dense city core, making cooling costs unsustainable.")
        elif heat_data['heat_index'] > 0.5:
            insights.append("This moderate heat zone suggests that while construction is viable, placing high-density residential units here without extensive green buffers will lead to 'thermal discomfort' for lower-floor residents during peak summer.")
        else:
            insights.append("This is a 'Cool Pocket'—ideal for sustainable development. You have more flexibility with materials without risking severe heat retention.")

        # Building features (if available)
        if building_features:
            if building_features.get('estimated_size') == 'large' and heat_data['heat_index'] > 0.7:
                insights.append("For a 5+ storey proposal in this hotspot, reconsider the ground floor layout; heat trapped at street level will significantly impact livability for ground-floor commercial or residential units.")
            
            if building_features.get('heat_absorption') == 'high':
                insights.append("Your current schematic suggests a high-absorption exterior. In this specific climate zone, that color choice alone could increase interior temperatures by 4-6°C compared to local benchmarks.")

        if score < 40:
            insights.append("Strategic Warning: Building here without a complete redesign (e.g., pilotis for air flow, massive vertical greening) is likely to result in a 'failed building' status from an environmental efficiency standpoint.")
        elif score > 80:
            insights.append("Pro Tip: This site is a rare 'Thermal Asset'. Use this to market the property's natural cooling efficiency and low long-term energy footprint.")

        return " ".join(insights[:2]) # Keep it concise as requested

    def _get_mitigation_strategies(self, heat_data, building_features):
        """Get mitigation strategies to reduce heat impact"""
        strategies = []
        
        # Universal strategies
        strategies.append({
            'strategy': 'Green Roof Installation',
            'benefit': 'Reduces roof temperature by 20-30°C and provides insulation',
            'effectiveness': 'High'
        })
        
        strategies.append({
            'strategy': 'Vertical Gardens',
            'benefit': 'Cools building perimeter and improves air quality',
            'effectiveness': 'Medium'
        })
        
        # Heat-specific strategies
        if heat_data['heat_index'] > 0.6:
            strategies.append({
                'strategy': 'Double-Glazed Windows',
                'benefit': 'Reduces heat transfer by 40-50%',
                'effectiveness': 'High'
            })
            
            strategies.append({
                'strategy': 'Strategic Shading',
                'benefit': 'Use overhangs, louvers, and external shading devices',
                'effectiveness': 'High'
            })
        
        # Building-specific strategies
        if building_features and building_features.get('heat_absorption') == 'high':
            strategies.append({
                'strategy': 'Cool Roof Coating',
                'benefit': 'Reflective coating can reduce surface temperature by 20-25°C',
                'effectiveness': 'Very High'
            })
        
        return strategies
