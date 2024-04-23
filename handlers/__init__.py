# -*- coding: utf-8 -*-
__author__ = "erastoff (yury.erastov@gmail.com)"

from aiogram import Router


# from . import messages, calculations_handler
from .calculations_handler import router as calculations_handler_router
from .messages import router as messages_router


router = Router(name="handlers")
router.include_routers(calculations_handler_router, messages_router)
