
class Route(object):
    def __init__(self, company, route_id, route_name, route_number, direction1, direction2, days_active):
        self.company = company
        self.route_id = route_id
        self.route_name = route_name
        self.route_number = route_number
        self.direction1 = direction1
        self.direction2 = direction2
        self.days_active = days_active

class StopOrder(object):
    def __init__(self, company, route_id, direction, stop_id, stop_name, stop_order, stop_day):
        self.company = company
        self.route_id = route_id
        self.direction = direction
        self.stop_id = stop_id
        self.stop_name = stop_name
        self.stop_order = stop_order
        self.stop_day = stop_day

class StopLocation(object):
    def __init__(self, company, route_id, direction, stop_id, stop_name, latitude, longitude):
        self.company = company
        self.route_id = route_id
        self.direction = direction
        self.stop_id = stop_id
        self.stop_name = stop_name
        self.latitude = latitude
        self.longitude = longitude
