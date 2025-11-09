#!/usr/bin/env python3
from flask import Flask, render_template_string, jsonify, request
import json
import uuid
from datetime import datetime

app = Flask(__name__)

# In-memory data store for demo
products_db = [
    {
        'product_id': 'prod-001',
        'name': 'Wireless Headphones',
        'description': 'High-quality wireless headphones with noise cancellation',
        'price': 99.99,
        'category': 'electronics',
        'stock': 50,
        'image_url': 'https://via.placeholder.com/300x200/4F46E5/FFFFFF?text=Headphones'
    },
    {
        'product_id': 'prod-002',
        'name': 'Smart Watch',
        'description': 'Feature-rich smartwatch with health tracking',
        'price': 199.99,
        'category': 'electronics',
        'stock': 30,
        'image_url': 'https://via.placeholder.com/300x200/059669/FFFFFF?text=Smart+Watch'
    },
    {
        'product_id': 'prod-003',
        'name': 'Coffee Mug',
        'description': 'Ceramic coffee mug with custom design',
        'price': 12.99,
        'category': 'home',
        'stock': 100,
        'image_url': 'https://via.placeholder.com/300x200/DC2626/FFFFFF?text=Coffee+Mug'
    },
    {
        'product_id': 'prod-004',
        'name': 'Laptop Stand',
        'description': 'Ergonomic aluminum laptop stand',
        'price': 49.99,
        'category': 'accessories',
        'stock': 25,
        'image_url': 'https://via.placeholder.com/300x200/7C3AED/FFFFFF?text=Laptop+Stand'
    }
]

cart_db = {}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Serverless E-Commerce Demo</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/axios/dist/axios.min.js"></script>
</head>
<body class="bg-gray-50">
    <!-- Header -->
    <header class="bg-white shadow-sm border-b">
        <div class="container mx-auto px-4 py-4 flex items-center justify-between">
            <h1 class="text-2xl font-bold text-blue-600">🛒 E-Commerce Demo</h1>
            <div class="flex items-center gap-4">
                <button onclick="showCart()" class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors">
                    Cart (<span id="cart-count">0</span>)
                </button>
            </div>
        </div>
    </header>

    <main class="container mx-auto px-4 py-8">
        <!-- Products Section -->
        <div id="products-section">
            <div class="mb-8">
                <h2 class="text-3xl font-bold text-gray-900 mb-2">Products</h2>
                <p class="text-gray-600">Serverless E-Commerce Platform Demo</p>
            </div>
            
            <div id="products-grid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                <!-- Products will be loaded here -->
            </div>
        </div>

        <!-- Cart Section -->
        <div id="cart-section" class="hidden">
            <div class="mb-8">
                <button onclick="showProducts()" class="text-blue-600 hover:text-blue-800 mb-4">← Back to Products</button>
                <h2 class="text-3xl font-bold text-gray-900 mb-2">Shopping Cart</h2>
            </div>
            
            <div id="cart-items" class="space-y-4">
                <!-- Cart items will be loaded here -->
            </div>
            
            <div id="cart-total" class="mt-8 p-6 bg-white rounded-lg shadow-md">
                <!-- Cart total will be shown here -->
            </div>
        </div>
    </main>

    <script>
        let cart = {};
        
        // Load products on page load
        document.addEventListener('DOMContentLoaded', function() {
            loadProducts();
        });
        
        async function loadProducts() {
            try {
                const response = await axios.get('/api/products');
                const products = response.data.products;
                displayProducts(products);
            } catch (error) {
                console.error('Error loading products:', error);
            }
        }
        
        function displayProducts(products) {
            const grid = document.getElementById('products-grid');
            grid.innerHTML = products.map(product => `
                <div class="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow duration-300">
                    <img src="${product.image_url}" alt="${product.name}" class="w-full h-48 object-cover">
                    <div class="p-6">
                        <h3 class="text-xl font-semibold text-gray-900 mb-2">${product.name}</h3>
                        <p class="text-gray-600 mb-4 text-sm">${product.description}</p>
                        <div class="flex items-center justify-between mb-4">
                            <span class="text-2xl font-bold text-blue-600">$${product.price}</span>
                            <span class="text-sm text-gray-500">Stock: ${product.stock}</span>
                        </div>
                        <button 
                            onclick="addToCart('${product.product_id}')"
                            class="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors duration-300"
                            ${product.stock === 0 ? 'disabled' : ''}
                        >
                            ${product.stock === 0 ? 'Out of Stock' : 'Add to Cart'}
                        </button>
                    </div>
                </div>
            `).join('');
        }
        
        async function addToCart(productId) {
            try {
                const response = await axios.post(`/api/cart/user123/add`, {
                    product_id: productId,
                    quantity: 1
                });
                
                if (response.status === 200) {
                    updateCartCount();
                    showNotification('Product added to cart!');
                }
            } catch (error) {
                console.error('Error adding to cart:', error);
                showNotification('Error adding to cart', 'error');
            }
        }
        
        async function updateCartCount() {
            try {
                const response = await axios.get('/api/cart/user123');
                const cartData = response.data;
                document.getElementById('cart-count').textContent = cartData.item_count || 0;
            } catch (error) {
                console.error('Error updating cart count:', error);
            }
        }
        
        async function showCart() {
            try {
                const response = await axios.get('/api/cart/user123');
                const cartData = response.data;
                displayCart(cartData);
                
                document.getElementById('products-section').classList.add('hidden');
                document.getElementById('cart-section').classList.remove('hidden');
            } catch (error) {
                console.error('Error loading cart:', error);
            }
        }
        
        function displayCart(cartData) {
            const cartItems = document.getElementById('cart-items');
            const cartTotal = document.getElementById('cart-total');
            
            if (cartData.items && cartData.items.length > 0) {
                cartItems.innerHTML = cartData.items.map(item => `
                    <div class="bg-white p-6 rounded-lg shadow-md flex items-center justify-between">
                        <div class="flex items-center gap-4">
                            <img src="${item.image_url}" alt="${item.name}" class="w-16 h-16 object-cover rounded">
                            <div>
                                <h3 class="font-semibold text-gray-900">${item.name}</h3>
                                <p class="text-gray-600">$${item.price} each</p>
                            </div>
                        </div>
                        <div class="flex items-center gap-4">
                            <div class="flex items-center gap-2">
                                <button onclick="updateQuantity('${item.product_id}', ${item.quantity - 1})" class="bg-gray-200 px-2 py-1 rounded">-</button>
                                <span class="px-3">${item.quantity}</span>
                                <button onclick="updateQuantity('${item.product_id}', ${item.quantity + 1})" class="bg-gray-200 px-2 py-1 rounded">+</button>
                            </div>
                            <span class="font-semibold">$${item.item_total.toFixed(2)}</span>
                            <button onclick="removeFromCart('${item.product_id}')" class="text-red-600 hover:text-red-800">Remove</button>
                        </div>
                    </div>
                `).join('');
                
                cartTotal.innerHTML = `
                    <div class="flex justify-between items-center">
                        <span class="text-xl font-semibold">Total: $${cartData.total_amount.toFixed(2)}</span>
                        <button class="bg-green-600 text-white px-6 py-3 rounded-lg hover:bg-green-700 transition-colors">
                            Checkout (${cartData.item_count} items)
                        </button>
                    </div>
                `;
            } else {
                cartItems.innerHTML = '<div class="text-center py-12 text-gray-500">Your cart is empty</div>';
                cartTotal.innerHTML = '';
            }
        }
        
        function showProducts() {
            document.getElementById('cart-section').classList.add('hidden');
            document.getElementById('products-section').classList.remove('hidden');
        }
        
        function showNotification(message, type = 'success') {
            const notification = document.createElement('div');
            notification.className = `fixed top-4 right-4 px-6 py-3 rounded-lg text-white z-50 ${type === 'error' ? 'bg-red-600' : 'bg-green-600'}`;
            notification.textContent = message;
            document.body.appendChild(notification);
            
            setTimeout(() => {
                notification.remove();
            }, 3000);
        }
        
        // Initialize cart count
        updateCartCount();
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/products', methods=['GET'])
def get_products():
    return jsonify({
        'products': products_db,
        'count': len(products_db)
    })

