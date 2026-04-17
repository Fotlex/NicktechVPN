from celery import shared_task
import requests
from django.utils import timezone
from datetime import timedelta

from backend.core.config import config



