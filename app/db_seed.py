from datetime import datetime, timedelta
import random
from .database import SessionLocal
from . import models

def seed_database():
    db = SessionLocal()
    try:
        # Check if we already have data
        existing_products = db.query(models.Product).first()
        if existing_products:
            print("Database already seeded, skipping...")
            return

        # Create sample products
        products = [
            models.Product(
                name="iPhone 13",
                description="Latest Apple smartphone",
                price=999.99,
                category="electronics"
            ),
            models.Product(
                name="Samsung TV",
                description="55-inch 4K Smart TV",
                price=799.99,
                category="electronics"
            ),
            models.Product(
                name="Nike Running Shoes",
                description="Professional running shoes",
                price=129.99,
                category="sports"
            ),
            models.Product(
                name="Coffee Maker",
                description="Automatic drip coffee maker",
                price=49.99,
                category="appliances"
            ),
            models.Product(
                name="Yoga Mat",
                description="Premium yoga mat",
                price=29.99,
                category="sports"
            )
        ]
        
        # Add products and create their inventory
        for product in products:
            db.add(product)
            db.flush()  # Get the product ID
            
            inventory = models.Inventory(
                product_id=product.id,
                quantity=100  # Start with 100 units of each product
            )
            db.add(inventory)
        
        db.commit()
        
        # Create some sample sales
        sales = []
        for product in products:
            # Create 3-5 sales for each product
            for i in range(3, 6):
                # Generate random date within last 7 days
                random_days = random.uniform(0, 7)
                random_hours = random.uniform(0, 24)
                random_minutes = random.uniform(0, 60)
                
                sale_date = datetime.utcnow() - timedelta(
                    days=random_days,
                    hours=random_hours,
                    minutes=random_minutes
                )
                
                quantity = random.randint(1, 5)  # Random quantity between 1 and 5
                total_amount = product.price * quantity
                
                sale = models.Sale(
                    product_id=product.id,
                    quantity=quantity,
                    total_amount=total_amount,
                    sale_date=sale_date
                )
                sales.append(sale)
                
                # Update inventory
                inventory = db.query(models.Inventory).filter(
                    models.Inventory.product_id == product.id
                ).first()
                inventory.quantity -= quantity
        
        db.add_all(sales)
        db.commit()
        
        print("Database seeded successfully!")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close() 