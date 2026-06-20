# test_github.py
from mcp.github import read_file, write_file, list_directory

# Test reading a file that exists in your repo
content = read_file("README.md")
print("README content preview:")
print(content[:200])

# Test listing a directory
files = list_directory("")
print("\nRoot files:")
for f in files:
    print(f)

# Test writing a file
write_file(
    path="test-agent-output.txt",
    content="Hello from the dev assistant agent.",
    message="test: verify MCP write works"
)
print("\nWrite successful. Check your repo on GitHub.")