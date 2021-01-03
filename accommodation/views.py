import json
from django.shortcuts import render
from django.views     import View
from django.http      import JsonResponse
from django.db.models import Count, Avg
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
    AccommodationPayment,
    PaymentMethod
)


class AccommodationDetailView(View):
    def get(self, request, accommodation_id):
        try:
            limit  = int(request.GET.get("limit", "5"))
            offset = int(request.GET.get("offset", "0"))
            average_star_rating = Review.objects.filter(accommodation_id= accommodation_id).aggregate(Avg('star_rating'))["star_rating__avg"]
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

            accommodation_detail = [
                {
                'id'                        : accommodation.id,
                'name'                      : accommodation.name,
                'description'               : accommodation.description,
                'number_of_guest'           : accommodation.number_of_guest,
                'check_in'                  : accommodation.check_in,
                'check_out'                 : accommodation.check_out,
                'address'                   : accommodation.address,
                'is_immediate_confirmation' : accommodation.is_immediate_confirmation,
                'image_url'                 : [ image.image_url for image in accommodation.accommodationimage_set.all() ],
                'host'                      : [
                    {
                        'name'      : accommodation.host.name,
                        'image_url' : accommodation.host.image_url
                    }
                ],
                'theme'                     : [
                    {
                        'name': theme.name
                    }for theme in accommodation.theme_set.all()
                ],
                'free_service'              : [
                    {
                        'id' : freeservice.id,
                        'image_url': freeservice.image_url,
                        'name': freeservice.name
                    }for freeservice in accommodation.accommodation_service.all()
                ],
                'shared_facility'           : [
                    {
                        'image_url': facility.image_url,
                        'name': facility.name
                    }for facility in accommodation.accommodation_facility.all ()
                ],
                'roomtype'                  : [
                    {
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
                        'star_rating'       : round(average_star_rating, 1),
                        'number_of_reviews' : accommodation.review_set.count(),
                        'user_reviews'      : [
                            {
                                'id'          : review.id,
                                'context'     : review.context,
                                'created_at'  : review.created_at,
                                'star_rating' : review.star_rating,
                                'user_id'     : User.objects.get(id=review.user_id).name,
                                'image_url'   : review.image_url,
                            }for review in accommodation.review_set.all()[offset:limit]
                        ]
                    }
                ]
                }
            ]
            return JsonResponse({'message': 'SUCCESS', 'accommodation_detail': accommodation_detail}, status=200)
        
        except Accommodation.DoesNotExist:
            return JsonResponse({'message': 'ACCOMMODATION_NOT_FOUND'}, status = 404)
        

