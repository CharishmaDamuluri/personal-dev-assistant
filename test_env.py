import os
from dotenv import load_dotenv

load_dotenv()

print("Anthropic key present:", bool(os.getenv("OPENAI_API_KEY")))
print("GitHub token present:", bool(os.getenv("GITHUB_TOKEN")))
print("Repo:", os.getenv("GITHUB_REPO"))
print("Branch:", os.getenv("GITHUB_BRANCH"))