# This context processor function makes the PROJECT_NAME available in every template
from configdata import PROJECT_NAME

def add_project_name(request):
    return {
        'project_name': PROJECT_NAME
    }
