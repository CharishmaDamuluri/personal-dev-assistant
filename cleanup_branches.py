# cleanup_branches.py
from mcp.github import delete_branch
import requests
import os
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = os.getenv("GITHUB_REPO")
BASE_URL = "https://api.github.com"
HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
}

# Get all branches
response = requests.get(
    f"{BASE_URL}/repos/{GITHUB_REPO}/branches",
    headers=HEADERS
)

branches = response.json()
agent_branches = [b["name"] for b in branches if b["name"].startswith("feat/agent-task-")]

print(f"Found {len(agent_branches)} agent branches to delete")

for branch in agent_branches:
    try:
        delete_branch(branch)
        print(f"Deleted: {branch}")
    except Exception as e:
        print(f"Failed to delete {branch}: {e}")