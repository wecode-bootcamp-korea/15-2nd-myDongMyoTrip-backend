import json
from django.shortcuts import render
from django.views     import View
from django.http      import JsonResponse, HttpResponse
from django.db.models import Count, Avg, Q, Max
from user.models      import User
from .models          import  (
    Theme,
    AccommodationTheme, 
    Accommodation, 
    Host, 
    RoomAmenity, 
    RoomType,
    RoomTypeAmenity,
    AccommodationImage,
    FreeService,
    AccommodationService,
    SharedFacility,
    AccommodationFacility,
    Dormitory,
    AccommodationDormitory,
    GeneralRoom,
    AccommodationRoom,
    Review,
    AgeGroup,
    TravelType,
    Reservation,
    Coupon,
    UserCoupon,
)


class AccommodationDetailView(View):
        
    def get(self, request, accommodation_id):
        try:
            limit               = int(request.GET.get("limit", 5))
            offset              = int(request.GET.get("offset", 0))
            average_star_rating = Review.objects.filter(accommodation_id=accommodation_id).aggregate(Avg('star_rating'))["star_rating__avg"]
            
            accommodation = Accommodation.objects.select_related(
                'host'
                ).prefetch_related(
                'accommodation_service',
                'accommodation_facility',
                'accommodation_dormitory',
                'accommodation_room',
                'accommodationimage_set',
                'theme_set',
                'roomtype_set',
                'review_set',
                ).get(id=accommodation_id)
   

            accommodation_detail = {
                'id'                        : accommodation.id,
                'name'                      : accommodation.name,
                'description'               : accommodation.description,
                'number_of_guest'           : accommodation.number_of_guest,
                'check_in'                  : accommodation.check_in,
                'check_out'                 : accommodation.check_out,
                'address'                   : accommodation.address,
                'is_immediate_confirmation' : accommodation.is_immediate_confirmation,
                'image_url'                 : [image.image_url for image in accommodation.accommodationimage_set.all()],
                
                'host'                      : 
                    {
                        'name'      : accommodation.host.name,
                        'image_url' : accommodation.host.image_url
                    },
                'theme'                     : [
                    {
                        'name': theme.name
                    }for theme in accommodation.theme_set.all()
                ],
                'free_service'              : [
                    {
                        'id'        : freeservice.id,
                        'image_url' : freeservice.image_url,
                        'name'      : freeservice.name
                    }for freeservice in accommodation.accommodation_service.all()
                ],
                'shared_facility'           : [
                    {
                        'image_url' : facility.image_url,
                        'name'      : facility.name
                    }for facility in accommodation.accommodation_facility.all ()
                ],
                'roomtype'                  : [
                    {
                        'id'                 : roomtype.id,
                        'name'               : roomtype.name,
                        'price'              : roomtype.price,
                        'minimum'            : roomtype.minimum,
                        'maximum'            : roomtype.maximum,
                        'number_of_bed'      : roomtype.number_of_bed,
                        'minimum_reservation': roomtype.minimum_reservation,
                        'image'              : roomtype.image_url,
                        'room_type_amenity'  : [
                            {   
                                'name': roomamenity.name
                            }for roomamenity in accommodation.roomtype_set.all()
                        ]                        
                    } for roomtype in accommodation.roomtype_set.all()
                ],
                'review'                     : [
                    {
                        'star_rating'         : average_star_rating,
                        'number_of_reviews'   : accommodation.review_set.count(),
                        'user_reviews'        : [
                            {
                                'id'          : review.id,
                                'context'     : review.context,
                                'created_at'  : review.created_at,
                                'star_rating' : review.star_rating,
                                'user_name'   : review.user.name,
                                'image_url'   : review.image_url,
                            }for review in accommodation.review_set.all()[offset:limit+offset]
                        ]
                    }
                ]
            }
            return JsonResponse({'message': 'SUCCESS', 'accommodation_detail': accommodation_detail}, status=200)
        
        except Accommodation.DoesNotExist:
            return JsonResponse({'message': 'ACCOMMODATION_NOT_FOUND'}, status=404)
            

class AccommodationListView(View):
    def get(self, request):
        offset              = int(request.GET.get("offset", 0))
        limit               = int(request.GET.get("limit", 10))
        check_in            = request.GET.get("check_in",None)
        check_out           = request.GET.get("check_out",None)
        number_of_guest     = request.GET.get("number_of_guest",0)
        theme               = request.GET.get("theme",None)
        roomtype            = request.GET.get("roomtype",None)
        order               = request.GET.get('order',None)
        roomamenities       = [int(room_amenity) for room_amenity in request.GET.getlist("room_amenities")]
        shared_facilities   = [int(shared_facility) for shared_facility in request.GET.getlist("shared_facilities")]
        free_services       = [int(free_service) for free_service in request.GET.getlist("free_services")]
        dormitories         = [int(dormitory) for dormitory in request.GET.getlist("dormitories")]
        general_rooms       = [int(general_room) for general_room in request.GET.getlist("general_rooms")]

        print(type(order))
        q = Q()

        if theme:
            q &= Q(theme=theme)

        if shared_facilities:
            q &= Q(accommodationfacility__shared_facility_id__in= shared_facilities)

        if free_services:
            q &= Q(accommodationservice__free_service_id__in=free_services)

        if dormitories:
            q &= Q(accommodationdormitory__dormitory_id__in= dormitories)
        
        if general_rooms:
            q &= Q(accommodationroom__general_room_id__in=general_rooms)
        
        if roomamenities:
            q &= Q(roomtype__roomtypeamenity__room_amenity_id__in= roomamenities)

        sorting = {
            '0': 'price',
            '1': '-price',
            '2': '-star_rating'
        }
    
        accommodations = Accommodation.objects.prefetch_related(
            'accommodation_service',
            'accommodation_facility',
            'accommodationimage_set',
            'accommodation_dormitory',
            'accommodation_room',
            'roomtype_set',
            'theme_set',
        ).filter(q).order_by(sorting[order])

        accommodation_list = [ {
            'id'               : accommodation.id,
            'name'             : accommodation.name,
            'check-in'         : accommodation.check_in,
            'check-out'        : accommodation.check_out,
            'number_of_guest'  : accommodation.number_of_guest,
            'description'      : accommodation.description,
            'star_rating'      : accommodation.star_rating,
            'number_of_reviews': accommodation.review_set.count(),
            'price'            : accommodation.price,
            'image_url'        : accommodation.accommodationimage_set.all()[0].image_url,
        } for accommodation in accommodations[offset:limit+offset]]
        return JsonResponse({'message': 'SUCCESS', 'accommodation_list': list(accommodation_list)}, status=200)