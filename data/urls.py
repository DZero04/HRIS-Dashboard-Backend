
from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter 
from .views import *
from .views import OverviewMetricsView


router = DefaultRouter()
router.register('datatab1totab3', DataTab1ToTab3Viewset, basename='datatab1totab3')
router.register('datatab4', DataTab4Viewset, basename='datatab4')
router.register('datatab5ot', DataTab5OTViewset, basename='datatab5ot')
router.register('datatab05travel', DataTab5TravelViewset, basename='datatab05travel')
router.register('datatab6', DataTab6Viewset, basename='datatab6')
router.register('datatab8', DataTab8Viewset, basename='datatab8')
router.register('datatab9', DataTab9Viewset, basename='datatab9')
router.register('datachurnrisk', DataChurnRiskViewset, basename='datachurnrisk')
router.register('datatab7', DataTab7Viewset, basename='datatab7')



urlpatterns = router.urls + [
    path('overview-metrics/', OverviewMetricsView.as_view(), name='overview-metrics'),
    path('employee-composition/', EmployeeCompositionView.as_view(), name='employee-composition'),
    path('leave-analytics/', LeaveAnalyticsView.as_view(), name='leave-analytics'),
    path('overtime-travel/', OvertimeTravelAnalyticsView.as_view(), name = 'overtime-travel'),
    path('workforce-turnover/', SeparatedEmployeeAnalyticsView.as_view(), name = 'workforce-turnover'),
    path('request-summary/', RequestSummaryView.as_view(), name='request-summary'),
    path('training-analytics/', TrainingAnalyticsView.as_view(), name='training-analytics'),
    path('aspirations/', TalentDevelopmentView.as_view(), name = 'aspirations'),
    path('churn-risk/', RiskScoreView.as_view(), name = 'churn-risk'),
    path('hiring-data/', HiringAnalyticsView.as_view(), name = 'hiring-data'),


]
