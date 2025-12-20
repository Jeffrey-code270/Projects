import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'https://your-api-gateway-url';

function ProductList() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [cart, setCart] = useState([]);

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/products`);
      setProducts(response.data.products || []);
    } catch (error) {
      console.error('Error fetching products:', error);
      // Fallback to sample data for demo
      setProducts([
        {
          product_id: 'prod-001',
          name: 'Wireless Headphones',
          description: 'High-quality wireless headphones with noise cancellation',
          price: 99.99,
          category: 'electronics',
          stock: 50,
          image_url: 'https://via.placeholder.com/300x200?text=Headphones'
        },
        {
          product_id: 'prod-002',
          name: 'Smart Watch',
          description: 'Feature-rich smartwatch with health tracking',
          price: 199.99,
          category: 'electronics',
          stock: 30,
          image_url: 'https://via.placeholder.com/300x200?text=Smart+Watch'
        },
        {
          product_id: 'prod-003',
          name: 'Coffee Mug',
          description: 'Ceramic coffee mug with custom design',
          price: 12.99,
          category: 'home',
          stock: 100,
          image_url: 'https://via.placeholder.com/300x200?text=Coffee+Mug'
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const addToCart = async (product) => {
    try {
      // In a real app, this would call the cart API
      const existingItem = cart.find(item => item.product_id === product.product_id);
      
      if (existingItem) {
        setCart(cart.map(item => 
          item.product_id === product.product_id 
            ? { ...item, quantity: item.quantity + 1 }
            : item
        ));
      } else {
        setCart([...cart, { ...product, quantity: 1 }]);
      }
      
      alert('Product added to cart!');
    } catch (error) {
      console.error('Error adding to cart:', error);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Products</h1>
        <p className="text-gray-600">Discover our amazing collection</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {products.map((product) => (
          <div key={product.product_id} className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow duration-300">
            <img
              src={product.image_url}
              alt={product.name}
              className="w-full h-48 object-cover"
            />
            <div className="p-6">
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                {product.name}
              </h3>
              <p className="text-gray-600 mb-4 text-sm">
                {product.description}
              </p>
              <div className="flex items-center justify-between">
                <span className="text-2xl font-bold text-blue-600">
                  ${product.price}
                </span>
                <span className="text-sm text-gray-500">
                  Stock: {product.stock}
                </span>
              </div>
              <button
                onClick={() => addToCart(product)}
                disabled={product.stock === 0}
                className="w-full mt-4 bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors duration-300"
              >
                {product.stock === 0 ? 'Out of Stock' : 'Add to Cart'}
              </button>
            </div>
          </div>
        ))}
      </div>

      {products.length === 0 && (
        <div className="text-center py-12">
          <p className="text-gray-500 text-lg">No products available</p>
        </div>
      )}
    </div>
  );
}

export default ProductList;