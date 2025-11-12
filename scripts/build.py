import os
import subprocess

# Dossiers
ARTICLES_DIR = "articles"
SITE_DIR = "site"
TEMPLATE_FILE = "templates/article_template.html"

# Crée le dossier site si nécessaire
os.makedirs(SITE_DIR, exist_ok=True)

# Lister tous les fichiers Markdown
md_files = [f for f in os.listdir(ARTICLES_DIR) if f.endswith(".md")]

# Stocker les liens pour index.html
article_links = []

for md_file in md_files:
    md_path = os.path.join(ARTICLES_DIR, md_file)
    html_filename = md_file.replace(".md", ".html")
    html_path = os.path.join(SITE_DIR, html_filename)

    # Convertir Markdown en HTML brut avec Pandoc
    result = subprocess.run(
        ["pandoc", md_path, "-t", "html"],
        capture_output=True,
        text=True
    )
    html_content = result.stdout

    # Lire le template
    with open(TEMPLATE_FILE, "r") as f:
        template = f.read()

    # Insérer le contenu de l'article dans le template
    final_html = template.replace("{{ content }}", html_content)

    # Sauvegarder le HTML final
    with open(html_path, "w") as f:
        f.write(final_html)

    # Ajouter le lien pour index.html
    title = md_file.replace(".md", "").replace("-", " ").title()
    article_links.append(f'<li><a href="{html_filename}">{title}</a></li>')

# Générer index.html
index_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Blog-IT</title>
</head>
<body>
    <h1>Blog-IT</h1>
    <ul>
        {''.join(article_links)}
    </ul>
</body>
</html>
"""

with open(os.path.join(SITE_DIR, "index.html"), "w") as f:
    f.write(index_html)

print("✅ Site généré avec succès !")
