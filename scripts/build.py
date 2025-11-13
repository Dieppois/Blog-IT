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

# Stocker le HTML des cards pour la page d'accueil
cards_html = []

for md_file in md_files:
    md_path = os.path.join(ARTICLES_DIR, md_file)
    html_filename = md_file.replace(".md", ".html")
    html_path = os.path.join(SITE_DIR, html_filename)

    # Titre de l’article (nom du fichier propre)
    title = md_file.replace(".md", "").replace("-", " ").title()

    # Convertir Markdown -> HTML
    result = subprocess.run(
        ["pandoc", md_path, "-t", "html"],
        capture_output=True,
        text=True
    )
    html_content = result.stdout.strip()

    # 🔹 Générer la page individuelle de l’article
    article_html = template.replace(
        "{{ title }}", title
    ).replace(
        "{{ content }}", f"<articles class='prose prose-invert max-w-none'>{html_content}</articles>"
    )

    with open(html_path, "w") as f:
        f.write(article_html)

    # 🔹 Créer la card pour la home
    # Extrait tronqué du Markdown converti en HTML (par exemple 200 caractères)
    snippet = html_content[:200] + "..." if len(html_content) > 200 else html_content

    card_html = f"""
    <div class="bg-[#171717] border border-neutral-800 rounded-lg p-6 hover:border-neutral-700 transition">
        <h2 class="text-lg font-medium text-white">{title}</h2>
        <div class="text-[#a1a1a1] my-3">{snippet}</div>
        <a href="{html_filename}" class="inline-block bg-[#e5e5e5] text-black px-4 py-2 rounded-lg font-semibold hover:bg-white transition">
            Lire la suite →
        </a>
    </div>
    """
    cards_html.append(card_html)

# 🔹 Générer la page d'accueil
index_content = "\n".join(cards_html)

index_html = template.replace(
    "{{ title }}", "Blog-IT"
).replace(
    "{{ content }}", index_content
)

with open(os.path.join(SITE_DIR, "index.html"), "w") as f:
    f.write(index_html)

print("✅ Site généré : page d'accueil avec cards et pages individuelles pour chaque article !")
