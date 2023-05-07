import os
import pytest
import requests
import random

URL = 'http://localhost:8989/route'
KEY = '0d85b42e-4fc5-41f9-9cb8-f3fd892a03b1'
HEADERS = {'Content-Type': 'application/json'}


# Define a test class
class TestGetRoute:
    # Class method that generates random coordinates within the Berlin city limits
    @classmethod
    def get_random_coordinates(cls):
        berlin_lat = random.uniform(52.509730, 52.510565)
        berlin_lng = random.uniform(13.246165, 13.524944)
        return berlin_lat, berlin_lng

    # Class method that generates a list of 10,000 pairs of random start and end coordinates
    @classmethod
    @pytest.fixture
    def coordinates(cls):
        coordinates = []
        for i in range(10000):
            start, end = cls.get_random_start_end()
            coordinates.append((start, end))
        return coordinates

    # Class method that generates a random start and end pair of coordinates
    @classmethod
    def get_random_start_end(cls):
        start = cls.get_random_coordinates()
        end = cls.get_random_coordinates()
        return start, end

    # Test method that checks whether a path exists for each pair of coordinates in the coordinates list
    def test_path_exists(self, coordinates):
        for i, (start_point, end_point) in enumerate(coordinates):
            start = {'lat': start_point[0], 'lng': start_point[1]}
            end = {'lat': end_point[0], 'lng': end_point[1]}

            # Set the parameters for the request
            params = {
                'point': [f"{start['lat']},{start['lng']}", f"{end['lat']},{end['lng']}"],
                'profile': 'car',
                'locale': 'de',
                'calc_points': False,
                'key': KEY
            }

            # Make the request and check that the response has a path
            response = requests.get(URL, params=params, headers=HEADERS)
            # Raise an error if the response status code is not successful
            response.raise_for_status()
            paths = response.json().get('paths')
            assert paths is not None and len(paths) > 0, f'No paths found for coordinates {start_point}, {end_point}'

    # Test method that checks the correct response is returned for a single start and end pair of coordinates
    def test_single_point(self, coordinates):
        # Get random start and end coordinates
        start, end = self.get_random_start_end()

        # Set the parameters for the request
        params = {
            'point': [f"{start[0]},{start[1]}", f"{end[0]},{end[1]}"],
            'profile': 'car',
            'locale': 'de',
            'calc_points': False,
            'key': KEY
        }

        # Send a GET request to the API with the parameters
        response = requests.get(URL, params=params, headers=HEADERS)
        # Raise an error if the response status code is not successful
        response.raise_for_status()

        # Check that the response contains the expected data
        json_data = response.json()
        assert "hints" in json_data
        assert "visited_nodes.sum" in json_data["hints"]
        assert "visited_nodes.average" in json_data["hints"]
        assert "info" in json_data
        assert "copyrights" in json_data["info"]
        assert "took" in json_data["info"]
        assert "paths" in json_data
        assert len(json_data["paths"]) == 1

        path = json_data["paths"][0]
        assert "distance" in path
        assert "weight" in path
        assert "time" in path
        assert "transfers" in path
        assert "snapped_waypoints" in path

    # This function tests the structure of the response from the API
    def test_response_structure(self):
        # Get random start and end coordinates
        start, end = self.get_random_start_end()

        # Send a GET request to the API with the coordinates, profile, and other parameters
        response = requests.get(
            f'{URL}?point={start[0]},{start[1]}&point={end[0]},{end[1]}&profile=car&locale=de'
            f'calc_points=false&key={KEY}',
            headers=HEADERS)
        # Raise an error if the response status code is not successful
        response.raise_for_status()
        # Convert the response to JSON format
        json_response = response.json()

        # Check the structure of the JSON response by making sure certain keys exist and have expected values
        assert "paths" in json_response, "No paths found in response"
        assert isinstance(json_response["paths"], list), "Paths is not a list"
        assert all(isinstance(path, dict) for path in json_response["paths"]), "Paths contains non-dict elements"
        assert all("distance" in path for path in json_response["paths"]), "Distance not found in some paths"
        assert all("time" in path for path in json_response["paths"]), "Time not found in some paths"
        assert all("points" in path for path in json_response["paths"]), "Points not found in some paths"
        if "points" in json_response:
            assert isinstance(json_response["points"], list), "Points is not a list"
        if "instructions" in json_response:
            assert isinstance(json_response["instructions"], list), "Instructions is not a list"
            assert "hints" in json_response, "Hints not found in response"
            assert isinstance(json_response["hints"], dict), "Hints is not a dictionary"
            assert "visited_nodes.average" in json_response["hints"], "Visited_nodes.average not found in hints"
            assert "visited_nodes.sum" in json_response["hints"], "Visited_nodes.sum not found in hints"
            assert "info" in json_response, "Info not found in response"
            assert isinstance(json_response["info"], dict), "Info is not a dictionary"
            assert "copyrights" in json_response["info"], "Copyrights not found in info"
            assert "took" in json_response["info"], "Took not found in info"

    # This function tests for suspicious routes by comparing the expected duration
    # with the actual duration for each coordinate pair
    def test_suspicious_routes(self, coordinates):
        # Create an empty list to store suspicious routes
        suspicious_routes = []
        # Iterate over each pair of coordinates
        for i, (start_point, end_point) in enumerate(coordinates):
            # Convert the coordinates into the required format
            start = {'lat': start_point[0], 'lng': start_point[1]}
            end = {'lat': end_point[0], 'lng': end_point[1]}

            # Set the parameters for the request
            params = {
                'point': [f"{start['lat']},{start['lng']}", f"{end['lat']},{end['lng']}"],
                'profile': 'car',
                'locale': 'de',
                'calc_points': False,
                'key': KEY
            }

            # Send a GET request to the API with the query parameters
            response = requests.get(URL, params=params, headers=HEADERS)
            # Raise an error if the response status code is not successful
            response.raise_for_status()
            # Convert the response to JSON format
            response_data = response.json()
            # Store the distance and the duration(converted ms to s) from the response
            duration = response_data["paths"][0]["time"]/1000
            distance = response_data["paths"][0]["distance"]

            # Calculate the expected duration(in milliseconds)
            # 50 km/h as an average driving speed in Berlin
            # The expression 50/3.6 converts the speed from km/h to m/s, because the distance value is in meters.
            # Dividing distance by the speed gives the time it would take to travel that distance at that speed,
            # in seconds.
            expected_duration = distance / (50 / 3.6)

            # Check if the duration and distance match
            if abs(expected_duration - duration) <= 0.1 * expected_duration:  # Allow 10% tolerance
                suspicious_routes.append(coordinates)

        # Delete suspicious_routes.txt file if exist.
        if os.path.exists('suspicious_routes.txt'):
            os.remove('suspicious_routes.txt')

        # Write to suspicious_routes.txt the inconsistent coordinates if any
        if suspicious_routes:
            with open('suspicious_routes.txt', 'w') as f:
                for coordinate_pair in suspicious_routes:
                    f.write(f'{coordinate_pair}\n')

    # This function tests the response returns error 400 with error message as per the documentation when an invalid
    # vehicle type sent in the request.
    def test_get_route_with_invalid_profile(self):
        # Get random start and end coordinates
        start, end = self.get_random_start_end()

        # Set the parameters for the request with invalid profile
        params = {
            'point': [f"{start[0]},{start[1]}", f"{end[0]},{end[1]}"],
            'profile': 'invalid_vehicle',
            'locale': 'de',
            'calc_points': False,
            'key': KEY
        }

        # Send a GET request to the API with the parameters
        response = requests.get(URL, params=params, headers=HEADERS)

        # Check whether the response status code is 400 (Bad Request).
        if response.status_code != 400:
            # If it's not, the test fails with an AssertionError message.
            raise AssertionError(f"Expected status code 400 but got {response.status_code}")

        # Check whether the response body contains a specific error message indicating that the requested vehicle
        # type is invalid.
        assert "The requested profile 'invalid_vehicle' does not exist.\n" \
               "Available profiles: [car]" in response.json()["message"]

    # This function tests the response returns error 400
    # with error message as per the documentation when start point is missing
    def test_get_route_with_missing_start_point(self):
        # Get random start and end coordinates
        start, end = self.get_random_start_end()

        # Set the parameters for the request with missing end point
        params = {
            'point': [f"{start[0]},{start[1]}"],
            'profile': 'car',
            'locale': 'de',
            'calc_points': False,
            'key': KEY
        }

        # Send a GET request to the API with the parameters
        response = requests.get(URL, params=params, headers=HEADERS)

        # Check whether the response status code is 400 (Bad Request).
        if response.status_code != 400:
            # If it's not, the test fails with an AssertionError message.
            raise AssertionError(f"Expected status code 400 but got {response.status_code}")

        # Check whether the response body contains a specific error message indicating that at least two points have
        # to be specified.
        assert "At least 2 points have to be specified, but was:1" in response.json()["message"]
