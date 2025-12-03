from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.model_loader import generate_prompt

app = Flask(__name__)
CORS(app)

@app.route('/api/enhance', methods=['POST'])
def enhance_prompt():
    data = request.json
    user_input = data.get('input', '')
    task_type = data.get('task_type', 'website')
    
    try:
        enhanced = generate_prompt(user_input, task_type)
        return jsonify({
            'success': True,
            'enhanced_prompt': enhanced,
            'task_type': task_type
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
