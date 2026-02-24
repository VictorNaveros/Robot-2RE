from ultralytics import YOLO
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RUTA_MODELO = os.path.join(BASE_DIR, "yolov8n.pt")

# Descargar modelo automáticamente si no existe
def get_modelo():
    if not os.path.exists(RUTA_MODELO):
        print("📥 Descargando modelo YOLO por primera vez...")
        modelo_temp = YOLO('yolov8n.pt')
        # YOLO lo descarga automáticamente a ~/.cache/
        import shutil
        cache_path = os.path.expanduser('~/.cache/ultralytics/yolov8n.pt')
        if os.path.exists(cache_path):
            shutil.copy(cache_path, RUTA_MODELO)
            print("✅ Modelo YOLO descargado correctamente")
    
    return YOLO(RUTA_MODELO)

modelo = get_modelo()
ID_BOTELLA = 39

def detectar_botella(
    ruta_imagen: str,
    conf: float = 0.25,
    iou: float = 0.3
) -> int:
    """
    Detecta si hay al menos una botella en la imagen.
    
    Args:
        ruta_imagen (str): ruta a la imagen a analizar
        conf (float): confianza mínima
        iou (float): IoU para NMS
    
    Returns:
        int: 1 si hay botella, 0 si no hay
    """
    resultados = modelo(ruta_imagen, conf=conf, iou=iou)
    
    for r in resultados:
        clases = r.boxes.cls.tolist()
        if ID_BOTELLA in clases:
            return 1
    
    return 0