from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def github_webhook():
    data = request.get_json()
    print("🔔 Webhook Triggered!")

    if not data:
        return jsonify({"error": "No data received"}), 400

    repo = data.get("repository", {}).get("full_name")
    commits = data.get("commits", [])

    print(f"📦 Repo: {repo}")
    for commit in commits:
        print(f"➡️ Commit message: {commit['message']}")
        print(f"📝 Modified files: {commit['modified']}")

    return jsonify({"status": "received"}), 200

if __name__ == '__main__':
    app.run(port=5000)
