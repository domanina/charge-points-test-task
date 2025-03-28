# Test automation script (API + UI)


---

---
### Prerequisites (Before Running Locally)
1. Minimal version of python `python3.11`
2. Using `.env_example` file create `.env` file to load environment variables 
3. Install the required python packages:

```bash
  pip3 install -r requirements.txt
  playwright install
```

---
## Running Tests

To execute the tests, use the following commands:

Run all tests with verbose output:

```bash
  pytest -v
```
---

## Allure

run with Allure reports:

```bash
  pytest -v --alluredir=allure-results
```

create local Allure report:

```bash
  allure serve allure-results
```


## Test Coverage
### UI Tests
- Navigation across key pages
- Verification of form elements, field validation, and button visibility.
- Tests for creating and deleting points.

### Functional Tests
- Validation of API requests (`POST`, `GET`, `DELETE`).
- Ensuring data integrity between UI elements and backend responses.
- Tests for edge cases and invalid inputs.
- Verification of error messages and status handling for failed actions.
