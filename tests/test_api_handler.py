import pytest
import requests

from src.api_handler import HeadHunterAPI


@pytest.fixture
def mock_hh_response_data():
    """Фикстура, имитирующая ответ от HH API с одним элементом."""
    return {
        "items": [
            {
                "id": "1",
                "name": "Тестовая Вакансия 1",
                "alternate_url": "http://test.com/vac1",
                "salary": {"from": 1000, "to": 2000, "currency": "RUR", "gross": False},
                "employer": {"name": "Тестовая Компания"},
                "snippet": {"requirement": "Test Req", "responsibility": "Test Resp"},
            }
        ],
        "found": 1,
        "pages": 1,
        "per_page": 10,
        "page": 0,
    }


def test_headhunter_api_get_vacancies_success(requests_mock, mock_hh_response_data):
    """Тестирует успешное получение вакансий от HeadHunter API."""
    api = HeadHunterAPI()
    search_query = "Python разработчик"
    requests_mock.get(api._base_url, json=mock_hh_response_data, status_code=200)

    vacancies = api.get_vacancies(search_query)

    assert isinstance(vacancies, list)
    assert len(vacancies) == 1
    assert vacancies[0]["name"] == "Тестовая Вакансия 1"
    assert requests_mock.call_count == 1
    assert requests_mock.last_request.qs == {
        "text": ["python разработчик"],
        "per_page": ["10"],
        "page": ["0"],
    }


def test_headhunter_api_get_vacancies_no_results(requests_mock):
    """Тестирует случай, когда нет результатов."""
    api = HeadHunterAPI()
    search_query = "Очень редкая вакансия"

    mock_empty_data = {"items": [], "found": 0, "pages": 0, "per_page": 10, "page": 0}
    requests_mock.get(api._base_url, json=mock_empty_data, status_code=200)

    vacancies = api.get_vacancies(search_query)

    assert isinstance(vacancies, list)
    assert len(vacancies) == 0


def test_headhunter_api_get_vacancies_http_error(requests_mock):
    """Тестирует обработку HTTP-ошибок (например, 404, 500) в _make_request."""
    api = HeadHunterAPI()
    search_query = "Ошибка"

    requests_mock.get(api._base_url, status_code=404)

    with pytest.raises(requests.exceptions.HTTPError):
        api.get_vacancies(search_query)


def test_headhunter_api_headers(requests_mock):
    api = HeadHunterAPI()
    search_query = "Заголовки"

    requests_mock.get(api._base_url, json={"items": []}, status_code=200)
    api.get_vacancies(search_query)

    assert requests_mock.last_request.headers["User-Agent"] == "Mozilla/5.0"


def test_headhunter_api_connect():
    api = HeadHunterAPI()
    try:
        api.connect_to_api()
        assert True
    except Exception:
        pytest.fail("connect_to_api raised an unexpected exception!")
