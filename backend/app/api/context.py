from fastapi import APIRouter
from app.engines.personal_alignment import personal_alignment_status, context_status, alignment_score, adaptive_workflow, energy_safeguards, simplification_layer
from app.engines.wisdom_architecture import anti_maximalism
from app.engines.reality_anchoring import reality_status

router = APIRouter()


@router.get('/status')
async def get_context_status():
    return {"context": context_status({}), "no_execution": True, "human_final_authority": True}


@router.get('/alignment-score')
async def get_alignment_score():
    return {"alignment": alignment_score({}), "advisory_only": True}


@router.get('/personal-alignment')
async def get_personal_alignment():
    return {"personal_alignment": personal_alignment_status({}), "no_execution": True}


@router.post('/adaptive-workflow')
async def post_adaptive_workflow(body: dict):
    mode = str(body.get("mode", "simplified_mode"))
    return adaptive_workflow(mode, body)


@router.post('/energy-safeguards')
async def post_energy_safeguards(body: dict):
    return energy_safeguards(body)


@router.post('/simplification-layer')
async def post_simplification_layer(body: dict):
    return simplification_layer(body)


@router.get('/adaptive-restraint')
async def get_adaptive_restraint():
    return {
        "anti_maximalism": anti_maximalism({}),
        "reality_anchoring": reality_status({}),
        "cognitive_sustainability": alignment_score({})["cognitive_sustainability_score"],
        "grounded_adaptation": True,
    }
