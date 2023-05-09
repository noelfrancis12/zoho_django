from.import views
from django.urls import path,include,re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.static import serve

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('base', views.base, name='base'),
    path('logout', views.logout, name='logout'),
    path('view_profile', views.view_profile, name='view_profile'),
    path('edit_profile/<pk>', views.edit_profile, name='edit_profile'),
    path('itemview',views.itemview,name='itemview'),
    path('additem',views.additem,name='additem'),

    path('add',views.add,name='add'),
    path('add_account',views.add_account,name='add_account'),
    path('detail/<int:id>',views.detail,name='detail'),
    path('edititem/<int:id>',views.edititem,name='edititem'),
    path('edit_db/<int:id>',views.edit_db,name='edit_db'),
    path('Action/<int:id>',views.Action,name='Action'),
    path('cleer/<int:id>',views.cleer,name='cleer'),
    path('add_unit',views.add_unit,name='add_unit'),
    path('sales',views.add_sales,name='add_sales'),
    path('vendor/',views.vendor,name='vendor'),
    path('add_vendor/',views.add_vendor,name='add_vendor'),
    path('sample/',views.sample,name="sample"),
    path('view_vendor_list/',views.view_vendor_list,name='view_vendor_list'),
    path('view_vendor_details/<int:pk>',views.view_vendor_details,name='view_vendor_details'),
    path('add_comment/<int:pk>',views.add_comment,name='add_comment'),
    path('sendmail/<int:pk>',views.sendmail,name='sendmail'),
    path('edit_vendor/<int:pk>',views.edit_vendor,name='edit_vendor'),
    path('edit_vendor_details/<int:pk>',views.edit_vendor_details,name='edit_vendor_details'),
    path('upload_document/<int:pk>',views.upload_document,name='upload_document'),
    path('download_doc/<int:pk>',views.download_doc,name='download_doc'),
    path('cancel_vendor/',views.cancel_vendor,name='cancel_vendor'),
    path('delete_vendor/<int:pk>',views.delete_vendor,name='delete_vendor'),
    
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)