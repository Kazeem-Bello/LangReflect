from github import Github
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

#  CONFIGURATION 
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

file_content = """# --- LANGUAGE CLASSIFICATION FIXES ---
*.ipynb linguist-language=Python
*.py linguist-language=Python
**/*.ipynb linguist-language=Python
"""

# INITIALIZE 
g = Github(GITHUB_TOKEN)
user = g.get_user()
USERNAME = user.login

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
log_entries = [f"GitHub .gitattributes Update Log \nRun Time: {timestamp}\nUser: {USERNAME}\n\n"]

print(f"\n Updating .gitattributes for all repositories owned by {USERNAME}...\n")

for repo in user.get_repos():
    try:
        # Skip archived or forked repos
        if repo.archived:
            msg = f"Skipped {repo.name} (archived)"
            print(msg)
            log_entries.append(msg + "\n")
            continue
        if repo.fork:
            msg = f"Skipped {repo.name} (forked repo)"
            print(msg)
            log_entries.append(msg + "\n")
            continue

        # Try to fetch existing .gitattributes
        try:
            file = repo.get_contents(".gitattributes")
            current_content = file.decoded_content.decode("utf-8")

            if current_content.strip() != file_content.strip():
                repo.update_file(
                    path=".gitattributes",
                    message=" Update .gitattributes for proper language detection",
                    content=file_content,
                    sha=file.sha,
                    branch= repo.default_branch 
                )
                msg = f"Updated .gitattributes in {repo.name}"
            else:
                msg = f"{repo.name}: already up to date"

        except Exception:
            # File doesn’t exist — create it
            repo.create_file(
                path=".gitattributes",
                message="Add .gitattributes for proper language detection",
                content=file_content,
                branch= repo.default_branch 
            )
            msg = f"Created .gitattributes in {repo.name}"

        print(msg)
        log_entries.append(msg + "\n")

    except Exception as e:
        msg = f" Error updating {repo.name}: {e}"
        print(msg)
        log_entries.append(msg + "\n")

# === WRITE LOG FILE ===
with open("update_log.txt", "w", encoding="utf-8") as log_file:
    log_file.writelines(log_entries)

print("\nDone! All repositories processed.")
print("Log file saved as 'update_log.txt'\n")
