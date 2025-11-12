import os
import subprocess

ARTICLES_DIR = "articles"
SITE_DIR = "site"
TEMPLATE_FILE = "templates/article_template.html"

os.makedirs(SITE_DIR, exist_ok=True)

md_files = [f for f in os.listdir(ARTICLES_DIR) if f.endswith(".md")]
article_links = []

for md_file in md_files:
    md_path = os.path.join(ARTICLES_DIR, md_file)
    html_filename = md_file.replace(".md", ".html")
    html_path = os.path.join(SITE_DIR, html_filename)

    # Convertir Markdown en HTML
    result = subprocess.run(
        ["pandoc", md_path, "-t", "html"],
        capture_output=True,
        text=True
    )
    html_content = result.stdout

    # Lire le template
    with open(TEMPLATE_FILE, "r") as f:
        template = f.read()

    # Remplacer {{ title }} et {{ content }}
    title = md_file.replace(".md", "").replace("-", " ").title()
    final_html = template.replace("{{ title }}", title).replace("{{ content }}", html_content)

    # Sauvegarder le HTML final
    with open(html_path, "w") as f:
        f.write(final_html)

    # Ajouter le lien pour index.html
    article_links.append(f'<li><a class="text-blue-600 hover:underline" href="{html_filename}">{title}</a></li>')

# Générer index.html
index_content = f"""
<h2 class="text-2xl font-bold mb-4">Articles récents</h2>
<ul class="space-y-2">
    {''.join(article_links)}
</ul>
"""

# Réutiliser le même template pour index.html
with open(TEMPLATE_FILE, "r") as f:
    template = f.read()

with open(os.path.join(SITE_DIR, "index.html"), "w") as f:
    f.write(template.replace("{{ title }}", "Blog-IT").replace("{{ content }}", index_content))

print("✅ Site généré avec style Tailwind !")
