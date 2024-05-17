import math
from typing import List, Dict, Any
import requests
from models import Vehicle
from dataclasses import asdict


class VehicleManager:
    def __init__(self, url: str):
        self.url = url

    def get_vehicles(self) -> List[Vehicle]:
        url = f"{self.url}/vehicles"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return [Vehicle(**item) for item in data]
        return []

    def filter_vehicles(self, params: Dict[str, Any]) -> List[Vehicle]:
        def result(vehicle: Vehicle) -> bool:
            return all(getattr(vehicle, key, None) == value for key, value in params.items())

        all_vehicles = self.get_vehicles()
        return [vehicle for vehicle in all_vehicles if result(vehicle)]

    def get_vehicle(self, vehicle_id: int) -> Vehicle | None:
        url = f"{self.url}/vehicles/{vehicle_id}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return Vehicle(**data)
        return None

    def add_vehicle(self, vehicle: Vehicle) -> Vehicle | None:
        url = f"{self.url}/vehicles"
        response = requests.post(url, data=asdict(vehicle))
        if response.status_code == 201:
            return vehicle
        return None

    def update_vehicle(self, vehicle: Vehicle) -> Vehicle | None:
        data = asdict(vehicle)
        url = f"{self.url}/vehicles/{data['id']}"
        response = requests.put(url, data=data)
        if response.status_code == 200:
            return vehicle
        return None

    def delete_vehicle(self, id: int) -> Any:
        url = f"{self.url}/vehicles/{id}"
        response = requests.delete(url)
        if response.status_code == 204:
            return 204
        return None

    def get_distance(self, id1: int, id2: int) -> float | None:
        first_car = self.get_vehicle(vehicle_id=id1)
        second_car = self.get_vehicle(vehicle_id=id2)

        if first_car is None or second_car is None:
            return None

        r = 6371.0
        lat1 = math.radians(first_car.latitude)
        lon1 = math.radians(first_car.longitude)
        lat2 = math.radians(second_car.latitude)
        lon2 = math.radians(second_car.longitude)

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        distance = r * c
        return distance

    def get_nearest_vehicle(self, id: int) -> Vehicle | None:

        distances = {}
        for vehicle in self.get_vehicles():
            if vehicle.id != id:
                distance = self.get_distance(id1=id, id2=vehicle.id)
                if distance is not None:
                    distances[vehicle.id] = distance

        if distances:
            nearest_id = min(distances, key=distances.get)
            nearest_vehicle = self.get_vehicle(vehicle_id=nearest_id)
            return nearest_vehicle
