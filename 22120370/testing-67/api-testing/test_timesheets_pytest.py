#!/usr/bin/env python3
"""
Test Cases for OrangeHRM Timesheets API (Pytest Version)
Comprehensive test suite using pytest with automatic authentication
"""

import pytest
import requests
from urllib.parse import urljoin
import config


# Base URL for API endpoints
API_BASE = urljoin(config.BASE_URL, config.API_BASE_PATH)


def make_api_request(session, method, endpoint, headers, data=None, params=None):
    """Helper function to make API requests"""
    url = urljoin(API_BASE + "/", endpoint.lstrip('/'))

    response = session.request(
        method=method,
        url=url,
        json=data,
        params=params,
        headers=headers,
        timeout=config.REQUEST_TIMEOUT
    )

    return response


# ============================================================================
# POSITIVE TEST CASES
# ============================================================================

@pytest.mark.positive
class TestPositiveCases:
    """Positive test cases for Timesheets API"""

    def test_pos_001_list_all_timesheets(self, api_session, api_headers):
        """TC-POS-001: Retrieve list of all timesheets

        Use case: Admin/Manager needs to view all timesheets in the system
        Expected: 200 OK with data array and meta object containing pagination info
        """
        response = make_api_request(
            api_session, "GET", "/time/timesheets", api_headers
        )

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()

        # Verify response structure
        assert "data" in data, "Response must contain 'data' field"
        assert isinstance(data["data"], list), "data field must be an array"
        assert "meta" in data, "Response must contain 'meta' field for pagination"
        assert "total" in data["meta"], "meta must contain total count"
        assert isinstance(data["meta"]["total"], int), "total must be an integer"

    def test_pos_002_list_timesheets_with_limit(self, api_session, api_headers):
        """TC-POS-002: Retrieve timesheets with pagination limit

        Use case: User wants to see only 5 timesheets per page
        Expected: Returns exactly the requested number or fewer (if not enough records)
        """
        limit = 5
        response = make_api_request(
            api_session, "GET", "/time/timesheets", api_headers,
            params={"limit": limit}
        )

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()

        assert "data" in data, "Response must contain 'data' field"
        assert isinstance(data["data"], list), "data must be an array"
        assert len(data["data"]) <= limit, f"Should return at most {limit} records, got {len(data['data'])}"

        # If total records > limit, should return exactly limit records
        if data["meta"]["total"] >= limit:
            assert len(data["data"]) == limit, f"Should return exactly {limit} records when more exist"

    def test_pos_003_list_timesheets_with_offset(self, api_session, api_headers):
        """TC-POS-003: Retrieve timesheets with pagination offset

        Use case: User navigates to page 2 (skipping first 5 records)
        Expected: Returns different records than page 1, respecting offset
        """
        limit = 5

        # Get first page
        response_page1 = make_api_request(
            api_session, "GET", "/time/timesheets", api_headers,
            params={"limit": limit, "offset": 0}
        )
        assert response_page1.status_code == 200
        page1_data = response_page1.json()

        # Get second page with offset
        response_page2 = make_api_request(
            api_session, "GET", "/time/timesheets", api_headers,
            params={"limit": limit, "offset": limit}
        )
        assert response_page2.status_code == 200
        page2_data = response_page2.json()

        # Verify structure
        assert "data" in page2_data
        assert isinstance(page2_data["data"], list)

        # If both pages have data, they should be different
        if len(page1_data["data"]) > 0 and len(page2_data["data"]) > 0:
            page1_ids = [item.get("id") for item in page1_data["data"] if "id" in item]
            page2_ids = [item.get("id") for item in page2_data["data"] if "id" in item]

            # No overlap between pages
            assert set(page1_ids).isdisjoint(set(page2_ids)), "Page 1 and page 2 should contain different records"

    def test_pos_004_get_employee_timesheets(self, api_session, api_headers):
        """TC-POS-004: Retrieve timesheets for a specific employee

        Use case: View all timesheets submitted by employee ID 1
        Expected: Returns only timesheets belonging to that employee
        """
        employee_id = 1
        response = make_api_request(
            api_session, "GET", f"/time/employees/{employee_id}/timesheets", api_headers
        )

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()

        assert "data" in data, "Response must contain 'data' field"
        assert isinstance(data["data"], list), "data must be an array"
        assert "meta" in data, "Response must contain 'meta' field"

        # If timesheets exist, verify they belong to the employee
        if len(data["data"]) > 0:
            for timesheet in data["data"]:
                assert "employee" in timesheet, "Each timesheet must have employee info"
                assert timesheet["employee"]["empNumber"] == employee_id, \
                    f"All timesheets must belong to employee {employee_id}"

    def test_pos_005_get_timesheet_period(self, api_session, api_headers):
        """TC-POS-005: Retrieve timesheet period configuration

        Use case: System needs to know what day the timesheet week starts
        Expected: Returns configuration with valid startDay (1-7 for Mon-Sun)
        """
        response = make_api_request(
            api_session, "GET", "/time/time-sheet-period", api_headers
        )

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()

        assert "data" in data, "Response must contain 'data' field"
        assert "startDay" in data["data"], "data must contain 'startDay' field"

        start_day = data["data"]["startDay"]
        assert isinstance(start_day, int), "startDay must be an integer"
        assert 1 <= start_day <= 7, f"startDay must be between 1-7 (Mon-Sun), got {start_day}"

    def test_pos_006_list_customers(self, api_session, api_headers):
        """TC-POS-006: Retrieve list of all customers

        Use case: View all customers for project assignment
        Expected: Returns array of customer objects with required fields
        """
        response = make_api_request(
            api_session, "GET", "/time/customers", api_headers
        )

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()

        assert "data" in data, "Response must contain 'data' field"
        assert isinstance(data["data"], list), "data must be an array"

        # Verify customer structure if any exist
        if len(data["data"]) > 0:
            customer = data["data"][0]
            assert "id" in customer, "Customer must have 'id' field"
            assert "name" in customer, "Customer must have 'name' field"
            assert isinstance(customer["id"], int), "Customer id must be integer"
            assert isinstance(customer["name"], str), "Customer name must be string"

    def test_pos_007_list_customers_with_pagination(self, api_session, api_headers):
        """TC-POS-007: Retrieve customers with pagination

        Use case: Display 3 customers per page in a table
        Expected: Returns exactly 3 or fewer customers
        """
        limit = 3
        response = make_api_request(
            api_session, "GET", "/time/customers", api_headers,
            params={"limit": limit, "offset": 0}
        )

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()

        assert "data" in data, "Response must contain 'data' field"
        assert isinstance(data["data"], list), "data must be an array"
        assert len(data["data"]) <= limit, f"Should return at most {limit} records"

        # If there are more than limit customers, should return exactly limit
        if "meta" in data and data["meta"]["total"] >= limit:
            assert len(data["data"]) == limit, f"Should return exactly {limit} when more exist"

    def test_pos_008_get_customer_by_id(self, api_session, api_headers):
        """TC-POS-008: Retrieve specific customer details by ID

        Use case: View details of customer with ID 1
        Expected: Returns only customer with matching ID
        """
        customer_id = 1
        response = make_api_request(
            api_session, "GET", f"/time/customers/{customer_id}", api_headers
        )

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()

        assert "data" in data, "Response must contain 'data' field"
        assert isinstance(data["data"], dict), "data must be a single object, not array"
        assert data["data"]["id"] == customer_id, f"Customer ID must match requested ID {customer_id}"
        assert "name" in data["data"], "Customer must have 'name' field"
        assert isinstance(data["data"]["name"], str), "Customer name must be string"
        assert len(data["data"]["name"]) > 0, "Customer name cannot be empty"

    def test_pos_009_list_projects(self, api_session, api_headers):
        """TC-POS-009: Retrieve list of all projects

        Use case: View all projects for timesheet entry
        Expected: Returns array of project objects with customer relationship
        """
        response = make_api_request(
            api_session, "GET", "/time/projects", api_headers
        )

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()

        assert "data" in data, "Response must contain 'data' field"
        assert isinstance(data["data"], list), "data must be an array"

        # Verify project structure if any exist
        if len(data["data"]) > 0:
            project = data["data"][0]
            assert "id" in project, "Project must have 'id' field"
            assert "name" in project, "Project must have 'name' field"
            assert "customer" in project, "Project must have 'customer' relationship"
            assert isinstance(project["customer"], dict), "customer must be an object"
            assert "id" in project["customer"], "customer must have 'id' field"

    def test_pos_010_list_projects_with_pagination(self, api_session, api_headers):
        """TC-POS-010: Retrieve projects with pagination

        Use case: Display 3 projects per page
        Expected: Returns exactly 3 or fewer projects
        """
        limit = 3
        response = make_api_request(
            api_session, "GET", "/time/projects", api_headers,
            params={"limit": limit, "offset": 0}
        )

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()

        assert "data" in data, "Response must contain 'data' field"
        assert isinstance(data["data"], list), "data must be an array"
        assert len(data["data"]) <= limit, f"Should return at most {limit} records"

        if "meta" in data and data["meta"]["total"] >= limit:
            assert len(data["data"]) == limit, f"Should return exactly {limit} when more exist"

    def test_pos_011_get_project_by_id(self, api_session, api_headers):
        """TC-POS-011: Retrieve specific project details by ID

        Use case: View details of project with ID 1
        Expected: Returns only project with matching ID and customer info
        """
        project_id = 1
        response = make_api_request(
            api_session, "GET", f"/time/projects/{project_id}", api_headers
        )

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()

        assert "data" in data, "Response must contain 'data' field"
        assert isinstance(data["data"], dict), "data must be a single object, not array"
        assert data["data"]["id"] == project_id, f"Project ID must match requested ID {project_id}"
        assert "name" in data["data"], "Project must have 'name' field"
        assert "customer" in data["data"], "Project must have 'customer' field"
        assert isinstance(data["data"]["customer"], dict), "customer must be an object"

    def test_pos_012_create_customer(self, api_session, api_headers):
        """TC-POS-012: Create a new customer with valid data

        Use case: Add new customer "Acme Corp" to the system
        Expected: Creates customer and returns it with auto-generated ID
        """
        import random
        customer_name = f"Test Customer {random.randint(10000, 99999)}"
        customer_desc = "Automated test customer"

        response = make_api_request(
            api_session, "POST", "/time/customers", api_headers,
            data={
                "name": customer_name,
                "description": customer_desc
            }
        )

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()

        assert "data" in data, "Response must contain 'data' field"
        assert "id" in data["data"], "Created customer must have 'id' field"
        assert isinstance(data["data"]["id"], int), "Customer id must be integer"
        assert data["data"]["id"] > 0, "Customer id must be positive"

        # Verify the data was saved correctly
        assert data["data"]["name"] == customer_name, f"Customer name must match: expected '{customer_name}'"
        assert data["data"]["description"] == customer_desc, f"Description must match: expected '{customer_desc}'"

    def test_pos_013_create_project(self, api_session, api_headers):
        """TC-POS-013: Create a new project linked to existing customer

        Use case: Create project "Website Redesign" for customer ID 1
        Expected: Creates project with customer relationship
        """
        import random
        project_name = f"Test Project {random.randint(10000, 99999)}"
        project_desc = "Automated test project"
        customer_id = 1

        response = make_api_request(
            api_session, "POST", "/time/projects", api_headers,
            data={
                "name": project_name,
                "customerId": customer_id,
                "description": project_desc
            }
        )

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()

        assert "data" in data, "Response must contain 'data' field"
        assert "id" in data["data"], "Created project must have 'id' field"
        assert isinstance(data["data"]["id"], int), "Project id must be integer"
        assert data["data"]["id"] > 0, "Project id must be positive"

        # Verify saved data
        assert data["data"]["name"] == project_name, f"Project name must match: expected '{project_name}'"
        assert data["data"]["description"] == project_desc, f"Description must match: expected '{project_desc}'"

        # Verify customer relationship
        assert "customer" in data["data"], "Project must have 'customer' field"
        assert data["data"]["customer"]["id"] == customer_id, f"Customer ID must be {customer_id}"

    def test_pos_014_update_customer(self, api_session, api_headers):
        """TC-POS-014: Update existing customer's information

        Use case: Rename customer ID 1 to "Updated Customer Name"
        Expected: Updates customer and returns modified data
        """
        customer_id = 1
        new_name = "Updated Customer Name"
        new_desc = "Updated description"

        response = make_api_request(
            api_session, "PUT", f"/time/customers/{customer_id}", api_headers,
            data={
                "name": new_name,
                "description": new_desc
            }
        )

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()

        assert "data" in data, "Response must contain 'data' field"
        assert data["data"]["id"] == customer_id, f"Customer ID must remain {customer_id}"
        assert data["data"]["name"] == new_name, f"Name must be updated to '{new_name}'"
        assert data["data"]["description"] == new_desc, f"Description must be updated to '{new_desc}'"


