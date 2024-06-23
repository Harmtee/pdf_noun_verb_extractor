from rest_framework.exceptions import ValidationError
from mongoengine.errors import NotUniqueError
from rest_framework.views import APIView
from django.views import generic
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
import uuid
from .models import PDF
from .serializers import PDFSerializer
from api.utils.pdf_processing import extract_text_from_pdf, extract_nouns_verbs


class PDFView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file_serializer = PDFSerializer(data=request.data)
        if file_serializer.is_valid():
            pdf_file = request.data["pdf_file"]
            filename = f'uploads/{uuid.uuid4()}.{pdf_file.name.split(".")[-1]}'
            with open(filename, "wb+") as destination:
                for chunk in pdf_file.chunks():
                    destination.write(chunk)

            try:
                text = extract_text_from_pdf(filename)
                nouns, verbs = extract_nouns_verbs(text)
            except Exception as e:
                return Response({"error": "Something went wrong", "details": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                file_serializer.save(
                    nouns=nouns,
                    verbs=verbs,
                    src=filename,
                    client_name=pdf_file.name,
                    upload_date=datetime.now(),
                )
                return Response(file_serializer.data, status=status.HTTP_201_CREATED)
            except NotUniqueError as e:
                return Response({
                    "error": "Duplicate email detected",
                    "details": f"The email '{file_serializer.validated_data['email']}' is already in use."
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        pdfs = PDF.objects.all()
        serializer = PDFSerializer(pdfs, many=True)
        return Response(serializer.data)

class UploadView(generic.TemplateView):
    template_name = "upload.html"