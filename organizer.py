import os
import shutil
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

DOWNLOADS_DIR = os.path.expanduser("~/Downloads")
DOCUMENTS_DIR = os.path.expanduser("~/Documents")
TARGET_EXTENSIONS = (".pdf", ".pptx")

def move_matching_files():
    for filename in os.listdir(DOWNLOADS_DIR):
        if filename.lower().endswith(TARGET_EXTENSIONS):
            source_path = os.path.join(DOWNLOADS_DIR, filename)
            dest_path = os.path.join(DOCUMENTS_DIR, filename)
            
            if os.path.isfile(source_path):
                try:
                    shutil.move(source_path, dest_path)
                    print(f"Déplacé : {filename} -> Documents")
                except Exception as e:
                    print(f"Impossible de déplacer {filename} : {e}")

class DownloadHandler(FileSystemEventHandler):
    def on_modified(self, event):
        move_matching_files()

    def on_created(self, event):
        move_matching_files()

if __name__ == "__main__":
    print("Nettoyage des fichiers existants dans Téléchargements...")
    move_matching_files()
    
    print(f"Surveillance de {DOWNLOADS_DIR} pour les PDF et PPTX... (Ctrl+C pour arrêter)")
    event_handler = DownloadHandler()
    observer = Observer()
    observer.schedule(event_handler, DOWNLOADS_DIR, recursive=False)
    observer.start()
    
    try:
        while True:
            time.sleep(2)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

