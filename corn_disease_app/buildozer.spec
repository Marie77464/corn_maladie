[app]

# Nom de ton application
title = Corn Disease Detector

# Nom du package (utilise ton propre nom de domaine inversé)
package.name = corndisease

# Domaine du package
package.domain = org.maisdisease

# Répertoire source de ton app
source.dir = .

# Fichier principal
source.include_exts = py,png,jpg,jpeg,kv,tflite

# Fichier principal Python
source.main = main.py

# Version de l'app
version = 1.0

# Requirements Python - modules nécessaires
requirements = python3,kivy,numpy,pillow,tensorflow

# Permissions Android
android.permissions = CAMERA,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,INTERNET

# Orientation
orientation = portrait

# Icône de l'app (facultatif, crée une icône si tu veux)
#icon.filename = %(source.dir)s/icon.png

# Écran de démarrage (facultatif)
#presplash.filename = %(source.dir)s/presplash.png

# Android API à utiliser
android.api = 31
android.minapi = 21
android.ndk = 25b
android.sdk = 31

# Architecture
android.archs = arm64-v8a,armeabi-v7a

# Activer AndroidX
android.enable_androidx = True

# Inclure le modèle TFLite dans les assets
# Place ton fichier corn_disease_model.tflite dans le dossier de l'app
source.include_patterns = assets/*,corn_disease_model.tflite

# Android assets
android.add_assets = corn_disease_model.tflite

[buildozer]

# Log level
log_level = 2

# Avertissements
warn_on_root = 1
