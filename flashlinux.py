#!/usr/bin/env python3
import sys
import os
import subprocess
import time
import shlex
import base64
import urllib.request
import re
from bs4 import BeautifulSoup
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                           QComboBox, QPushButton, QLabel, QMessageBox,
                           QProgressBar, QTextEdit, QMenuBar, QMenu, QTabWidget,
                           QHBoxLayout, QFileDialog, QLineEdit)
from PySide6.QtCore import Qt, QThread, Signal, QSize
from PySide6.QtGui import QPixmap, QImage, QPainter, QColor, QIcon
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtSvgWidgets import QSvgWidget
import pyudev
import requests
import threading
import humanize

# Dicionário de traduções
TRANSLATIONS = {
    'pt_BR': {
        'file_menu': 'Arquivo',
        'refresh_devices': 'Atualizar Dispositivos',
        'exit': 'Sair',
        'tools_menu': 'Ferramentas',
        'format_usb': 'Formatar USB',
        'download_images': 'Baixar Imagens',
        'write_iso': 'Gravar ISO',
        'check_updates': 'Verificar Atualizações',
        'settings_menu': 'Configurações',
        'theme_menu': 'Tema',
        'light_theme': 'Claro',
        'dark_theme': 'Escuro',
        'system_theme': 'Sistema',
        'language_menu': 'Idioma',
        'help_menu': 'Ajuda',
        'documentation': 'Documentação',
        'about': 'Sobre',
        'report_bug': 'Reportar Problema',
        'select_device': 'Selecione o dispositivo USB:',
        'format_device': 'Formatar Dispositivo',
        'operations_log': 'Log de operações:',
        'ready_to_format': 'Pronto para formatar. Selecione um dispositivo USB.',
        'select_distro': 'Selecione a distribuição Linux:',
        'download_image': 'Baixar Imagem',
        'pause': 'Pausar',
        'resume': 'Continuar',
        'stop': 'Parar',
        'download_log': 'Log de download:',
        'select_iso': 'Selecionar ISO',
        'write_button': 'Gravar ISO',
        'cancel': 'Cancelar',
        'write_log': 'Log de gravação:',
        'donate_button': 'Faça uma doação via PIX',
        'donate_title': 'Doar via PIX',
        'donate_message': 'Sua contribuição é muito importante!\n\nChave PIX: danmuciolemos@gmail.com\n\nAgradecemos seu apoio!',
        'about_title': 'FlashLinux',
        'about_version': 'Versão',
        'about_description': 'Utilitário especializado para formatação e preparação de dispositivos USB\ncom suporte a sistemas de arquivos EXT4 e FAT32, otimizado para\ncriação de mídias bootáveis com distribuições Linux.',
        'about_developer': 'Desenvolvido por DML Desenvolvimentos',
        'about_email': 'Email: danmuciolemos@gmail.com'
    },
    'es': {
        'file_menu': 'Archivo',
        'refresh_devices': 'Actualizar Dispositivos',
        'exit': 'Salir',
        'tools_menu': 'Herramientas',
        'format_usb': 'Formatear USB',
        'download_images': 'Descargar Imágenes',
        'write_iso': 'Grabar ISO',
        'check_updates': 'Verificar Actualizaciones',
        'settings_menu': 'Configuración',
        'theme_menu': 'Tema',
        'light_theme': 'Claro',
        'dark_theme': 'Oscuro',
        'system_theme': 'Sistema',
        'language_menu': 'Idioma',
        'help_menu': 'Ayuda',
        'documentation': 'Documentación',
        'about': 'Acerca de',
        'report_bug': 'Reportar Problema',
        'select_device': 'Seleccione el dispositivo USB:',
        'format_device': 'Formatear Dispositivo',
        'operations_log': 'Registro de operaciones:',
        'ready_to_format': 'Listo para formatear. Seleccione un dispositivo USB.',
        'select_distro': 'Seleccione la distribución Linux:',
        'download_image': 'Descargar Imagen',
        'pause': 'Pausar',
        'resume': 'Continuar',
        'stop': 'Detener',
        'download_log': 'Registro de descarga:',
        'select_iso': 'Seleccionar ISO',
        'write_button': 'Grabar ISO',
        'cancel': 'Cancelar',
        'write_log': 'Registro de grabación:',
        'donate_button': 'Haga una donación vía PIX',
        'donate_title': 'Donar vía PIX',
        'donate_message': '¡Su contribución es muy importante!\n\nClave PIX: danmuciolemos@gmail.com\n\n¡Gracias por su apoyo!',
        'about_title': 'Formateador USB para Linux',
        'about_version': 'Versión',
        'about_description': 'Utilidad especializada para formatear y preparar dispositivos USB\ncon soporte para sistemas de archivos EXT4 y FAT32, optimizado para\ncrear medios de arranque con distribuciones Linux.',
        'about_developer': 'Desarrollado por DML Desenvolvimentos',
        'about_email': 'Email: danmuciolemos@gmail.com'
    },
    'en': {
        'file_menu': 'File',
        'refresh_devices': 'Refresh Devices',
        'exit': 'Exit',
        'tools_menu': 'Tools',
        'format_usb': 'Format USB',
        'download_images': 'Download Images',
        'write_iso': 'Write ISO',
        'check_updates': 'Check Updates',
        'settings_menu': 'Settings',
        'theme_menu': 'Theme',
        'light_theme': 'Light',
        'dark_theme': 'Dark',
        'system_theme': 'System',
        'language_menu': 'Language',
        'help_menu': 'Help',
        'documentation': 'Documentation',
        'about': 'About',
        'report_bug': 'Report Bug',
        'select_device': 'Select USB device:',
        'format_device': 'Format Device',
        'operations_log': 'Operations log:',
        'ready_to_format': 'Ready to format. Select a USB device.',
        'select_distro': 'Select Linux distribution:',
        'download_image': 'Download Image',
        'pause': 'Pause',
        'resume': 'Resume',
        'stop': 'Stop',
        'download_log': 'Download log:',
        'select_iso': 'Select ISO',
        'write_button': 'Write ISO',
        'cancel': 'Cancel',
        'write_log': 'Write log:',
        'donate_button': 'Make a PIX donation',
        'donate_title': 'Donate via PIX',
        'donate_message': 'Your contribution is very important!\n\nPIX key: danmuciolemos@gmail.com\n\nThank you for your support!',
        'about_title': 'USB Formatter for Linux',
        'about_version': 'Version',
        'about_description': 'Specialized utility for formatting and preparing USB devices\nwith support for EXT4 and FAT32 file systems, optimized for\ncreating bootable media with Linux distributions.',
        'about_developer': 'Developed by DML Desenvolvimentos',
        'about_email': 'Email: danmuciolemos@gmail.com'
    }
}

VERSION = "0.01"

