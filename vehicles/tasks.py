import asyncio
from itertools import chain

import httpx

from .models import Manufacturer, CarModel

_MANUFACTURERS_URL = 'https://vpic.nhtsa.dot.gov/api/vehicles/getallmakes?format=json'
_MODELS_URL = 'https://vpic.nhtsa.dot.gov/api/vehicles/getmodelsformakeid/{}?format=json'


def fetch_manufacturers_and_models():
    """
    Updates car manufacturers and models
    """
    manufacturers_data = httpx.get(_MANUFACTURERS_URL).json()
    manufacturers_by_id = manufacturers_data['Results']
    manufacturers_by_id = {m['Make_ID']: m['Make_Name'] for m in manufacturers_by_id.items()}
    old_manufacturer_ids = set(Manufacturer.objects.values_list('id', flat=True))

    new_manufacturers = [
        Manufacturer(_id, name)
        for _id, name in manufacturers_by_id.items()
        if _id not in old_manufacturer_ids
    ]
    Manufacturer.objects.bulk_create(new_manufacturers)

    manufacturer_ids = Manufacturer.objects.values_list('id', flat=True)
    old_model_ids = set(CarModel.objects.values_list('id', flat=True))

    batch_size = 50
    batch_cursor = 0

    async with httpx.AsyncClient() as httpx_client:
        while batch_ids := manufacturer_ids[batch_cursor:batch_cursor + batch_size]:
            models_responses = asyncio.gather(*[
                httpx_client.get(_MANUFACTURERS_URL.format(_id)) for _id in batch_ids
            ])
            models_data = chain([data.json()['Results'] for data in models_responses])
            models_data = {
                {
                    'id': model['Model_ID'],
                    'manufacturer': model['Make_ID'],
                    'name': model['Model_Name']
                } for model in models_data
            }

            new_models = [
                CarModel(*model_data)
                for model_data in models_data
                if model_data['id'] not in old_model_ids
            ]
            CarModel.objects.bulk_create(new_models)

            batch_cursor += batch_size
