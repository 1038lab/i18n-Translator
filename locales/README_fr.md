# GitHub i18n Actions Traduction automatique

## 🌍 Langues disponibles

| 🌐 Langue | 📄 Fichier | 📊 Statut |
|:-----------|:--------|:----------|
| Anglais | [README_en.md](./README_en.md) | ✅ Disponible |
| Anglais | [README_en.md](./README_en.md) | ✅ Disponible |
| Chinois (中文) | [README_zh.md](./README_zh.md) | ✅ Disponible |
| Japonais (日本語) | [README_ja.md](./README_ja.md) | ✅ Disponible |
| Coréen (한국어) | [README_ko.md](./README_ko.md) | ✅ Disponible |
| Espagnol (Español) | [README_es.md](./README_es.md) | ✅ Disponible |
| Français (Français) | [README_fr.md](./README_fr.md) | ✅ Disponible |
| Russe (Русский) | [README_ru.md](./README_ru.md) | ✅ Disponible |

## 📋 **Aperçu**

Ce guide vous aidera à configurer rapidement un système de traduction automatique d'actions GitHub à l'aide de nos outils fournis pour traduire automatiquement les fichiers anglais README.md en plusieurs langues.

**🆓 Nous proposons désormais deux modes de traduction :**
- **Mode libre** (recommandé) - Aucune configuration, pas besoin de clé API
- **Mode API** - Précision accrue avec Google Translate API (nécessite la clé API)

### **Fonctionnalités**
- ✅ **Deux modes de traduction** : Gratuit (sans configuration) et API (haute qualité)
- ✅ Détection automatique des mises à jour de README.md et déclenchement de la traduction
- ✅ Prise en charge de plusieurs langues cibles (chinois, japonais, coréen, espagnol, etc.)
- ✅ Protection des termes techniques contre la traduction
- ✅ Maintien du formatage Markdown complet
- ✅ Gestion sécurisée des clés API (mode API uniquement)
- ✅ Traduction incrémentale (ne traduit que le contenu mis à jour)
- ✅ Navigation linguistique intuitive
- ✅ Interrupteur marche/arrêt pour économiser sur les coûts de API
- ✅ Protection intelligente contre l'écrasement (4 modes)
- ✅ Détection et protection des modifications manuelles
- ✅ Déclenchement manuel du flux de travail avec options de forçage

---

## 🆓 **Démarrage rapide (mode gratuit - recommandé)**