# Lista de distribuições Linux populares com informações de atualização
DISTROS = {
    "Ubuntu": {
        "url": "https://releases.ubuntu.com/24.04/ubuntu-24.04.2-desktop-amd64.iso",
        "description": "A distribuição Linux mais popular, conhecida por sua facilidade de uso e interface amigável.",
        "pattern": r'ubuntu-\d+\.\d+\.\d+-desktop-amd64\.iso'
    },
    "Linux Mint": {
        "url": "https://mirrors.edge.kernel.org/linuxmint/stable/22.1/linuxmint-22.1-cinnamon-64bit.iso",
        "description": "Baseado no Ubuntu, com foco em simplicidade e interface familiar para usuários de Windows.",
        "pattern": r'linuxmint-\d+\.\d+-cinnamon-64bit\.iso'
    },
    "Fedora": {
        "url": "https://download.fedoraproject.org/pub/fedora/linux/releases/40/Workstation/x86_64/iso/Fedora-Workstation-Live-x86_64-40-1.6.iso",
        "description": "Distribuição patrocinada pela Red Hat, conhecida por ter as tecnologias mais recentes.",
        "pattern": r'Fedora-Workstation-Live-x86_64-\d+.*\.iso'
    },
    "Pop!_OS": {
        "url": "https://iso.pop-os.org/24.04/amd64/intel/11/pop-os_24.04_amd64_intel_11.iso",
        "description": "Desenvolvido pela System76, otimizado para desenvolvimento e jogos.",
        "pattern": r'pop-os_\d+\.\d+.*_amd64_intel.*\.iso'
    },
    "Zorin OS": {
        "url": "https://mirrors.edge.kernel.org/zorinos/16/Zorin-OS-16.3-Core-64-bit.iso",
        "description": "Projetado para ser amigável para usuários vindos do Windows.",
        "pattern": r'Zorin-OS-\d+\.\d+-Core-64-bit\.iso'
    },
    "Elementary OS": {
        "url": "https://sgp1.dl.elementary.io/download/MTcwODQ3MzE0OQ==/elementary-os-7.1-stable.20240124rc.iso",
        "description": "Conhecido por seu design elegante e minimalista inspirado no macOS.",
        "pattern": r'elementary-os-\d+\.\d+-stable\..*\.iso'
    },
    "MX Linux": {
        "url": "https://sourceforge.net/projects/mx-linux/files/Final/Xfce/MX-23.2_x64.iso",
        "description": "Distribuição leve baseada no Debian, com foco em estabilidade.",
        "pattern": r'MX-\d+\.\d+_x64\.iso'
    },
    "Manjaro": {
        "url": "https://download.manjaro.org/kde/23.1.3/manjaro-kde-23.1.3-minimal-240304-linux67.iso",
        "description": "Baseado no Arch Linux, com foco em facilidade de uso e atualizações contínuas.",
        "pattern": r'manjaro-kde-.*-minimal-.*-linux.*\.iso'
    },
    "KDE Neon": {
        "url": "https://files.kde.org/neon/images/user/20240314-1205/neon-user-20240314-1205.iso",
        "description": "Distribuição oficial do KDE com as versões mais recentes do ambiente KDE Plasma.",
        "pattern": r'neon-user-\d{8}-\d{4}\.iso'
    },
    "Linux Lite": {
        "url": "https://downloads.sourceforge.net/linux-lite/linux-lite-6.6-64bit.iso",
        "description": "Distribuição leve baseada no Ubuntu, ideal para computadores mais antigos.",
        "pattern": r'linux-lite-\d+\.\d+-64bit\.iso'
    }
}

# Logo em base64 (PNG)
LOGO_PNG = '''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'''

