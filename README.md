# Landing page ReliefRoll™ (thème Shopify Sense)

Fichiers ajoutés au thème **« Sense – ReliefRoll LP »** (copie non publiée de Sense, boutique melkanova.com).
Le dossier `theme-sense/` reproduit exactement l'arborescence du thème Shopify.

## Ce qui a été créé

| Fichier | Rôle |
|---|---|
| `templates/product.reliefroll.json` | Le template produit : ordre des sections + tous les textes |
| `assets/reliefroll.css` | Le design commun à toutes les sections (couleurs, boutons, cartes…) |
| `snippets/rr-icon.liquid` | Les icônes |
| `snippets/rr-media.liquid` | Affiche une image, sinon une photo du produit, sinon un emplacement gris étiqueté |
| `snippets/rr-stars.liquid` | Les étoiles de notation |
| `sections/rr-*.liquid` | 10 sections réutilisables, modifiables dans l'éditeur de thème (elles s'appellent « RR · … ») |

## Ordre de la page

1. Bloc d'achat (section produit native de Sense, restylée)
2. Bandeau défilant de réassurance
3. Problème — « Vous avez déjà tout essayé » (image **A1**)
4. Solution — « Le geste de 10 minutes » (image **A2**)
5. 6 bénéfices en cartes (images **B1 à B6**)
6. Mode d'emploi en 3 étapes (images **C1 à C3**, masquées par défaut)
7. « Pas chez le kiné » — fond foncé (image **D1**)
8. Tableau comparatif (crème, coussin, foam roller, kiné)
9. Transformation — « Ce que vous allez pouvoir refaire » (image **E1**)
10. Avis clients
11. Garantie 30 jours
12. FAQ (9 questions)
13. Offre finale avec bouton d'achat (image **F1**)
14. Barre d'achat qui reste en bas de l'écran pendant le défilement

## Changer une image

Éditeur de thème → Produits → template **reliefroll** → cliquer sur la section → « Image ».
Tant qu'aucune image n'est choisie, la section affiche la photo produit n° X (réglage « Sinon, utiliser la photo produit n° »).
Mettre ce réglage à 0 affiche l'emplacement gris avec son repère (A1, B3…).
