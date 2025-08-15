from django.urls import path
from . import views
from .views import ceo_reports_analytics
from .views import expected_daily_amounts
from .views import ceo_accumulated_balances
from .views import ceo_terms_and_conditions
from .views import get_client_details
from .views import reject_client 
from django.urls import path
from .views import ceo_terms_and_conditions, delete_terms_and_conditions


urlpatterns = [
    path('register/', views.register_client, name='register_client'),
    path('my-clients/', views.view_my_clients, name='view_my_clients'),
    path('submit-report/', views.submit_daily_report, name='submit_daily_report'),
    path('approved-clients/', views.view_approved_clients, name='view_approved_clients'),
    path('monthly-summary/', views.print_monthly_summary, name='print_monthly_summary'),
    path('ceo/pending-clients/', views.view_pending_clients, name='view_pending_clients'),
    path('ceo/loan/approve/<int:loan_id>/', views.approve_loan, name='approve_loan'),
    path('ceo/loan/reject/<int:loan_id>/', views.reject_loan, name='reject_loan'),
    path('ceo/announcements/', views.list_announcements, name='list_announcements'),
    path('ceo/announcements/new/', views.create_announcement, name='create_announcement'),
    path('ceo/announcements/delete/<int:id>/', views.delete_announcement, name='delete_announcement'),
    path('ceo/reports-analytics/', views.ceo_reports_analytics, name='ceo_reports_analytics'),
    path('ceo/reports/', ceo_reports_analytics, name='ceo_reports_analytics'),
    path('ceo/clients/all/', views.view_all_clients, name='view_all_clients'),
    path('ceo/payments/', views.view_all_payments, name='ceo_view_all_payments'),
    path('ceo/reports/officers/', views.view_officer_reports, name='view_officer_reports'),
    path('ceo/expected-daily-amounts/', expected_daily_amounts, name='expected_daily_amounts'),
    path('ceo/accumulated-balances/', ceo_accumulated_balances, name='ceo_accumulated_balances'),
    path('ceo/total-expected-funds/', views.ceo_total_expected_funds, name='ceo_total_expected_funds'),
    path('ceo/terms-and-conditions/', ceo_terms_and_conditions, name='ceo_terms_and_conditions'),
    path('ceo/edit-profile/', views.ceo_edit_profile, name='ceo_edit_profile'),
    path('', views.home, name='home'),
    path('api/details/<int:client_id>/', views.client_details_api, name='client_details_api'),
    path("apply-loan/", views.apply_loan, name="apply_loan"),
    path('api/edit/<int:client_id>/', get_client_details, name='get_client_details'),
    path('api/edit/<int:client_id>/', views.edit_client_api, name='edit_client_api'),
    path('api/update/', views.update_client, name='update_client'),
    path('api/delete/<int:client_id>/', views.delete_client, name='delete_client'),
    path('api/loan/<int:loan_id>/repayment-days/', views.get_repayment_days, name='get_repayment_days'),
    path('api/repayment-day/<int:day_id>/mark/', views.mark_repayment_day_paid, name='mark_repayment_day_paid'),
    path('ceo/dashboard/', views.ceo_dashboard, name='ceo_dashboard'),
    path('approve-client/<int:client_id>/', views.approve_client, name='approve_client'),
    path('clients/<int:client_id>/reject/', reject_client, name='reject_client'),
    path('clients/search/', views.search_clients_by_nrc, name='search_clients_by_nrc'),
    path('officer/edit-profile/', views.loan_officer_edit_profile, name='loan_officer_edit_profile'),
    path('clients/search/', views.search_clients_by_nrc, name='search_clients_by_nrc'),
    path('ceo/payments/update/', views.update_payment, name='update_payment'),
    path('ceo/reports/export/xlsx/', views.export_reports_xlsx, name='export_reports_xlsx'),
    path('ceo/create-loan-officer/', views.create_loan_officer, name='create_loan_officer'),
    path('ceo/terms/', ceo_terms_and_conditions, name='ceo_terms_and_conditions'),
    path('ceo/terms/delete/<int:pk>/', delete_terms_and_conditions, name='delete_terms_and_conditions'),
]

