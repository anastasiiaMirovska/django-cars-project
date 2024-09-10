from django.urls import path

from apps.users.views import (
    AdminToUserView,
    PremiumToUserView,
    UserBlockView,
    UserCreateView,
    UserDestroyView,
    UserListView,
    UserRetrieveView,
    UserToAdminView,
    UserToPremiumView,
    UserUnBlockView,
    UserUpdateView,
)

urlpatterns = [
    path('', UserListView.as_view(), name='user_list'),
    path('/create', UserCreateView.as_view(), name='user_create'),
    path('/<int:pk>/retrieve', UserRetrieveView.as_view(), name='user_retrieve'),
    path('/<int:pk>/update', UserUpdateView.as_view(), name='user_update'),
    path('/<int:pk>/destroy', UserDestroyView.as_view(), name='user_destroy'),

    path('/premium', UserToPremiumView.as_view(), name='user-to-premium'),
    path('/<int:pk>/remove-premium', PremiumToUserView.as_view(), name='premium-to-user'),
    path('/<int:pk>/block', UserBlockView.as_view(), name='user_block'),
    path('/<int:pk>/un_block', UserUnBlockView.as_view(), name='user_un_block'),
    path('/<int:pk>/user_to_admin', UserToAdminView.as_view(), name='user_to_admin'),
    path('/<int:pk>/admin_to_user', AdminToUserView.as_view(), name='admin_to_user')
]
