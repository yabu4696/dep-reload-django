from django.urls import path

from . import views

app_name = 'ca_lens'
urlpatterns = [
    # path('rayout',views.rayout,name='rayout'),
    path('',  views.index, name='index'),
    path('item/<slug:slug>', views.detail, name='detail'),
    path('form', views.form, name='form'),
    path('delete', views.delete, name='delete'),
    path('reload',views.reload, name='reload'),
    path('item/<slug:slug>/edit', views.edit,name='edit'),
    path('item/<slug:slug>/exclusion', views.exclusion, name='exclusion'),
    path('item/<slug:slug>/reload', views.reload_one, name='reload_one'),
    path('maker_index',views.maker_index, name='maker_index'),
    path('maker/<slug:slug>', views.maker_detail, name='maker_detail'),
    # path('celery_test/', views.celery_test, name='celery_test'),
    path('search_result', views.search_result, name='search_result'),
    path('contact', views.contact, name='contact'), 
    path('contact/done', views.done, name='done'),
    path('preturn', views.preturn, name="preturn"),
]