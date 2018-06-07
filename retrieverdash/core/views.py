from django.http import HttpResponse
from django.views import View
from django.shortcuts import render

import json


class DashboardView(View):
    template_name = "dashboard.html"

    def get(self, request, *args, **kwargs):
        dataset_detail = json.load(open('../dashboard_script/dataset_details.json', 'r'))
        return render(request, self.template_name, context={'datasets': dataset_detail})
