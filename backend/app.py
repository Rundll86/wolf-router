from flask import Flask, request, Response, jsonify, send_from_directory
from flask_cors import CORS
import json
import os

from config import ModelName
from router import call_router_llm
from models import stream_model_response

app = Flask(__name__, static_folder='../public', static_url_path='')
CORS(app)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, '../public'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_input = data.get('message', '')
        
        if not user_input:
            return jsonify({"error": "请提供消息内容"}), 400

        route_result = call_router_llm(user_input)
        
        if not route_result:
            return jsonify({"error": "路由失败，请稍后重试"}), 500

        model_name = route_result.model
        reason = route_result.reason

        def generate():
            yield json.dumps({
                "type": "route",
                "model": model_name.value,
                "reason": reason
            }) + '\n'
            
            for chunk in stream_model_response(model_name, user_input):
                yield json.dumps({
                    "type": "response",
                    "content": chunk
                }) + '\n'

        return Response(generate(), mimetype='application/json')
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/models', methods=['GET'])
def get_models():
    models = [model.value for model in ModelName]
    return jsonify({"models": models})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)