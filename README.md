# Blog-IT 🖥️

Bienvenue sur **Blog-IT**, un blog collaboratif low-code pour partager des articles IT et tech.

---

## 🔹 À propos du projet

**Blog-IT** est un site statique généré automatiquement à partir d’articles écrits en **Markdown**.  
Chaque nouvel article ajouté dans le dossier `articles/` est converti en page HTML grâce à **Python** et **Pandoc**, et stylé avec **TailwindCSS** et un CSS personnalisé.

### 🔧 Technologies utilisées
- **Markdown** : pour rédiger facilement les articles.
- **Python & Pandoc** : conversion Markdown → HTML.
- **TailwindCSS** : mise en page et style moderne.
- **GitHub Actions** : automation pour générer et déployer le site.
- **GitHub Pages** : hébergement du site statique.

### ⚡ Comment ça fonctionne
1. Vous ajoutez un fichier Markdown dans `articles/`.
2. Vous créez une **pull request** sur GitHub.
3. GitHub Actions détecte votre PR et exécute le script `build.py` :
   - Convertit le Markdown en HTML.
   - Génère une page individuelle pour votre article.
   - Met à jour la page d’accueil avec un aperçu de votre article.
4. Si tout est correct, votre PR peut être mergée, et votre article apparaît automatiquement sur le site en ligne.

## Comment contribuer

C’est très simple ! Suivez ces étapes :

### 1️⃣ Ajouter un nouvel article
- Allez dans le dossier `articles/` du dépôt GitHub.
- Cliquez sur **Add file → Create new file**.
- Nommez votre fichier avec `.md`, par exemple :
- Cliquez sur Commit changes

mon-article.md

- Écrivez votre article en **Markdown**. Exemple :
```markdown
# Titre de l'article

Votre texte ici...

## Sous-titre

Plus de texte...

*Écrit par Votre Nom*
📅 Novembre 2025
💡 #tag #autreTag

```

2️⃣ Automatisation

Dès que votre Commit est créée :

Le site est automatiquement mis à jour.
Votre article apparaît sur la page d’accueil.
Les lecteurs peuvent cliquer pour lire l’article complet.
Votre article apparaît sur la page d’accueil.
Les lecteurs peuvent cliquer pour lire l’article complet.
