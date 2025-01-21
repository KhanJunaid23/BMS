import logging
import traceback
from django.http import JsonResponse
from rest_framework.views import APIView
from .models import Transactions
from .serializers import TransactionSerializer

# Setup logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


class TransactionAPIView(APIView):
    def get(self, request, trnx_id=None, *args, **kwargs):
        try:
            if trnx_id:
                transaction = Transactions.objects.filter(
                    transaction_id=trnx_id).first()
                if transaction is None:
                    return JsonResponse({
                        "error_code": 404,
                        "message": "Transaction not found",
                        "data": [],
                        "error": []
                    }, status=404)

                serializer = TransactionSerializer(transaction)
                logger.info(f"Fetched transaction: {
                            transaction.transaction_id}")
                return JsonResponse({
                    "error_code": 200,
                    "message": "Transactiion found",
                    "data": [serializer.data],
                    "error": []
                }, status=200)

            else:
                transactions = Transactions.objects.all()
                logger.warning("No transactions found")
                if not transaction:
                    return JsonResponse({
                        "error_code": 400,
                        "message": "No transaction found",
                        "data": [],
                        "error": []
                    }, status=400)

                serializer = TransactionSerializer(transactions, many=True)
                logger.info("Fetched all transactions")
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
            serializer = TransactionSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"Created transaction: {
                            serializer.data['transaction_id']}")

                return JsonResponse({
                    "error_code": 200,
                    "message": "Transaction created successfully",
                    "data": [serializer.data],
                    "error": []
                }, status=201)

            logger.error(f"Failed to create transaction: {serializer.errors}")
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

    def put(self, request, trnx_id, *args, **kwargs):
        try:
            transaction = Transactions.objects.filter(pk=trnx_id).first()
            if transaction is None:
                logger.error(f"Transaction with ID {trnx_id} not found")
                return JsonResponse({
                    "error_code": 404,
                    "message": "Transaction not found",
                    "data": [],
                    "error": []
                }, status=404)

            serializer = TransactionSerializer(transaction, data=request.data)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"Updated transaction: {transaction.trnx_id}")
                return JsonResponse({
                    "error_code": 200,
                    "message": "Transaction updated successfully",
                    "data": [serializer.data],
                    "error": []
                }, status=200)

            logger.error(f"Failed to update transaction: {serializer.errors}")
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

    def delete(self, request, trnx_id, *args, **kwargs):
        try:
            transaction = Transactions.objects.filter(pk=trnx_id).first()
            if transaction is None:
                logger.error(f"Transaction with ID {trnx_id} not found")
                return JsonResponse({
                    "error_code": 404,
                    "message": "Transaction not found",
                    "data": [],
                    "error": []
                }, status=404)

            trnx_id = transaction.transaction_id
            transaction.delete()
            logger.info(f"Deleted transaction: {trnx_id}")
            return JsonResponse({
                "error_code": 200,
                "message": "Transaction deleted successfully",
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
