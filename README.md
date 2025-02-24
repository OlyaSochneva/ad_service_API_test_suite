### Ad Service API Test Suite
The test suite covers 27 REST API requests. It reproduces approximately 80% of manual test cases, covering both positive and negative scenarios, ensuring high overall test coverage. 
 Project includes user and card creation/deletion, adding/removing cards from favorites, archiving/restoring, dialogs functionality, notifications (creation and reading), and retrieving lists of users, cities, and categories.
All tests are independent; each test generates its own test data, which is deleted after execution.
#### Navigation:

**assistant_methods.py** - generators, etc.

**check_response.py** - response parsing

**conftest.py** - fixtures

**data.py** - external data

**payloads.py** - methods for creating request bodies

**response_samples.py** - samples for parsing



