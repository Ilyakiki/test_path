import requests
from json import loads
from math import sin,cos,acos,pi

class Vehicle:
    ids=0
    @classmethod
    def add(cls):
        cls.ids+=1
        return cls.ids



    def __init__(self,id=None,name=None,model=None,year=0,color=None,price=-10000,latitude=0,longitude=0):
        self.ids = self.add()
        if id==None:
            self.id=self.ids
        else:
            self.id=id

        self.name=name
        self.model=model
        self.year=year
        self.color=color
        self.price=price
        self.latitude=latitude
        self.longitude=longitude


    def __repr__(self):
        return f"<Vehicle: {self.name} {self.model} {self.year} {self.color} {self.price}>"


class VehicleManager:
    def __init__(self,url):
        self.url=url
        self.vehicle_list = []
        r = requests.get(self.url + "/vehicles").content
        r = loads(r)
        for vehicle in r:
            self.vehicle_list.append(Vehicle(vehicle['id'],vehicle['name'],vehicle['model'],vehicle['year'],vehicle['color'],vehicle['price'],vehicle['latitude'],vehicle['longitude']))

    def add_vehicle(self,vehicle:Vehicle):
        self.vehicle_list.append(vehicle)
        return vehicle

    def delite_vehicle(self,id):
        for i in range(len(self.vehicle_list)):
            if self.vehicle_list[i].id==id:
                del self.vehicle_list[i]
                return 'Элемент удален'
        return 'Такого элемента нет'

    def filter_vehicles(self,params:dict):
        filtered_list=[]
        for i in self.vehicle_list:
            f=True
            obj_dict=i.__dict__
            for y in params.keys():
                if obj_dict[y]!=params[y]:
                    f=False
            if f:
                filtered_list.append(i)
        return filtered_list

    def get_vehicles(self):
        return self.vehicle_list
    def get_vehicle(self,**kwargs):
        for i in self.vehicle_list:
            if i.id==kwargs['vehicle_id']:
                return i
        return None

    def update_vehicle(self,vehicle:Vehicle):
        for i in range(len(self.vehicle_list)):
            if self.vehicle_list[i].id==vehicle.id:
                self.vehicle_list[i]=vehicle
        return vehicle

    def get_distance(self,id1,id2):
        latitude1 = self.get_vehicle(vehicle_id=id1).latitude
        longitude1 = self.get_vehicle(vehicle_id=id1).longitude
        latitude2 = self.get_vehicle(vehicle_id=id2).latitude
        longitude2 = self.get_vehicle(vehicle_id=id2).longitude
        d = acos(sin(latitude1 * (pi / 180)) * sin(latitude2 * (pi / 180)) + cos(latitude1 * (pi / 180)) * cos(
            latitude2 * (pi / 180)) * (cos(longitude1 * (pi / 180) - longitude2 * (pi / 180))))
        R=6371
        return d*R*1000


    def get_nearest_vehicle(self,id):
        min_distance=99999999999999999999
        nearest_vechicle=None
        for i in self.vehicle_list:
            if i.id!=id:
                if self.get_distance(id,i.id)<min_distance:
                    min_distance=self.get_distance(id,i.id)
                    nearest_vechicle=i

        return nearest_vechicle

