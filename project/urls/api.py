from django.urls import path, include

urlpatterns = [
    path('', include('visit.urls'), name='visit')
]
