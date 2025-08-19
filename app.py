from flask import Flask, jsonify, request
import mcp_handler

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello, MCP!"

@app.route("/tap", methods=["POST"])
def tap():
    data = request.get_json()
    x = data.get("x")
    y = data.get("y")
    if x is None or y is None:
        return jsonify({"error": "Missing x or y"}), 400

    output, error = mcp_handler.handle_tap(x, y)
    if error:
        return jsonify({"error": error}), 500
    return jsonify({"output": output})

@app.route("/swipe", methods=["POST"])
def swipe():
    data = request.get_json()
    x1 = data.get("x1")
    y1 = data.get("y1")
    x2 = data.get("x2")
    y2 = data.get("y2")
    duration = data.get("duration", 100) # default duration 100ms
    if x1 is None or y1 is None or x2 is None or y2 is None:
        return jsonify({"error": "Missing coordinates"}), 400

    output, error = mcp_handler.handle_swipe(x1, y1, x2, y2, duration)
    if error:
        return jsonify({"error": error}), 500
    return jsonify({"output": output})

@app.route("/type", methods=["POST"])
def type_text():
    data = request.get_json()
    text = data.get("text")
    if text is None:
        return jsonify({"error": "Missing text"}), 400

    output, error = mcp_handler.handle_type(text)
    if error:
        return jsonify({"error": error}), 500
    return jsonify({"output": output})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
