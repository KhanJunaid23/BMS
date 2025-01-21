import logging
import traceback
from django.http import JsonResponse
from rest_framework.views import APIView
from .models import Party, CompanyPartyInvoiceDetails
from .serializers import PartySerializer, CompanyPartyInvoiceSerializer

# Setup logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


class PartyAPIView(APIView):
    def get(self, request, party_id=None, *args, **kwargs):
        try:
            if party_id:
                party = Party.objects.filter(party_id=party_id).first()
                if party is None:
                    return JsonResponse({
                        "error_code": 404,
                        "message": "Party not found",
                        "data": [],
                        "error": []
                    }, status=404)

                serializer = PartySerializer(party)
                logger.info(f"Fetched party: {party.party_id}")
                return JsonResponse({
                    "error_code": 200,
                    "message": "Party found",
                    "data": [serializer.data],
                    "error": []
                }, status=200)

            else:
                partys = Party.objects.all()
                logger.warning("No Partys found")
                if not partys:
                    return JsonResponse({
                        "error_code": 400,
                        "message": "No partys found",
                        "data": [],
                        "error": []
                    }, status=400)

                serializer = PartySerializer(partys, many=True)
                logger.info("Fetched all partys")
                return JsonResponse({
                    "error_code": 200,
                    "message": "Data found",
                    "data": serializer.data,
                    "error": []
                }, status=200)

        except Exception as e:
            return JsonResponse({
                "error_code": 500,
                "message": "Internal Server Error",
                "data": [],
                "error": traceback.format_exc().splitlines()
            }, status=500)

    def post(self, request, *args, **kwargs):
        try:
            serializer = PartySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"Created Party: {serializer.data['party_id']}")

                return JsonResponse({
                    "error_code": 200,
                    "message": "Party created successfully",
                    "data": [serializer.data],
                    "error": []
                }, status=201)

            logger.error(f"Failed to create party: {serializer.errors}")
            return JsonResponse({
                "error_code": 400,
                "message": "Validation failed",
                "data": [],
                "error": serializer.errors
            }, status=400)

        except Exception as e:
            return JsonResponse({
                "error_code": 500,
                "message": "Internal Server Error",
                "data": [],
                "error": traceback.format_exc().splitlines()
            }, status=500)

    def put(self, request, party_id, *args, **kwargs):
        try:
            party = Party.objects.filter(pk=party_id).first()
            if party is None:
                logger.error(f"Party with ID {party_id} not found")
                return JsonResponse({
                    "error_code": 404,
                    "message": "Party not found",
                    "data": [],
                    "error": []
                }, status=404)

            serializer = PartySerializer(party, data=request.data)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"Updated party: {party.party_id}")
                return JsonResponse({
                    "error_code": 200,
                    "message": "Party updated successfully",
                    "data": [serializer.data],
                    "error": []
                }, status=200)

            logger.error(f"Failed to update Party: {serializer.errors}")
            return JsonResponse({
                "error_code": 400,
                "message": "Validation failed",
                "data": [],
                "error": serializer.errors
            }, status=400)

        except Exception as e:
            logger.error(f"Internal Server Error: {str(e)}")
            return JsonResponse({
                "error_code": 500,
                "message": "Internal Server Error",
                "data": [],
                "error": traceback.format_exc().splitlines()
            }, status=500)

    def delete(self, request, party_id, *args, **kwargs):
        try:
            party = Party.objects.filter(pk=party_id).first()
            if party is None:
                logger.error(f"Tax with ID {party_id} not found")
                return JsonResponse({
                    "error_code": 404,
                    "message": "Party not found",
                    "data": [],
                    "error": []
                }, status=404)

            party_id = party.party_id
            party.delete()
            logger.info(f"Deleted party: {party_id}")
            return JsonResponse({
                "error_code": 200,
                "message": "Party deleted successfully",
                "data": [],
                "error": []
            }, status=200)

        except Exception as e:
            logger.error(f"Internal Server Error: {str(e)}")
            return JsonResponse({
                "error_code": 500,
                "message": "Internal Server Error",
                "data": [],
                "error": traceback.format_exc().splitlines()
            }, status=500)
