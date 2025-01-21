import logging
import traceback
from django.http import JsonResponse
from rest_framework.views import APIView
from .models import GSTDetails, Items, Remarks, Tax
from .serializers import GSTDetailSerializer, ItemSerializer, RemarkSerializer, TaxSerializer

# Setup logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


class ItemsAPIView(APIView):
    def get(self, request, item_id=None, *args, **kwargs):
        try:
            if item_id:
                item = Items.objects.filter(item_id=item_id).first()
                if item is None:
                    return JsonResponse({
                        "error_code": 404,
                        "message": "Item not found",
                        "data": [],
                        "error": []
                    }, status=404)

                serializer = ItemSerializer(item)
                logger.info(f"Fetched item: {item.item_name}")
                return JsonResponse({
                    "error_code": 200,
                    "message": "Item found",
                    "data": [serializer.data],
                    "error": []
                }, status=200)

            else:
                items = Items.objects.all()
                logger.warning("No Items found")
                if not items:
                    return JsonResponse({
                        "error_code": 400,
                        "message": "No items found",
                        "data": [],
                        "error": []
                    }, status=400)

                serializer = ItemSerializer(items, many=True)
                logger.info("Fetched all items")
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
            serializer = ItemSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"Created Item: {serializer.data['item_name']}")

                return JsonResponse({
                    "error_code": 200,
                    "message": "Item created successfully",
                    "data": [serializer.data],
                    "error": []
                }, status=201)

            logger.error(f"Failed to create item: {serializer.errors}")
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

    def put(self, request, item_id, *args, **kwargs):
        try:
            item = Items.objects.filter(pk=item_id).first()
            if item is None:
                logger.error(f"Item with ID {item_id} not found")
                return JsonResponse({
                    "error_code": 404,
                    "message": "Item not found",
                    "data": [],
                    "error": []
                }, status=404)

            serializer = ItemSerializer(item, data=request.data)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"Updated item: {item.item_name}")
                return JsonResponse({
                    "error_code": 200,
                    "message": "Item updated successfully",
                    "data": [serializer.data],
                    "error": []
                }, status=200)

            logger.error(f"Failed to update Item: {serializer.errors}")
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

    def delete(self, request, item_id, *args, **kwargs):
        try:
            item = Items.objects.filter(pk=item_id).first()
            if item is None:
                logger.error(f"Item with ID {item} not found")
                return JsonResponse({
                    "error_code": 404,
                    "message": "Item not found",
                    "data": [],
                    "error": []
                }, status=404)

            item_name = item.item_name
            item.delete()
            logger.info(f"Deleted item: {item_name}")
            return JsonResponse({
                "error_code": 200,
                "message": "Item deleted successfully",
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


class RemarkAPIView(APIView):
    def get(self, request, remark_id=None, *args, **kwargs):
        try:
            if remark_id:
                remark = Remarks.objects.filter(remark_id=remark_id).first()
                if remark is None:
                    return JsonResponse({
                        "error_code": 404,
                        "message": "Remark not found",
                        "data": [],
                        "error": []
                    }, status=404)

                serializer = RemarkSerializer(remark)
                logger.info(f"Fetched remark: {remark.remark}")
                return JsonResponse({
                    "error_code": 200,
                    "message": "Remark found",
                    "data": [serializer.data],
                    "error": []
                }, status=200)

            else:
                remarks = Remarks.objects.all()
                logger.warning("No Remarks found")
                if not remarks:
                    return JsonResponse({
                        "error_code": 400,
                        "message": "No remarks found",
                        "data": [],
                        "error": []
                    }, status=400)

                serializer = RemarkSerializer(remarks, many=True)
                logger.info("Fetched all remarks")
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
            serializer = RemarkSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"Created Remark: {serializer.data['remark']}")

                return JsonResponse({
                    "error_code": 200,
                    "message": "Remark created successfully",
                    "data": [serializer.data],
                    "error": []
                }, status=201)

            logger.error(f"Failed to create remark: {serializer.errors}")
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

    def put(self, request, remark_id, *args, **kwargs):
        try:
            remark = Remarks.objects.filter(pk=remark_id).first()
            if remark is None:
                logger.error(f"Remark with ID {remark_id} not found")
                return JsonResponse({
                    "error_code": 404,
                    "message": "Remark not found",
                    "data": [],
                    "error": []
                }, status=404)

            serializer = RemarkSerializer(remark, data=request.data)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"Updated remark: {remark.remark}")
                return JsonResponse({
                    "error_code": 200,
                    "message": "Remark updated successfully",
                    "data": [serializer.data],
                    "error": []
                }, status=200)

            logger.error(f"Failed to update Remark: {serializer.errors}")
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

    def delete(self, request, remark_id, *args, **kwargs):
        try:
            remark = Remarks.objects.filter(pk=remark_id).first()
            if remark is None:
                logger.error(f"Remark with ID {remark} not found")
                return JsonResponse({
                    "error_code": 404,
                    "message": "Remark not found",
                    "data": [],
                    "error": []
                }, status=404)

            remark_name = remark.remark
            remark.delete()
            logger.info(f"Deleted remark: {remark_name}")
            return JsonResponse({
                "error_code": 200,
                "message": "Remark deleted successfully",
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


class TaxAPIView(APIView):
    def get(self, request, tax_id=None, *args, **kwargs):
        try:
            if tax_id:
                tax = Tax.objects.filter(tax_id=tax_id).first()
                if tax is None:
                    return JsonResponse({
                        "error_code": 404,
                        "message": "Tax not found",
                        "data": [],
                        "error": []
                    }, status=404)

                serializer = TaxSerializer(tax)
                logger.info(f"Fetched tax: {tax.tax_id}")
                return JsonResponse({
                    "error_code": 200,
                    "message": "Tax found",
                    "data": [serializer.data],
                    "error": []
                }, status=200)

            else:
                taxs = Tax.objects.all()
                logger.warning("No Taxs found")
                if not taxs:
                    return JsonResponse({
                        "error_code": 400,
                        "message": "No taxs found",
                        "data": [],
                        "error": []
                    }, status=400)

                serializer = TaxSerializer(taxs, many=True)
                logger.info("Fetched all taxs")
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
            serializer = TaxSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"Created Tax: {serializer.data['tax_id']}")

                return JsonResponse({
                    "error_code": 200,
                    "message": "Tax created successfully",
                    "data": [serializer.data],
                    "error": []
                }, status=201)

            logger.error(f"Failed to create tax: {serializer.errors}")
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

    def put(self, request, tax_id, *args, **kwargs):
        try:
            tax = Tax.objects.filter(pk=tax_id).first()
            if tax is None:
                logger.error(f"Tax with ID {tax_id} not found")
                return JsonResponse({
                    "error_code": 404,
                    "message": "Tax not found",
                    "data": [],
                    "error": []
                }, status=404)

            serializer = TaxSerializer(tax, data=request.data)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"Updated tax: {tax.tax_id}")
                return JsonResponse({
                    "error_code": 200,
                    "message": "Tax updated successfully",
                    "data": [serializer.data],
                    "error": []
                }, status=200)

            logger.error(f"Failed to update Tax: {serializer.errors}")
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

    def delete(self, request, tax_id, *args, **kwargs):
        try:
            tax = Tax.objects.filter(pk=tax_id).first()
            if tax is None:
                logger.error(f"Tax with ID {tax} not found")
                return JsonResponse({
                    "error_code": 404,
                    "message": "Tax not found",
                    "data": [],
                    "error": []
                }, status=404)

            tax_id = tax.tax_id
            tax.delete()
            logger.info(f"Deleted tax: {tax_id}")
            return JsonResponse({
                "error_code": 200,
                "message": "Tax deleted successfully",
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


class GSTAPIView(APIView):
    def get(self, request, gst_id=None, *args, **kwargs):
        try:
            if gst_id:
                gst = GSTDetails.objects.filter(gst_id=gst_id).first()
                if gst is None:
                    return JsonResponse({
                        "error_code": 404,
                        "message": "GST not found",
                        "data": [],
                        "error": []
                    }, status=404)

                serializer = GSTDetailSerializer(gst)
                logger.info(f"Fetched GST: {gst.gst_id}")
                return JsonResponse({
                    "error_code": 200,
                    "message": "GST found",
                    "data": [serializer.data],
                    "error": []
                }, status=200)

            else:
                gsts = GSTDetails.objects.all()
                logger.warning("No GST's found")
                if not gsts:
                    return JsonResponse({
                        "error_code": 400,
                        "message": "No GST's found",
                        "data": [],
                        "error": []
                    }, status=400)

                serializer = GSTDetailSerializer(gsts, many=True)
                logger.info("Fetched all GST's")
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
            serializer = GSTDetailSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"Created GST: {serializer.data['gst_id']}")

                return JsonResponse({
                    "error_code": 200,
                    "message": "GST created successfully",
                    "data": [serializer.data],
                    "error": []
                }, status=201)

            logger.error(f"Failed to create GST: {serializer.errors}")
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

    def put(self, request, gst_id, *args, **kwargs):
        try:
            gst = GSTDetails.objects.filter(pk=gst_id).first()
            if gst is None:
                logger.error(f"GST with ID {gst_id} not found")
                return JsonResponse({
                    "error_code": 404,
                    "message": "GST not found",
                    "data": [],
                    "error": []
                }, status=404)

            serializer = GSTDetailSerializer(gst, data=request.data)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"Updated GST: {gst.gst_id}")
                return JsonResponse({
                    "error_code": 200,
                    "message": "GST updated successfully",
                    "data": [serializer.data],
                    "error": []
                }, status=200)

            logger.error(f"Failed to update GST: {serializer.errors}")
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

    def delete(self, request, gst_id, *args, **kwargs):
        try:
            gst = GSTDetails.objects.filter(pk=gst_id).first()
            if gst is None:
                logger.error(f"GST with ID {gst_id} not found")
                return JsonResponse({
                    "error_code": 404,
                    "message": "GST not found",
                    "data": [],
                    "error": []
                }, status=404)

            gst_id = gst.gst_id
            gst.delete()
            logger.info(f"Deleted GST: {gst_id}")
            return JsonResponse({
                "error_code": 200,
                "message": "GST deleted successfully",
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
