import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

import os
import requests
import json

import subprocess


## verifica se existe atualizacao

def get_latest_version(repo_url):
    api_url = f"https://api.github.com/repos/{repo_url}/releases/latest"
    response = requests.get(api_url)
    data = response.json()
    return data['tag_name']

def is_update_available(current_version, latest_version):
    return current_version < latest_version


## baixa e aplica atualizacao

def download_latest_release(repo_url, download_path):
    api_url = f"https://api.github.com/repos/{repo_url}/releases/latest"
    response = requests.get(api_url)
    data = response.json()
    download_url = data['assets'][0]['browser_download_url']
    
    response = requests.get(download_url)
    with open(download_path, 'wb') as f:
        f.write(response.content)

def apply_update(download_path, executable_path):
    os.rename(executable_path, f"{executable_path}.old")
    os.rename(download_path, executable_path)



## integracao


CURRENT_VERSION = "1.0.0"
REPO_URL = "LaCoit/Dizer_Hola"

def check_for_updates():
    latest_version = get_latest_version(REPO_URL)
    if is_update_available(CURRENT_VERSION, latest_version):
        msg_box = QMessageBox()
        msg_box.setText(f"Uma nova versão ({latest_version}) está disponível. Deseja atualizar?")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        ret = msg_box.exec_()
        
        if ret == QMessageBox.Yes:
            download_path = "new_version.exe"
            executable_path = sys.argv[0]
            download_latest_release(REPO_URL, download_path)
            apply_update(download_path, executable_path)
            QMessageBox.information(None, "Atualização", "O programa será reiniciado para aplicar a atualização.")
            os.execv(executable_path, sys.argv)




## classe principal

class HolaApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Hola App')

        layout = QVBoxLayout()

        self.label = QLabel('Digite seu nome:', self)
        layout.addWidget(self.label)

        self.name_input = QLineEdit(self)
        layout.addWidget(self.name_input)

        self.button = QPushButton('Dizer Hola', self)
        self.button.clicked.connect(self.show_message)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def show_message(self):
        name = self.name_input.text()
        if name:
            QMessageBox.information(self, 'Hola', f'Hola {name}!')
        else:
            QMessageBox.warning(self, 'Atenção', 'Por favor, digite um nome.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # check_for_updates()
    ex = HolaApp()
    ex.show()
    sys.exit(app.exec_())



