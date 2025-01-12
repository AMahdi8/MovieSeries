from model_bakery import baker
from .models import *

genre = baker.make(Genre, _quantity=10)