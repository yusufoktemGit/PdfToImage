import os
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pdf2image import convert_from_path

WATCH_FOLDER = r"G:\2026 Sample Picture\Nirvana_Picture"

# Log ayarı
logging.basicConfig(
    filename="PdfToImage.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class PdfHandler(FileSystemEventHandler):

    def on_created(self, event):
        if event.is_directory:
            return

        if event.src_path.lower().endswith(".pdf"):
            self.process_pdf(event.src_path)

    def wait_until_ready(self, file_path, timeout=30):
        start_time = time.time()
        while True:
            try:
                with open(file_path, 'rb'):
                    return True
            except:
                if time.time() - start_time > timeout:
                    return False
                time.sleep(1)

    def process_pdf(self, pdf_path):
        logging.info(f"PDF bulundu: {pdf_path}")

        if not self.wait_until_ready(pdf_path):
            logging.error("Dosya kilitli, işlenemedi.")
            return

        try:
            images = convert_from_path(pdf_path, dpi=200)

            folder = os.path.dirname(pdf_path)
            file_name = os.path.splitext(os.path.basename(pdf_path))[0]

            for i, image in enumerate(images):
                output_path = os.path.join(folder, f"{file_name}_page_{i+1}.jpg")
                image.save(output_path, "JPEG")

            os.remove(pdf_path)
            logging.info("PDF başarıyla dönüştürüldü ve silindi.")

        except Exception as e:
            logging.error(f"Hata: {e}")

if __name__ == "__main__":
    observer = Observer()
    observer.schedule(PdfHandler(), WATCH_FOLDER, recursive=True)
    observer.start()

    logging.info("PdfToImage servisi başlatıldı.")

    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
