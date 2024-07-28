import datetime
import re
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from fcm_django.models import FCMDevice
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
