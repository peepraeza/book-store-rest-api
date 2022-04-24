from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from appconfig.models import AppConfig
from middleware.decorators import is_authentication


class AppConfigView(APIView):
    @is_authentication(allowed_role=['ADMIN'])
    def put(self, request):
        appconfig_data = request.data
        try:
            app_config = AppConfig.objects.get(app_config_key='point_ratio')
            print(app_config)
            app_config.app_config_value = appconfig_data['point_ratio']
            app_config.save()
        except Exception as e:
            raise Exception(e)

        return Response({'detail': 'Point Ratio Updated Successfully'})
