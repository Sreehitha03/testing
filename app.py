import os
import git
from flask import Flask, request, jsonify

app = Flask(__name__)

# Path where your repo will be cloned
REPO_PATH = "C:/Users/kadav/Desktop/coding/AI AGENT"

@app.route('/webhook', methods=['POST'])
def github_webhook():
    data = request.get_json()
    print("🔔 Webhook Triggered!")

    if not data:
        return jsonify({"error": "No data received"}), 400

    repo_name = data.get("repository", {}).get("full_name")
    commits = data.get("commits", [])
    print(f"📦 Repo: {repo_name}")

    # Clone the repo if not already cloned
    if not os.path.exists(REPO_PATH):
        print("Cloning repository...")
        git.Repo.clone_from(f'https://github.com/{repo_name}.git', REPO_PATH)

    # Track modified files
    modified_files = []
    for commit in commits:
        print(f"➡️ Commit message: {commit['message']}")
        print(f"📝 Modified files: {commit['modified']}")
        modified_files.extend(commit.get('modified', []))

    if modified_files:
        # Stage and commit modified files
        repo = git.Repo(REPO_PATH)
        repo.git.add(modified_files)
        repo.git.commit('-m', 'Auto-commit: Changes detected via webhook')

        # Push the changes back to GitHub
        origin = repo.remote(name='origin')
        origin.push()

        print("✅ Changes committed and pushed to GitHub.")
    else:
        print("🔄 No files modified.")

    return jsonify({"status": "received"}), 200


if __name__ == '__main__':
    app.run(port=5000)
