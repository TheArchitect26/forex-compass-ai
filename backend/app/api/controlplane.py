from fastapi import APIRouter
from app.engines.operator_control_plane import control_plane_status, control_plane_summary, top_actions, console_sprawl, focus_view, control_plane_memory

router = APIRouter()


@router.get('/status')
async def get_control_plane_status():
    return control_plane_status()


@router.post('/summary')
async def post_control_plane_summary(body: dict):
    return control_plane_summary(body)


@router.post('/top-actions')
async def post_control_plane_top_actions(body: dict):
    return top_actions(body)


@router.post('/console-sprawl')
async def post_control_plane_console_sprawl(body: dict):
    return console_sprawl(body)


@router.post('/focus-view')
async def post_control_plane_focus_view(body: dict):
    return focus_view(body)


@router.get('/memory')
async def get_control_plane_memory():
    return control_plane_memory()
