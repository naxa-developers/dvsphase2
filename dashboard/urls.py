from django.contrib import admin
from django.urls import path, include
from dashboard import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('upload/', views.uploadData, name='upload'),
    path('upload-shapefile/', views.ShapefileUpload, name='upload-shapefile'),


    path('invitation/', views.Invitation, name='invitation'),
    path('create-role/', views.create_role, name='create-role'),
    path('login-test/', views.login_test, name='login-test'),
    # path('login-test/<int:group>/<int:partner>', views.login_test, name='login-test'),
    path('logout/', auth_views.logout, {'next_page': '/dashboard/login/'}, name='logout'),
    path('signup/<int:group>/<int:partner>/<int:program>/<int:project>', views.signup, name='signup'),
    path('login/', auth_views.login, name='login'),
    path('check-login/', views.check_login, name='check-login'),
    path('token/', views.auth, name='token'),
    path('main/', views.Dashboard.as_view(), name='main'),

    path('page_province/', views.province_list, name='page_province'),

    path('program-list/', views.ProgramList.as_view(), name='program-list'),
    path('program-add/', views.ProgramCreate.as_view(), name='program-add'),
    path('program-edit/<int:pk>', views.ProgramUpdate.as_view(), name='program-edit'),
    path('program-delete/<int:pk>', views.ProgramDelete.as_view(), name='program-delete'),

    path('partner-list/', views.PartnerList.as_view(), name='partner-list'),
    path('partner-add/', views.PartnerCreate.as_view(), name='partner-add'),
    path('partner-edit/<int:pk>', views.PartnerUpdate.as_view(), name='partner-edit'),
    path('partner-delete/<int:pk>', views.PartnerDelete.as_view(), name='partner-delete'),

    path('sector-list/', views.SectorList.as_view(), name='sector-list'),
    path('sector-add/', views.SectorCreate.as_view(), name='sector-add'),
    path('sector-edit/<int:pk>', views.SectorUpdate.as_view(), name='sector-edit'),
    path('sector-delete/<int:pk>', views.SectorDelete.as_view(), name='sector-delete'),

    path('subsector-list/', views.SubSectorList.as_view(), name='subsector-list'),
    path('subsector-add/', views.SubSectorCreate.as_view(), name='subsector-add'),
    path('subsector-edit/<int:pk>', views.SubSectorUpdate.as_view(), name='subsector-edit'),
    path('subsector-delete/<int:pk>', views.SubSectorDelete.as_view(), name='subsector-delete'),

    path('marker-list/', views.MarkerList.as_view(), name='marker-list'),
    path('marker-cat-add/', views.MarkerCategoryCreate.as_view(), name='marker-cat-add'),
    path('marker-cat-edit/<int:pk>', views.MarkerCategoryUpdate.as_view(), name='marker-cat-edit'),
    path('marker-cat-delete/<int:pk>', views.MarkerCategoryDelete.as_view(), name='marker-cat-delete'),

    path('markervalue-list/', views.MarkerValueList.as_view(), name='markervalue-list'),
    path('markervalue-add/', views.MarkerValueCreate.as_view(), name='markervalue-add'),
    path('markervalue-edit/<int:pk>', views.MarkerValueUpdate.as_view(), name='markervalue-edit'),
    path('markervalue-delete/<int:pk>', views.MarkerValueDelete.as_view(), name='markervalue-delete'),

    path('indicator-list/', views.IndicatorList.as_view(), name='indicator-list'),
    path('indicator-add/', views.IndicatorCreate.as_view(), name='indicator-add'),
    path('indicator-edit/<int:pk>', views.IndicatorUpdate.as_view(), name='indicator-edit'),
    path('indicator-delete/<int:pk>', views.IndicatorDelete.as_view(), name='indicator-delete'),

    path('indicator-data/', views.IndicatorValueList.as_view(), name='indicator-data'),
    # path('program-list/', views.ProgramList.as_view(), name='program-list'),

    path('gis-layer-list/', views.GisLayerList.as_view(), name='gis-layer-list'),
    path('layer-add/', views.gisLayer_create, name='layer-add'),
    path('gis-edit/<int:pk>', views.GisLayerUpdate.as_view(), name='gis-edit'),
    path('gis-replace/<int:pk>', views.gisLayer_replace, name='gis-replace'),
    path('gis-delete/<int:pk>', views.gisLayer_delete, name='gis-delete'),

    path('province-list/', views.ProvinceList.as_view(), name='province-list'),
    path('province-add/', views.ProvinceCreate.as_view(), name='province-add'),
    path('province-edit/<int:pk>', views.ProvinceUpdate.as_view(), name='province-edit'),
    path('province-delete/<int:pk>', views.ProvinceDelete.as_view(), name='province-delete'),

    path('district-list/', views.DistrictList.as_view(), name='district-list'),
    path('district-add/', views.DistrictCreate.as_view(), name='district-add'),
    path('district-edit/<int:pk>', views.DistrictUpdate.as_view(), name='district-edit'),
    path('district-delete/<int:pk>', views.DistrictDelete.as_view(), name='district-delete'),

    path('palika-list/', views.PalikaList.as_view(), name='palika-list'),
    path('palika-add/', views.PalilkaCreate.as_view(), name='palika-add'),
    path('palika-delete/<int:pk>', views.PalikaDelete.as_view(), name='palika-delete'),

    path('user-list/', views.UserList.as_view(), name='user-list'),
    path('activate/<int:id>', views.activate_user, name='activate'),
    path('assign-role/<int:id>', views.assign_role, name='assign-role'),

    path('project-list/', views.ProjectList.as_view(), name='project-list'),
    path('project-add/', views.ProjectCreate.as_view(), name='project-add'),
    path('project-edit/<int:pk>', views.ProjectUpdate.as_view(), name='project-edit'),
    path('project-delete/<int:pk>', views.ProjectDelete.as_view(), name='project-delete'),

    path('permission-list/', views.PermissionList.as_view(), name='permission-list'),
    path('permission-add/', views.PermissionCreate.as_view(), name='permission-add'),
    path('permission-edit/<int:pk>', views.PermissionUpdate.as_view(), name='permission-edit'),
    path('permission-delete/<int:pk>', views.PermissionDelete.as_view(), name='permission-delete'),

    path('vector-map/', views.VectorMap.as_view(), name='vector-map'),

]
