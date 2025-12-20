import json
import boto3
from decimal import Decimal
from datetime import datetime

# Initialize DynamoDB
dynamodb = boto3.resource('dynamodb')
cart_table = dynamodb.Table('ecommerce-cart')
products_table = dynamodb.Table('ecommerce-products')

def lambda_handler(event, context):
    """Main Lambda handler for cart API"""
    
    http_method = event['httpMethod']
    path = event['path']
    
    try:
        if http_method == 'GET':
            # Get cart for user
            user_id = event['pathParameters']['user_id']
            return get_cart(user_id)
            
        elif http_method == 'POST':
            # Add item to cart
            user_id = event['pathParameters']['user_id']
            return add_to_cart(user_id, json.loads(event['body']))
            
        elif http_method == 'PUT':
            # Update cart item quantity
            user_id = event['pathParameters']['user_id']
            product_id = event['pathParameters']['product_id']
            return update_cart_item(user_id, product_id, json.loads(event['body']))
            
        elif http_method == 'DELETE':
            if 'product_id' in event['pathParameters']:
                # Remove specific item
                user_id = event['pathParameters']['user_id']
                product_id = event['pathParameters']['product_id']
                return remove_from_cart(user_id, product_id)
            else:
                # Clear entire cart
                user_id = event['pathParameters']['user_id']
                return clear_cart(user_id)
                
    except Exception as e:
        return error_response(str(e))

def get_cart(user_id):
    """Get user's cart with product details"""
    try:
        # Get cart items
        response = cart_table.query(
            KeyConditionExpression='user_id = :user_id',
            ExpressionAttributeValues={':user_id': user_id}
        )
        
        cart_items = response['Items']
        total_amount = Decimal('0')
        detailed_items = []
        
        # Get product details for each cart item
        for item in cart_items:
            product_response = products_table.get_item(
                Key={'product_id': item['product_id']}
            )
            
            if 'Item' in product_response:
                product = product_response['Item']
                item_total = product['price'] * item['quantity']
                total_amount += item_total
                
                detailed_items.append({
                    'product_id': item['product_id'],
                    'name': product['name'],
                    'price': float(product['price']),
                    'quantity': item['quantity'],
                    'item_total': float(item_total),
                    'image_url': product.get('image_url', '')
                })
        
        return {
            'statusCode': 200,
            'headers': cors_headers(),
            'body': json.dumps({
                'user_id': user_id,
                'items': detailed_items,
                'total_amount': float(total_amount),
                'item_count': len(detailed_items)
            })
        }
    except Exception as e:
        return error_response(str(e))

def add_to_cart(user_id, item_data):
    """Add item to cart or update quantity if exists"""
    try:
        product_id = item_data['product_id']
        quantity = item_data.get('quantity', 1)
        
        # Check if product exists
        product_response = products_table.get_item(
            Key={'product_id': product_id}
        )
        
        if 'Item' not in product_response:
            return {
                'statusCode': 404,
                'headers': cors_headers(),
                'body': json.dumps({'error': 'Product not found'})
            }
        
        product = product_response['Item']
        
        # Check stock availability
        if product['stock'] < quantity:
            return {
                'statusCode': 400,
                'headers': cors_headers(),
                'body': json.dumps({'error': 'Insufficient stock'})
            }
        
        # Check if item already in cart
        cart_response = cart_table.get_item(
            Key={'user_id': user_id, 'product_id': product_id}
        )
        
        if 'Item' in cart_response:
            # Update existing item
            new_quantity = cart_response['Item']['quantity'] + quantity
            
            if product['stock'] < new_quantity:
                return {
                    'statusCode': 400,
                    'headers': cors_headers(),
                    'body': json.dumps({'error': 'Insufficient stock'})
                }
            
            cart_table.update_item(
                Key={'user_id': user_id, 'product_id': product_id},
                UpdateExpression='SET quantity = :quantity, updated_at = :updated_at',
                ExpressionAttributeValues={
                    ':quantity': new_quantity,
                    ':updated_at': datetime.utcnow().isoformat()
                }
            )
        else:
            # Add new item
            cart_table.put_item(
                Item={
                    'user_id': user_id,
                    'product_id': product_id,
                    'quantity': quantity,
                    'added_at': datetime.utcnow().isoformat(),
                    'updated_at': datetime.utcnow().isoformat()
                }
            )
        
        return {
            'statusCode': 200,
            'headers': cors_headers(),
            'body': json.dumps({'message': 'Item added to cart successfully'})
        }
    except Exception as e:
        return error_response(str(e))

def update_cart_item(user_id, product_id, update_data):
    """Update cart item quantity"""
    try:
        new_quantity = update_data['quantity']
        
        if new_quantity <= 0:
            return remove_from_cart(user_id, product_id)
        
        # Check product stock
        product_response = products_table.get_item(
            Key={'product_id': product_id}
        )
        
        if 'Item' not in product_response:
            return {
                'statusCode': 404,
                'headers': cors_headers(),
                'body': json.dumps({'error': 'Product not found'})
            }
        
        product = product_response['Item']
        
        if product['stock'] < new_quantity:
            return {
                'statusCode': 400,
                'headers': cors_headers(),
                'body': json.dumps({'error': 'Insufficient stock'})
            }
        
        cart_table.update_item(
            Key={'user_id': user_id, 'product_id': product_id},
            UpdateExpression='SET quantity = :quantity, updated_at = :updated_at',
            ExpressionAttributeValues={
                ':quantity': new_quantity,
                ':updated_at': datetime.utcnow().isoformat()
            }
        )
        
        return {
            'statusCode': 200,
            'headers': cors_headers(),
            'body': json.dumps({'message': 'Cart item updated successfully'})
        }
    except Exception as e:
        return error_response(str(e))

def remove_from_cart(user_id, product_id):
    """Remove item from cart"""
    try:
        cart_table.delete_item(
            Key={'user_id': user_id, 'product_id': product_id}
        )
        
        return {
            'statusCode': 200,
            'headers': cors_headers(),
            'body': json.dumps({'message': 'Item removed from cart'})
        }
    except Exception as e:
        return error_response(str(e))

def clear_cart(user_id):
    """Clear entire cart for user"""
    try:
        # Get all cart items for user
        response = cart_table.query(
            KeyConditionExpression='user_id = :user_id',
            ExpressionAttributeValues={':user_id': user_id}
        )
        
        # Delete each item
        for item in response['Items']:
            cart_table.delete_item(
                Key={'user_id': user_id, 'product_id': item['product_id']}
            )
        
        return {
            'statusCode': 200,
            'headers': cors_headers(),
            'body': json.dumps({'message': 'Cart cleared successfully'})
        }
    except Exception as e:
        return error_response(str(e))

def cors_headers():
    """CORS headers for API responses"""
    return {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
        'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS'
    }

def error_response(message):
    """Standard error response"""
    return {
        'statusCode': 500,
        'headers': cors_headers(),
        'body': json.dumps({'error': message})
    }