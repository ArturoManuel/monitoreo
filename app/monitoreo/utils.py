import json
import os

import socket

def request_system_stats(ip):
    try:
        # Conéctate al daemon de monitoreo en worker (puerto 9999)
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((ip, 9999))  # Reemplaza con la IP real de worker

        # Recibe la respuesta en formato JSON
        response = client_socket.recv(4096).decode()
        client_socket.close()

        return json.loads(response)
    
    except ConnectionRefusedError:
        return {"status": 400, "error": "No se pudo conectar al servidor de monitoreo."}
    except socket.timeout:
        return {"status": 500, "error": "El servidor no respondió a tiempo."}
    except Exception as e:
        return {"status": 500, "error": f"Error inesperado: {str(e)}"}

def format_stats(stats):
    # Verifica si el estado es 200, de lo contrario devuelve el mensaje de error
    if stats.get("status") != 200:
        return {
            "status": stats.get("status", 500),
            "error": stats.get("error", "Error desconocido")
        }

    # Formatea solo los datos relevantes cuando la respuesta es exitosa
    resources = stats.get("resources", {})
    uso_cpu = resources.get("cpu_usage", "N/D")
    info_memoria = resources.get("memory_info", {})
    uso_disco = resources.get("disk_usage", {})

    stats_formateadas = {
        "status": 200,
        "uso_cpu": f"{uso_cpu}%",  # Uso de CPU en porcentaje
        "memoria": {
            "total": f"{info_memoria.get('total', 'N/D') / (1024 ** 3):.2f} GB",
            "usada": f"{info_memoria.get('used', 'N/D') / (1024 ** 3):.2f} GB",
            "disponible": f"{info_memoria.get('available', 'N/D') / (1024 ** 3):.2f} GB",
            "porcentaje_usada": f"{info_memoria.get('percent', 'N/D')}%"
        },
        "disco": {
            "usado": f"{uso_disco.get('used', 'N/D') / (1024 ** 3):.2f} GB",
            "libre": f"{uso_disco.get('free', 'N/D') / (1024 ** 3):.2f} GB",
            "porcentaje_usado": f"{uso_disco.get('percent', 'N/D')}%"
        }
    }

    return stats_formateadas