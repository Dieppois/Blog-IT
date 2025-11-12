import os
import glob
import subprocess

ARTICLES_DIR = "articles"
SITE_DIR = "site"
TEMPLATE = "templates/article_template.html"

os.makedirs(SITE_DIR, exist_ok=True)

# Charger le template HTML
with open(TEMPLATE, "r", encoding="utf-8") as f:
    template = f.read()

index_content = "<h1>Blog IT - Contributions</h1>\n<ul>"

# Conversion de chaque article
for md_file in glob.glob(f"{ARTICLES_DIR}/*.md"):
    base = os.path.basename(md_file).replace(".md", "")
    html_file = f"{SITE_DIR}/{base}.html"

    subprocess.run(["pandoc", md_file, "-o", html_file])

    # Injecter le contenu dans le template
    with open(html_file, "r", encoding="utf-8") as f:
        article_html = f.read()

    final_html = template.replace("{{content}}", article_html)
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(final_html)

    index_content += f'<li><a href="{base}.html">{base}</a></li>\n'

index_content += "</ul>"

# Générer la page d'accueil
with open(f"{SITE_DIR}/index.html", "w", encoding="utf-8") as f:
    f.write(index_content)

print("✅ Site généré avec succès !")
