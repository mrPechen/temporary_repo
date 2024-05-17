from services import VehicleManager
from models import Vehicle

manager = VehicleManager(url="https://test.tspb.su/test-task")
print(manager.get_vehicles())
print(manager.filter_vehicles(params={'name': "Toyota"}))
print(manager.get_vehicle(vehicle_id=1))
print(manager.add_vehicle(vehicle=Vehicle(name='new_name', model='_new_model',
                                          year=123, color='new_color',
                                          price=1344, latitude=1.123,
                                          longitude=1.234)))
print(manager.update_vehicle(vehicle=Vehicle(id=1, name='update_name', model='update_model',
                                             year=321, color='update_color',
                                             price=4431, latitude=2.22,
                                             longitude=3.333)))

print(manager.delete_vehicle(id=1))
print(manager.get_distance(id1=1, id2=2))
print(manager.get_nearest_vehicle(id=1))