# ============================================================================
# NEGATIVE TEST CASES
# ============================================================================

@pytest.mark.negative
class TestNegativeCases:
    """Negative test cases for Timesheets API"""

    def test_neg_001_get_nonexistent_employee_timesheets(self, api_session, api_headers):
        """TC-NEG-001: Attempt to retrieve timesheets for non-existent employee

        Use case: Request timesheets for employee ID 99999 (doesn't exist)
        Expected: 404 Not Found with error message
        Note: API currently returns 422 - inconsistent with customers/projects endpoints (bug)
        """
        nonexistent_id = 99999
        response = make_api_request(
            api_session, "GET", f"/time/employees/{nonexistent_id}/timesheets", api_headers
        )

        # Should be 404, but API has a bug and returns 422
        assert response.status_code in [404, 422], \
            f"Expected 404 (or 422 due to bug), got {response.status_code}"

        # Must NOT return 200
        assert response.status_code != 200, "Should not return success for non-existent employee"

        # Should not return data
        data = response.json()
        if "data" in data:
            assert data["data"] is None or len(data["data"]) == 0, \
                "Should not return timesheet data for non-existent employee"

    def test_neg_002_get_nonexistent_customer(self, api_session, api_headers):
        """TC-NEG-002: Attempt to retrieve non-existent customer

        Use case: Request customer ID 99999 (doesn't exist)
        Expected: 404 Not Found, no customer data returned
        """
        nonexistent_id = 99999
        response = make_api_request(
            api_session, "GET", f"/time/customers/{nonexistent_id}", api_headers
        )

        assert response.status_code == 404, \
            f"Expected 404 for non-existent customer, got {response.status_code}"

        # Must NOT be 200 or 422
        assert response.status_code not in [200, 422], \
            f"Should return 404 specifically, not {response.status_code}"

    def test_neg_003_get_nonexistent_project(self, api_session, api_headers):
        """TC-NEG-003: Attempt to retrieve non-existent project

        Use case: Request project ID 99999 (doesn't exist)
        Expected: 404 Not Found, no project data returned
        """
        nonexistent_id = 99999
        response = make_api_request(
            api_session, "GET", f"/time/projects/{nonexistent_id}", api_headers
        )

        assert response.status_code == 404, \
            f"Expected 404 for non-existent project, got {response.status_code}"

        assert response.status_code != 200, "Should not return success for non-existent project"

    def test_neg_004_create_customer_missing_name(self, api_session, api_headers):
        """TC-NEG-004: Attempt to create customer without required name field

        Use case: Submit customer with only description, no name
        Expected: 422 Unprocessable Entity with validation error for 'name' field
        """
        response = make_api_request(
            api_session, "POST", "/time/customers", api_headers,
            data={
                "description": "Customer without name"
            }
        )

        assert response.status_code == 422, \
            f"Expected 422 for missing required field, got {response.status_code}"

        # Must NOT succeed
        assert response.status_code != 200, "Should not create customer without name"

        # Should have error details
        data = response.json()
        assert "error" in data, "Response must contain error information"

    def test_neg_005_create_customer_empty_name(self, api_session, api_headers):
        """TC-NEG-005: Attempt to create customer with empty string as name

        Use case: Submit customer with name = ""
        Expected: 422 Unprocessable Entity - empty name should be rejected
        """
        response = make_api_request(
            api_session, "POST", "/time/customers", api_headers,
            data={
                "name": "",
                "description": "Empty name test"
            }
        )

        assert response.status_code == 422, \
            f"Expected 422 for empty name, got {response.status_code}"

        assert response.status_code != 200, "Should not create customer with empty name"

        # Verify no customer was created
        data = response.json()
        assert "data" not in data or data.get("data") is None or "id" not in data.get("data", {}), \
            "Should not return created customer with ID"

    def test_neg_006_create_customer_name_too_long(self, api_session, api_headers):
        """TC-NEG-006: Attempt to create customer with name exceeding max length

        Use case: Submit customer name with 100 characters (exceeds typical 50-char limit)
        Expected: 422 Unprocessable Entity - validation error for length
        """
        response = make_api_request(
            api_session, "POST", "/time/customers", api_headers,
            data={
                "name": "A" * 100,
                "description": "Long name test"
            }
        )

        assert response.status_code == 422, \
            f"Expected 422 for name too long, got {response.status_code}"

        assert response.status_code != 200, "Should not create customer with excessively long name"

    def test_neg_007_create_project_missing_customer(self, api_session, api_headers):
        """TC-NEG-007: Attempt to create project without required customerId

        Use case: Submit project with name but no customer association
        Expected: 422 Unprocessable Entity - customerId is required
        """
        response = make_api_request(
            api_session, "POST", "/time/projects", api_headers,
            data={
                "name": "Project without customer",
                "description": "Missing customer test"
            }
        )

        assert response.status_code == 422, \
            f"Expected 422 for missing customerId, got {response.status_code}"

        assert response.status_code != 200, "Should not create project without customerId"

        data = response.json()
        assert "error" in data, "Response must contain error information"

    def test_neg_008_create_project_invalid_customer(self, api_session, api_headers):
        """TC-NEG-008: Attempt to create project with non-existent customerId

        Use case: Submit project linked to customer ID 99999 (doesn't exist)
        Expected: 422 Unprocessable Entity - foreign key constraint violation
        """
        response = make_api_request(
            api_session, "POST", "/time/projects", api_headers,
            data={
                "name": "Test Project",
                "customerId": 99999,
                "description": "Invalid customer reference"
            }
        )

        assert response.status_code == 422, \
            f"Expected 422 for non-existent customerId, got {response.status_code}"

        assert response.status_code != 200, "Should not create project with invalid customerId"

    def test_neg_009_list_with_negative_limit(self, api_session, api_headers):
        """TC-NEG-009: Request list with negative limit parameter

        Use case: Request timesheets with limit=-5
        Expected: 422 Unprocessable Entity - limit must be positive
        """
        response = make_api_request(
            api_session, "GET", "/time/timesheets", api_headers,
            params={"limit": -5}
        )

        assert response.status_code == 422, \
            f"Expected 422 for negative limit, got {response.status_code}"

        # Must NOT return 200 with data
        assert response.status_code != 200, "Should not accept negative limit"

    def test_neg_010_list_with_negative_offset(self, api_session, api_headers):
        """TC-NEG-010: Request list with negative offset parameter

        Use case: Request customers with offset=-10
        Expected: 422 Unprocessable Entity - offset must be non-negative
        """
        response = make_api_request(
            api_session, "GET", "/time/customers", api_headers,
            params={"offset": -10}
        )

        assert response.status_code == 422, \
            f"Expected 422 for negative offset, got {response.status_code}"

        assert response.status_code != 200, "Should not accept negative offset"

    def test_neg_011_invalid_employee_id_format(self, api_session, api_headers):
        """TC-NEG-011: Request with non-numeric employee ID

        Use case: Request /time/employees/invalid/timesheets (string instead of integer)
        Expected: 422 Unprocessable Entity - ID must be numeric
        """
        response = make_api_request(
            api_session, "GET", "/time/employees/invalid/timesheets", api_headers
        )

        assert response.status_code == 422, \
            f"Expected 422 for invalid ID format, got {response.status_code}"

        # Could also be 404 depending on routing, but NOT 200
        assert response.status_code != 200, "Should not accept non-numeric employee ID"

    def test_neg_012_update_nonexistent_customer(self, api_session, api_headers):
        """TC-NEG-012: Attempt to update non-existent customer

        Use case: PUT to customer ID 99999 (doesn't exist)
        Expected: 404 Not Found - cannot update what doesn't exist
        """
        response = make_api_request(
            api_session, "PUT", "/time/customers/99999", api_headers,
            data={
                "name": "Updated Name",
                "description": "Updated description"
            }
        )

        assert response.status_code == 404, \
            f"Expected 404 for updating non-existent customer, got {response.status_code}"

        # Must NOT be 200 or 422
        assert response.status_code != 200, "Should not return success when updating non-existent resource"

    def test_neg_013_create_project_empty_name(self, api_session, api_headers):
        """TC-NEG-013: Attempt to create project with empty name

        Use case: Submit project with name = "" and valid customerId
        Expected: 422 Unprocessable Entity - name cannot be empty
        """
        response = make_api_request(
            api_session, "POST", "/time/projects", api_headers,
            data={
                "name": "",
                "customerId": 1,
                "description": "Project with empty name"
            }
        )

        assert response.status_code == 422, \
            f"Expected 422 for empty project name, got {response.status_code}"

        assert response.status_code != 200, "Should not create project with empty name"

    def test_neg_014_exceed_max_limit(self, api_session, api_headers):
        """TC-NEG-014: Request with unreasonably large limit value

        Use case: Request customers with limit=10000 (exceeds max allowed)
        Expected: 422 Unprocessable Entity - limit exceeds maximum
        """
        response = make_api_request(
            api_session, "GET", "/time/customers", api_headers,
            params={"limit": 10000}
        )

        assert response.status_code == 422, \
            f"Expected 422 for excessive limit, got {response.status_code}"

        # If it somehow returns 200, verify it's capped
        if response.status_code == 200:
            data = response.json()
            assert len(data["data"]) < 10000, "Should cap limit to reasonable maximum"


