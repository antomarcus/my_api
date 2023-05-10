from django.test import TestCase
from rest_framework.test import APIClient

class EndpointTests(TestCase):

    def test_predict_view(self):
        client = APIClient()
        input_data = {
              "1":71,
              "2":103,
              "3":111,
              "4 ":155,
              " 5":165,
              "6 ":251,
              "7 ":345,
              " 8":517,
              "9 ":667,
              " 10":965,
              "11 ":1321,
              "12 ":1708,
              "13 ":2223,
              "14 ":2423,
              "15 ":2810,
              "16 ":2944,
              "17 ":2786,
              "18 ":2566,
              "19 ":2327,
              " 20":1751,
              "21 ":1297,
              "22 ":885,
              " 23":517.1,
              "24 ":410,
              "25 ":224,
              " 26":130,
              "27 ":98,
              " 28":79,
              "29 ":76,
              "30 ":57,
              "31 ":51,
              " 32":46,
              "33 ":42
}
        model_url = "/model_Lead/predict"
        response = client.post(model_url, input_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["label"], "Above_MAL")
        self.assertTrue("request_id" in response.data)
        self.assertTrue("status" in response.data)