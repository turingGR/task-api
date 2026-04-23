from flask import Flask, jsonify, request, abort
from datetime import datetime, timezone
 
 
def create_app():
    app = Flask(__name__)
 
    # In-memory store (αρκεί για το μάθημα)
    tasks = {}
    state = {"next_id": 1}
 
    @app.get("/health")
    def health():
        return jsonify(
            status="ok",
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
 
    @app.get("/tasks")
    def list_tasks():
        return jsonify(list(tasks.values()))
 
    @app.post("/tasks")
    def create_task():
        data = request.get_json(silent=True) or {}
        title = data.get("title", "").strip()
        if not title:
            abort(400, description="title is required")
        task = {
            "id": state["next_id"],
            "title": title,
            "done": False,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        tasks[state["next_id"]] = task
        state["next_id"] += 1
        return jsonify(task), 201
 
    @app.put("/tasks/<int:task_id>")
    def update_task(task_id):
        if task_id not in tasks:
            abort(404)
        data = request.get_json(silent=True) or {}
        if "title" in data:
            tasks[task_id]["title"] = data["title"]
        if "done" in data:
            tasks[task_id]["done"] = bool(data["done"])
        return jsonify(tasks[task_id])
 
    @app.delete("/tasks/<int:task_id>")
    def delete_task(task_id):
        if task_id not in tasks:
            abort(404)
        del tasks[task_id]
        return "", 204
 
    return app
 
app = create_app()
 
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