### **Étape 1 : Copier les fichiers du projet**
Copiez les fichiers suivants du projet [i18n](https://github.com/1038lab/i18n) vers votre projet :

```
your-project/
├── .github/
│   ├── i18n-config.yml                    # Configuration file
│   ├── workflows/
│   │   ├── translate-readme-api.yml       # API mode workflow
│   │   └── translate-readme-free.yml      # Free mode workflow (default)
│   └── scripts/
│       ├── translate_readme_api.py        # API translation script
│       └── translate_readme_free.py       # Free translation script
└── README.md                              # Your English README
```

### **Étape 2 : Exécuter la traduction gratuite**
1. Dans votre dépôt GitHub, cliquez sur l'onglet **Actions**.
2. Sélectionnez le flux de travail **Traduction automatique README (gratuite)**.
3. Cliquez sur **Exécuter le flux de travail** → Sélectionnez la branche `main` → Cliquez sur **Exécuter le flux de travail**.
4. Attendez la fin de l'opération et vérifiez si le dossier `locales/` contient des fichiers traduits.

**🎉 C'est tout ! Pas besoin de clé API.**

---

## 💰 **Mise à niveau vers le mode API (facultatif - qualité supérieure)**

Si vous souhaitez une précision de traduction plus élevée, vous pouvez passer au mode API :

## 🚀 **Étape 1 : Configurer Google Cloud Translation API**

### **1.1 Créer un projet Google Cloud**
1. Accédez à [Google Cloud Console](https://console.cloud.google.com/)
2. Cliquez sur le sélecteur de projet et créez un nouveau projet.
3. Saisissez le nom du projet (par exemple, `readme-translator`).
4. Cliquez sur « Créer ».

### **1.2 Activer la traduction API**
1. Dans Google Cloud Console, assurez-vous d'avoir sélectionné le bon projet.
2. Recherchez « Cloud Translation API » dans la barre de recherche.
3. Cliquez sur le résultat « Cloud Translation API ».
4. Cliquez sur le bouton « Activer ».
5. Attendez que API soit activé.

### **1.3 Créer une clé API**
1. Accédez à « API et services » → « Identifiants »
2. Cliquez sur « Créer des identifiants » → « Clé API »
3. Copiez la clé API générée (format : `AIzaSyC...`)
4. **Important** : Enregistrez cette clé immédiatement ; vous en aurez besoin ultérieurement.

### **1.4 Restreindre les autorisations de la clé API (recommandé)**
1. Sur la page « Identifiants », cliquez sur la clé API que vous venez de créer.
2. Dans la section « Restrictions API » :
- Sélectionnez « Restreindre la clé ».
- Cochez « Cloud Translation API ».
3. Cliquez sur « Enregistrer ».

---

## 🔐 **Étape 2 : Configurer API Saisissez GitHub**

### **2.1 Définir le secret du dépôt**
1. Dans votre dépôt GitHub, cliquez sur l'onglet **Paramètres**
2. Dans le menu de gauche, sélectionnez **Secrets et variables** → **Actions**
3. Cliquez sur **Nouveau secret du dépôt**
4. Renseignez les informations suivantes :
- **Nom** : `GOOGLE_TRANSLATE_API_KEY`
- **Secret** : Collez la clé API obtenue à l'étape 1.3
5. Cliquez sur **Ajouter un secret**

### **2.2 Vérifier la configuration du secret**
Après la configuration, vous devriez voir dans la liste des secrets :
```
GOOGLE_TRANSLATE_API_KEY    Updated now
```

---

## 📁 **Étape 3 : Passer en mode API**

### **3.1 Mettre à jour la configuration**
Ouvrez `.github/i18n-config.yml` et modifiez le mode :

```yaml
translation:
  mode: "api"  # Change from "free" to "api"
```

### **3.2 Descriptions des fichiers**
- **`i18n-config.yml`** - Fichier de configuration de traduction, contrôle des langues, protection des termes, etc.
- **`translate-readme-api.yml`** - Fichier de workflow d'actions en mode API et GitHub
- **`translate-readme-free.yml`** - Fichier de workflow d'actions en mode libre GitHub
- **`translate_readme_api.py`** - Script de traduction API
- **`translate_readme_free.py`** - Script de traduction libre

---

## ⚙️ **Étape 4 : Configurer les paramètres de traduction**

### **4.1 Modifier le fichier de configuration**
Ouvrez le fichier `.github/i18n-config.yml` et modifiez-le selon vos besoins :

#### **Choisir le mode de traduction**
```yaml
translation:
  enabled: true           # Set to false to disable translation
  mode: "free"           # "free" (no API key) or "api" (higher quality)
```

#### **Sélectionner les langues cibles**
```yaml
enabled_languages:
  - en    # English (always enabled)
  - zh    # Chinese
  - ja    # Japanese
  - ko    # Korean
  # - es  # Spanish - comment out languages you don't need
  # - fr  # French
  # - ru  # Russian
```

#### **Ajouter des conditions spécifiques au projet**
```yaml
protected_terms:
  # Add your project terms at the end of the list
  - "YourProjectName"
  - "YourSpecialFeature"
  - "YourAPI"
```

#### **Paramètres du mode Écraser**
```yaml
translation:
  overwrite_mode: "auto"  # Smart overwrite mode
  # Options: "always", "never", "auto", "create_new"
```

### **4.2 Explication de la configuration**
- **`enabled`** : Active ou non la traduction automatique
- **`mode`** : Mode de traduction - `"free"` (sans clé API) ou `"api"` (qualité supérieure)
- **`enabled_languages`** : Liste des langues cibles à traduire
- **`protected_terms`** : Liste des termes à ne pas traduire
- **`output_dir`** : Répertoire de sortie des fichiers de traduction (par défaut : `locales`)
- **`overwrite_mode`** : Mode d'écrasement
- `"always"` : Toujours écraser les traductions existantes
- `"never"` : Ne jamais écraser les traductions existantes
- `"auto"` : Écrasement intelligent (recommandé)
- `"create_new"` : Créer de nouveaux fichiers avec le suffixe de date

### **4.3 Comparaison des modes**

| Fonctionnalité | Mode gratuit | Mode API |
|---------|-----------|----------|
| **Clé API** | ❌ Non nécessaire | ✅ Requis |
| **Coût** | 🆓 Entièrement gratuit | 💰 Paiement à l'utilisation |
| **Qualité de traduction** | ⭐⭐⭐⭐ Bonne | ⭐⭐⭐⭐⭐ Excellente |
| **Stabilité** | ⭐⭐⭐ Modérée | ⭐⭐⭐⭐⭐ Très stable |
| **Difficulté d'installation** | ⭐⭐⭐⭐⭐ Aucune configuration | ⭐⭐ Configuration API requise |

---

## 🧪 **Étape 5 : Tester le système de traduction**

### **5.1 Fichiers de validation**
```bash
git add .github/
git commit -m "Add auto-translation system"
git push origin main
```

### **5.2 Test de déclenchement manuel**

**Pour le mode gratuit** :
1. Dans votre dépôt GitHub, cliquez sur l'onglet **Actions**
2. Sélectionnez le flux de travail **Traduction automatique README (gratuit)**
3. Cliquez sur le bouton **Exécuter le flux de travail**
4. Sélectionnez la branche `main`
5. Cliquez sur le bouton vert **Exécuter le flux de travail**

**Pour le mode API** :
1. Sélectionnez plutôt le flux de travail **« Traduction automatique README (API) »**.
2. Suivez les mêmes étapes que ci-dessus.

### **5.3 Surveiller l'exécution**
1. Cliquez sur l'instance de workflow en cours d'exécution.
2. Cliquez sur la tâche `translate`.
3. Développez chaque étape pour afficher les journaux d'exécution.
4. Vérifiez les éventuels messages d'erreur.

### **5.4 Vérification des résultats**
Une fois l'opération terminée, vous devriez voir les nouveaux fichiers générés dans votre dépôt :
```
locales/
├── README_en.md    # English version (for completeness)
├── README_zh.md    # Chinese version
├── README_ja.md    # Japanese version
└── README_ko.md    # Korean version (if enabled)
```

**Remarque** : le dossier `locales/` est automatiquement créé lors de la première traduction.

---

## 🔄 **Étape 6 : Flux de travail automatisé**

### **6.1 Déclenchement automatique**
Le système exécutera automatiquement la traduction dans les cas suivants :
- Lorsque vous mettez à jour le fichier `README.md` et le transférez vers la branche `main`
- La retraduction ne se fait que lorsque le fichier source est plus récent que les fichiers de traduction (traduction incrémentale)

### **6.2 Résultats de la traduction**
Chaque fichier de traduction contient :
- 🌍 **Tableau de navigation linguistique élégant** - Avec des icônes de drapeau pour faciliter le changement de langue
- 📝 **Contenu traduit** - Conserve la mise en forme et les blocs de code d'origine
- 🔗 **Informations de pied de page localisées** - Contient des notes de traduction et des liens vers des projets
- 🛡️ **Protection contre les modifications manuelles** - Détecte et protège automatiquement les modifications des utilisateurs

---

## 💡 **Conseils d'utilisation**

### **🎛️ Contrôle de traduction**

#### **Arrêt complet vs Contrôle d'écrasement**

Il existe deux manières différentes de contrôler le système de traduction :

**1. Arrêter complètement la traduction automatique :**
```yaml
translation:
  enabled: false                     # Stops all translation activity
```
- ✅ Les actions GitHub s'exécutent, mais se terminent immédiatement.
- ✅ Aucun appel API n'est effectué (économies pour le mode API).
- ✅ Aucun fichier n'est créé ni mis à jour.

**2. Écrasement du fichier de contrôle :**
```yaml
translation:
  overwrite_mode: "never"            # Controls file overwrite behavior
```
- ✅ GitHub Les actions continueront d'être exécutées
- ✅ Créera de nouveaux fichiers de traduction s'ils n'existent pas
- ❌ Ne mettra PAS à jour les fichiers de traduction existants

**3. Forcer la traduction (déclenchement manuel) :**
Les deux workflows prennent en charge l'option `force_translate` en cas de déclenchement manuel :
- Définissez `true` pour remplacer le paramètre `enabled: false`
- Utile pour les traductions ponctuelles sans modification de la configuration

#### **Comparaison du mode d'écrasement**

| Mode | Déclenchement automatique | Écraser les fichiers existants | Créer de nouveaux fichiers |
|------|-------------|-------------------|------------------|
| `enabled: false` | ❌ Le script se termine | ❌ | ❌ |
| `overwrite_mode: "never"` | ✅ S'exécute | ❌ Ignorer les fichiers existants | ✅ Crée un nouveau fichier |
| `overwrite_mode: "auto"` | ✅ S'exécute | 🤔 Détection intelligente | ✅ Crée un nouveau fichier |
| `overwrite_mode: "always"` | ✅ S'exécute | ✅ Écrase toujours | ✅ Crée un nouveau fichier |

### **Économisez API (Mode API)**
1. **Utiliser le mode gratuit** : Définissez `mode: "free"` pour un coût nul
2. **Désactiver la traduction** : Définissez `enabled: false` dans `i18n-config.yml`
3. **Réduire le nombre de langues** : Activez uniquement les langues dont vous avez réellement besoin
4. **Traduction incrémentielle** : Le système traduit automatiquement uniquement le contenu mis à jour

### **Protection des termes personnalisés**
Ajouter à `protected_terms` :
- Noms de projets
- Noms de fonctionnalités spéciales
- Noms de points de terminaison API
- Noms de marques

### **Protéger les modifications manuelles**
Ajouter des marqueurs aux fichiers de traduction pour protéger les modifications manuelles :
```markdown
<!-- MANUAL EDIT -->
This content will not be overwritten by auto-translation
```

### **Contrôle de la qualité des traductions**
- **Mode gratuit** : Convient à la plupart des cas d'utilisation, entièrement gratuit
- **Mode API** : Précision accrue pour les projets professionnels
- Vérification régulière des résultats de traduction
- Ajustement des termes protégés si nécessaire
- Correction manuelle des fichiers de traduction si nécessaire

---

## 🛠️ **Dépannage**

### **Problèmes courants**

#### **Erreur de clé API**
```
Error: API connection failed: 403 Forbidden
```
**Solution** : Vérifiez que la clé API est correctement définie et dispose des autorisations suffisantes.

#### **Traduction ignorée**
```
Skipping zh: locales/README_zh.md is up to date
```
**Explication** : Il s'agit d'un comportement normal de traduction incrémentielle. Le fichier source n'a pas été mis à jour.

#### **Traduction désactivée**
```
Translation is disabled in configuration
```
**Solution** : Définissez `enabled: true` dans `i18n-config.yml` ou utilisez le déclencheur manuel avec `force_translate: true`

#### **Mauvais workflow sélectionné**
**Problème** : Utilisation du workflow API sans la clé API ou inversement
**Solution** :
- Pour le mode gratuit : utilisez le workflow « Traduction automatique README (gratuit) »
- Pour le mode API : utilisez le workflow « Traduction automatique README (API) » et assurez-vous que la clé API est définie

### **Obtenir de l'aide**
- Afficher [project documentation](https://github.com/1038lab/i18n)
- Envoyer un [Issue](https://github.com/1038lab/i18n/issues)
- Consulter les journaux d'exécution des actions

---

## 🎉 **Terminé !**

Votre projet dispose désormais d'une fonctionnalité de traduction automatique ! À chaque mise à jour de README.md, le système génère automatiquement des versions multilingues, rendant votre projet plus accessible aux utilisateurs internationaux.

---

> 🌐 Ce guide est fourni par le projet [i18n](https://github.com/1038lab/i18n)


---
> 🌐 Ce document a été traduit automatiquement avec Google Translate. Consultez la [version anglaise](./README_en.md) pour plus de précision | Outil: [i18n](https://github.com/1038lab/i18n)

<!-- AUTO-GENERATED TRANSLATION - To prevent overwriting, add "MANUAL EDIT" comment anywhere in this file -->