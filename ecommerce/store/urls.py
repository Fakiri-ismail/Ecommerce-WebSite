from django.urls import path
from . import views

urlpatterns = [
        #Leave as empty string for base url
	path('', views.home, name="home"),
	path("store/", views.store, name="store"),
	path("about/", views.about, name="about"),
	path("contact/", views.contact, name="contact"),
	path('cart/', views.cart, name="cart"),

	path("privacyPolicy/", views.privacyPolicy, name="privacyPolicy"),
	path("refundPolicy/", views.refundPolicy, name="refundPolicy"),
	path('termsService/', views.termsService, name="termsService"),

	path('checkout/', views.checkout, name="checkout"),
	path("myStore/", views.myStore, name="myStore"),
	path("archProducts/", views.archProducts, name="archProducts"),

	path("store/<int:id>/", views.product_details, name="product_details"),
	path("myStore/addProduct", views.addProduct, name="addProduct"),
	path("myStore/deleteProduct/<int:id>/", views.deleteProduct, name="deleteProduct"),
	path("myStore/updatePrudact/<int:id>/", views.updatePrudact, name="updatePrudact"),
	path("myStore/archivePrudact/<int:id>/", views.archivePrudact, name="archivePrudact"),

	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),

]