"""
Application Android de Détection de Maladies du Maïs
Utilise TensorFlow Lite pour la prédiction hors ligne
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image as KivyImage
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from kivy.graphics.texture import Texture
from kivy.core.window import Window
from kivy.clock import Clock

import numpy as np
from PIL import Image
import io

# Pour Android
try:
    from android.permissions import request_permissions, Permission
    from android.storage import app_storage_path
    request_permissions([Permission.CAMERA, Permission.READ_EXTERNAL_STORAGE, 
                        Permission.WRITE_EXTERNAL_STORAGE])
    ANDROID = True
except ImportError:
    ANDROID = False

# TensorFlow Lite
try:
    import tensorflow as tf
    TFLITE_AVAILABLE = True
except ImportError:
    TFLITE_AVAILABLE = False

class CornDiseaseApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.interpreter = None
        self.input_details = None
        self.output_details = None
        self.classes = ['Blight', 'Common_Rust', 'Gray_Leaf_Spot', 'Healthy']
        
    def build(self):
        Window.clearcolor = (0.95, 0.95, 0.95, 1)
        
        # Layout principal
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Titre
        title = Label(
            text='🌽 Détection Maladies Maïs',
            size_hint=(1, 0.1),
            font_size='24sp',
            bold=True,
            color=(0.2, 0.6, 0.2, 1)
        )
        layout.add_widget(title)
        
        # Zone d'affichage de l'image
        self.image_display = KivyImage(
            size_hint=(1, 0.5),
            allow_stretch=True,
            keep_ratio=True
        )
        layout.add_widget(self.image_display)
        
        # Label pour le résultat
        self.result_label = Label(
            text='Chargez une image pour commencer',
            size_hint=(1, 0.15),
            font_size='18sp',
            color=(0.3, 0.3, 0.3, 1)
        )
        layout.add_widget(self.result_label)
        
        # Boutons
        btn_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.15), spacing=10)
        
        # Bouton charger image
        load_btn = Button(
            text='📁 Charger Image',
            background_color=(0.2, 0.6, 0.8, 1),
            font_size='16sp'
        )
        load_btn.bind(on_press=self.open_file_chooser)
        btn_layout.add_widget(load_btn)
        
        # Bouton prendre photo (pour Android)
        if ANDROID:
            camera_btn = Button(
                text='📷 Prendre Photo',
                background_color=(0.2, 0.8, 0.6, 1),
                font_size='16sp'
            )
            camera_btn.bind(on_press=self.take_photo)
            btn_layout.add_widget(camera_btn)
        
        layout.add_widget(btn_layout)
        
        # Charger le modèle
        Clock.schedule_once(lambda dt: self.load_model(), 0.5)
        
        return layout
    
    def load_model(self):
        """Charge le modèle TensorFlow Lite"""
        try:
            # Chercher le modèle dans le dossier de l'app
            model_path = 'corn_disease_model.tflite'
            
            if ANDROID:
                # Sur Android, le modèle doit être dans assets
                from jnius import autoclass
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                activity = PythonActivity.mActivity
                assets = activity.getAssets()
                
                # Lire depuis assets
                input_stream = assets.open(model_path)
                bytes_array = []
                byte = input_stream.read()
                while byte != -1:
                    bytes_array.append(byte)
                    byte = input_stream.read()
                
                model_data = bytes(bytes_array)
                self.interpreter = tf.lite.Interpreter(model_content=model_data)
            else:
                # Sur PC pour test
                self.interpreter = tf.lite.Interpreter(model_path=model_path)
            
            self.interpreter.allocate_tensors()
            self.input_details = self.interpreter.get_input_details()
            self.output_details = self.interpreter.get_output_details()
            
            self.result_label.text = '✅ Modèle chargé avec succès!'
            self.result_label.color = (0.2, 0.7, 0.2, 1)
            
        except Exception as e:
            self.result_label.text = f'❌ Erreur chargement modèle: {str(e)}'
            self.result_label.color = (0.9, 0.2, 0.2, 1)
    
    def open_file_chooser(self, instance):
        """Ouvre le sélecteur de fichiers"""
        content = BoxLayout(orientation='vertical')
        
        # File chooser
        filechooser = FileChooserIconView(
            filters=['*.png', '*.jpg', '*.jpeg'],
            path='/' if ANDROID else '.'
        )
        content.add_widget(filechooser)
        
        # Boutons
        btn_layout = BoxLayout(size_hint=(1, 0.1), spacing=10)
        
        select_btn = Button(text='Sélectionner')
        cancel_btn = Button(text='Annuler')
        
        btn_layout.add_widget(select_btn)
        btn_layout.add_widget(cancel_btn)
        content.add_widget(btn_layout)
        
        popup = Popup(
            title='Choisir une image',
            content=content,
            size_hint=(0.9, 0.9)
        )
        
        def select_file(instance):
            if filechooser.selection:
                self.process_image(filechooser.selection[0])
                popup.dismiss()
        
        select_btn.bind(on_press=select_file)
        cancel_btn.bind(on_press=popup.dismiss)
        
        popup.open()
    
    def take_photo(self, instance):
        """Prendre une photo avec la caméra (Android)"""
        if not ANDROID:
            self.result_label.text = 'Caméra disponible seulement sur Android'
            return
        
        try:
            from android import activity
            from jnius import autoclass
            
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            Intent = autoclass('android.content.Intent')
            MediaStore = autoclass('android.provider.MediaStore')
            
            intent = Intent(MediaStore.ACTION_IMAGE_CAPTURE)
            activity.startActivityForResult(intent, 1)
            
            # Note: Pour une version complète, il faudrait gérer onActivityResult
            self.result_label.text = 'Fonctionnalité caméra en cours de développement...'
            
        except Exception as e:
            self.result_label.text = f'Erreur caméra: {str(e)}'
    
    def process_image(self, image_path):
        """Traite l'image et fait la prédiction"""
        try:
            # Charger et afficher l'image
            img = Image.open(image_path)
            
            # Afficher dans l'interface
            self.display_image(img)
            
            if self.interpreter is None:
                self.result_label.text = '❌ Modèle non chargé'
                return
            
            # Prétraiter l'image
            img_processed = self.preprocess_image(img)
            
            # Prédiction
            self.interpreter.set_tensor(self.input_details[0]['index'], img_processed)
            self.interpreter.invoke()
            output_data = self.interpreter.get_tensor(self.output_details[0]['index'])
            
            # Résultats
            predicted_class_idx = np.argmax(output_data[0])
            confidence = output_data[0][predicted_class_idx] * 100
            predicted_class = self.classes[predicted_class_idx]
            
            # Afficher le résultat
            self.show_result(predicted_class, confidence, output_data[0])
            
        except Exception as e:
            self.result_label.text = f'❌ Erreur: {str(e)}'
            self.result_label.color = (0.9, 0.2, 0.2, 1)
    
    def preprocess_image(self, img):
        """Prétraite l'image pour le modèle"""
        # Redimensionner à 224x224
        img = img.resize((224, 224))
        
        # Convertir en array numpy
        img_array = np.array(img)
        
        # S'assurer qu'on a 3 canaux (RGB)
        if len(img_array.shape) == 2:
            img_array = np.stack([img_array] * 3, axis=-1)
        elif img_array.shape[2] == 4:
            img_array = img_array[:, :, :3]
        
        # Normaliser (0-1)
        img_array = img_array.astype(np.float32) / 255.0
        
        # Ajouter dimension batch
        img_array = np.expand_dims(img_array, axis=0)
        
        return img_array
    
    def display_image(self, pil_image):
        """Affiche l'image dans l'interface"""
        # Convertir PIL Image en texture Kivy
        img_data = io.BytesIO()
        pil_image.save(img_data, format='PNG')
        img_data.seek(0)
        
        texture = Texture.create(size=pil_image.size)
        texture.blit_buffer(pil_image.tobytes(), colorfmt='rgb', bufferfmt='ubyte')
        texture.flip_vertical()
        
        self.image_display.texture = texture
    
    def show_result(self, predicted_class, confidence, all_probabilities):
        """Affiche le résultat de la prédiction"""
        # Emoji et couleur selon la classe
        if predicted_class == 'Healthy':
            emoji = '✅'
            color = (0.2, 0.7, 0.2, 1)
            status = 'SAINE'
        else:
            emoji = '⚠️'
            color = (0.9, 0.4, 0.1, 1)
            status = 'MALADE'
        
        # Traduire le nom de la maladie
        disease_names = {
            'Blight': 'Mildiou',
            'Common_Rust': 'Rouille Commune',
            'Gray_Leaf_Spot': 'Tache Grise',
            'Healthy': 'Saine'
        }
        
        disease_fr = disease_names.get(predicted_class, predicted_class)
        
        result_text = f'{emoji} PLANTE {status}\n'
        result_text += f'Diagnostic: {disease_fr}\n'
        result_text += f'Confiance: {confidence:.1f}%\n\n'
        result_text += 'Détails:\n'
        
        for i, class_name in enumerate(self.classes):
            prob = all_probabilities[i] * 100
            class_fr = disease_names.get(class_name, class_name)
            result_text += f'  {class_fr}: {prob:.1f}%\n'
        
        self.result_label.text = result_text
        self.result_label.color = color

if __name__ == '__main__':
    CornDiseaseApp().run()
