import os
from typing import Dict
import requests
import json
from pathlib import Path

_DEFAULT_ENDPOINT = "https://www.jma.go.jp/bosai"

class JMA_Weather(object):
    def __init__(self, jma_endpoint=None, areas=None):
        self.endpoint =jma_endpoint
        if self.endpoint is None:
            self.endpoint = _DEFAULT_ENDPOINT

        self.areas = areas
        if self.areas is None:
            self.areas = self.get_area()

    def get_json(self, url) -> Dict:
        res = requests.get(url)
        if res.status_code == 200:
            return res.json()
        return None

    def get_area(self) -> Dict:
        url = f"{self.endpoint}/common/const/area.json"
        return self.get_json(url)

    def get_contents(self) -> Dict:
        url = f"{self.endpoint}/common/const/contents.json"
        return self.get_json(url)

    def get_amedas_table(self) -> Dict:
        url = f"{self.endpoint}/amedas/const/amedastable.json"
        return self.get_json(url)

    def get_forecast(self, path_code: str) -> Dict:
        url = f"{self.endpoint}/forecast/data/forecast/{path_code}.json"
        return self.get_json(url)

    def get_overview_forecast(self, path_code: str) -> Dict:
        url = f"{self.endpoint}/forecast/data/overview_forecast/{path_code}.json"
        return self.get_json(url)

    def get_overview_week(self, path_code: str) -> Dict:
        url = f"{self.endpoint}/forecast/data/overview_week/{path_code}.json"
        return self.get_json(url)
