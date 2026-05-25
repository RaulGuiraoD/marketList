from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('lista/<int:lista_id>/', views.ver_lista, name='ver_lista'),
    path('lista/cambiar-tienda/<int:lista_id>/', views.cambiar_tienda_lista, name='cambiar_tienda_lista'),
    path('lista/eliminar/<int:lista_id>/', views.eliminar_lista, name='eliminar_lista'),
    path('item/cambiar-cantidad/<int:item_id>/<str:operacion>/', views.cambiar_cantidad, name='cambiar_cantidad'),
    path('item/completar/<int:item_id>/', views.completar_item, name='completar_item'),
    path('item/eliminar/<int:item_id>/', views.eliminar_item, name='eliminar_item'),
    path('lista/finalizar/<int:lista_id>/', views.finalizar_compra, name='finalizar_compra'),
    path('archivadas/', views.listas_archivadas, name='listas_archivadas'),
    path('lista/reabrir/<int:lista_id>/', views.reabrir_lista, name='reabrir_lista'),
    path('archivadas/eliminar-multiple/', views.eliminar_multiple_listas, name='eliminar_multiple_listas'),
    
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='registration/password_reset_form.html',
             html_email_template_name='registration/password_reset_email.html' # 🌟 NUEVA LÍNEA
         ), 
         name='password_reset'),
    
    # 2. Pantalla que confirma que el correo ha sido enviado
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), 
         name='password_reset_done'),
    
    # 3. Enlace con token seguro que le llega al usuario a su email
    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), 
         name='password_reset_confirm'),
    
    # 4. Pantalla que confirma que la contraseña se cambio correctamente
    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), 
         name='password_reset_complete'),
]