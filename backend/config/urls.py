from django.urls import include, path

urlpatterns = [
    path("api/", include("apps.wallets.urls")),
    path("api/", include("apps.transactions.urls")),
]
