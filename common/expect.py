"""
expected conditions are utility's that allow us to check for a certain state, for example a "i am logged in" check will
return true if the current session is successfully authenticated.
these utility's are passed in to a "wait" instance and a executed in a loop until the expected response is returned
or the wait time has passed.
so if i want to [wait] [until] [i am logged in] my code will look like this: wait.until(i_am_logged_in())
"""
# don't remove these imports!!
from selenium.webdriver.support.expected_conditions import *

if visibility_of_element_located:
    pass  # this code is here just to keep pycharm from automatically removing the expected_conditions import
