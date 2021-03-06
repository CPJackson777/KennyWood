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
        #the fields are the columns you want to include in the database
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
        new_itinerary_item.customer_id = request.auth.user.customer.id
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


    def list(self, request):
            """Handle GET requests to itinerary resource
            Returns:
                Response -- JSON serialized list of itinerary
            """
            itinerary_items = Itinerary.objects.all()
            serializer = ItinerarySerializer(
                itinerary_items, many=True, context={'request': request})
            return Response(serializer.data)


    #handles PUT
    def update(self, request, pk=None):
        """Handle PUT requests for a itinerary
        Returns:
            Response -- Empty body with 204 status code
        """
        itinerary_item = Itinerary.objects.get(pk=pk)
        itinerary_item.starttime = request.data["starttime"]

        itinerary_item.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    #handles DELETE
    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single itinerary item
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            itinerary = Itinerary.objects.get(pk=pk)

            itinerary.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Attraction.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
