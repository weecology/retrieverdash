from django.http import HttpResponse
from django.views import View
from django.shortcuts import render

from retrieverdash.settings.common import PROJECT_ROOT

import os
import json

file_path = os.path.join(PROJECT_ROOT, 'dashboard_script/dataset_details.json')

class DashboardView(View):
    template_name = "dashboard.html"

    def get(self, request, *args, **kwargs):
        dataset_detail = json.load(open(file_path, 'r'))
        return render(request, self.template_name, context={'datasets': dataset_detail})
