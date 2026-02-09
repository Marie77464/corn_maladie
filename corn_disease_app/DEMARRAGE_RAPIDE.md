# 🚀 DÉMARRAGE RAPIDE - 5 MINUTES

## ⚡ Tu veux juste compiler ton app? Suis ces étapes!

### 📋 Ce dont tu as besoin MAINTENANT:
- ✅ Un ordinateur Linux ou WSL (Windows)
- ✅ Ton modèle TensorFlow (.h5 ou SavedModel)
- ✅ 30-60 minutes pour la première compilation

---

## 🎯 ÉTAPES RAPIDES

### 1️⃣ Installation (5 minutes)

```bash
# Ouvre un terminal et va dans le dossier
cd corn_disease_app

# Lance l'installation automatique
chmod +x setup.sh
./setup.sh
```

Attends que tout s'installe... ☕

---

### 2️⃣ Convertis ton modèle (2 minutes)

```bash
# Active l'environnement (si pas déjà fait)
source corn_env/bin/activate

# Lance la conversion
python convert_model_to_tflite.py
```

Quand il te demande le chemin, entre le nom de ton fichier modèle, par exemple:
```
mon_modele.h5
```

Tu dois obtenir: `corn_disease_model.tflite` ✅

---

### 3️⃣ Compile l'APK (30-60 min la première fois)

```bash
# Compile pour Android
buildozer android debug
```

**ATTENTION:** La première fois prend 30-60 minutes! ⏰
Buildozer télécharge plein de choses. C'est normal!

Les prochaines fois prendront 5-10 minutes seulement.

---

### 4️⃣ Installe sur ton téléphone

L'APK est dans: `bin/corndisease-1.0-arm64-v8a-debug.apk`

**Option A - Via USB:**
```bash
# Active le mode développeur sur ton téléphone
# Active "Débogage USB"
# Connecte en USB

buildozer android deploy run
```

**Option B - Manuellement:**
1. Copie le fichier `.apk` sur ton téléphone
2. Ouvre-le sur le téléphone
3. Installe (autorise "sources inconnues" si demandé)

---

## ✅ VÉRIFICATION

### Ton dossier doit ressembler à ça:

```
corn_disease_app/
├── main.py                           ✅
├── buildozer.spec                    ✅
├── convert_model_to_tflite.py       ✅
├── corn_disease_model.tflite        ✅ (après conversion)
├── GUIDE_INSTALLATION.md             ✅
├── README.md                         ✅
├── setup.sh                          ✅
└── corn_env/                         ✅ (après installation)
```

---

## 🐛 PROBLÈMES FRÉQUENTS

### "command not found: buildozer"
```bash
source corn_env/bin/activate
pip install buildozer
```

### "Java not found"
```bash
sudo apt install openjdk-17-jdk
```

### L'app crash sur le téléphone
```bash
# Voir les erreurs
buildozer android logcat
```

### Recommencer à zéro
```bash
buildozer android clean
rm -rf .buildozer
buildozer android debug
```

---

## 📱 UTILISATION DE L'APP

1. Ouvre l'app sur ton téléphone
2. Autorise les permissions (stockage)
3. Clique "📁 Charger Image"
4. Choisis une photo de feuille de maïs
5. Vois le résultat! ✅ ou ⚠️

---

## 🆘 AIDE

**Si ça bloque:**
1. Regarde l'erreur exacte
2. Consulte GUIDE_INSTALLATION.md (plus détaillé)
3. Vérifie que tu as bien suivi TOUTES les étapes

---

## 🎓 TU VEUX PLUS DE DÉTAILS?

Lis le fichier complet: **GUIDE_INSTALLATION.md**

---

**C'EST PARTI! 🚀**
