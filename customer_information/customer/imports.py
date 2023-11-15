import re
from rest_framework.views import APIView
from rest_framework.views import Response
import json
import requests
from random import randint, randrange
from datetime import date
from dateutil.relativedelta import relativedelta

import uuid
from django.http import HttpResponseRedirect
from django.http import (HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseServerError)
from rest_framework import status
import os
from rest_framework.throttling import UserRateThrottle,AnonRateThrottle

import base64
import random, string

from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization,hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from django.db import transaction

import os
from django.core import serializers
import random