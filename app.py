from fastapi import FastAPI, HTTPException, Form, Request, Cookie
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from pymongo import MongoClient
import hashlib
from dotenv import load_dotenv
import os 
load_dotenv
app = FastAPI(title="Ecommerce Store")
MONGO_URI = os.getenv("MONGO_URI")

# MongoDB Atlas connection
client = MongoClient(MONGO_URI)
# client = MongoClient("mongodb+srv://sruthypriyankapanigrahi123:Sruthy123456@cluster0.gn21n1r.mongodb.net/")
db = client.ecommerce
users_collection = db.users
orders_collection = db.orders
products_collection = db.products

# Initialize products if empty
try:
    if products_collection.count_documents({}) == 0:
        products = [
    {"_id": 1, "name": "iPhone 15", "price": 79999, "category": "Electronics", "stock": 50},
    {"_id": 2, "name": "MacBook Pro", "price": 199999, "category": "Electronics", "stock": 25},
    {"_id": 3, "name": "AirPods Pro", "price": 24999, "category": "Electronics", "stock": 100},
    {"_id": 4, "name": "Samsung TV 55", "price": 45999, "category": "Electronics", "stock": 30},
    {"_id": 5, "name": "Nike Shoes", "price": 8999, "category": "Fashion", "stock": 75},
    {"_id": 6, "name": "Adidas T-Shirt", "price": 1999, "category": "Fashion", "stock": 200},
    {"_id": 7, "name": "Python Book", "price": 899, "category": "Books", "stock": 150},
    {"_id": 8, "name": "Gaming Chair", "price": 15999, "category": "Furniture", "stock": 40},
    {"_id": 9, "name": "Coffee Mug", "price": 299, "category": "Home", "stock": 500},
    {"_id": 10, "name": "Wireless Mouse", "price": 1299, "category": "Electronics", "stock": 80},
    {"_id": 11, "name": "Smart Watch", "price": 15999, "category": "Electronics", "stock": 60},
    {"_id": 12, "name": "Bluetooth Speaker", "price": 4999, "category": "Electronics", "stock": 90},
    {"_id": 13, "name": "Leather Wallet", "price": 2499, "category": "Fashion", "stock": 120},
    {"_id": 14, "name": "Running Shoes", "price": 6999, "category": "Fashion", "stock": 110},
    {"_id": 15, "name": "Gaming Laptop", "price": 129999, "category": "Electronics", "stock": 20},
    {"_id": 16, "name": "4K Monitor", "price": 34999, "category": "Electronics", "stock": 35},
    {"_id": 17, "name": "Wireless Earbuds", "price": 4999, "category": "Electronics", "stock": 150},
    {"_id": 18, "name": "Smartphone Stand", "price": 799, "category": "Accessories", "stock": 300},
    {"_id": 19, "name": "Gaming Headset", "price": 3999, "category": "Electronics", "stock": 70},
    {"_id": 20, "name": "Portable Charger", "price": 1999, "category": "Accessories", "stock": 200},
    {"_id": 21, "name": "Yoga Mat", "price": 1499, "category": "Fitness", "stock": 180},
    {"_id": 22, "name": "Fitness Tracker", "price": 4999, "category": "Fitness", "stock": 90},  ]

        products_collection.insert_many(products)
except:
    pass

admin_users = {"admin": "admin123"}

def hash_password(password: str) -> str:
    return hashlib.md5(password.encode()).hexdigest()

