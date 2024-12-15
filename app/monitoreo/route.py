
from app.models.monitoreo import SystemStatsRequest
from fastapi import APIRouter, Path , HTTPException, Path, status , Depends
from app.monitoreo.utils import request_system_stats, format_stats
from app.security import get_current_token

router = APIRouter()

@router.post("/system-stats")
async def get_system_stats(
    request_body: SystemStatsRequest, 
    token: str = Depends(get_current_token)
):
    # Obtener las estadísticas del sistema usando la IP proporcionada
    stats = request_system_stats(request_body.ip)

    # Verifica si hubo un error y maneja la respuesta adecuadamente
    if stats.get("status") != 200:
        raise HTTPException(status_code=stats.get("status"), detail=stats.get("error"))

    # Formatea y devuelve los datos relevantes
    formatted_stats = format_stats(stats)
    return formatted_stats

