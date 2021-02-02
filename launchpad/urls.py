from django.urls import path, re_path
from . import views as launchpad_views

urlpatterns = [
    
    path('addresses', launchpad_views.AddressList.as_view(), name='addresses-list'),
    path('address/<uuid:address_id>', launchpad_views.AddressDetail.as_view(), name='address-detail'),
    path('address/new', launchpad_views.AddressCreateView.as_view(), name='address-create'),

    path('people', launchpad_views.PeopleList.as_view(), name='people-list'),
    path('people/<uuid:person_id>', launchpad_views.PersonDetail.as_view(), name='person-detail'),
    path('people/new', launchpad_views.PersonCreateView.as_view(), name='person-create'),
 
    
]