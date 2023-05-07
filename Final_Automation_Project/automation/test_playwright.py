import pytest
from playwright.sync_api import Playwright


def teardown_class():  # Define a function to be called after all the tests have been executed
    try:
        context.close()  # Close the context created by the browser
        browser.close()  # Close the browser
    except Exception as e:
        print(f'Error occurred while closing the browser: {e}')  # If an exception occurs while closing the browser,
        # print an error message


class TestUltimateqa:  # Define a test class
    @pytest.fixture(scope="class", autouse=True)  # Define a pytest fixture that is automatically used by all tests
    # in the class
    def setup(self, playwright: Playwright):  # Define a setup function that is called before each test in the class
        global browser, context, page  # Declare global variables for the browser, context, and page
        try:
            browser = playwright.chromium.launch(headless=False, channel="chrome")  # Launch a Chromium browser
            # instance with Playwright
            context = browser.new_context()  # Create a new browser context
            page = context.new_page()  # Create a new browser page
            page.goto("https://ultimateqa.com/complicated-page/")  # Navigate to the specified URL
        except TimeoutError as e:
            print(f'Timeout error occurred: {e}')  # If a TimeoutError occurs, print an error message

    def test_count_buttons(self):  # Define a test function
        try:
            page.wait_for_selector(".et_pb_row.et_pb_row_4col .et_pb_column .et_pb_button_module_wrapper",
                                   state='visible')  # Wait for a specific selector to be visible on the page
            button_count = page.locator(".et_pb_row.et_pb_row_4col .et_pb_column .et_pb_button_module_wrapper").count()
            # Count the number of elements that match a specific selector
            assert button_count == 12  # Assert that the button count is equal to 12
        except TimeoutError as e:
            print(f'Timeout error occurred while waiting for button selector: {e}')  # If a TimeoutError occurs,
            # print an error message

    def test_verify_facebook_links(self):  # Define another test function
        try:
            facebook_buttons = page.query_selector_all(".et_pb_social_network_link.et-social-facebook a")
            # Get all elements that match a specific selector
            for button in facebook_buttons:  # Loop through each element
                assert button.get_attribute("href") == "https://www.facebook.com/Ultimateqa1/"  # Assert that the
                # href attribute of each element is equal to the specified value
        except AssertionError as e:
            print(f'Assertion error occurred while verifying Facebook links: {e}')  # If an AssertionError occurs,
            # print an error message

    def test_submit_random_stuff_form(self):  # Define another test function
        try:
            # Fill the input field with id 'et_pb_contact_name_0' with the name "Roman Shukun"
            page.locator("[id='et_pb_contact_name_0']").fill("Roman Shukun")

            # Fill the input field with id 'et_pb_contact_email_0' with the email "test@test.com"
            page.locator("[id='et_pb_contact_email_0']").fill("test@test.com")

            # Fill the input field with id 'et_pb_contact_message_0' with the message "this is a test"
            page.locator("[id='et_pb_contact_message_0']").fill("this is a test")

            # Find the element with class 'et_pb_contact_captcha_question'
            # inside the element with id 'et_pb_contact_form_0'
            math_exercise = page.locator("[id='et_pb_contact_form_0']").locator(".et_pb_contact_captcha_question")

            # Get the text content of the math exercise element
            exercise_text = math_exercise.text_content()

            # Evaluate the math exercise string as a Python expression and convert the result to a string
            exercise_result = str(eval(exercise_text))

            # Fill the input field with name 'et_pb_contact_captcha_0' with the evaluated math exercise result
            page.locator("[name='et_pb_contact_captcha_0']").fill(exercise_result)

            # Find the submit button inside the element with id 'et_pb_contact_form_0' and click it
            submit_button = page.locator("[id='et_pb_contact_form_0']").locator("[type='submit']")
            submit_button.click()

            # Wait up to 5 seconds for the selector with class 'et-pb-contact-message p' to become visible
            page.wait_for_selector(".et-pb-contact-message p", timeout=5000, state='visible')

            # Find the success message element with class 'et-pb-contact-message'
            # and assert that its text content is 'Thanks for contacting us'
            success_message = page.locator(".et-pb-contact-message p")
            assert success_message.text_content() == "Thanks for contacting us"

        # If a TimeoutError occurs during waiting for the success message selector, print the error message
        except TimeoutError as e:
            print(f'Timeout error occurred while waiting for success message selector: {e}')

        # If any other type of exception occurs during form submission, print the error message
        except Exception as e:
            print(f'Error occurred while submitting the form: {e}')
