import base64
import os

def lambda_handler(event, context):
    try:
        # 1. Obtener el código del usuario desde el body (asumiendo que event["body"] es un string)
        user_code = event.get("body", "").strip()
        if not user_code:
            return {
                "statusCode": 400,
                "body": "Error: No se proporcionó código. Ejemplo de uso: 'EC2(\"web\") >> RDS(\"db\")'"
            }

        # 2. Plantilla para el diagrama (sin restricciones de seguridad)
        diagram_template = f"""
from diagrams import Diagram
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB

with Diagram("Mi Diagrama", show=False, outformat="png", filename="/tmp/diagram"):
{indent(user_code, '    ')}
"""
        # 3. Ejecutar el código (¡Cuidado! Esto es inseguro en producción)
        exec(diagram_template, {})

        # 4. Leer la imagen generada
        image_path = "/tmp/diagram.png"
        with open(image_path, "rb") as img_file:
            encoded_image = base64.b64encode(img_file.read()).decode("utf-8")

        # 5. Limpiar el archivo temporal (opcional pero recomendado)
        os.remove(image_path)

        # 6. Devolver la imagen en base64
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": f'{{"image": "data:image/png;base64,{encoded_image}"}}'
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": f"Error: {str(e)}"
        }

def indent(text, prefix):
    """Helper para indentar el código del usuario."""
    return "\n".join(
        prefix + line if line.strip() else line  # Respeta líneas vacías
        for line in text.splitlines()
    )
que te parece este codigo eh de recalcar que estoy en un ambiente academico asi que la seguridad no estan importante