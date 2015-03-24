# -*- coding: utf-8 -*-
from models import EveCharacter
from models import EveApiKeyPair
from models import EveAllianceInfo
from models import EveCorporationInfo
from models import AuthInfo
from models import User

import datetime as dt

from recruit_app.user.eve_api_manager import EveApiManager

from recruit_app.extensions import bcrypt

from redis import Redis
redis_conn = Redis()

from rq.decorators import job

from flask import flash


