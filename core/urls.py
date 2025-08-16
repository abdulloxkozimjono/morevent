from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ContactViewSet, FeedbackViewSet, FAQViewSet, AboutViewSet

router = DefaultRouter()
router.register(r'contacts', ContactViewSet)
router.register(r'feedbacks', FeedbackViewSet)
router.register(r'faqs', FAQViewSet)
router.register(r'about', AboutViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("api/", include("referals.urls")),

]
