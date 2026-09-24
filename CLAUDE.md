# Boutique melkanova.com — méthode pour créer une page produit

L'utilisateur est débutant en code : répondre en français, simplement, et expliquer ce qui est fait.
La page ReliefRoll (`theme-sense/`) est la référence validée par l'utilisateur (« copywriting 9/10 ») :
chaque nouvelle page produit doit atteindre ce niveau et suivre ce process.

## Contexte boutique
- Thème en ligne : **Sense** (couleurs : turquoise `#1BC7C2`, noir ; police Avenir Next). Marché FR, prix en €.
- Connecteur Shopify : pas d'écriture sur le thème en ligne (MAIN) et pas de publication de thème → toujours
  travailler sur une **copie** (`themeDuplicate`), puis l'utilisateur publie lui-même.
- Le `templates/product.json` par défaut de Sense a sa section `main` **désactivée** (les anciennes pages passent
  par PageFly / PagePilot). Ne jamais basculer un produit vers un template qui n'existe pas sur le thème en ligne.
- Thème copie actuel : « Sense – ReliefRoll LP » (`gid://shopify/OnlineStoreTheme/182913794371`).

## Les sections réutilisables (déjà dans la copie du thème)
Les 10 sections `rr-*` + `assets/reliefroll.css` + snippets `rr-icon`, `rr-media`, `rr-stars` sont génériques.
Pour un nouveau produit : **réutiliser ces sections** et créer seulement `templates/product.<nom>.json`
(si on travaille sur une nouvelle copie du thème, recopier aussi ces fichiers).

## Process (dans cet ordre)
1. **Comprendre le produit** : fiche Shopify (titre, prix, prix barré, photos, description fournisseur),
   page existante éventuelle (PageFly) pour reprendre l'angle et les vrais avis.
2. **Choisir UN angle** : un public précis + un moment précis + une douleur concrète
   (ReliefRoll : dos raide au réveil, 10 min assis au bord du lit, public 55+).
3. **Structure de page (14 blocs)** :
   bloc d'achat (sur-titre, H1 FR, étoiles → #avis, prix, 4 bénéfices, économie, bouton, date de livraison,
   3 badges, logos paiement, mini-avis, onglets Caractéristiques / Dans la boîte / Livraison / Garantie)
   → bandeau défilant → Problème (liste rouge + phrase choc) → Solution → 6 bénéfices en cartes
   → 3 étapes → section « objection / moment » sur fond foncé → comparatif (vs 4 alternatives)
   → transformation (ce qu'on refait) → avis → garantie → FAQ (8-9 questions dont contre-indications)
   → offre finale avec bouton → barre d'achat collante.
4. **Copywriting** : vouvoiement, phrases courtes, scènes concrètes du quotidien, « Ce n'est pas votre faute »,
   mots-clés colorés via `<em>` dans les titres, boutons à la 1re personne (« Je veux… », « Je commande… »).
5. **Images** : chaque emplacement a un repère (A1, A2, B1…B6, C1…C3, D1, E1, F1) et, en attendant,
   une photo produit par défaut (réglage `fallback`). Ensuite, fournir un prompt ChatGPT par repère,
   en précisant si la photo du produit doit être jointe et le format (portrait / carré / paysage).
   **Règle d'or des images (validée par l'utilisateur)** : chaque image doit être au moins l'une de ces 3 choses,
   idéalement plusieurs : **éducative** (montre comment ça marche / l'invisible, ex. muscle sous la peau),
   **relatable** (scène où le client se reconnaît, ex. enfiler ses chaussures en retenant son souffle),
   **très émotionnelle** (ex. grand-mère qui accueille sa petite-fille en courant dans le jardin = référence E1).
   Interdit : images décoratives (produit sur une table, dans un tiroir, réveil seul) et **packshot / boîte
   près des boutons d'achat** — ça casse l'émotion. Les packshots vont uniquement dans la galerie produit.
   L'image de l'offre finale doit **boucler l'histoire** en reprenant la scène du problème (A1), résolue.
6. **Vérifier avant de livrer** : retélécharger les fichiers envoyés et les comparer au local,
   lancer Theme Check (`@shopify/theme-check-node`) sur les fichiers `rr-*`.
7. **Mise en ligne** : l'utilisateur publie la copie, PUIS on assigne le template au produit (`templateSuffix`).

## Pièges déjà rencontrés
- Nom de section / preset / bloc dans un schema : **25 caractères max**.
- Les blocs « Custom Liquid » n'ont pas accès à l'objet `section` (pas de `section.id`) ; `render` fonctionne.
- Pas de filtres dans les paramètres nommés d'un filtre (`alt: x | default: y` interdit → faire un `assign` avant).
- Une URL vide (`""`) dans un réglage de type `url` fait échouer le template → ne pas mettre la clé.
- Le réseau du sandbox bloque melkanova.com et cdn.shopify.com : impossible de voir la page ou les photos,
  le dire à l'utilisateur et lui demander une capture.

## Honnêteté (obligatoire)
- Avis : uniquement des vrais avis, avec mention de leur origine. Jamais d'avis inventés (illégal en France).
- Pas d'allégation invérifiable (ex. « Certifié CE », chiffres de ventes) sans preuve de l'utilisateur.
- Pas de promesse médicale ; FAQ avec contre-indications et « ne remplace pas un avis médical ».
- Signaler à l'utilisateur tout ce qui a été supposé (contenu de la boîte, délais, garantie).
