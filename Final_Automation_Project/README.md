================
Final-Automation-Project
================

This Final Automation project includes 3 parts :

Final_Automation_Project/questions : 
Part 1 - Pokemon Damage Calculator and Take Highest Note.

Final_Automation_Project/automation :
3- API automation using PyTest.
4- FE Automation using PlayWright and PyTest.

================
Part 1 - Pokemon Damage Calculator
===============

This program is a simple text-based game where two players select a type of attack and defense for their Pokemon and battle against each other. The game uses a matchup dictionary to determine the effectiveness of the attack type against the defense type, and calculates damage based on the attack power and defense power.

++++++++++++
requirements:
++++++++++++

This program requires the logging module from Python's standard library.

++++++++++++
Classes:
++++++++++++

Player:

The Player class represents a player in the game. It has three attributes: first_name, last_name, and pokemon_name. It also has a life attribute which starts at 100 and decreases as the player takes damage.

PokemonBattle:

The PokemonBattle class represents a game instance. It takes two Player objects as arguments in its constructor, representing the first and second players in the game.

The play method starts the game loop and handles turn-based gameplay. It alternates between the attack player and defense player, prompting each player to select an attack or defense type and a power level. It then calculates the damage and updates the players' life totals. The game continues until one of the players has a life total of zero or less, at which point the _print_winner method is called to declare the winner.

The calculate_damage method is a static method that takes the attack type, defense type, attack power, and defense power as arguments, and uses the matchup dictionary to calculate the damage inflicted on the defense player.

The _turn method is a static method that takes a Player object and an action (either "attack" or "defense") as arguments, and prompts the player to select an action type and a power level. It validates the input and returns the action type and power level as a tuple.

++++++++++++
instructions to run:
++++++++++++

To use this program, create two Player objects with their first name, last name, and Pokemon name. Then create a PokemonBattle object with the two Player objects as arguments. Finally, call the play method on the PokemonBattle object to start the game.

For example:

player_1 = Player("Avi", "Via", "Charmander")
player_2 = Player("Moshe", "Via", "Squirtle")

game = PokemonBattle(player_1, player_2)
game.play()

================
Part 2 - Take Highest Note
===============

This program returns the highest note from a list of students with their respective notes.

++++++++++++
requirements:
++++++++++++

Python 3.x

++++++++++++
How the program works:
++++++++++++

The code creates a list called students_list, which contains dictionaries of students' names and their respective lists of notes. Each note is a float or integer between 0 and 10.

The highest_note function receives a list of students as input and returns a list of dictionaries with the name of each student and their highest note. The max function is used to find the highest note of each student. If a student has no notes, their top note is set to 0 using the default parameter of the max function.

Finally, the highest_note function is called with the students_list as the argument, and the result is printed to the console. The result is a list of dictionaries, where each dictionary contains the name of the student and their highest note.

++++++++++++
instructions to run:
++++++++++++

To use the script, follow these steps:

Edit the students_list variable in the script to include a list of students with their respective notes.
Run the script in your Python environment.
The script will output a list of dictionaries, each containing the name of a student and their highest note achieved.

Output example:

[
    {'name': 'Avi', 'top_note': 5},
    {'name': 'Moshe', 'top_note': 5.5},
    {'name': 'Roman', 'top_note': 0}
]

================
Part 3 - API automation using PyTest.
===============
The code is a Python script that contains a test suite written using the Pytest testing framework. 
The script uses the Requests library to send HTTP requests to a get route service from GraphHopper and verify that the responses are valid.

The script defines 4 test methods:

test_path_exists: This test sends HTTP GET requests to the Get Route service for 10,000 randomly generated pairs of start and end coordinates and verifies that the response contains at least one valid path.

test_single_point: This test sends an HTTP GET request to the Get Route service for a randomly generated pair of start and end coordinates and verifies that the correct response is returned (as per the documentation).

test_response_structure: This test sends an HTTP GET request to the Get Route service for a randomly generated pair of start and end coordinates and verifies that the response has the expected JSON structure.

test_suspicious_routes: This test sends HTTP GET requests to the Get Route service for a list of coordinate pairs and verifies that the response does not contain any suspicious routes.

test_get_route_with_invalid_profile: This test sends HTTP GET requests to the Get Route service for a randomly generated pair of start and end coordinate and invalid profile and verifies that the response returns error code 400 with the expected error message .

test_get_route_with_missing_start_point: This test sends HTTP GET requests to the Get Route service for a randomly generated pair of start and end coordinate and missing start point and verifies that the response returns error code 400 with the expected error message .

++++++++++++
requirements:
++++++++++++

Python 3.x
pytest module
requests module
os library

++++++++++++
How the program works:
++++++++++++

The TestGetRoute class contains a few methods that are used to generate random sets of coordinates and to make requests to the GetRoute API with those coordinates.

The get_random_coordinates() method generates a random latitude and longitude within a specific range in Berlin, Germany.
        
The get_random_start_end() method generates two random sets of coordinates using the get_random_coordinates() method. These are used as the start and end points for a route.

The coordinates method is a pytest fixture that generates 10,000 sets of random start and end coordinates using the get_random_start_end() method. 

Each test function takes a set of geographic coordinates as input and sends a request to the API. The response from the API is then checked to see whether it meets the expectations of the test function.

