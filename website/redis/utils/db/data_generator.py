class DataGenerator:

    def __init__(self):
        self.data = None

    def generate_data(self):
        self.data = [{
            f"planes:0":
                {
                    "kind": "tourist",
                    "name": "AirPacensus-0",
                    "num_seats": 40,
                    "category": "global",
                    "from": "Badajoz",
                    "to": "Barcelona",
                    "days": "Tuesday",
                    "hour": "7:00",
                    "price": 32
                },
            f"planes:1":
                {
                    "kind": "tourist",
                    "name": "AirPacensus-1",
                    "num_seats": 50,
                    "category": "global",
                    "from": "Badajoz",
                    "to": "Barcelona",
                    "days": "Thursday",
                    "hour": "7:00",
                    "price": 40,
                }
        }]

        for data in self.data:
            for plane in data.keys():
                cur_plane = self.data[0][plane]
                for seat in range(cur_plane['num_seats']):
                    self.data[0][plane]["seat_"+str(seat)] = ''

    def get_data(self):
        return self.data
