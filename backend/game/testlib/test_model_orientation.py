from rest_framework.test import APITestCase, APIClient

from .. import models

# Create your tests here.

class OrientationTest(APITestCase):
    fixtures = ['game/fixtures/data.json',]

    def test_orientations(self):
        expected = [
            (1, False, True, False, True),
            (1, False, True, True, False),
            (1, True, False, False, True),
            (1, True, False, True, False),
            (2, False, True, True, True),
            (2, True, False, True, True),
            (2, True, True, False, True),
            (2, True, True, True, False),
            (3, True, True, False, False),
            (3, False, False, True, True)
        ]
        orientations = models.GamePieceOrientation.objects.all().order_by('id')
        self.assertEqual(orientations.count(), 10)
        for orientation in orientations:
            shape, up, down, left, right = expected.pop(0)
            self.assertEqual(orientation.shape.id, shape)
            self.assertEqual(orientation.up, up)
            self.assertEqual(orientation.down, down)
            self.assertEqual(orientation.left, left)
            self.assertEqual(orientation.right, right)