@app.route('/api/products/<product_id>', methods=['GET'])
def get_product(product_id):
    product = next((p for p in products_db if p['product_id'] == product_id), None)
    if product:
        return jsonify(product)
    return jsonify({'error': 'Product not found'}), 404

@app.route('/api/cart/<user_id>', methods=['GET'])
def get_cart(user_id):
    user_cart = cart_db.get(user_id, {})
    items = []
    total_amount = 0
    
    for product_id, quantity in user_cart.items():
        product = next((p for p in products_db if p['product_id'] == product_id), None)
        if product:
            item_total = product['price'] * quantity
            total_amount += item_total
            items.append({
                'product_id': product_id,
                'name': product['name'],
                'price': product['price'],
                'quantity': quantity,
                'item_total': item_total,
                'image_url': product['image_url']
            })
    
    return jsonify({
        'user_id': user_id,
        'items': items,
        'total_amount': total_amount,
        'item_count': len(items)
    })

@app.route('/api/cart/<user_id>/add', methods=['POST'])
def add_to_cart(user_id):
    data = request.json
    product_id = data['product_id']
    quantity = data.get('quantity', 1)
    
    # Check if product exists
    product = next((p for p in products_db if p['product_id'] == product_id), None)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    # Initialize user cart if not exists
    if user_id not in cart_db:
        cart_db[user_id] = {}
    
    # Add or update quantity
    if product_id in cart_db[user_id]:
        cart_db[user_id][product_id] += quantity
    else:
        cart_db[user_id][product_id] = quantity
    
    return jsonify({'message': 'Item added to cart successfully'})

if __name__ == '__main__':
    print("🛒 Starting Serverless E-Commerce Demo...")
    print("🌐 Open http://localhost:5001 in your browser")
    print("📱 Features: Product catalog, shopping cart, responsive design")
    print("Press Ctrl+C to stop")
    app.run(host='0.0.0.0', port=5001, debug=False)