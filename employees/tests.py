from rest_framework import status
from rest_framework.test import APITestCase

from employees.models import Employee


class EmployeeTestCase(APITestCase):
    """ Test case for Employee model """

    def setUp(self):
        """Creating test employee"""
        self.employee_data = {
            "last_name": "testov",
            "first_name": "test",
            "middle_name": "testovich",
            "position": "test",
            "company": "test",
        }
        self.test_obj = Employee.objects.create(**self.employee_data, email="admin@admin")

    def test_create_employee(self):
        """Testing create"""
        test_data = self.employee_data
        test_data["email"] = "test@test.com"

        response = self.client.post('/employees/', data=test_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.json()['first_name'], 'test')

    def test_list_employee(self):
        """Testing list"""

        response = self.client.get('/employees/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertTrue(Employee.objects.all().exists())
        self.assertTrue(len(response.json()) in (1, 2))

    def test_retrieve_employee(self):
        """Testing retrieve"""

        response = self.client.get(f'/employees/{self.test_obj.id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(

            response.json(),
            {
                "id": self.test_obj.id,
                "tasks": [],
                "last_name": "testov",
                "first_name": "test",
                "middle_name": "testovich",
                "position": "test",
                "company": "test",
                "email": "admin@admin",
                "phone": None
            }
        )

    def test_update_employee(self):
        """Testing update"""
        response = self.client.patch(
            f'/employees/{self.test_obj.id}/',
            data={"first_name": "test2"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.json(),
            {
                "id": self.test_obj.id,
                "tasks": [],
                "last_name": "testov",
                "first_name": "test2",
                "middle_name": "testovich",
                "position": "test",
                "company": "test",
                "email": "admin@admin",
                "phone": None
            }
        )

    def test_delete_employee(self):
        """Testing delete"""

        response = self.client.delete(f'/employees/{self.test_obj.id}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
