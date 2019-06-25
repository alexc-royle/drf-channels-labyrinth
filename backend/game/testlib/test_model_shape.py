from rest_framework.test import APITestCase, APIClient

from .. import models

# Create your tests here.

class ShapeTest(APITestCase):
    fixtures = ['game/fixtures/data.json',]

    def test_shapes(self):
        expected = ['bend', 'tjunction', 'straight']
        shapes = models.GamePieceShape.objects.all().order_by('id')
        self.assertEqual(shapes.count(), 3)
        for shape in shapes:
            self.assertEqual(shape.title, expected.pop(0))
