from django.shortcuts import render
import psycopg2
from collections import Counter, defaultdict
from django.db import connections
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_car_db_connection():
    return connections['default']  # This will use the 'default' database in settings.py

def get_user_db_connection():
    return connections['user_db']  # This will use the 'user_db' database in settings.py

def homepage(request):
    return render(request, 'carapp/homepage.html')

def dashboard_view(request):
    # Connect to the car database
    conn = get_car_db_connection()
    cursor = conn.cursor()

    # Make counts
    cursor.execute("SELECT make, COUNT(*) FROM cars GROUP BY make")
    make_counts = dict(cursor.fetchall())

    # Make to Horsepower > 200
    cursor.execute("""
        SELECT make, horsepower::integer 
        FROM cars 
        WHERE horsepower ~ '^[0-9]+$' AND horsepower::integer > 200
    """)
    make_horsepower = cursor.fetchall()

    # Pie chart for Average Price by Body Type
    cursor.execute("""
        SELECT body_style, AVG(price::numeric) 
        FROM cars 
        WHERE price ~ '^[0-9]+$' AND price IS NOT NULL 
        GROUP BY body_style
    """)
    price_bodytype = cursor.fetchall()

    # Scatter plot for Price vs. Horsepower
    cursor.execute("""
        SELECT price::numeric, horsepower::integer 
        FROM cars 
        WHERE price ~ '^[0-9]+$' AND horsepower ~ '^[0-9]+$' 
        AND price IS NOT NULL 
        AND horsepower IS NOT NULL
    """)
    price_horsepower = cursor.fetchall()

    cursor.close()
    conn.close()

    # Logging example (optional)
    logger.info(f"Dashboard data retrieved: {len(make_counts)} makes, "
                f"{len(price_bodytype)} price by body type entries.")

    cursor.close()
    conn.close()

    context = {
        'make_counts': make_counts,
        'make_horsepower': make_horsepower,
        'price_bodytype': price_bodytype,
        'price_horsepower': price_horsepower,
    }

    return render(request, 'carapp/dashboard.html', context)

