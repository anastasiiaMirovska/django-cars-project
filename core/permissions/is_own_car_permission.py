from rest_framework.permissions import BasePermission


class IsOwnCar(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        car_id = view.kwargs['pk']
        if user.user_cars.filter(id=car_id).exists():
            return True
        return False
