"""
Script pour convertir un modèle TensorFlow en TensorFlow Lite
Pour l'application de détection de maladies du maïs
"""

import tensorflow as tf
import numpy as np

def convert_model_to_tflite(model_path, output_path='corn_disease_model.tflite'):
    """
    Convertit un modèle TensorFlow (.h5 ou SavedModel) en TensorFlow Lite
    
    Args:
        model_path: Chemin vers ton modèle (.h5 ou dossier SavedModel)
        output_path: Nom du fichier .tflite de sortie
    """
    
    print("🔄 Chargement du modèle...")
    # Charger le modèle
    model = tf.keras.models.load_model(model_path)
    
    print("📊 Architecture du modèle:")
    model.summary()
    
    # Créer le convertisseur
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    
    # Options d'optimisation pour réduire la taille
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    
    print("⚙️ Conversion en cours...")
    tflite_model = converter.convert()
    
    # Sauvegarder le modèle TFLite
    with open(output_path, 'wb') as f:
        f.write(tflite_model)
    
    # Afficher la taille du fichier
    import os
    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"✅ Modèle converti avec succès!")
    print(f"📁 Fichier: {output_path}")
    print(f"💾 Taille: {size_mb:.2f} MB")
    
    # Tester le modèle TFLite
    print("\n🧪 Test du modèle TFLite...")
    test_tflite_model(output_path)

def test_tflite_model(tflite_path):
    """
    Teste le modèle TFLite avec une image aléatoire
    """
    # Charger le modèle TFLite
    interpreter = tf.lite.Interpreter(model_path=tflite_path)
    interpreter.allocate_tensors()
    
    # Obtenir les détails d'entrée et de sortie
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    
    print(f"📥 Input shape: {input_details[0]['shape']}")
    print(f"📤 Output shape: {output_details[0]['shape']}")
    
    # Créer une image de test (224x224x3)
    test_image = np.random.rand(1, 224, 224, 3).astype(np.float32)
    
    # Faire une prédiction test
    interpreter.set_tensor(input_details[0]['index'], test_image)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])
    
    classes = ['Blight', 'Common_Rust', 'Gray_Leaf_Spot', 'Healthy']
    predicted_class = np.argmax(output_data[0])
    confidence = output_data[0][predicted_class] * 100
    
    print(f"🎯 Test réussi!")
    print(f"   Classe prédite: {classes[predicted_class]}")
    print(f"   Confiance: {confidence:.2f}%")

if __name__ == "__main__":
    print("=" * 60)
    print("🌽 CONVERTISSEUR DE MODÈLE - Détection Maladies Maïs")
    print("=" * 60)
    
    # REMPLACE CE CHEMIN PAR LE CHEMIN VERS TON MODÈLE
    # Exemples:
    # - Si tu as un fichier .h5: model_path = "mon_modele.h5"
    # - Si tu as un dossier SavedModel: model_path = "mon_modele_dossier/"
    
    model_path = input("\n📂 Entre le chemin vers ton modèle (.h5 ou SavedModel): ").strip()
    
    try:
        convert_model_to_tflite(model_path)
        print("\n✅ Conversion terminée! Tu peux maintenant utiliser le fichier .tflite dans ton app.")
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        print("\n💡 Assure-toi que:")
        print("   - Le chemin vers ton modèle est correct")
        print("   - TensorFlow est installé: pip install tensorflow")
