class DataSet(object):
    all_routes = {}
    all_stop_orders = {}
    all_stop_locations = {}

    # all_routes -> comany -> route
    def saveRoute(self, route):
        company = route.company
        if company not in self.all_routes:
            self.all_routes[company] = []
        self.all_routes[company].append(route.__dict__)

    # all_stop_orders -> company -> route_id -> direction -> stopOrder
    def saveStopOrder(self, stopOrder):
        company = stopOrder.company
        route_id = stopOrder.route_id
        direction = stopOrder.direction
        if company not in self.all_stop_orders:
            self.all_stop_orders[company] = {}
        if route_id not in self.all_stop_orders[company]:
            self.all_stop_orders[company][route_id] = {}
        if direction not in self.all_stop_orders[company][route_id]:
            self.all_stop_orders[company][route_id][direction] = []
        self.all_stop_orders[company][route_id][direction].append(stopOrder.__dict__)

    # all_stop_locations -> company -> route_id -> direction -> stopLocation
    def saveStopLocation(self, stopLocation):
        company = stopLocation.company
        route_id = stopLocation.route_id
        direction = stopLocation.direction
        if company not in self.all_stop_locations:
            self.all_stop_locations[company] = {}
        if route_id not in self.all_stop_locations[company]:
            self.all_stop_locations[company][route_id] = {}
        if direction not in self.all_stop_locations[company][route_id]:
            self.all_stop_locations[company][route_id][direction] = []
        self.all_stop_locations[company][route_id][direction].append(stopLocation.__dict__)
