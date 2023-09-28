def is_admin(ParkingSystemUser):
    return ParkingSystemUser.is_authenticated and ParkingSystemUser.is_superuser