def calculate_super_coins(user_id: int) -> int:
    try:
        user_orders = list(orders_collection.find({"user_id": user_id, "status": "Delivered"}))
        total_spent = sum(o["total"] for o in user_orders)
        return int(total_spent // 1000) * 10
    except:
        return 0

def update_user_super_coins(user_id: int):
    try:
        super_coins = calculate_super_coins(user_id)
        users_collection.update_one({"_id": user_id}, {"$set": {"super_coins": super_coins}})
    except:
        pass

@app.get("/")
async def home():
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>ShopEasy - Your Premium Store</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: 'Segoe UI', sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; display: flex; align-items: center; justify-content: center; }
            .container { background: white; padding: 3rem; border-radius: 20px; box-shadow: 0 20px 40px rgba(0,0,0,0.1); text-align: center; max-width: 500px; width: 90%; }
            h1 { color: #333; margin-bottom: 1rem; font-size: 2.5rem; font-weight: 700; }
            .subtitle { color: #666; margin-bottom: 2rem; font-size: 1.1rem; }
            .btn { display: inline-block; padding: 15px 30px; margin: 10px; background: linear-gradient(45deg, #667eea, #764ba2); color: white; text-decoration: none; border-radius: 50px; font-weight: 600; transition: all 0.3s ease; box-shadow: 0 4px 15px rgba(0,0,0,0.2); }
            .btn:hover { transform: translateY(-2px); box-shadow: 0 8px 25px rgba(0,0,0,0.3); }
            .btn.register { background: linear-gradient(45deg, #56ab2f, #a8e6cf); }
            .btn.admin { background: linear-gradient(45deg, #ff6b6b, #ee5a24); }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🛍️ ShopEasy</h1>
            <p class="subtitle">Your Premium Shopping Destination</p>
            <a href="/register" class="btn register">Create Account</a><br>
            <a href="/user-login" class="btn">Customer Login</a><br>
            <a href="/admin-login" class="btn admin">Admin Portal</a>
        </div>
    </body>
    </html>
    """)

@app.get("/register")
async def register_page():
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Create Account - ShopEasy</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: 'Segoe UI', sans-serif; background: linear-gradient(135deg, #56ab2f 0%, #a8e6cf 100%); min-height: 100vh; display: flex; align-items: center; justify-content: center; }
            .form-container { background: white; padding: 2.5rem; border-radius: 15px; box-shadow: 0 15px 35px rgba(0,0,0,0.1); max-width: 400px; width: 90%; }
            h2 { color: #333; margin-bottom: 1.5rem; text-align: center; font-size: 2rem; }
            .form-group { margin-bottom: 1.5rem; }
            input { width: 100%; padding: 15px; border: 2px solid #e1e1e1; border-radius: 10px; font-size: 1rem; transition: border-color 0.3s; }
            input:focus { outline: none; border-color: #56ab2f; }
            .btn { width: 100%; padding: 15px; background: linear-gradient(45deg, #56ab2f, #a8e6cf); color: white; border: none; border-radius: 10px; font-size: 1.1rem; font-weight: 600; cursor: pointer; transition: all 0.3s; }
            .btn:hover { transform: translateY(-2px); box-shadow: 0 8px 20px rgba(0,0,0,0.2); }
            .back-link { display: block; text-align: center; margin-top: 1rem; color: #666; text-decoration: none; }
        </style>
    </head>
    <body>
        <div class="form-container">
            <h2>Create Account</h2>
            <form method="post" action="/register">
                <div class="form-group">
                    <input name="name" placeholder="Full Name" required>
                </div>
                <div class="form-group">
                    <input name="email" type="email" placeholder="Email Address" required>
                </div>
                <div class="form-group">
                    <input name="password" type="password" placeholder="Password" required>
                </div>
                <button type="submit" class="btn">Create Account</button>
            </form>
            <a href="/" class="back-link">← Back to Home</a>
        </div>
    </body>
    </html>
    """)

@app.post("/register")
async def register_user(name: str = Form(), email: str = Form(), password: str = Form()):
    try:
        if users_collection.find_one({"email": email}):
            return HTMLResponse("<h3>Email already exists</h3><a href='/register'>Try again</a>")
        
        last_user = users_collection.find_one(sort=[("_id", -1)])
        user_id = (last_user["_id"] + 1) if last_user else 1
        
        new_user = {
            "_id": user_id,
            "name": name,
            "email": email,
            "password": hash_password(password),
            "super_coins": 0
        }
        users_collection.insert_one(new_user)
        return RedirectResponse(url="/user-login", status_code=302)
    except:
        return HTMLResponse("<h3>Database error</h3><a href='/register'>Try again</a>")

@app.get("/user-login")
async def user_login_page():
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Customer Login - ShopEasy</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: 'Segoe UI', sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; display: flex; align-items: center; justify-content: center; }
            .form-container { background: white; padding: 2.5rem; border-radius: 15px; box-shadow: 0 15px 35px rgba(0,0,0,0.1); max-width: 400px; width: 90%; }
            h2 { color: #333; margin-bottom: 1.5rem; text-align: center; font-size: 2rem; }
            .form-group { margin-bottom: 1.5rem; }
            input { width: 100%; padding: 15px; border: 2px solid #e1e1e1; border-radius: 10px; font-size: 1rem; transition: border-color 0.3s; }
            input:focus { outline: none; border-color: #667eea; }
            .btn { width: 100%; padding: 15px; background: linear-gradient(45deg, #667eea, #764ba2); color: white; border: none; border-radius: 10px; font-size: 1.1rem; font-weight: 600; cursor: pointer; transition: all 0.3s; }
            .btn:hover { transform: translateY(-2px); box-shadow: 0 8px 20px rgba(0,0,0,0.2); }
            .back-link { display: block; text-align: center; margin-top: 1rem; color: #666; text-decoration: none; }
        </style>
    </head>
    <body>
        <div class="form-container">
            <h2>Welcome Back</h2>
            <form method="post" action="/user-login">
                <div class="form-group">
                    <input name="email" type="email" placeholder="Email Address" required>
                </div>
                <div class="form-group">
                    <input name="password" type="password" placeholder="Password" required>
                </div>
                <button type="submit" class="btn">Sign In</button>
            </form>
            <a href="/" class="back-link">← Back to Home</a>
        </div>
    </body>
    </html>
    """)

@app.post("/user-login")
async def user_login(email: str = Form(), password: str = Form()):
    try:
        hashed_pw = hash_password(password)
        user = users_collection.find_one({"email": email, "password": hashed_pw})
        if user:
            response = RedirectResponse(url="/shop", status_code=302)
            response.set_cookie("user_id", str(user["_id"]))
            return response
    except:
        pass
    return HTMLResponse("<h3>Invalid credentials</h3><a href='/user-login'>Try again</a>")

@app.get("/shop")
async def shop_page(user_id: str = Cookie(None)):
    if not user_id:
        return RedirectResponse(url="/user-login")
    
    try:
        user = users_collection.find_one({"_id": int(user_id)})
        if not user:
            return RedirectResponse(url="/user-login")
        
        super_coins = user.get("super_coins", 0)
        products = list(products_collection.find({}))
        
        products_html = ""
        for product in products:
            products_html += f"""
            <div class="product-card">
                <div class="product-name">{product['name']}</div>
                <div class="product-price">₹{product['price']:,}</div>
                <div class="product-info">
                    <div>📂 {product['category']}</div>
                    <div>📦 Stock: {product['stock']}</div>
                </div>
                <form method="post" action="/order" class="order-form">
                    <input type="hidden" name="product_id" value="{product['_id']}">
                    <input type="number" name="quantity" value="1" min="1" max="{min(10, product['stock'])}" class="quantity-input">
                    <button type="submit" class="order-btn">🛒 Add to Cart</button>
                </form>
            </div>
            """
        
        return HTMLResponse(f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Shop - ShopEasy</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{ font-family: 'Segoe UI', sans-serif; background: #f8f9fa; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 2rem; text-align: center; box-shadow: 0 4px 20px rgba(0,0,0,0.1); }}
                .header h2 {{ font-size: 2rem; margin-bottom: 0.5rem; }}
                .coins {{ font-size: 1.2rem; margin: 1rem 0; padding: 10px 20px; background: rgba(255,255,255,0.2); border-radius: 25px; display: inline-block; }}
                .nav {{ margin-top: 1rem; }}
                .nav a {{ color: white; text-decoration: none; margin: 0 15px; padding: 8px 16px; border-radius: 20px; background: rgba(255,255,255,0.2); transition: all 0.3s; }}
                .nav a:hover {{ background: rgba(255,255,255,0.3); transform: translateY(-2px); }}
                .products-container {{ max-width: 1200px; margin: 2rem auto; padding: 0 1rem; }}
                .products-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 2rem; }}
                .product-card {{ background: white; border-radius: 15px; padding: 1.5rem; box-shadow: 0 8px 25px rgba(0,0,0,0.1); transition: all 0.3s; }}
                .product-card:hover {{ transform: translateY(-5px); box-shadow: 0 15px 40px rgba(0,0,0,0.15); }}
                .product-name {{ font-size: 1.3rem; font-weight: 600; color: #333; margin-bottom: 0.5rem; }}
                .product-price {{ font-size: 1.5rem; font-weight: 700; color: #667eea; margin-bottom: 0.5rem; }}
                .product-info {{ color: #666; margin-bottom: 1rem; }}
                .order-form {{ display: flex; align-items: center; gap: 10px; }}
                .quantity-input {{ width: 60px; padding: 8px; border: 2px solid #e1e1e1; border-radius: 8px; text-align: center; }}
                .order-btn {{ flex: 1; padding: 12px; background: linear-gradient(45deg, #56ab2f, #a8e6cf); color: white; border: none; border-radius: 8px; font-weight: 600; cursor: pointer; transition: all 0.3s; }}
                .order-btn:hover {{ transform: translateY(-2px); box-shadow: 0 4px 15px rgba(0,0,0,0.2); }}
            </style>
        </head>
        <body>
            <div class="header">
                <h2>Welcome back, {user['name']}! 👋</h2>
                <div class="coins">Super Coins: {super_coins} 🪙</div>
                <div class="nav">
                    <a href="/my-orders">📦 My Orders</a>
                    <a href="/logout">🚪 Logout</a>
                </div>
            </div>
            <div class="products-container">
                <h3 style="text-align: center; margin-bottom: 2rem; color: #333; font-size: 2rem;">🛍️ Featured Products</h3>
                <div class="products-grid">
                    {products_html}
                </div>
            </div>
        </body>
        </html>
        """)
    except:
        return RedirectResponse(url="/user-login")

@app.post("/order")
async def place_order(product_id: int = Form(), quantity: int = Form(), user_id: str = Cookie(None)):
    if not user_id:
        return RedirectResponse(url="/user-login")
    
    try:
        user = users_collection.find_one({"_id": int(user_id)})
        if not user:
            return RedirectResponse(url="/user-login")
        
        product = products_collection.find_one({"_id": product_id})
        if not product or product["stock"] < quantity:
            return HTMLResponse("<h3>Product not available</h3><a href='/shop'>Back to Shop</a>")
        
        total = product["price"] * quantity
        last_order = orders_collection.find_one(sort=[("_id", -1)])
        order_id = (last_order["_id"] + 1) if last_order else 1
        
        new_order = {
            "_id": order_id,
            "user_id": int(user_id),
            "product_name": product["name"],
            "product_id": product_id,
            "quantity": quantity,
            "total": total,
            "status": "Delivered",
            "date": datetime.now()
        }
        orders_collection.insert_one(new_order)
        
        products_collection.update_one({"_id": product_id}, {"$inc": {"stock": -quantity}})
        update_user_super_coins(int(user_id))
        
        return RedirectResponse(url="/my-orders", status_code=302)
    except:
        return HTMLResponse("<h3>Order failed</h3><a href='/shop'>Back to Shop</a>")

@app.get("/my-orders")
async def my_orders(user_id: str = Cookie(None)):
    if not user_id:
        return RedirectResponse(url="/user-login")
    
    try:
        user = users_collection.find_one({"_id": int(user_id)})
        if not user:
            return RedirectResponse(url="/user-login")
        
        user_orders = list(orders_collection.find({"user_id": int(user_id)}).sort("date", -1))
        super_coins = user.get("super_coins", 0)
        
        orders_html = ""
        for order in user_orders:
            orders_html += f"""
            <tr>
                <td><strong>#{order['_id']}</strong></td>
                <td>{order['product_name']}</td>
                <td>{order['quantity']}</td>
                <td>₹{order['total']:,.0f}</td>
                <td><span style="background:#d4edda;color:#155724;padding:4px 12px;border-radius:20px;">{order['status']}</span></td>
                <td>{order['date'].strftime('%d %b %Y')}</td>
            </tr>
            """
        
        return HTMLResponse(f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>My Orders - ShopEasy</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{ font-family: 'Segoe UI', sans-serif; background: #f8f9fa; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 2rem; text-align: center; }}
                .header h2 {{ font-size: 2rem; margin-bottom: 0.5rem; }}
                .coins {{ font-size: 1.2rem; margin: 1rem 0; padding: 10px 20px; background: rgba(255,255,255,0.2); border-radius: 25px; display: inline-block; }}
                .nav {{ margin-top: 1rem; }}
                .nav a {{ color: white; text-decoration: none; margin: 0 15px; padding: 8px 16px; border-radius: 20px; background: rgba(255,255,255,0.2); }}
                .orders-container {{ max-width: 1200px; margin: 2rem auto; padding: 0 1rem; }}
                .orders-table {{ background: white; border-radius: 15px; overflow: hidden; box-shadow: 0 8px 25px rgba(0,0,0,0.1); }}
                table {{ width: 100%; border-collapse: collapse; }}
                th {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 1rem; }}
                td {{ padding: 1rem; border-bottom: 1px solid #e1e1e1; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h2>📦 My Orders</h2>
                <div class="coins">Super Coins: {super_coins} 🪙</div>
                <div class="nav">
                    <a href="/shop">🛍️ Continue Shopping</a>
                    <a href="/logout">🚪 Logout</a>
                </div>
            </div>
            <div class="orders-container">
                <div class="orders-table">
                    <table>
                        <tr><th>Order ID</th><th>Product</th><th>Quantity</th><th>Total</th><th>Status</th><th>Date</th></tr>
                        {orders_html if orders_html else '<tr><td colspan="6" style="text-align:center;padding:2rem;">No orders yet</td></tr>'}
                    </table>
                </div>
            </div>
        </body>
        </html>
        """)
    except:
        return RedirectResponse(url="/user-login")

@app.get("/admin-login")
async def admin_login_page():
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Admin Portal - ShopEasy</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: 'Segoe UI', sans-serif; background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%); min-height: 100vh; display: flex; align-items: center; justify-content: center; }
            .form-container { background: white; padding: 2.5rem; border-radius: 15px; box-shadow: 0 15px 35px rgba(0,0,0,0.1); max-width: 400px; width: 90%; }
            h2 { color: #333; margin-bottom: 1.5rem; text-align: center; font-size: 2rem; }
            .admin-icon { text-align: center; font-size: 3rem; margin-bottom: 1rem; }
            .form-group { margin-bottom: 1.5rem; }
            input { width: 100%; padding: 15px; border: 2px solid #e1e1e1; border-radius: 10px; font-size: 1rem; }
            input:focus { outline: none; border-color: #ff6b6b; }
            .btn { width: 100%; padding: 15px; background: linear-gradient(45deg, #ff6b6b, #ee5a24); color: white; border: none; border-radius: 10px; font-size: 1.1rem; font-weight: 600; cursor: pointer; }
            .back-link { display: block; text-align: center; margin-top: 1rem; color: #666; text-decoration: none; }
        </style>
    </head>
    <body>
        <div class="form-container">
            <div class="admin-icon">🔐</div>
            <h2>Admin Portal</h2>
            <form method="post" action="/admin-login">
                <div class="form-group">
                    <input name="username" placeholder="Admin Username" required>
                </div>
                <div class="form-group">
                    <input name="password" type="password" placeholder="Admin Password" required>
                </div>
                <button type="submit" class="btn">Access Dashboard</button>
            </form>
            <a href="/" class="back-link">← Back to Home</a>
        </div>
    </body>
    </html>
    """)

@app.post("/admin-login")
async def admin_login(username: str = Form(), password: str = Form()):
    if username in admin_users and admin_users[username] == password:
        response = RedirectResponse(url="/admin-dashboard", status_code=302)
        response.set_cookie("admin", "true")
        return response
    return HTMLResponse("<h3>Invalid admin credentials</h3><a href='/admin-login'>Try again</a>")

@app.get("/admin-dashboard")
async def admin_dashboard(admin: str = Cookie(None)):
    if admin != "true":
        return RedirectResponse(url="/admin-login")
    
    try:
        users = list(users_collection.find({}))
        total_orders = orders_collection.count_documents({})
        total_revenue = sum(o["total"] for o in orders_collection.find({}))
        total_coins = sum(u.get("super_coins", 0) for u in users)
        
        users_html = ""
        if users:
            for user in users:
                super_coins = user.get("super_coins", 0)
                user_orders = list(orders_collection.find({"user_id": user["_id"]}))
                total_spent = sum(o["total"] for o in user_orders)
                
                users_html += f"""
                <tr>
                    <td><strong>{user['_id']}</strong></td>
                    <td>{user['name']}</td>
                    <td>{user['email']}</td>
                    <td>{len(user_orders)}</td>
                    <td>₹{total_spent:,.0f}</td>
                    <td>{super_coins} 🪙</td>
                </tr>
                """
        else:
            users_html = "<tr><td colspan='6' style='text-align:center;padding:2rem;'>No users registered yet</td></tr>"
        
        return HTMLResponse(f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Admin Dashboard - ShopEasy</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{ font-family: 'Segoe UI', sans-serif; background: #f8f9fa; }}
                .header {{ background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%); color: white; padding: 2rem; text-align: center; }}
                .header h2 {{ font-size: 2.5rem; margin-bottom: 0.5rem; }}
                .logout-btn {{ margin-top: 1rem; padding: 10px 20px; background: rgba(255,255,255,0.2); color: white; text-decoration: none; border-radius: 20px; }}
                .dashboard-container {{ max-width: 1200px; margin: 2rem auto; padding: 0 1rem; }}
                .stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1.5rem; margin-bottom: 2rem; }}
                .stat-card {{ background: white; padding: 1.5rem; border-radius: 15px; box-shadow: 0 8px 25px rgba(0,0,0,0.1); text-align: center; }}
                .stat-number {{ font-size: 2rem; font-weight: 700; color: #ff6b6b; }}
                .stat-label {{ color: #666; margin-top: 0.5rem; }}
                .users-table {{ background: white; border-radius: 15px; overflow: hidden; box-shadow: 0 8px 25px rgba(0,0,0,0.1); }}
                table {{ width: 100%; border-collapse: collapse; }}
                th {{ background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%); color: white; padding: 1rem; }}
                td {{ padding: 1rem; border-bottom: 1px solid #e1e1e1; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h2>🔐 Admin Dashboard</h2>
                <p>Manage your ecommerce platform</p>
                <a href="/logout" class="logout-btn">🚪 Logout</a>
            </div>
            <div class="dashboard-container">
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-number">{len(users)}</div>
                        <div class="stat-label">👥 Total Users</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">{total_orders}</div>
                        <div class="stat-label">📦 Total Orders</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">₹{total_revenue:,.0f}</div>
                        <div class="stat-label">💰 Total Revenue</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">{total_coins}</div>
                        <div class="stat-label">🪙 Super Coins Issued</div>
                    </div>
                </div>
                <div class="users-table">
                    <table>
                        <tr><th>👤 User ID</th><th>📝 Name</th><th>📧 Email</th><th>📦 Orders</th><th>💰 Total Spent</th><th>🪙 Super Coins</th></tr>
                        {users_html}
                    </table>
                </div>
            </div>
        </body>
        </html>
        """)
    except Exception as e:
        return HTMLResponse(f"<h3>Database error: {str(e)}</h3><a href='/logout'>Logout</a>")

@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie("user_id")
    response.delete_cookie("admin")
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)