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

# Stocker le HTML des previews pour la home
articles_html_for_index = []

for md_file in md_files:
    md_path = os.path.join(ARTICLES_DIR, md_file)
    html_filename = md_file.replace(".md", ".html")
    html_path = os.path.join(SITE_DIR, html_filename)

    # Titre de l'article (propre)
    title = md_file.replace(".md", "").replace("-", " ").title()

    # Convertir Markdown → HTML
    result = subprocess.run(
        ["pandoc", md_path, "-t", "html"],
        capture_output=True,
        text=True
    )
    html_content = result.stdout.strip()

    # --- Page individuelle ---
    final_html = template.replace(
        "{{ title }}", title
    ).replace(
        "{{ content }}", f"<article class='custom-article bg-[#171717] col-span-full mt-12 border border-neutral-800 rounded-2xl p-6 max-w-4xl mx-auto'>{html_content}</article>"
    )

    with open(html_path, "w") as f:
        f.write(final_html)

    # --- Générer preview pour la home ---
    snippet = html_content[:200] + "..." if len(html_content) > 200 else html_content

    preview_html = f"""
    <div class="bg-[#171717] border border-neutral-800 rounded-2xl p-6 hover:border-[#ff6900] transition">
        <h2 class="text-xl font-bold text-white mb-3">{title}</h2>
        <div class="text-[#a1a1a1] overflow-hidden max-h-40">
            {snippet}
        </div>
        <a href="{html_filename}" class="inline-block bg-[#e5e5e5] text-black px-4 py-2 rounded-lg mt-4 font-semibold hover:bg-white transition">
            Lire la suite →
        </a>
    </div>
    """
    articles_html_for_index.append(preview_html)

    # --- Générer la home page ---
    index_content = "\n".join(articles_html_for_index)

    index_html = template.replace(
        "{{ title }}", "Blog-IT"
    ).replace(
        "{{ content }}", index_content
    )

    with open(os.path.join(SITE_DIR, "index.html"), "w") as f:
        f.write(index_html)

    print("✅ Site généré ! Home avec cards et pages articles individuelles.")
