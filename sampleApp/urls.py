
from django.urls import path

from .views import *

urlpatterns = [
    path('', MainPage.as_view(), name="main_page"),  
    path('login', LoginPage.as_view(), name="login_page"),  
    path('Add_Page/', AddPage.as_view(),name="Add_Page"),
    path('AdminDashboardPage/', AdminDashboardPage.as_view(),name="AdminDahboard_Page"),
    path('ApprovePage/', ApprovePage.as_view(),name="Approve_page"),
    path('user_reg/', UserReg.as_view(),name="user_reg"),
    path('manufacture/', Manufacture.as_view(),name="manufacture"),
    path('ManufactureDashboardPage/',ManufactureDashboardPage.as_view(),name='ManufactureDashboardPage'),
    path('AddProduct/', AddProduct.as_view(),name="AddProduct"),
    path('ViewAddProduct/',ViewAddProduct.as_view(),name='ViewAddProduct'),
    path('UpdateProduct/<int:id>/',UpdateProduct.as_view(),name='UpdateProduct'),
    path('DeleteProduct/<int:id>/',DeleteProduct.as_view(),name='DeleteProduct'),
    path('FeedBack/',viewFeedBack.as_view(),name="feedback"),
    ###############api##################
    path('register/', UserRegistration.as_view(), name='user_registration'),
    path('loginapi/',LoginPage.as_view(),name='LoginPage'),
     path('addfeedback/', FeedBackCreateAPIView.as_view(), name='add-feedback'),

    path('check_product/<str:product_id>/', CheckProductInBlock.as_view(), name='check_product_in_block'),
]
