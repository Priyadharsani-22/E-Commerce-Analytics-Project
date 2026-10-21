import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

print("=" * 60)
print("E-Commerce Sample Data Generation Script")
print("=" * 60)

# Generate Customers
print("\n1. Generating Customer Data...")
num_customers = 500
customers = pd.DataFrame({
    'customer_id': range(1001, 1001 + num_customers),
    'customer_name': [f'Customer_{i}' for i in range(1, num_customers + 1)],
    'email': [f'customer{i}@email.com' for i in range(1, num_customers + 1)],
    'country': np.random.choice(['USA', 'UK', 'India', 'Australia', 'Germany', 'Canada', 'France'], num_customers),
    'signup_date': [datetime(2022, 1, 1) + timedelta(days=random.randint(0, 730)) 
                    for _ in range(num_customers)],
    'customer_segment': np.random.choice(['Premium', 'Regular', 'Budget'], num_customers, p=[0.2, 0.5, 0.3])
})

print(f"   ✓ Created {len(customers)} customer records")

# Generate Products
print("2. Generating Product Data...")
num_products = 100
products = pd.DataFrame({
    'product_id': range(5001, 5001 + num_products),
    'product_name': [f'Product_{i}' for i in range(1, num_products + 1)],
    'category': np.random.choice(['Electronics', 'Clothing', 'Home', 'Sports', 'Books', 'Beauty'], num_products),
    'unit_price': np.random.uniform(10, 500, num_products).round(2),
    'cost_price': np.random.uniform(5, 250, num_products).round(2),
    'stock_quantity': np.random.randint(10, 1000, num_products),
    'reorder_level': np.random.randint(5, 50, num_products)
})

print(f"   ✓ Created {len(products)} product records")

# Generate Transactions
print("3. Generating Transaction Data...")
num_transactions = 2000
transactions = pd.DataFrame({
    'order_id': range(10001, 10001 + num_transactions),
    'customer_id': np.random.choice(customers['customer_id'], num_transactions),
    'product_id': np.random.choice(products['product_id'], num_transactions),
    'order_date': [datetime(2023, 1, 1) + timedelta(days=random.randint(0, 365)) 
                   for _ in range(num_transactions)],
    'quantity': np.random.randint(1, 10, num_transactions),
    'status': np.random.choice(['Completed', 'Pending', 'Cancelled', 'Shipped'], num_transactions, 
                               p=[0.70, 0.15, 0.10, 0.05])
})

# Add product price to transactions
transactions = transactions.merge(products[['product_id', 'unit_price']], on='product_id')
transactions['total_amount'] = (transactions['quantity'] * transactions['unit_price']).round(2)

# Add shipping date and delivery date for completed orders
transactions['shipping_date'] = transactions['order_date'] + timedelta(days=1)
transactions['delivery_date'] = transactions['shipping_date'] + transactions.apply(lambda x: timedelta(days=random.randint(3, 10)), axis=1)
print(f"   ✓ Created {len(transactions)} transaction records")

# Generate Reviews
print("4. Generating Review Data...")
num_reviews = int(num_transactions * 0.6)  # 60% of transactions have reviews
review_indices = np.random.choice(transactions.index, num_reviews, replace=False)
reviews = pd.DataFrame({
    'review_id': range(20001, 20001 + num_reviews),
    'order_id': transactions.loc[review_indices, 'order_id'].values,
    'customer_id': transactions.loc[review_indices, 'customer_id'].values,
    'product_id': transactions.loc[review_indices, 'product_id'].values,
    'rating': np.random.choice([1, 2, 3, 4, 5], num_reviews, p=[0.05, 0.10, 0.15, 0.30, 0.40]),
    'review_text': [f'Review_{i}' for i in range(1, num_reviews + 1)],
    'review_date': [datetime(2023, 1, 1) + timedelta(days=random.randint(0, 365)) 
                    for _ in range(num_reviews)]
})

print(f"   ✓ Created {len(reviews)} review records")

# Create datasets folder if it doesn't exist
datasets_folder = '../datasets/'
if not os.path.exists(datasets_folder):
    os.makedirs(datasets_folder)

# Save to CSV files
print("\n5. Saving CSV files...")
customers.to_csv(f'{datasets_folder}customers.csv', index=False)
print(f"   ✓ Saved: customers.csv")

products.to_csv(f'{datasets_folder}products.csv', index=False)
print(f"   ✓ Saved: products.csv")

transactions.to_csv(f'{datasets_folder}transactions.csv', index=False)
print(f"   ✓ Saved: transactions.csv")

reviews.to_csv(f'{datasets_folder}reviews.csv', index=False)
print(f"   ✓ Saved: reviews.csv")

# Summary Statistics
print("\n" + "=" * 60)
print("DATA SUMMARY")
print("=" * 60)
print(f"\nCustomers:")
print(f"   Total Records: {len(customers)}")
print(f"   Countries: {customers['country'].nunique()}")
print(f"   Segments: {customers['customer_segment'].unique().tolist()}")

print(f"\nProducts:")
print(f"   Total Records: {len(products)}")
print(f"   Categories: {products['category'].nunique()}")
print(f"   Price Range: ${products['unit_price'].min():.2f} - ${products['unit_price'].max():.2f}")

print(f"\nTransactions:")
print(f"   Total Records: {len(transactions)}")
print(f"   Date Range: {transactions['order_date'].min().date()} to {transactions['order_date'].max().date()}")
print(f"   Total Revenue: ${transactions['total_amount'].sum():,.2f}")
print(f"   Statuses: {transactions['status'].unique().tolist()}")

print(f"\nReviews:")
print(f"   Total Records: {len(reviews)}")
print(f"   Average Rating: {reviews['rating'].mean():.2f}/5.0")

print("\n" + "=" * 60)
print("✅ Sample data generation completed successfully!")
print("=" * 60)