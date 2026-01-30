from django.urls import path

from myapp import views


urlpatterns = [
    # path('',views.login),
    path("registration_post", views.registration_post),
    path("login_get", views.login_get),
    path("category_post", views.category_post),
    path("view_category/", views.view_category),
    path("delete_category/<id>", views.delete_category),
    path("notification_post", views.notification_post),
    path("view_notifications/", views.view_notifications),
    path("products_post", views.products_post),
    path("view_product/", views.view_product),
    path("delete_product/<id>", views.delete_product),
    path("view_registered_user/", views.view_registered_user),
    path("view_all_products_user/<category>", views.view_all_products_user),
    path("add_cart_post/", views.add_cart_post),
    path("view_cart/", views.view_cart),
    path("update_quantity/<id>/", views.update_quantity),
    path("delete_cart/<id>", views.delete_cart),
    path("add_order_post/", views.add_order_post),
    path("view_order/", views.view_order),
    path("view_order_more/", views.view_order_more),
    path("admin_view_order/", views.admin_view_order),
    path("admin_view_order_more/", views.admin_view_order_more),
    # path("search_products/", views.search_products),
    path("add_rating/", views.add_rating),
    # path("create_payment/", views.create_payment),
    # path("verify_payment/", views.verify_payment),
    path("edit_product/<id>", views.edit_product),
    path("edit_get/<id>", views.edit_get),
    path("edit_category/<id>", views.edit_category),
    path("edit_category_get/<id>", views.edit_category_get),

]