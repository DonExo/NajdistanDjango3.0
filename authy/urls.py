from django.urls import path, re_path, reverse_lazy

from authy import views


urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('register/complete/', views.RegisterCompleteView.as_view(), name='register_complete'),

    path('pw/change/', views.PasswordChangeView.as_view(), name='password_change'),
    path('pw/change-done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('pw/reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('pw/reset-done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),

    # path('pw/reset-confirm/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # dzirni ulepsaj go ova
    re_path(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
            views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    path('pw/reset-complete/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
