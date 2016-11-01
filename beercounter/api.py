from rest_framework import routers, serializers, viewsets
from beercounter.models import User, Drink, Consumption


# Serializers define the API representation.
class ConsumptionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Consumption
        fields = ('url', 'user', 'drink', 'datetime', 'count')


# ViewSets define the view behavior.
class ConsumptionViewSet(viewsets.ModelViewSet):
    queryset = Consumption.objects.all()
    serializer_class = ConsumptionSerializer


# Serializers define the API representation.
class DrinkSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Drink
        fields = ('url', 'name', 'crate_size')


# ViewSets define the view behavior.
class DrinkViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Drink.objects.all()
    serializer_class = DrinkSerializer


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'name')


# ViewSets define the view behavior.
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'drinks', DrinkViewSet)
router.register(r'consumption', ConsumptionViewSet)
