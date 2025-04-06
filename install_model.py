import argostranslate.package
import os

model_path = "D:\\Licenta\\Tools for agents\\models\\en_es.argosmodel"
if os.path.exists(model_path):
    argostranslate.package.install_from_path(model_path)
    print("Model installed successfully.")
else:
    print("Model file not found. Please check the path.")
