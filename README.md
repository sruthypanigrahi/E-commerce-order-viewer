# Ecommerce Order Viewer

Complete admin dashboard for viewing customer orders with Super Coins loyalty system.

## Features

### Milestone 1 - Data Loading ✅
- MongoDB integration with proper collections
- Sample data with orders, users, and order items
- Super Coins calculation (1 coin per $10 spent on delivered orders)

### Milestone 2 - Backend APIs ✅
- Search customers by name/email
- Fetch customer orders with filters
- Get order items details
- Calculate insights with MongoDB aggregations
- Super Coins and loyalty tier system

### Milestone 3 - User Interface ✅
- Customer search with live results
- Orders list with status color-coding
- Click order to see items in modal
- Super Coins and loyalty tier display

### Milestone 4 - End-to-End Flow ✅
- Search → Select Customer → View Orders → Click Order → See Items
- Real-time insights and Super Coins display
- Filters for status and price range

### Milestone 5 - Enhancements ✅
- Loyalty tiers: Bronze (<$500), Silver ($500-$999), Gold ($1000+)
- CSV export functionality
- Super Coins badges and visual indicators
- Responsive design with modal dialogs

## Quick Start

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Start MongoDB (default: localhost:27017)

3. Run the application:
```bash
python run.py
```

4. Open http://localhost:8000

## API Endpoints

- `GET /search?q={query}` - Search customers
- `GET /customers/{id}/orders` - Get customer orders
- `GET /orders/{id}/items` - Get order items
- `GET /customers/{id}/insights` - Get customer insights
- `GET /customers/{id}/export` - Export orders CSV

## Super Coins System

- Earn 1 Super Coin per $10 spent on delivered orders
- Loyalty tiers based on total spending
- Visual badges and indicators throughout UI