The test_path_exists function iterates over each coordinate pair in the input and sends a request to the API to check whether a path exists between the two coordinates. If a path is not found, an assertion error is raised.

The test_single_point function selects a random starting and ending point and sends a request to the API to retrieve information about the route between them. The response is checked to ensure that it has the expected structure and contains the necessary information.

The test_response_structure function sends a request to the API using a random set of starting and ending points and checks the structure of the response to ensure that it contains the expected keys and values.

The test_suspicious_routes function sends a request to the API for each coordinate pair in the input and After receiving the response from the API, the code extracts the duration and distance of the route from the JSON response. It then calculates the expected duration of the route based on an average speed of 50 km/h (13.89 m/s), and compares the actual and expected durations to see if they differ by more than 10%.

If the route's duration and expected duration differ by more than 10%, the code appends the coordinates of that route to a list called suspicious_routes.

Finally, if there are any suspicious routes, the code opens a file called suspicious_routes.txt and writes each pair of coordinates to the file. The pairs of coordinates are written to the file in a loop using the write method on the file object, with a newline character appended after each pair.

++++++++++++
instructions to run:
++++++++++++
Install pytest and requests modules:
pip install pytest requests

set up GraphHopper locally:
* Install Java
* Brew install Maven
* Brew install wget

* git clone --recursive git@github.com:graphhopper/graphhopper.git
* cd graphhopper

* mvn clean install -DskipTests
# start GraphHopper and before download the road data

* wget http://download.geofabrik.de/europe/germany/berlin-latest.osm.pbf
* java -Ddw.graphhopper.datareader.file=berlin-latest.osm.pbf -jar web/target/graphhopper-web-*.jar server config-example.yml
# This does the following things:
# - it creates routable files for graphhopper in the folder graph-data (see the config.yml)
# - it creates data for a special routing algorithm to improve query speed. (this and the previous step is skipped, if the graph-data folder is already present)
# - it starts the web service to service the UI and endpoints like /route
# After 'Server - Started' appears go to http://localhost:8989/ and you should see a GraphHopper map with a polygon.

Open a terminal or command prompt and navigate to your working directory.
Run the tests using the pytest command:
pytest GraphHopper.py

The pytest command will automatically discover and run all the tests defined in the TestGetRoute class. 
The output will indicate whether the tests passed or failed, and will provide additional information if any tests failed.

================
Part 4 - FE Automation using PlayWright and PyTest.
===============

This code is a Python script that uses the pytest testing framework and the Playwright library to perform automated web testing on the https://ultimateqa.com/complicated-page/ website.

The script defines a class named TestUltimateqa that contains three test methods: test_count_buttons, test_verify_facebook_links, and test_submit_random_stuff_form.

The setup method is defined as a pytest fixture with autouse=True, meaning it will run automatically before each test method in the class. The setup method launches a Chromium browser using the Playwright library and navigates to the target webpage.

The test_count_buttons method counts the number of buttons on the webpage and asserts that there are 12 buttons present.

The test_verify_facebook_links method verifies that all Facebook buttons on the webpage point to the correct Facebook page by checking the href attribute of each button.

The test_submit_random_stuff_form method fills out and submits a contact form on the webpage, including solving a math problem to complete the CAPTCHA. It then waits for a success message to appear and asserts that the message contains the text "Thanks for contacting us".

Finally, the teardown_class method is defined to close the browser after all the test methods have run. If an error occurs while closing the browser, the error message will be printed.

++++++++++++
requirements:
++++++++++++

Python 3.x:
pytest 
playwright library
chromium driver

++++++++++++
How the program works:
++++++++++++

The code imports the necessary libraries: pytest for testing and Playwright for automating the browser.

The teardown_class function is defined. This function is called after all tests in the test class have run, and it closes the browser window and context.

The TestUltimateqa class is defined, which contains three test methods:

test_count_buttons: This test checks that there are 12 buttons on the page.

test_verify_facebook_links: This test verifies that the Facebook links on the page lead to the correct page.

test_submit_random_stuff_form: This test fills out and submits a form on the page and verifies that the submission was successful.

The setup fixture is defined, which sets up the browser environment before each test. This fixture creates a new instance of the Chromium browser and a new context and page in the browser. It then navigates to the complicated page on the Ultimate QA website.

Each test method in the TestUltimateqa class uses the page object to interact with the webpage. The wait_for_selector method is used to wait for a specific element to be present on the page before proceeding. The locator method is used to locate an element on the page, and the fill and click methods are used to interact with the element. Assertions are used to check that the expected behavior occurs.

If any errors or exceptions occur during the tests, they are caught and printed to the console.

After all tests have run, the teardown_class function is called to close the browser window and context.

Overall, the code sets up a browser environment using Playwright, interacts with a webpage to perform tests, and verifies that the expected behavior occurs.

++++++++++++
instructions to run:
++++++++++++

Install pytest and playwright libraries. Open your terminal or command prompt and run the following commands:
pip install pytest
pip install playwright
Then, install the Chromium browser driver by running:
playwright install chromium
Open your terminal or command prompt and navigate to the directory where you saved the script.
Run the script by running the following command:
pytest test_playwright.py
The tests will run and the output will be displayed in the terminal/command prompt. Any errors or failures will be reported in the output.

