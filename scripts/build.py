import os
import subprocess

ARTICLES_DIR = "articles"
SITE_DIR = "site"
TEMPLATE_FILE = "templates/article_template.html"

os.makedirs(SITE_DIR, exist_ok=True)

# Charger le template HTML principal
with open(TEMPLATE_FILE, "r") as f:
    template = f.read()

# Lister tous les fichiers Markdown
md_files = [f for f in os.listdir(ARTICLES_DIR) if f.endswith(".md")]

# Stocker le HTML de tous les articles pour la home
articles_html_for_index = []

for md_file in md_files:
    md_path = os.path.join(ARTICLES_DIR, md_file)
    html_filename = md_file.replace(".md", ".html")
    html_path = os.path.join(SITE_DIR, html_filename)

    # Titre d’article propre
    title = md_file.replace(".md", "").replace("-", " ").title()

    # Convertir Markdown -> HTML
    result = subprocess.run(
        ["pandoc", md_path, "-t", "html"],
        capture_output=True,
        text=True
    )
    html_content = result.stdout

    # --- Vue individuelle de l’article ---
    final_html = (
        template
        .replace("{{ title }}", title)
        .replace("{{ content }}", html_content)
    )

    with open(html_path, "w") as f:
        f.write(final_html)

    # --- Extrait pour la page d’accueil ---
    preview_html = f"""
    <article class="bg-neutral-900 border border-neutral-800 rounded-lg p-6">
        <h2 class="text-2xl font-bold text-white mb-3">
            <a href="{html_filename}">{title}</a>
        </h2>
        <div class="text-neutral-500 prose max-w-none mb-4">
            {html_content[:400]}...
        </div>
        <a href="{html_filename}" class="inline-block bg-neutral-500 text-white px-4 py-2 rounded-lg">
            Lire la suite →
        </a>
    </article>
    """

    articles_html_for_index.append(preview_html)

# --- Générer la page d’accueil ---
index_content = "\n".join(articles_html_for_index)

# Remplacer dans le template
index_html = (
    template
    .replace("{{ title }}", "Blog-IT")
    .replace("{{ content }}", index_content)
)

with open(os.path.join(SITE_DIR, "index.html"), "w") as f:
    f.write(index_html)

print("✅ Site généré avec style Tailwind ! Les articles apparaissent sur la home.")
