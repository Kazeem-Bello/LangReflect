import os
import matplotlib.pyplot as plt
from github import Github
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
token = os.getenv("GITHUB_TOKEN")

# Authenticate
g = Github(token)
user = g.get_user()
username = user.login

print(f"Generating language chart for {username}...")

# Aggregate languages across all repositories
language_data = {}

for repo in user.get_repos():
    if repo.fork:
        continue  # Skip forked repos

    try:
        langs = repo.get_languages()
        for lang, size in langs.items():
            language_data[lang] = language_data.get(lang, 0) + size
    except Exception as e:
        print(f"Error fetching languages for {repo.name}: {e}")

# Sort by most used languages
language_data = dict(sorted(language_data.items(), key=lambda x: x[1], reverse=True))

# Convert bytes to percentage
total = sum(language_data.values())
language_percentages = {lang: (size / total) * 100 for lang, size in language_data.items()}


# --- Sort and compute percentages ---
language_data = dict(sorted(language_data.items(), key=lambda x: x[1], reverse=True))
total = sum(language_data.values())
languages = list(language_data.keys())
percentages = [round((size / total) * 100, 2) for size in language_data.values()]

# Filter out unwanted languages like Jupyter Notebook 
# ignore_langs = ["Jupyter Notebook", "TeX", "Shell"]
# for lang in ignore_langs:
#     language_percentages.pop(lang, None)

# Generate bar chart
plt.figure(figsize=(10, 6))
plt.barh(list(language_percentages.keys()), list(language_percentages.values()), color="skyblue")
plt.title(f"Most Used Languages by {username} (LangReflect)")
plt.xlabel("Percentage (%)")
plt.ylabel("Language")
plt.gca().invert_yaxis()
plt.tight_layout()

# Save chart
output_path = "langreflect_chart.png"
plt.savefig(output_path)
print(f"Chart saved as {output_path}")

# Generate a markdown snippet for README
snippet = f"![LangReflect Chart](./{output_path})"
with open("chart_snippet.md", "w") as f:
    f.write(snippet)
print("Markdown snippet generated: chart_snippet.md")






# --- Sort and compute percentages ---
language_data = dict(sorted(language_data.items(), key=lambda x: x[1], reverse=True))
total = sum(language_data.values())
languages = list(language_data.keys())
percentages = [round((size / total) * 100, 2) for size in language_data.values()]

# --- Optional: Exclude Jupyter Notebook ---
if "Jupyter Notebook" in languages:
    idx = languages.index("Jupyter Notebook")
    del languages[idx]
    del percentages[idx]

# --- Limit to top 6 for readability ---
languages = languages[:6]
percentages = percentages[:6]

# --- Chart style ---
fig, ax = plt.subplots(figsize=(8, 4.5))
fig.patch.set_facecolor("#0d1117")  # GitHub dark background
ax.set_facecolor("#0d1117")

# --- Colors for the dots and bars ---
colors = ["#e34c26", "#3572A5", "#f1e05a", "#563d7c", "#384d54", "#ff9900"]

# --- Title ---
ax.text(0.02, 1.05, "Most Used Languages", fontsize=18, color="#58a6ff", fontweight="bold", transform=ax.transAxes)

# --- Draw progress bar style chart ---
for i, (lang, perc) in enumerate(zip(languages, percentages)):
    y = len(languages) - i - 1
    ax.barh(y, perc, color=colors[i % len(colors)], height=0.25, edgecolor='none', zorder=3)
    ax.scatter(0, y, color=colors[i % len(colors)], s=120, zorder=4)
    ax.text(0.1, y, f"{lang} {perc:.2f}%", va='center', color="#94e2d5", fontsize=11, fontweight='bold')

# --- Style cleanup ---
ax.set_xlim(0, 100)
ax.set_ylim(-1, len(languages))
ax.axis('off')
plt.box(False)

# --- Rounded border like GitHub Readme Stats ---
for spine in ax.spines.values():
    spine.set_visible(False)
border = plt.Rectangle((-1, -1), 101, len(languages)+1,
                       linewidth=1.5, edgecolor="#94e2d5",
                       facecolor="none", zorder=5)
ax.add_patch(border)

plt.tight_layout()
plt.savefig("langreflect_chart.png", dpi=300, bbox_inches='tight', facecolor="#0d1117")
print("✅ Chart generated: langreflect_chart.png")
