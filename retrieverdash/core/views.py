from django.http import HttpResponse
from django.views import View
from django.shortcuts import render

from retrieverdash.settings.common import PROJECT_ROOT

import os
import json

file_path = os.path.join(PROJECT_ROOT,
                         'dashboard_script/dataset_details.json')
diff_path = os.path.join(PROJECT_ROOT,
                         'dashboard_script/diffs/')


class DashboardView(View):
    template_name = "new_dashboard.html"

    def get(self, request, *args, **kwargs):
        dataset_detail = json.load(open(file_path, 'r'))
        return render(request, self.template_name,
                      context={'datasets': dataset_detail,
                               'diff_path': diff_path})

class DiffView(View):
    def get(self, request, filename):
        return HttpResponse(open(os.path.join(diff_path, filename)))
