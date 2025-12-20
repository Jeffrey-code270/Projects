import json
import boto3
import uuid
from decimal import Decimal
from datetime import datetime

# Initialize DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ecommerce-products')

def lambda_handler(event, context):
    """Main Lambda handler for products API"""
    
    http_method = event['httpMethod']
    path = event['path']
    
    try:
        if http_method == 'GET':
            if '/products/' in path:
                # Get single product
                product_id = path.split('/')[-1]
                return get_product(product_id)
            else:
                # Get all products
                return get_all_products()
                
        elif http_method == 'POST':
            return create_product(json.loads(event['body']))
            
        elif http_method == 'PUT':
            product_id = path.split('/')[-1]
            return update_product(product_id, json.loads(event['body']))
            
        elif http_method == 'DELETE':
            product_id = path.split('/')[-1]
            return delete_product(product_id)
            
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': cors_headers(),
            'body': json.dumps({'error': str(e)})
        }

def get_all_products():
    """Get all products with pagination"""
    try:
        response = table.scan()
        products = response['Items']
        
        # Convert Decimal to float for JSON serialization
        for product in products:
            if 'price' in product:
                product['price'] = float(product['price'])
        
        return {
            'statusCode': 200,
            'headers': cors_headers(),
            'body': json.dumps({
                'products': products,
                'count': len(products)
            })
        }
    except Exception as e:
        return error_response(str(e))

def get_product(product_id):
    """Get single product by ID"""
    try:
        response = table.get_item(Key={'product_id': product_id})
        
        if 'Item' not in response:
            return {
                'statusCode': 404,
                'headers': cors_headers(),
                'body': json.dumps({'error': 'Product not found'})
            }
        
        product = response['Item']
        if 'price' in product:
            product['price'] = float(product['price'])
            
        return {
            'statusCode': 200,
            'headers': cors_headers(),
            'body': json.dumps(product)
        }
    except Exception as e:
        return error_response(str(e))

def create_product(product_data):
    """Create new product"""
    try:
        product_id = str(uuid.uuid4())
        
        product = {
            'product_id': product_id,
            'name': product_data['name'],
            'description': product_data.get('description', ''),
            'price': Decimal(str(product_data['price'])),
            'category': product_data.get('category', 'general'),
            'stock': product_data.get('stock', 0),
            'image_url': product_data.get('image_url', ''),
            'created_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat()
        }
        
        table.put_item(Item=product)
        
        # Convert Decimal for response
        product['price'] = float(product['price'])
        
        return {
            'statusCode': 201,
            'headers': cors_headers(),
            'body': json.dumps(product)
        }
    except Exception as e:
        return error_response(str(e))

def update_product(product_id, update_data):
    """Update existing product"""
    try:
        # Check if product exists
        response = table.get_item(Key={'product_id': product_id})
        if 'Item' not in response:
            return {
                'statusCode': 404,
                'headers': cors_headers(),
                'body': json.dumps({'error': 'Product not found'})
            }
        
        # Update product
        update_expression = "SET updated_at = :updated_at"
        expression_values = {':updated_at': datetime.utcnow().isoformat()}
        
        for key, value in update_data.items():
            if key in ['name', 'description', 'category', 'stock', 'image_url']:
                update_expression += f", {key} = :{key}"
                expression_values[f':{key}'] = value
            elif key == 'price':
                update_expression += f", {key} = :{key}"
                expression_values[f':{key}'] = Decimal(str(value))
        
        table.update_item(
            Key={'product_id': product_id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_values
        )
        
        # Get updated product
        updated_response = table.get_item(Key={'product_id': product_id})
        product = updated_response['Item']
        product['price'] = float(product['price'])
        
        return {
            'statusCode': 200,
            'headers': cors_headers(),
            'body': json.dumps(product)
        }
    except Exception as e:
        return error_response(str(e))

def delete_product(product_id):
    """Delete product"""
    try:
        table.delete_item(Key={'product_id': product_id})
        
        return {
            'statusCode': 200,
            'headers': cors_headers(),
            'body': json.dumps({'message': 'Product deleted successfully'})
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