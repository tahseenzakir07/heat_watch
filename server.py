from flask import Flask, request, jsonify, send_from_directory, session
import os
from werkzeug.utils import secure_filename
from heat_data import HeatDataProcessor
from building_analyzer import BuildingAnalyzer
from recommendations import RecommendationEngine

app = Flask(__name__, static_folder='static')
app.secret_key = 'your-secret-key-for-demo'  # Change in production

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Initialize processors
heat_processor = HeatDataProcessor()
building_analyzer = BuildingAnalyzer()
recommendation_engine = RecommendationEngine()

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Serve the main dashboard page"""
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def serve_file(filename):
    """Serve any file from the root directory (css, js, maps, etc.)"""
    return send_from_directory('.', filename)

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Handle building image upload"""
    try:
        if 'building_image' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['building_image']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Please upload an image.'}), 400
        
        # Save file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Analyze the building image
        analysis_result = building_analyzer.analyze_image(filepath)
        
        if not analysis_result['success']:
            return jsonify({'error': 'Failed to analyze image'}), 500
        
        # Store analysis in session
        session['building_analysis'] = analysis_result['building_features']
        session['uploaded_file'] = filename
        
        return jsonify({
            'success': True,
            'filename': filename,
            'analysis': analysis_result['image_info'],
            'message': 'File uploaded and analyzed successfully'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analyze-location', methods=['POST'])
def analyze_location():
    """Analyze location based on coordinates"""
    try:
        data = request.get_json()
        
        if not data or 'latitude' not in data or 'longitude' not in data:
            return jsonify({'error': 'Latitude and longitude required'}), 400
        
        lat = float(data['latitude'])
        lng = float(data['longitude'])
        
        # Get heat data for location
        heat_data = heat_processor.get_heat_data(lat, lng)
        
        # Get building features from session
        building_features = session.get('building_analysis', None)
        
        # Generate recommendations
        recommendations = recommendation_engine.generate_recommendations(
            heat_data, building_features
        )
        
        # Generate heatmap grid data
        heatmap_grid = heat_processor.generate_heatmap_grid(lat, lng)
        
        result = {
            'success': True,
            'heat_data': heat_data,
            'recommendations': recommendations,
            'heatmap_data': heatmap_grid
        }
        
        # Store in session for results page
        session['analysis_result'] = result
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/get-results', methods=['GET'])
def get_results():
    """Retrieve stored analysis results"""
    result = session.get('analysis_result', None)
    
    if not result:
        return jsonify({'error': 'No analysis data found'}), 404
    
    return jsonify(result)

@app.route('/static/<path:path>')
def send_static(path):
    """Serve static files"""
    return send_from_directory('static', path)

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    print("=" * 60)
    print("Urban Heat Island Builder Analysis Tool")
    print("=" * 60)
    print("\nServer starting...")
    print("Open your browser and navigate to: http://localhost:5000")
    print("\nFeatures:")
    print("   - Upload building schematics")
    print("   - Interactive location selection")
    print("   - AI-powered heat analysis")
    print("   - Construction recommendations")
    print("\n" + "=" * 60)
    
    app.run(debug=True, port=5000, host='0.0.0.0')
