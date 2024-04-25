# -*- coding: utf-8 -*-
import aioredis

from settings import get_settings

cfg = get_settings()

pool = aioredis.from_url(cfg.redis_url)