def get_auth_token():
    """Solicita autenticação e retorna o token de autenticação"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    auth_script = os.path.join(script_dir, 'auth_check.sh')
    
    try:
        # Solicita autenticação
        subprocess.run(['pkexec', auth_script], check=True)
        # Se chegou aqui, a autenticação foi bem sucedida
        return True
    except subprocess.CalledProcessError:
        return False

class FormatThread(QThread):
    progress_updated = Signal(int, str)
    finished = Signal(bool, str)
    
    def __init__(self, script_path, device):
        super().__init__()
        self.script_path = script_path
        self.device = device
    
    def run(self):
        try:
            # Garante que o script tenha permissão de execução
            os.chmod(self.script_path, 0o755)
            
            # Usa uma lista de argumentos em vez de string
            process = subprocess.Popen(
                ['sudo', self.script_path, self.device, 'format'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # Processa a saída linha por linha
            while True:
                line = process.stdout.readline()
                if not line and process.poll() is not None:
                    break
                    
                if line.startswith('PROGRESS:'):
                    _, percent, message = line.strip().split(':', 2)
                    self.progress_updated.emit(int(percent), message)
            
            # Verifica se houve erro
            if process.returncode == 0:
                self.finished.emit(True, "Formatação concluída com sucesso!")
            else:
                error = process.stderr.read()
                self.finished.emit(False, f"Erro na formatação: {error}")
                
        except Exception as e:
            self.finished.emit(False, str(e))

class DownloadThread(QThread):
    progress_updated = Signal(int, str)
    finished = Signal(bool, str)
    
    def __init__(self, url, save_path):
        super().__init__()
        self.url = url
        self.save_path = save_path
        self.paused = threading.Event()
        self.stopped = threading.Event()
        self.paused.set()  # Inicialmente não está pausado
    
    def pause(self):
        self.paused.clear()
    
    def resume(self):
        self.paused.set()
    
    def stop(self):
        self.stopped.set()
    
    def run(self):
        try:
            response = requests.get(self.url, stream=True)
            total_size = int(response.headers.get('content-length', 0))
            if total_size == 0:
                self.finished.emit(False, "Erro: Não foi possível determinar o tamanho do arquivo.")
                return
                
            block_size = 1024  # 1 Kibibyte
            written = 0
            start_time = time.time()
            last_update_time = start_time
            last_written = 0
            
            with open(self.save_path, 'wb') as f:
                for data in response.iter_content(block_size):
                    if self.stopped.is_set():
                        f.close()
                        try:
                            os.remove(self.save_path)
                        except:
                            pass
                        self.finished.emit(False, "Download cancelado pelo usuário.")
                        return
                    
                    while not self.paused.is_set():
                        if self.stopped.is_set():
                            f.close()
                            try:
                                os.remove(self.save_path)
                            except:
                                pass
                            self.finished.emit(False, "Download cancelado pelo usuário.")
                            return
                        time.sleep(0.1)
                    
                    written += len(data)
                    f.write(data)
                    
                    # Atualiza a cada 0.5 segundos
                    current_time = time.time()
                    if current_time - last_update_time >= 0.5:
                        interval = current_time - last_update_time
                        if interval > 0:
                            recent_written = written - last_written
                            speed = recent_written / interval
                            speed_text = humanize.naturalsize(speed) + "/s"
                            
                            if speed > 0:
                                remaining_bytes = total_size - written
                                eta_seconds = remaining_bytes / speed
                                if eta_seconds < 60:
                                    eta_text = f"{int(eta_seconds)} segundos"
                                elif eta_seconds < 3600:
                                    eta_text = f"{int(eta_seconds/60)} minutos"
                                else:
                                    eta_text = f"{int(eta_seconds/3600)} horas"
                            else:
                                eta_text = "calculando..."
                            
                            progress = (written / total_size) * 100
                            status_text = f"Velocidade: {speed_text} | ETA: {eta_text}"
                            self.progress_updated.emit(int(progress), status_text)
                            
                            last_update_time = current_time
                            last_written = written
            
            self.finished.emit(True, "Download concluído com sucesso!")
            
        except requests.exceptions.RequestException as e:
            self.finished.emit(False, f"Erro na conexão: {str(e)}")
        except IOError as e:
            self.finished.emit(False, f"Erro ao salvar arquivo: {str(e)}")
        except Exception as e:
            self.finished.emit(False, f"Erro no download: {str(e)}")

class AboutDialog(QMessageBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle(self.tr('about'))
        self.setIcon(QMessageBox.Information)
        self.setText(
            f"{self.tr('about_title')}\n"
            f"{self.tr('about_version')} {VERSION}\n\n"
            f"{self.tr('about_description')}\n\n"
            f"{self.tr('about_developer')}\n"
            f"{self.tr('about_email')}"
        )
        self.setStandardButtons(QMessageBox.Ok)

    def tr(self, key):
        """Traduz uma chave para o idioma atual"""
        return TRANSLATIONS[self.parent.current_language].get(key, key)

class UpdateDistrosThread(QThread):
    progress_updated = Signal(str)
    finished = Signal(dict)
    
    def run(self):
        updated_distros = DISTROS.copy()  # Cria uma cópia do dicionário original
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        })
        
        self.progress_updated.emit("Verificando disponibilidade dos links...")
        
        for distro_name, info in DISTROS.items():
            try:
                # Verifica se o link está acessível
                url = info['url']
                if check_link_status(url):
                    self.progress_updated.emit(f"{distro_name}: Link principal OK")
                else:
                    # Se o link principal estiver indisponível, busca alternativa
                    self.progress_updated.emit(f"Link principal indisponível para {distro_name}, buscando alternativa...")
                    alternative_url = find_alternative_link(distro_name, info['pattern'])
                    
                    if alternative_url:
                        updated_distros[distro_name]['url'] = alternative_url
                        self.progress_updated.emit(f"{distro_name}: Link alternativo encontrado e atualizado")
                    else:
                        self.progress_updated.emit(f"{distro_name}: Mantendo link original (nenhuma alternativa encontrada)")
                
            except Exception as e:
                self.progress_updated.emit(f"Erro ao verificar {distro_name}: {str(e)}")
        
        self.progress_updated.emit("\nStatus dos links:")
        for distro_name in sorted(updated_distros.keys()):
            url_changed = updated_distros[distro_name]['url'] != DISTROS[distro_name]['url']
            status = "Link atualizado" if url_changed else "Link original mantido"
            self.progress_updated.emit(f"{distro_name}: {status}")
        
        self.finished.emit(updated_distros)

def check_link_status(url):
    """Verifica se um link está acessível"""
    try:
        response = requests.head(url, timeout=5)
        return response.status_code == 200
    except:
        return False

def find_alternative_link(distro_name: str, pattern: str) -> str:
    """Busca um link alternativo para uma distribuição Linux quando o link principal está indisponível"""
    try:
        # Primeiro tenta buscar nos sites oficiais e mirrors conhecidos
        links = search_alternative_links(distro_name, pattern)
        if links:
            return links[0]  # Retorna o primeiro link válido encontrado
            
        # Se não encontrar nos sites oficiais, tenta uma busca mais ampla
        search_term = f"{distro_name} ISO download {pattern}"
        response = requests.get(
            f"https://www.google.com/search?q={urllib.parse.quote(search_term)}",
            headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'}
        )
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for link in soup.find_all('a'):
            href = link.get('href', '')
            if 'url=' in href:
                url = href.split('url=')[1].split('&')[0]
                url = urllib.parse.unquote(url)
                
                if re.search(pattern, url) and check_link_status(url):
                    return url
        
        return None
    except Exception as e:
        print(f"Erro ao buscar link alternativo para {distro_name}: {str(e)}")
        return None

def search_alternative_links(distro_name: str, pattern: str) -> list:
    """Busca links alternativos usando a API de busca na web"""
    try:
        # Constrói o termo de busca
        search_term = f"{distro_name} ISO download mirror site:{distro_name.lower().split()[0]}.org OR site:sourceforge.net OR site:github.com"
        
        # Faz a busca na web usando DuckDuckGo (mais amigável para scraping)
        response = requests.get(
            f"https://duckduckgo.com/html/?q={urllib.parse.quote(search_term)}",
            headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'}
        )
        
        # Usa BeautifulSoup para analisar os resultados
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Lista para armazenar os links encontrados
        found_links = []
        
        # Procura por links que correspondam ao padrão
        for link in soup.find_all('a', class_='result__url'):
            href = link.get('href', '')
            if href:
                # Verifica se a URL corresponde ao padrão e está acessível
                if re.search(pattern, href) and check_link_status(href):
                    found_links.append(href)
        
        return found_links
    except Exception as e:
        print(f"Erro ao buscar links alternativos para {distro_name}: {str(e)}")
        return []

class WriteISOThread(QThread):
    progress_updated = Signal(int, str)
    finished = Signal(bool, str)
    
    def __init__(self, iso_path, device):
        super().__init__()
        self.iso_path = iso_path
        self.device = device
        self.stopped = False
    
    def stop(self):
        self.stopped = True
    
    def run(self):
        try:
            # Obtém o tamanho total do arquivo ISO
            total_size = os.path.getsize(self.iso_path)
            
            # Usa dd com sudo para gravar a ISO
            command = ['sudo', 'dd', f'if={self.iso_path}', f'of={self.device}', 'bs=4M', 'status=progress']
            
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            
            written = 0
            while True:
                if self.stopped:
                    process.terminate()
                    self.finished.emit(False, "Gravação cancelada pelo usuário.")
                    return
                
                output = process.stderr.readline()
                if not output and process.poll() is not None:
                    break
                
                if 'bytes' in output:
                    try:
                        written = int(output.split('bytes')[0].strip())
                        progress = (written / total_size) * 100
                        self.progress_updated.emit(int(progress), f"Gravando... {progress:.1f}%")
                    except:
                        pass
            
            # Verifica se o processo terminou com sucesso
            if process.returncode == 0:
                # Força a sincronização do buffer
                subprocess.run(['sudo', 'sync'], check=True)
                self.finished.emit(True, "Imagem gravada com sucesso!")
            else:
                error = process.stderr.read()
                self.finished.emit(False, f"Erro durante a gravação: {error}")
                
        except Exception as e:
            self.finished.emit(False, f"Erro durante a gravação: {str(e)}")

class USBFormatter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_language = 'pt_BR'  # Idioma padrão
        self.setWindowTitle("FlashLinux")
        self.setMinimumSize(600, 450)  # Tamanho reduzido da janela
        
        # Configura os scripts
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.format_script = os.path.join(script_dir, 'format_operations.sh')
        
        # Widget principal com abas
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Container para a logo
        logo_container = QWidget()
        logo_container.setFixedHeight(80)  # Altura total do container reduzida
        logo_container.setMinimumWidth(100)  # Largura mínima reduzida
        logo_layout = QVBoxLayout(logo_container)
        logo_layout.setContentsMargins(0, 5, 10, 5)
        logo_layout.setSpacing(4)  # Espaçamento reduzido
        
        # Logo SVG animada
        logo_path = os.path.join(script_dir, 'dml_logo.svg')
        self.logo_widget = QSvgWidget(logo_path)
        self.logo_widget.setFixedSize(100, 40)  # Tamanho reduzido
        
        # Botão de doação
        self.donate_button = QPushButton("Doação")
        self.donate_button.setFixedSize(100, 25)  # Tamanho reduzido
        self.donate_button.setToolTip(self.tr('donate_button'))
        self.donate_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 3px;
                padding: 4px 8px;
                font-weight: 500;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #388E3C;
            }
            QPushButton:pressed {
                background-color: #2E7D32;
            }
        """)
        self.donate_button.clicked.connect(self.show_pix_info)
        
        # Adiciona widgets ao layout vertical
        logo_layout.addWidget(self.logo_widget, alignment=Qt.AlignCenter)
        logo_layout.addWidget(self.donate_button, alignment=Qt.AlignCenter)
        
        layout.addWidget(logo_container, alignment=Qt.AlignRight)
        
        # Abas
        self.tabWidget = QTabWidget()
        layout.addWidget(self.tabWidget)
        
        # Aba de Formatação
        format_tab = QWidget()
        format_layout = QVBoxLayout(format_tab)
        
        self.device_label = QLabel("Selecione o dispositivo USB:")
        format_layout.addWidget(self.device_label)
        
        self.device_combo = QComboBox()
        format_layout.addWidget(self.device_combo)
        
        # Barra de Progresso
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        format_layout.addWidget(self.progress_bar)
        
        self.refresh_button = QPushButton("Atualizar Dispositivos")
        self.refresh_button.clicked.connect(self.refresh_devices)
        format_layout.addWidget(self.refresh_button)
        
        self.format_button = QPushButton("Formatar Dispositivo")
        self.format_button.clicked.connect(self.format_device)
        self.format_button.setObjectName("dangerButton")
        format_layout.addWidget(self.format_button)
        
        # Área de Log
        log_label = QLabel("Log de operações:")
        format_layout.addWidget(log_label)
        
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.setMinimumHeight(100)  # Altura reduzida
        format_layout.addWidget(self.log_area)
        
        # Descrição da distribuição
        self.distro_info = QTextEdit()
        self.distro_info.setReadOnly(True)
        self.distro_info.setMaximumHeight(60)  # Altura reduzida
        format_layout.addWidget(self.distro_info)
        
        self.tabWidget.addTab(format_tab, "Formatar USB")
        
        # Aba de Download
        download_tab = self.create_download_tab()
        self.tabWidget.addTab(download_tab, "Baixar Imagens")
        
        # Nova aba de Gravação
        write_tab = self.create_write_tab()
        self.tabWidget.addTab(write_tab, "Gravar ISO")
        
        # Adiciona o label de créditos no rodapé
        credits_label = QLabel("Desenvolvido por DML Desenvolvimentos")
        credits_label.setAlignment(Qt.AlignCenter)
        credits_label.setStyleSheet("""
            QLabel {
                color: #888888;
                font-size: 10px;
                padding: 5px;
            }
        """)
        layout.addWidget(credits_label)
        
        # Thread de formatação e download
        self.format_thread = None
        self.download_thread = None
        
        # Inicializar lista de dispositivos
        self.refresh_devices()
        
        # Adiciona mensagem inicial ao log
        self.add_to_log("Pronto para formatar. Selecione um dispositivo USB.")
        
        # Atualiza informações da primeira distribuição
        self.update_distro_info(self.distro_combo.currentText())
        
        self.is_downloading = False
        self.is_paused = False
        
        # Cria a barra de menu
        self.create_menu_bar()
        
        # Solicita autenticação no início
        if not get_auth_token():
            QMessageBox.critical(self, "Erro", "É necessário privilégios de administrador para executar este programa.")
            sys.exit(1)
            
        # Inicia com o tema escuro
        self.change_theme("dark")
    
    def create_menu_bar(self):
        menubar = self.menuBar()
        
        # Menu Arquivo
        file_menu = menubar.addMenu(self.tr('file_menu'))
        
        # Ações do menu Arquivo
        refresh_action = file_menu.addAction(self.tr('refresh_devices'))
        refresh_action.triggered.connect(self.refresh_devices)
        
        file_menu.addSeparator()
        
        exit_action = file_menu.addAction(self.tr('exit'))
        exit_action.triggered.connect(self.close)
        
        # Menu Ferramentas
        tools_menu = menubar.addMenu(self.tr('tools_menu'))
        
        # Ações do menu Ferramentas
        format_action = tools_menu.addAction(self.tr('format_usb'))
        format_action.triggered.connect(lambda: self.tabWidget.setCurrentIndex(0))
        
        download_action = tools_menu.addAction(self.tr('download_images'))
        download_action.triggered.connect(lambda: self.tabWidget.setCurrentIndex(1))
        
        write_action = tools_menu.addAction(self.tr('write_iso'))
        write_action.triggered.connect(lambda: self.tabWidget.setCurrentIndex(2))
        
        tools_menu.addSeparator()
        
        check_updates_action = tools_menu.addAction(self.tr('check_updates'))
        check_updates_action.triggered.connect(self.check_distros_updates)
        
        # Menu Configurações
        settings_menu = menubar.addMenu(self.tr('settings_menu'))
        
        # Submenu Tema
        theme_menu = settings_menu.addMenu(self.tr('theme_menu'))
        
        # Ações do submenu Tema
        light_theme_action = theme_menu.addAction(self.tr('light_theme'))
        light_theme_action.triggered.connect(lambda: self.change_theme("light"))
        
        dark_theme_action = theme_menu.addAction(self.tr('dark_theme'))
        dark_theme_action.triggered.connect(lambda: self.change_theme("dark"))
        
        system_theme_action = theme_menu.addAction(self.tr('system_theme'))
        system_theme_action.triggered.connect(lambda: self.change_theme("system"))
        
        # Submenu Idioma
        language_menu = settings_menu.addMenu(self.tr('language_menu'))
        
        # Ações do submenu Idioma
        pt_br_action = language_menu.addAction("Português (Brasil)")
        pt_br_action.triggered.connect(lambda: self.change_language('pt_BR'))
        
        es_action = language_menu.addAction("Español")
        es_action.triggered.connect(lambda: self.change_language('es'))
        
        en_action = language_menu.addAction("English")
        en_action.triggered.connect(lambda: self.change_language('en'))
        
        # Menu Ajuda
        help_menu = menubar.addMenu(self.tr('help_menu'))
        
        # Ações do menu Ajuda
        docs_action = help_menu.addAction(self.tr('documentation'))
        docs_action.triggered.connect(self.show_documentation)
        
        help_menu.addSeparator()
        
        about_action = help_menu.addAction(self.tr('about'))
        about_action.triggered.connect(self.show_about)
        
        report_bug_action = help_menu.addAction(self.tr('report_bug'))
        report_bug_action.triggered.connect(self.report_bug)

    def tr(self, key):
        """Traduz uma chave para o idioma atual"""
        return TRANSLATIONS[self.current_language].get(key, key)

    def change_language(self, language):
        """Muda o idioma da interface"""
        if language in TRANSLATIONS:
            self.current_language = language
            self.retranslate_ui()

    def retranslate_ui(self):
        """Atualiza todos os textos da interface para o idioma atual"""
        # Atualiza o menu
        self.menuBar().clear()
        self.create_menu_bar()
        
        # Atualiza as abas
        self.tabWidget.setTabText(0, self.tr('format_usb'))
        self.tabWidget.setTabText(1, self.tr('download_images'))
        self.tabWidget.setTabText(2, self.tr('write_iso'))
        
        # Atualiza os labels e botões da aba de formatação
        self.device_label.setText(self.tr('select_device'))
        self.refresh_button.setText(self.tr('refresh_devices'))
        self.format_button.setText(self.tr('format_device'))
        
        # Atualiza os labels e botões da aba de download
        self.update_urls_button.setText(self.tr('check_updates'))
        self.download_button.setText(self.tr('download_image'))
        self.pause_button.setText(self.tr('pause'))
        self.stop_button.setText(self.tr('stop'))
        
        # Atualiza os labels e botões da aba de gravação
        self.write_button.setText(self.tr('write_button'))
        self.stop_write_button.setText(self.tr('cancel'))
        
        # Atualiza o botão de doação
        self.donate_button.setToolTip(self.tr('donate_button'))
    
    def change_theme(self, theme):
        """Altera o tema da aplicação"""
        if theme == "light":
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #f5f5f5;
                }
                QWidget {
                    background-color: #ffffff;
                    color: #000000;
                }
                QLabel {
                    color: #000000;
                    background-color: transparent;
                }
                QTextEdit {
                    background-color: #ffffff;
                    color: #000000;
                    border: 1px solid #cccccc;
                    padding: 4px;
                }
                QComboBox {
                    background-color: #ffffff;
                    color: #000000;
                    border: 1px solid #cccccc;
                    padding: 4px;
                    min-height: 20px;
                }
                QComboBox::drop-down {
                    border: none;
                }
                QComboBox::down-arrow {
                    image: none;
                    border: none;
                }
                QPushButton {
                    background-color: #2196F3;
                    color: white;
                    border: none;
                    padding: 6px 12px;
                    border-radius: 3px;
                    font-weight: 500;
                    min-width: 80px;
                }
                QPushButton:hover {
                    background-color: #1976D2;
                }
                QPushButton:pressed {
                    background-color: #0D47A1;
                }
                QPushButton:disabled {
                    background-color: #BDBDBD;
                    color: #757575;
                }
                QPushButton#dangerButton {
                    background-color: #f44336;
                }
                QPushButton#dangerButton:hover {
                    background-color: #d32f2f;
                }
                QPushButton#successButton {
                    background-color: #4CAF50;
                }
                QPushButton#successButton:hover {
                    background-color: #388E3C;
                }
                QMenuBar {
                    background-color: #f5f5f5;
                    color: #000000;
                    border-bottom: 1px solid #cccccc;
                }
                QMenuBar::item {
                    background-color: transparent;
                    color: #000000;
                    padding: 4px 8px;
                }
                QMenuBar::item:selected {
                    background-color: #2196F3;
                    color: white;
                }
                QMenu {
                    background-color: #ffffff;
                    color: #000000;
                    border: 1px solid #cccccc;
                }
                QMenu::item {
                    background-color: transparent;
                    color: #000000;
                    padding: 4px 20px;
                }
                QMenu::item:selected {
                    background-color: #2196F3;
                    color: white;
                }
                QProgressBar {
                    border: 1px solid #cccccc;
                    background-color: #ffffff;
                    color: #000000;
                    text-align: center;
                    height: 16px;
                }
                QProgressBar::chunk {
                    background-color: #2196F3;
                }
                QLineEdit {
                    background-color: #ffffff;
                    color: #000000;
                    border: 1px solid #cccccc;
                    padding: 4px;
                }
                QTabWidget::pane {
                    border: 1px solid #cccccc;
                    background-color: #ffffff;
                }
                QTabBar::tab {
                    background-color: #f5f5f5;
                    color: #000000;
                    border: 1px solid #cccccc;
                    padding: 6px 12px;
                }
                QTabBar::tab:selected {
                    background-color: #ffffff;
                    border-bottom: none;
                }
            """)
        elif theme == "dark":
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #1e1e1e;
                }
                QWidget {
                    background-color: #2d2d2d;
                    color: #ffffff;
                }
                QLabel {
                    color: #ffffff;
                    background-color: transparent;
                }
                QTextEdit {
                    background-color: #2d2d2d;
                    color: #ffffff;
                    border: 1px solid #3d3d3d;
                    padding: 4px;
                }
                QComboBox {
                    background-color: #2d2d2d;
                    color: #ffffff;
                    border: 1px solid #3d3d3d;
                    padding: 4px;
                    min-height: 20px;
                }
                QComboBox::drop-down {
                    border: none;
                }
                QComboBox::down-arrow {
                    image: none;
                    border: none;
                }
                QPushButton {
                    background-color: #2196F3;
                    color: white;
                    border: none;
                    padding: 6px 12px;
                    border-radius: 3px;
                    font-weight: 500;
                    min-width: 80px;
                }
                QPushButton:hover {
                    background-color: #1976D2;
                }
                QPushButton:pressed {
                    background-color: #0D47A1;
                }
                QPushButton:disabled {
                    background-color: #424242;
                    color: #757575;
                }
                QPushButton#dangerButton {
                    background-color: #f44336;
                }
                QPushButton#dangerButton:hover {
                    background-color: #d32f2f;
                }
                QPushButton#successButton {
                    background-color: #4CAF50;
                }
                QPushButton#successButton:hover {
                    background-color: #388E3C;
                }
                QMenuBar {
                    background-color: #1e1e1e;
                    color: #ffffff;
                    border-bottom: 1px solid #3d3d3d;
                }
                QMenuBar::item {
                    background-color: transparent;
                    color: #ffffff;
                    padding: 4px 8px;
                }
                QMenuBar::item:selected {
                    background-color: #2196F3;
                    color: white;
                }
                QMenu {
                    background-color: #2d2d2d;
                    color: #ffffff;
                    border: 1px solid #3d3d3d;
                }
                QMenu::item {
                    background-color: transparent;
                    color: #ffffff;
                    padding: 4px 20px;
                }
                QMenu::item:selected {
                    background-color: #2196F3;
                    color: white;
                }
                QProgressBar {
                    border: 1px solid #3d3d3d;
                    background-color: #2d2d2d;
                    color: #ffffff;
                    text-align: center;
                    height: 16px;
                }
                QProgressBar::chunk {
                    background-color: #2196F3;
                }
                QLineEdit {
                    background-color: #2d2d2d;
                    color: #ffffff;
                    border: 1px solid #3d3d3d;
                    padding: 4px;
                }
                QTabWidget::pane {
                    border: 1px solid #3d3d3d;
                    background-color: #2d2d2d;
                }
                QTabBar::tab {
                    background-color: #1e1e1e;
                    color: #ffffff;
                    border: 1px solid #3d3d3d;
                    padding: 6px 12px;
                }
                QTabBar::tab:selected {
                    background-color: #2d2d2d;
                    border-bottom: none;
                }
            """)
        else:  # system
            self.setStyleSheet("")  # Remove estilos personalizados
    
    def show_documentation(self):
        """Mostra a documentação do programa"""
        QMessageBox.information(self, self.tr('documentation'), 
            f"Formatador USB para Linux - Manual do Usuário\n\n"
            "1. Formatação USB:\n"
            "   • Selecione um dispositivo USB na lista\n"
            "   • Clique em 'Formatar Dispositivo'\n"
            "   • Confirme a operação\n"
            "   • Aguarde a conclusão do processo\n\n"
            "2. Download de Imagens:\n"
            "   • Escolha uma distribuição Linux\n"
            "   • Verifique a descrição e tamanho\n"
            "   • Clique em 'Baixar Imagem'\n"
            "   • Selecione local para salvar\n"
            "   • Controle: Pausar/Continuar/Cancelar\n\n"
            "3. Gravação de ISO:\n"
            "   • Selecione arquivo ISO no computador\n"
            "   • Escolha dispositivo USB destino\n"
            "   • Clique em 'Gravar ISO'\n"
            "   • Aguarde a conclusão\n\n"
            "4. Recursos Adicionais:\n"
            "   • Temas: Claro/Escuro/Sistema\n"
            "   • Idiomas: Português/Español/English\n"
            "   • Verificação de atualizações\n"
            "   • Suporte a múltiplos sistemas de arquivos\n\n"
            "5. Requisitos:\n"
            "   • Sistema Linux\n"
            "   • Privilégios de administrador\n"
            "   • Python 3.6 ou superior\n"
            "   • Bibliotecas: PySide6, pyudev\n\n"
            "Para suporte adicional:\n"
            "Email: danmuciolemos@gmail.com\n"
            "GitHub: github.com/dmldev/formatador-usb"
        )
    
    def report_bug(self):
        """Abre a página para reportar problemas"""
        QMessageBox.information(self, self.tr('report_bug'),
            f"{self.tr('report_bug')}:\n"
            "https://github.com/seu-usuario/formatador-usb/issues\n\n"
            "Email:\n"
            "suporte@formatadorusb.com.br"
        )
    
    def show_pix_info(self):
        """Mostra a informação do PIX"""
        QMessageBox.information(self, 
            self.tr('donate_title'),
            self.tr('donate_message')
        )
    
    def show_about(self):
        about_dialog = AboutDialog(self)
        about_dialog.exec()
    
    def add_to_log(self, message):
        self.log_area.append(message)
        # Rola para o final do log
        self.log_area.verticalScrollBar().setValue(
            self.log_area.verticalScrollBar().maximum()
        )
    
    def run_command(self, command):
        """Executa um comando com sudo"""
        try:
            cmd = ['sudo']
            cmd.extend(shlex.split(command))
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"Erro ao executar comando: {command}")
            print(f"Saída de erro: {e.stderr}")
            raise e
    
    def refresh_devices(self):
        self.device_combo.clear()
        self.add_to_log("Atualizando lista de dispositivos...")
        context = pyudev.Context()
        
        # Filtra dispositivos removíveis (USB, HDD externo, etc)
        removable = [device for device in context.list_devices(subsystem='block')
                    if device.get('ID_BUS') in ['usb', 'scsi', 'ata'] and 
                    device.get('ID_TYPE') == 'disk' and 
                    not device.get('DEVNAME', '').endswith(('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'))]
        
        for device in removable:
            device_name = device.get('DEVNAME')
            try:
                size_bytes = int(self.run_command(f"blockdev --getsize64 {device_name}"))
                size_gb = size_bytes / (1024**3)
                model = device.get('ID_MODEL', '').replace('_', ' ') or "Dispositivo Removível"
                bus_type = device.get('ID_BUS', '').upper()
                self.device_combo.addItem(f"{model} ({device_name}) - {size_gb:.1f} GB [{bus_type}]", device_name)
                self.add_to_log(f"Encontrado dispositivo: {model} em {device_name} ({size_gb:.1f} GB) [{bus_type}]")
            except Exception as e:
                self.add_to_log(f"Erro ao ler dispositivo {device_name}: {str(e)}")
                continue
        
        if self.device_combo.count() == 0:
            self.add_to_log("Nenhum dispositivo removível encontrado.")
    
    def update_progress(self, percent, message):
        self.progress_bar.setValue(percent)
        self.add_to_log(message)
    
    def format_finished(self, success, message):
        self.format_button.setEnabled(True)
        self.refresh_button.setEnabled(True)
        
        if success:
            self.add_to_log(message)
            QMessageBox.information(self, "Sucesso", message)
            self.refresh_devices()
        else:
            self.add_to_log(f"ERRO: {message}")
            QMessageBox.critical(self, "Erro", message)
    
    def format_device(self):
        if self.device_combo.currentIndex() == -1:
            QMessageBox.warning(self, "Erro", "Por favor, selecione um dispositivo USB")
            return
        
        device = self.device_combo.currentData()
        reply = QMessageBox.warning(
            self,
            "Confirmação",
            f"ATENÇÃO: Isso irá apagar TODOS os dados em {device}.\nTem certeza que deseja continuar?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Desabilita os botões durante a formatação
            self.format_button.setEnabled(False)
            self.refresh_button.setEnabled(False)
            
            # Reseta a barra de progresso
            self.progress_bar.setValue(0)
            self.add_to_log(f"\nIniciando formatação do dispositivo {device}...")
            
            # Inicia a thread de formatação
            self.format_thread = FormatThread(self.format_script, device)
            self.format_thread.progress_updated.connect(self.update_progress)
            self.format_thread.finished.connect(self.format_finished)
            self.format_thread.start()
    
    def update_distro_info(self, distro_name):
        if distro_name in DISTROS:
            url = DISTROS[distro_name]["url"]
            pattern = DISTROS[distro_name]["pattern"]
            description = DISTROS[distro_name]["description"]
            
            # Verifica o link principal
            status = check_link_status(url)
            if not status:
                # Se o link principal estiver indisponível, busca um alternativo
                self.add_to_download_log(f"Link principal indisponível para {distro_name}, buscando alternativa...")
                alternative_url = find_alternative_link(distro_name, pattern)
                
                if alternative_url:
                    # Atualiza a URL no dicionário DISTROS
                    DISTROS[distro_name]["url"] = alternative_url
                    url = alternative_url
                    status = True
                    self.add_to_download_log(f"Link alternativo definido para {distro_name}")
            
            size = self.get_iso_size(url)
            status_text = "Link disponível" if status else "Link indisponível"
            self.distro_info.setText(f"{description}\n\nTamanho do arquivo: {size}\nStatus: {status_text}")
            self.add_to_download_log(f"Tamanho da imagem {distro_name}: {size} - {status_text}")
    
    def create_download_tab(self):
        download_tab = QWidget()
        download_layout = QVBoxLayout(download_tab)
        
        # Container para botões superiores
        top_button_container = QWidget()
        top_button_layout = QHBoxLayout(top_button_container)
        
        # Botão de atualizar URLs
        self.update_urls_button = QPushButton("Verificar Atualizações")
        self.update_urls_button.clicked.connect(self.check_distros_updates)
        top_button_layout.addWidget(self.update_urls_button)
        
        download_layout.addWidget(top_button_container)
        
        # Seleção de distribuição
        distro_label = QLabel("Selecione a distribuição Linux:")
        download_layout.addWidget(distro_label)
        
        self.distro_combo = QComboBox()
        for distro in DISTROS:
            self.distro_combo.addItem(distro)
        
        self.distro_combo.currentTextChanged.connect(self.update_distro_info)
        download_layout.addWidget(self.distro_combo)
        
        # Descrição da distribuição
        self.distro_info = QTextEdit()
        self.distro_info.setReadOnly(True)
        self.distro_info.setMaximumHeight(60)  # Altura reduzida
        download_layout.addWidget(self.distro_info)
        
        # Container para progresso e velocidade
        progress_container = QWidget()
        progress_layout = QVBoxLayout(progress_container)
        
        # Barra de progresso
        self.download_progress = QProgressBar()
        self.download_progress.setMinimum(0)
        self.download_progress.setMaximum(100)
        self.download_progress.setValue(0)
        progress_layout.addWidget(self.download_progress)
        
        # Label para velocidade e tempo restante
        self.speed_label = QLabel("Velocidade: -- | ETA: --")
        progress_layout.addWidget(self.speed_label)
        
        download_layout.addWidget(progress_container)
        
        # Container para botões
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        
        # Botões de controle
        self.download_button = QPushButton("Baixar Imagem")
        self.download_button.clicked.connect(self.start_download)
        self.download_button.setObjectName("successButton")
        button_layout.addWidget(self.download_button)
        
        self.pause_button = QPushButton("Pausar")
        self.pause_button.clicked.connect(self.toggle_pause_download)
        self.pause_button.setEnabled(False)
        button_layout.addWidget(self.pause_button)
        
        self.stop_button = QPushButton("Parar")
        self.stop_button.clicked.connect(self.stop_download)
        self.stop_button.setObjectName("dangerButton")
        button_layout.addWidget(self.stop_button)
        
        download_layout.addWidget(button_container)
        
        # Log de download
        download_log_label = QLabel("Log de download:")
        download_layout.addWidget(download_log_label)
        
        self.download_log = QTextEdit()
        self.download_log.setReadOnly(True)
        self.download_log.setMinimumHeight(100)  # Altura reduzida
        download_layout.addWidget(self.download_log)
        
        # Ajuste de margens e espaçamentos
        download_layout.setContentsMargins(8, 8, 8, 8)  # Margens reduzidas
        download_layout.setSpacing(6)  # Espaçamento reduzido
        
        return download_tab
    
    def toggle_pause_download(self):
        if not self.download_thread:
            return
            
        if self.is_paused:
            self.download_thread.resume()
            self.pause_button.setText("Pausar")
            self.add_to_download_log("Download resumido")
        else:
            self.download_thread.pause()
            self.pause_button.setText("Continuar")
            self.add_to_download_log("Download pausado")
        
        self.is_paused = not self.is_paused
    
    def stop_download(self):
        if not self.download_thread:
            return
            
        reply = QMessageBox.question(
            self,
            "Confirmar",
            "Tem certeza que deseja cancelar o download?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.download_thread.stop()
            self.add_to_download_log("Download cancelado.")
            self.download_button.setEnabled(True)
            self.pause_button.setEnabled(False)
            self.stop_button.setEnabled(False)
            self.download_progress.setValue(0)
            self.speed_label.setText("Velocidade: -- | ETA: --")
            self.is_downloading = False
            self.is_paused = False
            self.pause_button.setText("Pausar")
    
    def start_download(self):
        distro_name = self.distro_combo.currentText()
        if distro_name not in DISTROS:
            return
        
        url = DISTROS[distro_name]["url"]
        
        save_path, _ = QFileDialog.getSaveFileName(
            self,
            "Salvar Imagem ISO",
            f"{distro_name.lower().replace(' ', '-')}.iso",
            "Arquivos ISO (*.iso)"
        )
        
        if not save_path:
            return
        
        # Atualiza estado dos botões
        self.download_button.setEnabled(False)
        self.pause_button.setEnabled(True)
        self.stop_button.setEnabled(True)
        self.download_progress.setValue(0)
        self.speed_label.setText("Velocidade: -- | ETA: --")
        self.add_to_download_log(f"Iniciando download de {distro_name}...")
        
        # Inicia o download
        self.download_thread = DownloadThread(url, save_path)
        self.download_thread.progress_updated.connect(self.update_download_progress)
        self.download_thread.finished.connect(self.download_finished)
        self.download_thread.start()
        self.is_downloading = True
    
    def update_download_progress(self, percent, status_text):
        self.download_progress.setValue(percent)
        self.speed_label.setText(status_text)
        
    def download_finished(self, success, message):
        self.download_button.setEnabled(True)
        self.pause_button.setEnabled(False)
        self.stop_button.setEnabled(False)
        self.is_downloading = False
        self.is_paused = False
        self.pause_button.setText("Pausar")
        
        if success:
            self.add_to_download_log(message)
            QMessageBox.information(self, "Sucesso", message)
        else:
            self.add_to_download_log(f"ERRO: {message}")
            QMessageBox.critical(self, "Erro", message)
        
        self.speed_label.setText("Velocidade: -- | ETA: --")

    def add_to_download_log(self, message):
        """Adiciona uma mensagem ao log de download"""
        self.download_log.append(message)
        # Rola para o final do log
        self.download_log.verticalScrollBar().setValue(
            self.download_log.verticalScrollBar().maximum()
        )

    def check_distros_updates(self):
        """Verifica e atualiza as URLs das distribuições"""
        self.update_urls_button.setEnabled(False)
        self.add_to_download_log("Iniciando verificação de atualizações...")
        
        self.update_thread = UpdateDistrosThread()
        self.update_thread.progress_updated.connect(self.add_to_download_log)
        self.update_thread.finished.connect(self.update_distros_finished)
        self.update_thread.start()
    
    def update_distros_finished(self, updated_distros):
        """Chamado quando a verificação de atualizações termina"""
        global DISTROS
        DISTROS = updated_distros
        
        # Atualiza o combo box mantendo a mesma ordem
        current_distro = self.distro_combo.currentText()
        self.distro_combo.clear()
        
        # Adiciona as distribuições na ordem original
        for distro in DISTROS.keys():
            self.distro_combo.addItem(distro)
        
        # Tenta restaurar a seleção anterior
        index = self.distro_combo.findText(current_distro)
        if index >= 0:
            self.distro_combo.setCurrentIndex(index)
        elif self.distro_combo.count() > 0:
            self.distro_combo.setCurrentIndex(0)
        
        self.update_urls_button.setEnabled(True)
        self.add_to_download_log("\nVerificação de atualizações concluída!")
        self.add_to_download_log("Links das distribuições foram verificados e atualizados quando necessário.")
        
        # Atualiza a descrição da distribuição atual
        self.update_distro_info(self.distro_combo.currentText())

    def get_iso_size(self, url):
        """Obtém o tamanho do arquivo ISO em bytes"""
        try:
            response = requests.head(url)
            if 'content-length' in response.headers:
                size = int(response.headers['content-length'])
                return humanize.naturalsize(size, binary=True)
            return "Tamanho desconhecido"
        except:
            return "Tamanho desconhecido"

    def create_write_tab(self):
        write_tab = QWidget()
        write_layout = QVBoxLayout(write_tab)
        
        # Seleção do arquivo ISO
        iso_container = QWidget()
        iso_layout = QHBoxLayout(iso_container)
        
        self.iso_path_edit = QLineEdit()
        self.iso_path_edit.setReadOnly(True)
        iso_layout.addWidget(self.iso_path_edit)
        
        browse_button = QPushButton("Selecionar ISO")
        browse_button.clicked.connect(self.browse_iso)
        iso_layout.addWidget(browse_button)
        
        write_layout.addWidget(QLabel("Arquivo ISO:"))
        write_layout.addWidget(iso_container)
        
        # Seleção do dispositivo USB
        write_layout.addWidget(QLabel("Dispositivo USB:"))
        self.write_device_combo = QComboBox()
        write_layout.addWidget(self.write_device_combo)
        
        # Botão para atualizar lista de dispositivos
        refresh_devices_button = QPushButton("Atualizar Dispositivos")
        refresh_devices_button.clicked.connect(self.refresh_write_devices)
        write_layout.addWidget(refresh_devices_button)
        
        # Barra de Progresso
        self.write_progress = QProgressBar()
        self.write_progress.setMinimum(0)
        self.write_progress.setMaximum(100)
        write_layout.addWidget(self.write_progress)
        
        # Botões de controle
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        
        self.write_button = QPushButton("Gravar ISO")
        self.write_button.clicked.connect(self.start_write)
        self.write_button.setObjectName("successButton")
        button_layout.addWidget(self.write_button)
        
        self.stop_write_button = QPushButton("Cancelar")
        self.stop_write_button.clicked.connect(self.stop_write)
        self.stop_write_button.setObjectName("dangerButton")
        button_layout.addWidget(self.stop_write_button)
        
        write_layout.addWidget(button_container)
        
        # Log de gravação
        write_layout.addWidget(QLabel("Log de gravação:"))
        self.write_log = QTextEdit()
        self.write_log.setReadOnly(True)
        self.write_log.setMinimumHeight(100)  # Altura reduzida
        write_layout.addWidget(self.write_log)
        
        # Ajuste de margens e espaçamentos
        write_layout.setContentsMargins(8, 8, 8, 8)  # Margens reduzidas
        write_layout.setSpacing(6)  # Espaçamento reduzido
        
        # Inicializa a lista de dispositivos
        self.refresh_write_devices()
        
        return write_tab

    def browse_iso(self):
        """Abre diálogo para selecionar arquivo ISO"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Selecionar Arquivo ISO",
            "",
            "Arquivos ISO (*.iso);;Todos os Arquivos (*.*)"
        )
        if file_path:
            self.iso_path_edit.setText(file_path)

    def refresh_write_devices(self):
        """Atualiza a lista de dispositivos removíveis disponíveis"""
        self.write_device_combo.clear()
        self.add_to_write_log("Atualizando lista de dispositivos...")
        context = pyudev.Context()
        
        # Filtra dispositivos removíveis (USB, HDD externo, etc)
        removable = [device for device in context.list_devices(subsystem='block')
                    if device.get('ID_BUS') in ['usb', 'scsi', 'ata'] and 
                    device.get('ID_TYPE') == 'disk' and 
                    not device.get('DEVNAME', '').endswith(('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'))]
        
        for device in removable:
            device_name = device.get('DEVNAME')
            try:
                size_bytes = int(self.run_command(f"blockdev --getsize64 {device_name}"))
                size_gb = size_bytes / (1024**3)
                model = device.get('ID_MODEL', '').replace('_', ' ') or "Dispositivo Removível"
                bus_type = device.get('ID_BUS', '').upper()
                self.write_device_combo.addItem(f"{model} ({device_name}) - {size_gb:.1f} GB [{bus_type}]", device_name)
                self.add_to_write_log(f"Encontrado dispositivo: {model} em {device_name} ({size_gb:.1f} GB) [{bus_type}]")
            except Exception as e:
                self.add_to_write_log(f"Erro ao ler dispositivo {device_name}: {str(e)}")
                continue
        
        if self.write_device_combo.count() == 0:
            self.add_to_write_log("Nenhum dispositivo removível encontrado.")

    def add_to_write_log(self, message):
        """Adiciona uma mensagem ao log de gravação"""
        self.write_log.append(message)
        self.write_log.verticalScrollBar().setValue(
            self.write_log.verticalScrollBar().maximum()
        )

    def update_write_progress(self, percent, message):
        """Atualiza a barra de progresso e o log durante a gravação"""
        self.write_progress.setValue(percent)
        self.add_to_write_log(message)

    def write_finished(self, success, message):
        """Chamado quando a gravação é concluída"""
        self.write_button.setEnabled(True)
        self.stop_write_button.setEnabled(False)
        self.write_progress.setValue(0)
        
        if success:
            self.add_to_write_log(message)
            QMessageBox.information(self, "Sucesso", message)
        else:
            self.add_to_write_log(f"ERRO: {message}")
            QMessageBox.critical(self, "Erro", message)

    def start_write(self):
        """Inicia o processo de gravação da ISO"""
        if not self.iso_path_edit.text():
            QMessageBox.warning(self, "Erro", "Por favor, selecione um arquivo ISO")
            return
        
        if self.write_device_combo.currentIndex() == -1:
            QMessageBox.warning(self, "Erro", "Por favor, selecione um dispositivo USB")
            return
        
        device = self.write_device_combo.currentData()
        
        reply = QMessageBox.warning(
            self,
            "Confirmação",
            f"ATENÇÃO: Isso irá apagar TODOS os dados em {device} e gravar a imagem ISO selecionada.\n"
            "Tem certeza que deseja continuar?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.write_button.setEnabled(False)
            self.stop_write_button.setEnabled(True)
            self.write_progress.setValue(0)
            self.add_to_write_log(f"\nIniciando gravação da ISO em {device}...")
            
            self.write_thread = WriteISOThread(self.iso_path_edit.text(), device)
            self.write_thread.progress_updated.connect(self.update_write_progress)
            self.write_thread.finished.connect(self.write_finished)
            self.write_thread.start()

    def stop_write(self):
        """Cancela o processo de gravação"""
        if hasattr(self, 'write_thread') and self.write_thread.isRunning():
            reply = QMessageBox.question(
                self,
                "Confirmar",
                "Tem certeza que deseja cancelar a gravação?",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                self.write_thread.stop()
                self.add_to_write_log("Cancelando gravação...")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = USBFormatter()
    window.show()
    sys.exit(app.exec()) 