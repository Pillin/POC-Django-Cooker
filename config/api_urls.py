from rest_framework import routers
from menus.views import MenuViewSet
from tags.views import TagViewSet
from meals.views import MealViewSet
from plates.views import PlateViewSet
from distributions.views import DistributionViewSet

Router = routers.SimpleRouter()
Router.register(r'menus', MenuViewSet)
Router.register(r'tags', TagViewSet)
Router.register(r'meals', MealViewSet)
Router.register(r'plates', PlateViewSet)
Router.register(r'distributions', DistributionViewSet)
