from flask import Flask, request, jsonify
import git
import os

app = Flask(__name__)

# Set the repository path (ensure this is correct for your system)
REPO_PATH = r"C:\Users\kadav\Desktop\coding\AI AGENT"

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

    try:
        # Initialize the repo and check if there are changes
        repo_path = REPO_PATH  # Path to the local Git repository
        repo = git.Repo(repo_path)

        # Stage the files for commit
        repo.git.add('app.py')  # Add the modified file(s) to staging area

        # Commit the changes
        repo.git.commit('-m', 'Auto-commit: Changes detected via webhook')

        # Push the commit to GitHub
        origin = repo.remotes.origin
        origin.push()

        return jsonify({"status": "success", "message": "Commit pushed to GitHub."}), 200

    except Exception as e:
        print(f"⚠️ Error: {e}")
        return jsonify({"error": "Failed to commit changes."}), 500

if __name__ == '__main__':
    app.run(port=5000)
