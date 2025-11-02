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

# Sort and compute percentages 
language_data = dict(sorted(language_data.items(), key=lambda x: x[1], reverse=True))
total = sum(language_data.values())
languages = list(language_data.keys())
percentages = [round((size / total) * 100, 2) for size in language_data.values()]


# Limit to top 6 for readability
languages = languages[:6]
percentages = percentages[:6]
# Chart style
fig, ax = plt.subplots(figsize=(6, 2.5))
fig.patch.set_facecolor("#1a1b27")  # GitHub dark background
ax.set_facecolor("#1a1b27")
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")

# Colors for the dots and bars 
colors = ["#f00ca8", "#3572A5", "#f1e05a", "#563d7c", "#384d54", "#ff9900"]

# Title 
ax.text(0.05, 1.05, "Most Used Languages", fontsize=18, color="#70a5fe", fontweight="bold")
ax.text(0.7, 0, "Powered By LangReflect", fontsize=6, color= "#70a5fe", fontweight="bold")



for spine in ax.spines.values():
    spine.set_visible(False)

l_offset = 0
r_offset = 0
p_offset = 0.00
v_start = 0.7
l_start = 0.1
r_start = 0.6
for i, (lang, perc) in enumerate(zip(languages, percentages)):
    if i%2 == 0:
        text = ax.text(l_start, v_start + l_offset, lang, fontsize=12, color= "#38b9ab", fontweight="bold")        
        # Draw the figure to calculate layout metrics
        fig.canvas.draw()

        # Get the text's bounding box in display (pixel) coordinates
        bbox = text.get_window_extent()

        # Convert that box to data coordinates
        inv = ax.transData.inverted()
        bbox_data = bbox.transformed(inv)

        num = ax.text(bbox_data.x1 + p_offset, v_start + l_offset, perc, fontsize=12, color= "#38b9ab", fontweight="bold")
        circle = ax.scatter(0.06, v_start + 0.04 + l_offset, color= colors[i], s=120) 
        l_offset -= 0.2


    else: 
        text = ax.text(r_start, v_start + r_offset, lang, fontsize=12, color= "#38b9ab", fontweight="bold")
        # Draw the figure to calculate layout metrics
        fig.canvas.draw()

        # Get the text's bounding box in display (pixel) coordinates
        bbox = text.get_window_extent()

        # Convert that box to data coordinates
        inv = ax.transData.inverted()
        bbox_data = bbox.transformed(inv)

        num = ax.text(bbox_data.x1 + p_offset, v_start + r_offset, perc, fontsize=12, color= "#38b9ab", fontweight="bold")
        circle = ax.scatter(0.56, v_start + 0.04 + r_offset, color= colors[i], s=120) 
        r_offset -= 0.2


fig.patch.set_linewidth(2)
fig.patch.set_edgecolor("#c7c5c7")
plt.tight_layout()

# Save chart
output_path = "langreflect_chart.png"
plt.savefig(output_path)

print(f"Chart saved as {output_path}")

# Generate a markdown snippet for README
snippet = f"`![LangReflect Chart](./{output_path})`"
with open("chart_snippet.md", "w") as f:
    f.write(snippet)
print("Markdown snippet generated: chart_snippet.md")







