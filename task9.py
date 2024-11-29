# tests/test_routes.py
import unittest
from app import app, db
from models import Product
from flask import json
from faker import Faker

fake = Faker()

class TestProductRoutes(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        # Setup the database
        with app.app_context():
            db.create_all()

    def tearDown(self):
        # Clean up the database
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_read_product(self):
        # Create a product and add it to the database
        product = Product(name=fake.company(),
                          description=fake.text(max_nb_chars=200),
                          price=99.99,
                          sku=fake.uuid4(),
                          category=fake.word(),
                          available=True)
        with app.app_context():
            db.session.add(product)
            db.session.commit()
        
        # Retrieve the product via the route
        response = self.app.get(f'/products/{product.id}')
        data = json.loads(response.data)

        # Check the response status and data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['name'], product.name)
        self.assertEqual(data['description'], product.description)
        self.assertEqual(data['price'], product.price)
        self.assertEqual(data['sku'], product.sku)
        self.assertEqual(data['category'], product.category)
        self.assertEqual(data['available'], product.available)

if __name__ == '__main__':
    unittest.main()
