# 🌽 Guide Complet - Application Détection Maladies Maïs

## 📋 Table des Matières
1. [Installation des outils](#installation)
2. [Conversion du modèle](#conversion)
3. [Test de l'application sur PC](#test-pc)
4. [Compilation de l'APK Android](#compilation)
5. [Installation sur smartphone](#installation-smartphone)
6. [Dépannage](#dépannage)

---

## 🔧 1. Installation des Outils

### Sur Linux (recommandé) ou WSL sur Windows:

```bash
# Installer Python et pip
sudo apt update
sudo apt install python3 python3-pip python3-venv

# Installer les dépendances système pour Kivy
sudo apt install -y git zip unzip openjdk-17-jdk python3-setuptools \
                    autoconf libtool pkg-config zlib1g-dev libncurses5-dev \
                    libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev

# Créer un environnement virtuel
python3 -m venv corn_env
source corn_env/bin/activate

# Installer les packages Python nécessaires
pip install --upgrade pip
pip install tensorflow pillow numpy kivy buildozer cython
```

### Sur Windows (pour test uniquement):

```bash
# Installer dans un environnement virtuel
python -m venv corn_env
corn_env\Scripts\activate

pip install tensorflow pillow numpy kivy
```

---

## 🔄 2. Conversion du Modèle TensorFlow

### Étape 1: Prépare ton modèle

Place ton modèle TensorFlow (fichier `.h5` ou dossier `SavedModel`) dans le même dossier.

### Étape 2: Exécute le script de conversion

```bash
python convert_model_to_tflite.py
```

Le script va te demander le chemin vers ton modèle. Entre par exemple:
- `mon_modele.h5` (si fichier .h5)
- `saved_model/` (si dossier SavedModel)

### Étape 3: Vérification

Après la conversion, tu devrais avoir un fichier `corn_disease_model.tflite`.
Le script affiche la taille du modèle et fait un test automatique.

**Exemple de sortie:**
```
✅ Modèle converti avec succès!
📁 Fichier: corn_disease_model.tflite
💾 Taille: 8.45 MB
🧪 Test du modèle TFLite...
📥 Input shape: [1, 224, 224, 3]
📤 Output shape: [1, 4]
🎯 Test réussi!
```

---

## 💻 3. Test de l'Application sur PC (Optionnel mais Recommandé)

Avant de compiler pour Android, teste l'app sur ton PC:

```bash
# Active l'environnement
source corn_env/bin/activate  # Linux
# ou
corn_env\Scripts\activate  # Windows

# Lance l'application
python main.py
```

**Tu devrais voir:**
- Une fenêtre avec l'interface
- Le message "✅ Modèle chargé avec succès!"
- Pouvoir charger une image et voir la prédiction

**Si erreur "Modèle non trouvé":**
- Vérifie que `corn_disease_model.tflite` est dans le même dossier que `main.py`

---

## 📱 4. Compilation de l'APK Android

### Préparation

```bash
# Structure de ton dossier:
corn_disease_app/
├── main.py
├── buildozer.spec
├── corn_disease_model.tflite
└── convert_model_to_tflite.py
```

### Compilation avec Buildozer

```bash
# Active l'environnement
source corn_env/bin/activate

# Première compilation (peut prendre 30-60 minutes)
buildozer android debug

# Les prochaines fois seront plus rapides (5-10 minutes)
```

### Que fait Buildozer?

1. ✅ Télécharge le SDK Android
2. ✅ Télécharge le NDK Android  
3. ✅ Compile Python pour Android
4. ✅ Compile Kivy pour Android
5. ✅ Compile TensorFlow Lite pour Android
6. ✅ Crée l'APK final

### Sortie finale

L'APK sera dans: `bin/corndisease-1.0-arm64-v8a-debug.apk`

---

## 📲 5. Installation sur Smartphone

### Méthode 1: USB

```bash
# Connecte ton téléphone en USB (mode développeur activé)
# Active "Débogage USB" dans les options développeur

# Installe l'APK
buildozer android deploy run

# Ou manuellement avec adb:
adb install bin/corndisease-1.0-arm64-v8a-debug.apk
```

### Méthode 2: Transfert de fichier

1. Copie le fichier APK sur ton téléphone
2. Ouvre le fichier sur le téléphone
3. Autorise l'installation depuis des sources inconnues si demandé
4. Installe l'application

### Méthode 3: Google Drive / Email

1. Upload l'APK sur Google Drive ou envoie par email
2. Télécharge sur le téléphone
3. Installe l'APK

---

## 🎯 Utilisation de l'Application

1. **Ouvre l'app** sur ton smartphone
2. **Autorise les permissions** (caméra, stockage) si demandé
3. **Clique sur "📁 Charger Image"**
4. **Sélectionne une photo** de feuille de maïs
5. **Vois le résultat:**
   - ✅ PLANTE SAINE ou ⚠️ PLANTE MALADE
   - Le type de maladie détecté
   - Le pourcentage de confiance
   - Les probabilités pour chaque classe

---

## 🔧 6. Dépannage

### Problème: "Modèle non chargé"

**Solution:**
- Vérifie que `corn_disease_model.tflite` est bien présent
- Re-compile l'APK avec `buildozer android clean` puis `buildozer android debug`

### Problème: Buildozer échoue

**Solutions:**
```bash
# Nettoie et recommence
buildozer android clean
rm -rf .buildozer

# Re-lance
buildozer android debug
```

### Problème: "Permission denied"

**Solution:**
```bash
chmod +x buildozer.spec
chmod 755 main.py
```

### Problème: L'app crash au démarrage

**Solutions:**
1. Vérifie les logs Android:
```bash
buildozer android logcat
```

2. Vérifie que toutes les dépendances sont dans `buildozer.spec`

3. Test sur PC d'abord avec `python main.py`

### Problème: Prédictions incorrectes

**Vérifications:**
1. Le modèle TFLite fonctionne-t-il sur PC?
2. Les images sont-elles bien prétraitées (224x224, normalisées)?
3. L'ordre des classes est-il correct?

```python
# Dans main.py, vérifie cette ligne:
self.classes = ['Blight', 'Common_Rust', 'Gray_Leaf_Spot', 'Healthy']
# Doit correspondre EXACTEMENT à l'ordre d'entraînement de ton modèle
```

### Problème: APK trop gros (>100MB)

**Solutions:**
- Utilise seulement l'architecture arm64-v8a dans buildozer.spec:
```
android.archs = arm64-v8a
```

- Optimise davantage le modèle avec quantification:
```python
# Dans convert_model_to_tflite.py, ajoute:
converter.optimizations = [tf.lite.Optimize.DEFAULT]
converter.target_spec.supported_types = [tf.float16]
```

---

## 📊 Améliorer l'Application

### Ajouter une icône

1. Crée une image PNG 512x512 nommée `icon.png`
2. Place-la dans le dossier
3. Décommente dans `buildozer.spec`:
```
icon.filename = %(source.dir)s/icon.png
```

### Ajouter un écran de démarrage

1. Crée une image PNG nommée `presplash.png`
2. Place-la dans le dossier
3. Décommente dans `buildozer.spec`:
```
presplash.filename = %(source.dir)s/presplash.png
```

### Activer la caméra (fonctionnalité avancée)

La prise de photo directe nécessite du code Java/Kotlin supplémentaire.
Pour l'instant, utilise "Charger Image" puis prends une photo avec l'app Caméra native.

---

## 📝 Checklist Finale

Avant de compiler:
- [ ] Modèle `.tflite` présent dans le dossier
- [ ] `main.py` testé sur PC
- [ ] `buildozer.spec` configuré
- [ ] Classes dans le bon ordre
- [ ] Environnement virtuel activé

Pour distribuer:
- [ ] APK testé sur au moins un appareil
- [ ] Permissions fonctionnelles
- [ ] Prédictions correctes
- [ ] Interface claire et lisible

---

## 🆘 Support

**Erreurs courantes:**

| Erreur | Solution |
|--------|----------|
| Java not found | `sudo apt install openjdk-17-jdk` |
| SDK download fails | Vérifie ta connexion internet, re-lance buildozer |
| Permission denied | `chmod +x` sur les fichiers |
| APK crash | Vérifie `buildozer android logcat` |

---

## 🎓 Ressources Supplémentaires

- [Documentation Kivy](https://kivy.org/doc/stable/)
- [Documentation Buildozer](https://buildozer.readthedocs.io/)
- [TensorFlow Lite Guide](https://www.tensorflow.org/lite/guide)
- [Android Debugging](https://developer.android.com/studio/debug)

---

**Bon courage! 🚀**

Si tu rencontres des problèmes, note l'erreur exacte et je pourrai t'aider davantage.
