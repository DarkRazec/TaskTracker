from rest_framework import status
from rest_framework.test import APITestCase

from employees.models import Employee
from tasks.models import Task


class TaskTestCase(APITestCase):
    """ Test case for Task model """

    def setUp(self):
        """Creating test employee and task model"""
        self.employee_data = {
            "first_name": "test",
            "last_name": "test",
            "company": "test",
            "position": "test"
        }
        self.task_data = {
            "name": "test"
        }
        self.employee = Employee.objects.create(**self.employee_data, email="admin@admin")
        self.test_obj = Task.objects.create(**self.task_data)

    def test_create_task(self):
        """Testing create"""

        response = self.client.post('/tasks/', data=self.task_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.json()['name'], 'test')

    def test_list_task(self):
        """Testing list"""

        response = self.client.get('/tasks/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertTrue(Task.objects.all().exists())
        self.assertTrue(len(response.json()) in (1, 2))

    def test_retrieve_task(self):
        """Testing retrieve"""

        response = self.client.get(f'/tasks/{self.test_obj.id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(

            response.json(),
            {
                'id': self.test_obj.id,
                'target_date': None,
                'name': 'test',
                'status': 'created',
                'urgency': 'low',
                'importance': 'low',
                'is_active': True,
                'parent_task': None,
                'employee': None
            }
        )

    def test_update_task(self):
        """Testing update"""
        new_data = {
            "employee": self.employee.id
        }
        response = self.client.patch(
            f'/tasks/{self.test_obj.id}/',
            data=new_data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.json(),
            {
                'id': self.test_obj.id,
                'target_date': None,
                'name': 'test',
                'status': 'assigned',
                'urgency': 'low',
                'importance': 'low',
                'is_active': True,
                'parent_task': None,
                'employee': self.employee.id
            }
        )

    def test_delete_task(self):
        """Testing delete"""

        response = self.client.delete(f'/tasks/{self.test_obj.id}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class ImportantTaskTestCase(APITestCase):
    """ Test case for important task list view """

    def setUp(self):
        """Creating test employee and task model"""
        self.employee_data = {
            "first_name": "test"
        }
        self.employee = Employee.objects.create(**self.employee_data, email="admin@admin")
        self.task_data = {
            "name": "test"
        }

    def test_list_important_task(self):
        parent_tasks = [Task.objects.create(**self.task_data, employee=self.employee, status="assigned") for i in range(3)]
        test_employee_data = {
            "first_name": "test2"
        }
        test_employee = Employee.objects.create(**test_employee_data)
        test_obj = Task.objects.create(**self.task_data, parent_task=parent_tasks[0])

        response = self.client.get('/tasks/important/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertTrue(len(response.json()) == 1)
        self.assertTrue(
            response.json()[0]['full_name'],
            ['', test_employee.first_name, None]
        )

        self.assertEqual(
            response.json()[0]['task_id'],
            test_obj.id
        )

