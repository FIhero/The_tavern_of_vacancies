from abc import ABC, abstractmethod
from typing import List, Optional

import requests


class BaseAPIHandler(ABC):
    def __init__(self):
        self._base_url = ""
        self._headers = {}

    @abstractmethod
    def connect_to_api(self):
        pass

    @abstractmethod
    def get_vacancies(self, query: str) -> List[dict]:
        pass

    def _make_request(self, url: str, params: Optional[dict] = None) -> dict:
        try:
            response = requests.get(url, headers=self._headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе API: {e}")
            raise e


class HeadHunterAPI(BaseAPIHandler):
    def __init__(self):
        super().__init__()
        self._base_url = "https://api.hh.ru/vacancies"
        self._headers = {"User-Agent": "Mozilla/5.0"}

    def connect_to_api(self):
        pass

    def get_vacancies(self, query: str) -> List[dict]:
        params = {"text": query, "per_page": 10, "page": 0}
        response_data = self._make_request(self._base_url, params)

        if "items" in response_data:
            return response_data["items"]
        return []
