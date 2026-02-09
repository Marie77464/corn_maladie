#!/bin/bash

# Script de démarrage rapide pour l'application de détection de maladies du maïs
# Ce script automatise l'installation et la compilation

echo "================================================"
echo "🌽 Installation App Détection Maladies Maïs"
echo "================================================"
echo ""

# Vérifier si on est sur Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo "⚠️  Ce script est conçu pour Linux/WSL"
    echo "Pour Windows, suis les instructions dans GUIDE_INSTALLATION.md"
    exit 1
fi

# Fonction pour vérifier si une commande existe
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# 1. Vérifier Python
echo "🔍 Vérification de Python..."
if ! command_exists python3; then
    echo "❌ Python3 n'est pas installé"
    echo "Installation de Python3..."
    sudo apt update
    sudo apt install -y python3 python3-pip python3-venv
else
    echo "✅ Python3 installé: $(python3 --version)"
fi

# 2. Installer les dépendances système
echo ""
echo "📦 Installation des dépendances système..."
sudo apt install -y git zip unzip openjdk-17-jdk autoconf libtool \
                    pkg-config zlib1g-dev libncurses5-dev \
                    libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev

# 3. Créer l'environnement virtuel
echo ""
echo "🐍 Création de l'environnement virtuel..."
if [ ! -d "corn_env" ]; then
    python3 -m venv corn_env
    echo "✅ Environnement virtuel créé"
else
    echo "✅ Environnement virtuel déjà existant"
fi

# 4. Activer l'environnement et installer les packages
echo ""
echo "📚 Installation des packages Python..."
source corn_env/bin/activate

pip install --upgrade pip
pip install tensorflow pillow numpy kivy buildozer cython

echo ""
echo "✅ Installation terminée!"
echo ""
echo "================================================"
echo "📋 PROCHAINES ÉTAPES:"
echo "================================================"
echo ""
echo "1️⃣  Convertir ton modèle en TensorFlow Lite:"
echo "    python convert_model_to_tflite.py"
echo ""
echo "2️⃣  Tester l'application sur PC (optionnel):"
echo "    python main.py"
echo ""
echo "3️⃣  Compiler l'APK Android:"
echo "    buildozer android debug"
echo ""
echo "4️⃣  L'APK sera dans: bin/corndisease-1.0-arm64-v8a-debug.apk"
echo ""
echo "📖 Pour plus de détails, consulte GUIDE_INSTALLATION.md"
echo ""
echo "🎯 Environnement activé! Tu peux maintenant lancer les commandes ci-dessus."
echo ""

# Garder l'environnement activé
bash
