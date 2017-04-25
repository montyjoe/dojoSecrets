from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^success$', views.success),
    url(r'^top_secrets$', views.popular_secrets),
    url(r'^add_secret$', views.new_secret),
    url(r'^success/(?P<secret_id>\d+)/likes$', views.add_like, name="likes"),
    url(r'^success/(?P<secret_id>\d+)/destroy$', views.destroy_secret),
]






# end
