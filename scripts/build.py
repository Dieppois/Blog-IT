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

    # Titre de l’article (nom du fichier propre)
    title = md_file.replace(".md", "").replace("-", " ").title()

    # Convertir Markdown → HTML
    result = subprocess.run(
        ["pandoc", md_path, "-t", "html"],
        capture_output=True,
        text=True
    )
    html_content = result.stdout.strip()

    # 🔹 Créer la page individuelle de l’article
    final_html = (
        template
        .replace("{{ title }}", title)
        .replace("<articles></articles>", f"<articles>{html_content}</articles>")
    )

    with open(html_path, "w") as f:
        f.write(final_html)

    # 🔹 Générer un aperçu (les 400 premiers caractères)
    snippet = html_content[:400] + "..." if len(html_content) > 400 else html_content

    preview_html = f"""
    <article class="bg-[#171717] border border-neutral-800 rounded-2xl p-6 hover:border-neutral-700 transition">
        <h2 class="text-2xl font-bold text-white mb-3">
            <a href="{html_filename}" class="hover:text-gray-300 transition">{title}</a>
        </h2>
        <div class="text-[#a1a1a1] overflow-hidden max-h-40">
            {snippet}
        </div>
        <a href="{html_filename}" class="inline-block bg-[#e5e5e5] text-black mt-4 px-4 py-2 rounded-lg font-semibold hover:bg-white transition">
            Lire la suite →
        </a>
    </article>
    """

    articles_html_for_index.append(preview_html)

# --- Générer la page d’accueil ---
index_content = "\n".join(articles_html_for_index)

index_html = (
    template
    .replace("{{ title }}", "Blog-IT")
    .replace("<articles></articles>", f"<articles>\n{index_content}\n</articles>")
)

with open(os.path.join(SITE_DIR, "index.html"), "w") as f:
    f.write(index_html)

print("✅ Site généré : tous les articles Markdown ont été convertis et stylés via <articles> !")
