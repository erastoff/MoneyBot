# -*- coding: utf-8 -*-
from aiogram import Router

from .calculations_handler import router as calculations_handler_router
from .messages import router as messages_router
from .rates_handler import router as rates_router

router = Router(name="handlers")
router.include_routers(calculations_handler_router, messages_router, rates_router)
