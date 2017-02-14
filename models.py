
class Route(object):
    def __init__(self, company, route_id, route_name, route_number, direction1, direction2, days_active):
        self.company = company
        self.route_id = route_id
        self.route_name = normalizeName(route_name)
        self.route_number = route_number
        self.direction1 = normalizeDirection(direction1)
        self.direction2 = normalizeDirection(direction2)
        self.days_active = days_active

class StopOrder(object):
    def __init__(self, company, route_id, direction, stop_id, stop_name, stop_order, stop_day):
        self.company = company
        self.route_id = route_id
        self.direction = normalizeDirection(direction)
        self.stop_id = stop_id
        self.stop_name = normalizeName(stop_name)
        self.stop_order = stop_order
        self.stop_day = stop_day

class StopLocation(object):
    def __init__(self, company, route_id, direction, stop_id, stop_name, latitude, longitude):
        self.company = company
        self.route_id = route_id
        self.direction = normalizeDirection(direction)
        self.stop_id = stop_id
        self.stop_name = normalizeName(stop_name)
        self.latitude = latitude
        self.longitude = longitude

def normalizeName(name):
    return name.title()

def normalizeDirection(direction):
    return direction.lower()
