from fastapi import APIRouter, Request
import skin_system

router = APIRouter()
router2 = router  # для совместимости с create_app

@router.get('/signature-verification-key.der')
@skin_system.token_required(0)
def func(request: Request):
    return skin_system.resolve("http://skinsystem.ely.by/signature-verification-key.der")

@router.get('/signature-verification-key.pem')
@skin_system.token_required(0)
def func2(request: Request):
    return skin_system.resolve("http://skinsystem.ely.by/signature-verification-key.pem")
