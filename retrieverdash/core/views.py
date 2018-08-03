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
    template_name = "dashboard.html"

    def get(self, request, *args, **kwargs):
        json_detail = json.load(open(file_path, 'r'))
        return render(request, self.template_name,
                      context={'datasets': json_detail['dataset_details'],
                               'diff_path': diff_path,
                               'last_checked_on':json_detail['last_checked_on']})

class DiffView(View):
    def get(self, request, filename):
        return HttpResponse(open(os.path.join(diff_path, filename)))
