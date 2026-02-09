# 🌽 Application de Détection de Maladies du Maïs

Application mobile Android utilisant l'intelligence artificielle pour détecter les maladies des feuilles de maïs en temps réel, hors ligne.

## 🎯 Fonctionnalités

- ✅ **Détection hors ligne** - Fonctionne sans connexion Internet
- 📸 **Simple d'utilisation** - Charge une photo et obtiens le résultat instantanément
- 🎯 **4 classes détectées**:
  - Mildiou (Blight)
  - Rouille Commune (Common Rust)
  - Tache Grise (Gray Leaf Spot)
  - Plante Saine (Healthy)
- 📊 **Résultats détaillés** - Pourcentage de confiance et probabilités pour chaque classe
- 🇫🇷 **Interface en français** - Facile à comprendre

## 📱 Aperçu

L'application utilise TensorFlow Lite pour faire tourner un modèle de deep learning directement sur le smartphone. Pas besoin de serveur ou de connexion Internet!

## 🚀 Installation Rapide

### Prérequis
- Linux ou WSL (Windows Subsystem for Linux)
- Python 3.8+
- Ton modèle TensorFlow entraîné (.h5 ou SavedModel)

### Installation en 3 étapes

```bash
# 1. Clone ou télécharge ce dossier
cd corn_disease_app

# 2. Lance le script d'installation
chmod +x setup.sh
./setup.sh

# 3. Convertis ton modèle
python convert_model_to_tflite.py
```

Pour les instructions détaillées, voir [GUIDE_INSTALLATION.md](GUIDE_INSTALLATION.md)

## 📦 Fichiers Inclus

| Fichier | Description |
|---------|-------------|
| `main.py` | Application Kivy principale |
| `convert_model_to_tflite.py` | Script de conversion du modèle |
| `buildozer.spec` | Configuration pour compiler l'APK |
| `GUIDE_INSTALLATION.md` | Guide complet étape par étape |
| `setup.sh` | Script d'installation automatique |

## 🔧 Compilation de l'APK

```bash
# Active l'environnement virtuel
source corn_env/bin/activate

# Compile l'APK (première fois: 30-60 min)
buildozer android debug

# L'APK sera dans:
# bin/corndisease-1.0-arm64-v8a-debug.apk
```

## 📲 Installation sur Smartphone

```bash
# Méthode 1: Via USB
buildozer android deploy run

# Méthode 2: Transfert manuel
# Copie le fichier .apk sur ton téléphone et installe-le
```

## 🎨 Personnalisation

### Changer les classes détectées

Dans `main.py`, ligne 38:
```python
self.classes = ['Blight', 'Common_Rust', 'Gray_Leaf_Spot', 'Healthy']
```
**Important:** L'ordre doit correspondre EXACTEMENT à l'ordre d'entraînement de ton modèle!

### Modifier la taille d'entrée

Si ton modèle utilise une taille différente de 224x224, modifie dans `main.py`:
```python
# Ligne ~169
img = img.resize((224, 224))  # Change ces valeurs
```

## 📊 Performance

- **Taille de l'APK**: ~50-80 MB (selon le modèle)
- **Temps de prédiction**: < 1 seconde
- **RAM utilisée**: ~150-200 MB
- **Compatibilité**: Android 5.0+ (API 21+)

## 🐛 Dépannage

### L'app crash au démarrage
```bash
# Voir les logs
buildozer android logcat
```

### Le modèle ne se charge pas
- Vérifie que `corn_disease_model.tflite` est dans le dossier
- Re-compile avec: `buildozer android clean && buildozer android debug`

### Buildozer échoue
```bash
# Nettoie et recommence
buildozer android clean
rm -rf .buildozer
buildozer android debug
```

Plus de solutions dans [GUIDE_INSTALLATION.md](GUIDE_INSTALLATION.md)

## 📈 Améliorations Futures

- [ ] Prise de photo directe avec la caméra
- [ ] Historique des détections
- [ ] Export des résultats en PDF
- [ ] Mode batch (analyser plusieurs photos)
- [ ] Recommandations de traitement

## 🤝 Contribution

Ce projet est open source. N'hésite pas à l'améliorer!

## 📄 Licence

MIT License - Utilise librement pour tes projets

## 🆘 Support

Si tu rencontres des problèmes:
1. Consulte le [GUIDE_INSTALLATION.md](GUIDE_INSTALLATION.md)
2. Vérifie la section Dépannage
3. Note l'erreur exacte pour obtenir de l'aide

## 👨‍💻 Technologies Utilisées

- **Python 3** - Langage principal
- **Kivy** - Framework mobile multiplateforme
- **TensorFlow Lite** - Inférence ML sur mobile
- **NumPy** - Traitement des arrays
- **Pillow** - Manipulation d'images
- **Buildozer** - Compilation APK Android

---

**Développé avec ❤️ pour aider les agriculteurs à détecter les maladies du maïs**

🌽 Bonne chance avec ton projet!
