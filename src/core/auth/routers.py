from fastapi import APIRouter
from . import endpoints_auth, endpoints_types, endppoints_users

router = APIRouter()


router.include_router(endppoints_users.router, prefix='/users')
router.include_router(endpoints_types.router, prefix='/users-types')
router.include_router(endpoints_auth.router, prefix='/auth')