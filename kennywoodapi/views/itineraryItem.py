# In this file, I am using a HyperlinkedModelSerializer. What this class does is take a Python object and convert it into JSON for you, and adds a virtual property of url to the resulting JSON.

"""View module for handling requests about intineraries"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from kennywoodapi.models import Attraction, ParkArea, Itinerary, Customer

class ItinerarySerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for intineraries

    Arguments:
        serializers
    """

    class Meta:
        model = Itinerary
        url = serializers.HyperlinkedIdentityField(
            view_name='itinerary',
            lookup_field='id'
        )
        fields = ('id', 'url', 'starttime', 'attraction', 'customer')
        depth = 2

class ItineraryItems(ViewSet):

    # Handles POST
    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized itinerary instance
        """
        new_itinerary_item = Itinerary()
        new_itinerary_item.attraction = request.data["ride_id"]
        new_itinerary_item.customer_id = request.auth.user.id
        new_itinerary_item.starttime = request.data["starttime"]

        new_itinerary_item.save()

        serializer = ItinerarySerializer(new_itinerary_item, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for a single itinerary item

        Returns:
            Response -- JSON serialized itinerary instance
        """
        try:
            itinerary_item = Itinerary.objects.get(pk=pk)
            serializer = ItinerarySerializer(itinerary_item, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def create(self, request):
        new_itinerary_item = Itinerary()
        new_itinerary_item.starttime = request.data["starttime"]
        new_itinerary_item.customer_id = request.auth.user.id
        new_itinerary_item.attraction_id = request.data["ride_id"]

        new_itinerary_item.save()

        serializer = ItinerarySerializer(new_itinerary_item, context={'request': request})

        return Response(serializer.data)