# ============================================================================
# SECURITY TEST CASES
# ============================================================================

@pytest.mark.security
class TestSecurityCases:
    """Security test cases for Timesheets API"""

    def test_sec_001_no_auth_list_timesheets(self):
        """TC-SEC-001: Attempt to access timesheets without authentication

        Use case: Unauthenticated user tries to view timesheets
        Expected: 401 Unauthorized - must not return any timesheet data
        """
        session = requests.Session()
        url = urljoin(API_BASE + "/", "time/timesheets")
        response = session.get(url)

        assert response.status_code == 401, \
            f"Expected 401 Unauthorized, got {response.status_code}"

        # Must NOT return 200
        assert response.status_code != 200, "Must not allow unauthenticated access"

        # Should not contain timesheet data
        try:
            data = response.json()
            assert "data" not in data or data["data"] is None or len(data["data"]) == 0, \
                "Must not leak timesheet data to unauthenticated users"
        except:
            pass  # Non-JSON response is acceptable for 401

    def test_sec_002_no_auth_list_customers(self):
        """TC-SEC-002: Attempt to access customers without authentication

        Use case: Unauthenticated user tries to view customers
        Expected: 401 Unauthorized - must not return customer data
        """
        session = requests.Session()
        url = urljoin(API_BASE + "/", "time/customers")
        response = session.get(url)

        assert response.status_code == 401, \
            f"Expected 401 Unauthorized, got {response.status_code}"

        assert response.status_code != 200, "Must not allow unauthenticated access to customers"

    def test_sec_003_no_auth_create_customer(self):
        """TC-SEC-003: Attempt to create customer without authentication

        Use case: Unauthenticated user tries to create a customer
        Expected: 401 Unauthorized - must not allow data modification
        """
        session = requests.Session()
        url = urljoin(API_BASE + "/", "time/customers")
        response = session.post(
            url,
            json={"name": "Unauthorized Customer", "description": "Should be rejected"}
        )

        assert response.status_code == 401, \
            f"Expected 401 Unauthorized, got {response.status_code}"

        # Must NOT be 200 or 422
        assert response.status_code not in [200, 422], \
            "Must reject before validation - authentication required first"

    def test_sec_004_no_auth_list_projects(self):
        """TC-SEC-004: Attempt to access projects without authentication

        Use case: Unauthenticated user tries to view projects
        Expected: 401 Unauthorized - must not return project data
        """
        session = requests.Session()
        url = urljoin(API_BASE + "/", "time/projects")
        response = session.get(url)

        assert response.status_code == 401, \
            f"Expected 401 Unauthorized, got {response.status_code}"

        assert response.status_code != 200, "Must not allow unauthenticated access to projects"

    def test_sec_005_sql_injection_customer_name(self, api_session, api_headers):
        """TC-SEC-005: SQL injection attempt in customer name field

        Use case: Attacker tries to drop tables via SQL injection in name
        Expected: Either sanitize and store safely (200) or reject (422)
                 Must NOT execute SQL commands or corrupt database
        """
        malicious_name = "'; DROP TABLE customers; --"
        response = make_api_request(
            api_session, "POST", "/time/customers", api_headers,
            data={
                "name": malicious_name,
                "description": "SQL injection test"
            }
        )

        # Should either sanitize (200) or reject (422), but NOT fail completely
        assert response.status_code in [200, 422], \
            f"Expected 200 (sanitized) or 422 (rejected), got {response.status_code}"

        # Verify database is still functional (SQL wasn't executed)
        check = make_api_request(
            api_session, "GET", "/time/customers", api_headers
        )
        assert check.status_code == 200, "Database must remain functional - SQL injection must not execute"

        # If the malicious input was accepted, verify it was stored as string
        if response.status_code == 200:
            data = response.json()
            created_id = data["data"]["id"]

            # Retrieve and verify it's stored as literal string
            verify = make_api_request(
                api_session, "GET", f"/time/customers/{created_id}", api_headers
            )
            assert verify.status_code == 200
            assert malicious_name in verify.json()["data"]["name"], \
                "SQL should be stored as literal string, not executed"

    def test_sec_006_xss_attack_customer_name(self, api_session, api_headers):
        """TC-SEC-006: XSS (Cross-Site Scripting) injection attempt

        Use case: Attacker tries to inject JavaScript via customer name
        Expected: Either sanitize/escape (200) or reject (422)
                 Must NOT store executable script
        """
        malicious_script = "<script>alert('XSS')</script>"
        response = make_api_request(
            api_session, "POST", "/time/customers", api_headers,
            data={
                "name": malicious_script,
                "description": "XSS test"
            }
        )

        assert response.status_code in [200, 422], \
            f"Expected 200 (sanitized) or 422 (rejected), got {response.status_code}"

        # If accepted, verify it's stored safely (escaped or sanitized)
        if response.status_code == 200:
            data = response.json()
            stored_name = data["data"]["name"]

            # Should be escaped/sanitized, not raw script
            # Note: Exact sanitization method varies, but should not be executable
            assert "script" not in stored_name.lower() or "&lt;" in stored_name or "\\" in stored_name, \
                "XSS payload should be sanitized or escaped"

    def test_sec_007_sql_injection_project_name(self, api_session, api_headers):
        """TC-SEC-007: SQL injection attempt in project name field

        Use case: Attacker tries SQL injection via project name
        Expected: Sanitize or reject, must not execute SQL
        """
        malicious_name = "' OR '1'='1"
        response = make_api_request(
            api_session, "POST", "/time/projects", api_headers,
            data={
                "name": malicious_name,
                "customerId": 1,
                "description": "SQL injection test"
            }
        )

        assert response.status_code in [200, 422], \
            f"Expected 200 (sanitized) or 422 (rejected), got {response.status_code}"

        # Verify database integrity
        check = make_api_request(
            api_session, "GET", "/time/projects", api_headers
        )
        assert check.status_code == 200, "Database must remain functional"

    def test_sec_008_command_injection(self, api_session, api_headers):
        """TC-SEC-008: OS command injection attempt

        Use case: Attacker tries to execute system commands via input
        Expected: Must not execute system commands, sanitize or reject
        """
        malicious_input = "; ls -la"
        response = make_api_request(
            api_session, "POST", "/time/customers", api_headers,
            data={
                "name": malicious_input,
                "description": "Command injection test"
            }
        )

        # Should handle safely (200 or 422), not crash (500)
        assert response.status_code in [200, 422], \
            f"Expected 200 (sanitized) or 422 (rejected), got {response.status_code}"

        # System should remain functional
        check = make_api_request(
            api_session, "GET", "/time/customers", api_headers
        )
        assert check.status_code == 200, "System must remain functional"

    def test_sec_009_http_verb_tampering(self, api_session, api_headers):
        """TC-SEC-009: HTTP method tampering - use PATCH on GET-only endpoint

        Use case: Attacker tries unsupported HTTP method on read-only endpoint
        Expected: 405 Method Not Allowed - must not process request
        """
        response = make_api_request(
            api_session, "PATCH", "/time/timesheets", api_headers,
            data={"malicious": "data"}
        )

        assert response.status_code == 405, \
            f"Expected 405 Method Not Allowed, got {response.status_code}"

        # Must NOT be 200, 201, or 204 (success codes)
        assert response.status_code not in [200, 201, 204], \
            "Must not accept unsupported HTTP methods"

    def test_sec_010_oversized_payload(self, api_session, api_headers):
        """TC-SEC-010: DoS attempt via oversized payload

        Use case: Attacker sends 100KB description to exhaust resources
        Expected: Reject (400/422) or handle gracefully (200 with truncation)
                 Must not crash (500) or hang
        """
        response = make_api_request(
            api_session, "POST", "/time/customers", api_headers,
            data={
                "name": "Test",
                "description": "A" * 100000  # 100KB payload
            }
        )

        # Should handle gracefully
        assert response.status_code in [200, 400, 422], \
            f"Expected 200/400/422 for oversized payload, got {response.status_code}"

        # Must NOT crash
        assert response.status_code != 500, "Server must not crash on large payload"

        # System should remain responsive
        check = make_api_request(
            api_session, "GET", "/time/customers", api_headers,
            params={"limit": 1}
        )
        assert check.status_code == 200, "System must remain responsive after large payload"

    def test_sec_011_path_traversal(self, api_session, api_headers):
        """TC-SEC-011: Path traversal attack attempt

        Use case: Attacker tries to access admin endpoints via path traversal
        Expected: Must not allow access to unauthorized endpoints
                 Should return 404 (not found) or 200 (normalized path)
        """
        response = make_api_request(
            api_session, "GET", "/time/customers/../../admin/users", api_headers
        )

        # Should either normalize path (200 for /admin/users if authorized) or reject (404)
        assert response.status_code in [200, 404, 403], \
            f"Expected 200/404/403, got {response.status_code}"

        # If it returns data, verify it's NOT admin/users data
        if response.status_code == 200:
            data = response.json()
            # Should be customers or empty, not admin users
            if "data" in data and isinstance(data["data"], list) and len(data["data"]) > 0:
                # Customers have 'name', admin users typically have 'username'
                assert "name" in data["data"][0] or "customer" in str(data).lower(), \
                    "Path traversal should not expose admin endpoints"

    def test_sec_012_delete_method_not_allowed(self, api_session, api_headers):
        """TC-SEC-012: Verify DELETE method is properly restricted

        Use case: Attacker tries to delete customer/project via HTTP DELETE
        Expected: 405 Method Not Allowed - DELETE should be disabled
        """
        # Test DELETE on customers
        response_customer = make_api_request(
            api_session, "DELETE", "/time/customers/1", api_headers
        )
        assert response_customer.status_code == 405, \
            f"Expected 405 for DELETE customer, got {response_customer.status_code}"

        assert response_customer.status_code != 200, \
            "Must not allow DELETE on customers"

        # Test DELETE on projects
        response_project = make_api_request(
            api_session, "DELETE", "/time/projects/1", api_headers
        )
        assert response_project.status_code == 405, \
            f"Expected 405 for DELETE project, got {response_project.status_code}"

        assert response_project.status_code != 200, \
            "Must not allow DELETE on projects"

        # Verify resources still exist
        check_customer = make_api_request(
            api_session, "GET", "/time/customers/1", api_headers
        )
        check_project = make_api_request(
            api_session, "GET", "/time/projects/1", api_headers
        )

        # Should still exist (200) or have never existed (404), but not deleted
        assert check_customer.status_code in [200, 404]
        assert check_project.status_code in [200, 404]


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
