# mcp/github.py
import os
import json
import subprocess
import requests
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = os.getenv("GITHUB_REPO")
GITHUB_BRANCH = os.getenv("GITHUB_BRANCH")

BASE_URL = "https://api.github.com"
HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}

def read_file(file_path: str) -> str:
    url = f"{BASE_URL}/repos/{GITHUB_REPO}/contents/{file_path}"
    params = {"ref": GITHUB_BRANCH}

    response = requests.get(url, headers=HEADERS, params=params)

    if response.status_code == 404:
        return ""  # file does not exist yet

    if response.status_code != 200:
        raise Exception(f"Failed to read file: {response.json()}")

    import base64
    content = response.json()["content"]
    return base64.b64decode(content).decode("utf-8")

def write_file(path: str, content: str, message: str, branch: str = None) -> dict:
    import os
    target_branch = branch or os.getenv("GITHUB_BRANCH")
    url = f"{BASE_URL}/repos/{GITHUB_REPO}/contents/{path}"

    # Get SHA if file exists on the target branch
    existing = requests.get(
        url,
        headers=HEADERS,
        params={"ref": target_branch}
    )
    sha = existing.json().get("sha") if existing.status_code == 200 else None

    import base64
    encoded = base64.b64encode(content.encode("utf-8")).decode("utf-8")

    body = {
        "message": message,
        "content": encoded,
        "branch": target_branch,
    }

    if sha:
        body["sha"] = sha

    response = requests.put(url, headers=HEADERS, json=body)

    if response.status_code not in [200, 201]:
        raise Exception(f"Failed to write file: {response.json()}")

    return response.json()
    
def list_directory(dir_path: str) -> list:
    url = f"{BASE_URL}/repos/{GITHUB_REPO}/contents/{dir_path}"
    params = {"ref": GITHUB_BRANCH}

    response = requests.get(url, headers=HEADERS, params=params)

    if response.status_code != 200:
        raise Exception(f"Failed to list directory: {response.json()}")

    return [item["path"] for item in response.json()]

def create_feature_branch(branch_name: str) -> str:
    # Get the SHA of the base branch
    ref_url = f"{BASE_URL}/repos/{GITHUB_REPO}/git/refs/heads/{GITHUB_BRANCH}"
    ref_response = requests.get(ref_url, headers=HEADERS)

    if ref_response.status_code != 200:
        raise Exception(f"Failed to get base branch: {ref_response.json()}")

    sha = ref_response.json()["object"]["sha"]

    # Create the new branch
    create_url = f"{BASE_URL}/repos/{GITHUB_REPO}/git/refs"
    body = {
        "ref": f"refs/heads/{branch_name}",
        "sha": sha,
    }

    response = requests.post(create_url, headers=HEADERS, json=body)

    if response.status_code not in [200, 201]:
        raise Exception(f"Failed to create branch: {response.json()}")

    return branch_name

def open_pull_request(title: str, body: str, head_branch: str) -> str:
    url = f"{BASE_URL}/repos/{GITHUB_REPO}/pulls"

    pr_body = {
        "title": title,
        "body": body,
        "head": head_branch,
        "base": GITHUB_BRANCH,
    }

    response = requests.post(url, headers=HEADERS, json=pr_body)

    if response.status_code not in [200, 201]:
        raise Exception(f"Failed to open PR: {response.json()}")

    return response.json()["html_url"]

def delete_branch(branch_name: str) -> bool:
    url = f"{BASE_URL}/repos/{GITHUB_REPO}/git/refs/heads/{branch_name}"
    response = requests.delete(url, headers=HEADERS)
    return response.status_code == 204