import os
import shutil
import subprocess

# ----------------------------
# Chemins absolus (fix GitHub Pages)
# ----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))      # /scripts
ROOT_DIR = os.path.dirname(BASE_DIR)                       # racine repo

ARTICLES_DIR = os.path.join(ROOT_DIR, "articles")
SITE_DIR = os.path.join(ROOT_DIR, "site")
TEMPLATE_FILE = os.path.join(ROOT_DIR, "templates/article_template.html")

CSS_SRC = os.path.join(ROOT_DIR, "css")
CSS_DST = os.path.join(SITE_DIR, "css")

# ----------------------------
# Préparation du dossier site/
# ----------------------------
os.makedirs(SITE_DIR, exist_ok=True)

# Copier le CSS proprement
if os.path.exists(CSS_DST):
    shutil.rmtree(CSS_DST)

shutil.copytree(CSS_SRC, CSS_DST)

# Charger le template
with open(TEMPLATE_FILE, "r") as f:
    template = f.read()

# Lister fichiers .md
md_files = sorted([f for f in os.listdir(ARTICLES_DIR) if f.endswith(".md")])

articles_html_for_index = []

# ----------------------------
# Traitement des articles
# ----------------------------
for md_file in md_files:

    md_path = os.path.join(ARTICLES_DIR, md_file)
    html_filename = md_file.replace(".md", ".html")
    html_path = os.path.join(SITE_DIR, html_filename)

    title = md_file.replace(".md", "").replace("-", " ").title()

    # Convertir Markdown via Pandoc
    result = subprocess.run(
        ["pandoc", md_path, "-t", "html"],
        capture_output=True,
        text=True
    )
    html_content = result.stdout.strip()

    # Générer page article
    full_article_html = template.replace(
        "{{ title }}", title
    ).replace(
        "{{ content }}",
        f"""
        <article class="custom-article bg-[#171717] col-span-full mt-12 border border-neutral-800 
                       rounded-2xl p-6 max-w-4xl mx-auto prose prose-invert">
            {html_content}
        </article>
        """
    )

    with open(html_path, "w") as f:
        f.write(full_article_html)

    snippet = html_content[:200] + "..." if len(html_content) > 200 else html_content

    preview_html = f"""
    <div class="bg-[#171717] border border-neutral-800 rounded-2xl p-6 hover:border-[#e5e5e5] transition">
        <h2 class="text-xl font-bold text-white mb-3">{title}</h2>
        <div class="text-[#a1a1a1] overflow-hidden max-h-40">
            {snippet}
        </div>
        <a href="{html_filename}"
           class="inline-block bg-[#e5e5e5] text-black px-4 py-2 rounded-lg mt-4 
                  font-semibold hover:bg-white transition">
            Lire la suite
        </a>
    </div>
    """

    articles_html_for_index.append(preview_html)

# ----------------------------
# Génération de la Home
# ----------------------------
index_content = "\n".join(articles_html_for_index)

index_html = template.replace(
    "{{ title }}", "Blog-IT"
).replace(
    "{{ content }}",
    f"""
    <section class="mt-12 grid lg:grid-cols-3 gap-6">
        {index_content}
    </section>
    """
)

with open(os.path.join(SITE_DIR, "index.html"), "w") as f:
    f.write(index_html)

print("✅ Site généré avec CSS chargé correctement (fix GitHub Pages).")
