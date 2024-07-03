from fastapi_amis_admin import i18n

i18n.set_language(language='en_US')
from fastapi_amis_admin.admin.settings import Settings
from fastapi_amis_admin.admin.site import AdminSite
from fastapi_amis_admin.admin import admin
from api.database.settings import DATABASE_URL
from api.database.tablas import Personas, Vehiculos, Oficiales

site = AdminSite(settings=Settings(database_url=DATABASE_URL))


@site.register_admin
class PersonaAdmin(admin.ModelAdmin):
    page_schema = 'Persona'
    # set model
    model = Personas


@site.register_admin
class VehiculoAdmin(admin.ModelAdmin):
    page_schema = 'Vehiculo'
    # set model
    model = Vehiculos


@site.register_admin
class OficialAdmin(admin.ModelAdmin):
    page_schema = 'Oficial'
    # set model
    model = Oficiales
