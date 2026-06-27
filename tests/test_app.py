import unittest
from copy import deepcopy

from fastapi.testclient import TestClient

from src.app import app, activities


class ActivityTests(unittest.TestCase):
    def setUp(self):
        self.original_activities = deepcopy(activities)
        self.client = TestClient(app)

    def tearDown(self):
        activities.clear()
        activities.update(deepcopy(self.original_activities))

    def test_remove_participant_from_activity(self):
        response = self.client.delete("/activities/Chess%20Club/participants/michael@mergington.edu")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Removed michael@mergington.edu from Chess Club")
        self.assertNotIn("michael@mergington.edu", activities["Chess Club"]["participants"])

    def test_remove_participant_not_found_returns_404(self):
        response = self.client.delete("/activities/Chess%20Club/participants/unknown@mergington.edu")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Participant not found")


if __name__ == "__main__":
    unittest.main()
