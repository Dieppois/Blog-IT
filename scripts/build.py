import os
import shutil
import subprocess

ARTICLES_DIR = "articles"
SITE_DIR = "site"
CSS_DIR = "css"
TEMPLATE_FILE = "templates/article_template.html"

# -------------------------------------------------
# 1️⃣ Préparation des dossiers
# -------------------------------------------------

os.makedirs(SITE_DIR, exist_ok=True)

# Copier le dossier CSS → site/css
DEST_CSS = os.path.join(SITE_DIR, "css")
if os.path.exists(DEST_CSS):
    shutil.rmtree(DEST_CSS)
shutil.copytree(CSS_DIR, DEST_CSS)

# Charger le template HTML général
with open(TEMPLATE_FILE, "r") as f:
    template = f.read()

# Récupérer tous les fichiers .md
md_files = [f for f in os.listdir(ARTICLES_DIR) if f.endswith(".md")]

# Conteneur pour les cards de la home
articles_cards = []

# -------------------------------------------------
# 2️⃣ Génération des pages articles
# -------------------------------------------------

for md_file in md_files:

    md_path = os.path.join(ARTICLES_DIR, md_file)
    html_filename = md_file.replace(".md", ".html")
    html_path = os.path.join(SITE_DIR, html_filename)

    # Titre basé sur le nom du fichier
    title = md_file.replace(".md", "").replace("-", " ").title()

    # Convertir Markdown → HTML
    result = subprocess.run(
        ["pandoc", md_path, "-t", "html"],
        capture_output=True,
        text=True
    )

    html_content = result.stdout.strip()

    # Page article individuelle
    article_html = template.replace(
        "{{ title }}", title
    ).replace(
        "{{ content }}",
        f"<articles class='prose prose-invert max-w-4xl mx-auto'>{html_content}</articles>"
    )

    with open(html_path, "w") as f:
        f.write(article_html)

    # -------------------------------------------------
    # 3️⃣ Création de la card pour la page d'accueil
    # -------------------------------------------------

    snippet = html_content[:250] + "..." if len(html_content) > 250 else html_content

    card = f"""
    <div class="bg-[#171717] border border-neutral-800 rounded-xl p-6 hover:border-[#ff6900] transition">
        <h2 class="text-xl font-medium text-white mb-3">{title}</h2>
        <p class="text-[#a1a1a1] mb-4">{snippet}</p>
        <a href="{html_filename}" class="inline-block bg-[#e5e5e5] text-black px-4 py-2 rounded-lg font-semibold hover:bg-white transition">
            Lire la suite →
        </a>
    </div>
    """

    articles_cards.append(card)

# -------------------------------------------------
# 4️⃣ Génération de la page d'accueil index.html
# -------------------------------------------------

index_content = "\n".join(articles_cards)

index_html = template.replace(
    "{{ title }}", "Blog IT"
).replace(
    "{{ content }}",
    f"""
    <section class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {index_content}
    </section>
    """
)

with open(os.path.join(SITE_DIR, "index.html"), "w") as f:
    f.write(index_html)

print("✅ Site généré avec succès ! CSS copié, articles convertis, cards créées.")
