import logging
from rest_framework.views import APIView
from rest_framework.response import Response

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


class SampleView(APIView):
    def get(self, request):
        return Response({"message": "Welcome to API v1!"})
