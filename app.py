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
       
        repo_path = REPO_PATH  
        repo = git.Repo(repo_path)

        
        repo.git.add('app.py')  

        if repo.is_dirty():
           
            repo.git.commit('-m', 'Auto-commit: Changes detected via webhook')

            
            origin = repo.remotes.origin
            origin.push()

            return jsonify({"status": "success", "message": "Commit pushed to GitHub."}), 200
        else:
            return jsonify({"status": "no changes", "message": "No changes to commit."}), 200

    except Exception as e:
        print(f"⚠️ Error: {e}")
        return jsonify({"error": "Failed to commit changes."}), 500

if __name__ == '__main__':
    app.run(port=5000)
