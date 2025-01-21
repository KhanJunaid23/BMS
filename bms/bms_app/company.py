import logging
import traceback
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Company, FinancialYear
from .serializers import CompanySerializer, FinancialYearSerializer

# Setup logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


class CompanyAPIView(APIView):
    """
    Handles retrieving, updating, and deleting a single company.
    """

    def get(self, request, company_id=None, *args, **kwargs):
        try:
            if company_id:
                company = Company.objects.filter(pk=company_id).first()
                if company is None:
                    logger.error(f"Company with ID {company_id} not found")
                    return JsonResponse({
                        "error_code": 404,
                        "message": "Company not found",
                        "data": [],
                        "error": []
                    }, status=404)

                serializer = CompanySerializer(company)
                logger.info(f"Fetched company: {company.name}")
                return JsonResponse({
                    "error_code": 200,
                    "message": "Company found",
                    "data": [serializer.data],
                    "error": []
                }, status=200)
            else:
                companies = Company.objects.all()
                if not companies:
                    logger.warning("No companies found")
                    return JsonResponse({
                        "error_code": 400,
                        "message": "No data found",
                        "data": [],
                        "error": []
                    }, status=400)

                serializer = CompanySerializer(companies, many=True)
                logger.info("Fetched all companies")
                return JsonResponse({
                    "error_code": 200,
                    "message": "Data found",
                    "data": serializer.data,
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

    def post(self, request, *args, **kwargs):
        try:
            serializer = CompanySerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                logger.info(f"Created company: {serializer.data['name']}")

                return JsonResponse({
                    "error_code": 200,
                    "message": "Company created successfully",
                    "data": [serializer.data],
                    "error": []
                }, status=201)

            logger.error(f"Failed to create company: {serializer.errors}")
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

    def put(self, request, company_id, *args, **kwargs):
        try:
            company = Company.objects.filter(pk=company_id).first()
            if company is None:
                logger.error(f"Company with ID {company_id} not found")
                return JsonResponse({
                    "error_code": 404,
                    "message": "Company not found",
                    "data": [],
                    "error": []
                }, status=404)

            serializer = CompanySerializer(company, data=request.data)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"Updated company: {company.name}")
                return JsonResponse({
                    "error_code": 200,
                    "message": "Company updated successfully",
                    "data": [serializer.data],
                    "error": []
                }, status=200)

            logger.error(f"Failed to update company: {serializer.errors}")
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

    def delete(self, request, company_id, *args, **kwargs):
        try:
            company = Company.objects.filter(pk=company_id).first()
            if company is None:
                logger.error(f"Company with ID {company_id} not found")
                return JsonResponse({
                    "error_code": 404,
                    "message": "Company not found",
                    "data": [],
                    "error": []
                }, status=404)

            company_name = company.name
            company.delete()
            logger.info(f"Deleted company: {company_name}")
            return JsonResponse({
                "error_code": 200,
                "message": "Company deleted successfully",
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


class FinancialYearAPIView(APIView):
    """
    Handles retrieving, creating, updating, and deleting financial year.
    """

    def get(self, request, financial_year_id=None, *args, **kwargs):
        try:
            if financial_year_id:
                financial_year = FinancialYear.objects.filter(
                    financial_year_id=financial_year_id).first()
                if not financial_year:
                    logger.error(f"Financial Year with ID {
                                 financial_year_id} not found")
                    return JsonResponse({
                        "error_code": 404,
                        "message": "Financial Year not found",
                        "data": [],
                        "error": []
                    }, status=404)

                serializer = FinancialYearSerializer(financial_year)
                logger.info(f"Fetched Financial Year: {
                            financial_year.financial_year_id}")
                return JsonResponse({
                    "error_code": 200,
                    "message": "Financial Year found",
                    "data": [serializer.data],
                    "error": []
                }, status=200)

            financial_years = FinancialYear.objects.all()
            serializer = FinancialYearSerializer(financial_years, many=True)
            return JsonResponse({
                "error_code": 200,
                "message": "Data found",
                "data": serializer.data,
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

    def post(self, request, *args, **kwargs):
        try:
            company_id = request.data.get('company')
            if not Company.objects.filter(id=company_id).exists():
                logger.error(f"Company with ID {company_id} does not exist.")
                return JsonResponse({
                    "error_code": 400,
                    "message": "Invalid Company",
                    "data": [],
                    "error": []
                }, status=400)

            serializer = FinancialYearSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"Created Financial Year: {
                            serializer.data['financial_year_id']}")
                return JsonResponse({
                    "error_code": 201,
                    "message": "Financial Year created successfully",
                    "data": [serializer.data],
                    "error": []
                }, status=201)

            logger.error(f"Failed to create Financial Year: {
                         serializer.errors}")
            return JsonResponse({
                "error_code": 400,
                "message": "Invalid data",
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

    def put(self, request, financial_year_id, *args, **kwargs):
        try:
            financial_year = FinancialYear.objects.filter(
                financial_year_id=financial_year_id).first()
            if not financial_year:
                logger.error(f"Financial Year with ID {
                             financial_year_id} not found")
                return JsonResponse({
                    "error_code": 404,
                    "message": "Financial Year not found",
                    "data": [],
                    "error": []
                }, status=404)

            serializer = FinancialYearSerializer(
                financial_year, data=request.data)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"Updated Financial Year: {
                            financial_year.financial_year_id}")
                return JsonResponse({
                    "error_code": 200,
                    "message": "Financial Year updated successfully",
                    "data": [serializer.data],
                    "error": []
                }, status=200)

            logger.error(f"Failed to update Financial Year: {
                         serializer.errors}")
            return JsonResponse({
                "error_code": 400,
                "message": "Invalid data",
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

    def delete(self, request, financial_year_id, *args, **kwargs):
        try:
            financial_year = FinancialYear.objects.filter(
                financial_year_id=financial_year_id).first()
            if not financial_year:
                logger.error(f"Financial Year with ID {
                             financial_year_id} not found")
                return JsonResponse({
                    "error_code": 404,
                    "message": "Financial Year not found",
                    "data": [],
                    "error": []
                }, status=404)

            financial_year.delete()
            logger.info(f"Deleted Financial Year: {financial_year_id}")
            return JsonResponse({
                "error_code": 200,
                "message": "Financial Year deleted successfully",
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
