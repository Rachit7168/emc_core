import json
import random
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Reservation, Brand, MenuItem

# 1. Homepage View
def index(request):
    return render(request, 'web/index.html')

# 2. Experience View (The Dynamic Menu)
def experience(request, brand_key):
    # Static Data for Styling (Themes, Images, Descriptions)
    brands = {
        'kitchen': {
            'name': 'THE CAFE',
            'tagline': 'Where Coffee Meets Soul',
            'theme': 'amber', 
            'bg_image': 'https://images.unsplash.com/photo-1509042239860-f550ce710b93?q=80&w=1974',
            'accent_text': 'text-amber-100',
            'accent_border': 'border-amber-100/30',
            'button_class': 'bg-amber-100 text-black hover:bg-white',
            'description': 'A curated selection of artisanal coffees, authentic ramen, and global fusion plates served in an ambiance of understated luxury.',
            'secret_dish': {
                'name': 'The Golden Ramen',
                'desc': '24-hour broth infused with truffle oil and topped with edible gold leaf.',
                'image': 'https://images.unsplash.com/photo-1569718212165-3a8278d5f624?q=80&w=1780',
                'price': '₹899'
            }
        },
        'dadho': {
            'name': 'DADHO SUTHO',
            'tagline': 'The Taste of Sindh',
            'theme': 'orange',
            'bg_image': 'https://images.unsplash.com/photo-1596797038530-2c107229654b?q=80&w=1935',
            'accent_text': 'text-orange-200',
            'accent_border': 'border-orange-200/30',
            'button_class': 'bg-orange-200 text-black hover:bg-white',
            'description': 'Heritage recipes passed down through generations. Experience the rich, aromatic spices of authentic Sindhi cuisine.',
            'secret_dish': {
                'name': 'Royal Shahi Thali',
                'desc': 'A feast fit for kings. 12 delicacies served on a silver platter.',
                'image': 'https://images.unsplash.com/photo-1546833999-b9f581a1996d?q=80&w=2070',
                'price': '₹1200'
            }
        },
        'zabardast': {
            'name': 'ZABARDAST',
            'tagline': 'Bold. Spicy. Fast.',
            'theme': 'yellow',
            'bg_image': 'https://images.unsplash.com/photo-1561758033-d8f19662cb23?q=80&w=2070',
            'accent_text': 'text-yellow-300',
            'accent_border': 'border-yellow-300/30',
            'button_class': 'bg-yellow-300 text-black hover:bg-white',
            'description': 'Street food reimagined for the modern palate. High energy, big flavors, and zero compromise.',
            'secret_dish': {
                'name': 'The Volcano Wrap',
                'desc': 'Super-spicy ghost pepper sauce, double cheese, and flaming presentation.',
                'image': 'https://images.unsplash.com/photo-1626700051175-6818013e1d4f?q=80&w=1964',
                'price': '₹450'
            }
        }
    }

    selected_brand = brands.get(brand_key, brands['kitchen'])

    # --- DATABASE LOGIC ---
    # 1. Find the Brand in the DB
    brand_obj = Brand.objects.filter(key=brand_key).first()

    menu_categories = []
    if brand_obj:
        # Define the exact order you want them to appear
        categories = [
            'ramen', 'appetizers', 'salad', 'burger', 'fries', 'baos', 'dumplings', 
            'pasta', 'sizzlers', 'rice', 'noodles', 'dessert'
        ]
        
        for cat in categories:
            items = MenuItem.objects.filter(brand=brand_obj, category=cat)
            if items.exists():
                menu_categories.append({
                    'name': cat.capitalize(),
                    'items': items
                })

    context = {
        'brand': selected_brand,
        'categories': menu_categories,
        'brand_key': brand_key
    }
    return render(request, 'web/experience.html', context)

# 3. Booking View
def book_table(request):
    brands = [
        {'key': 'kitchen', 'name': 'The Cafe', 'color': 'text-amber-100', 'border': 'border-amber-100'},
        {'key': 'dadho', 'name': 'Dadho Sutho', 'color': 'text-orange-200', 'border': 'border-orange-200'},
        {'key': 'zabardast', 'name': 'Zabardast', 'color': 'text-yellow-300', 'border': 'border-yellow-300'},
    ]
    return render(request, 'web/book.html', {'brands': brands})

# --- API TO SAVE BOOKING ---
@csrf_exempt 
def api_book_table(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            reservation = Reservation.objects.create(
                name=data.get('name'),
                phone=data.get('phone'),
                brand=data.get('brand'),
                date=data.get('date'),
                time=data.get('time'),
                guests=int(data.get('guests', 2)), 
                table_id=data.get('table_id')
            )
            
            return JsonResponse({'status': 'success', 'id': reservation.id})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
            
    return JsonResponse({'status': 'error', 'message': 'Invalid method'})

# 4. DASHBOARD: Main
def dashboard(request):
    recent_bookings = Reservation.objects.all().order_by('-created_at')[:10]
    total_bookings = Reservation.objects.count()
    today_bookings = Reservation.objects.filter(date=datetime.now().date()).count()
    
    context = {
        'recent_bookings': recent_bookings,
        'upcoming_reservations': today_bookings,
        'total_revenue': f"₹{total_bookings * 450}", 
        'active_tables': random.randint(3, 12), 
        'secret_dish_status': 'Active',
        'chart_data': [12, 19, 3, 5, 2, 30, 45, 35, 20],
        'active_tab': 'dashboard'
    }
    return render(request, 'web/dashboard.html', context)

# 5. DASHBOARD: Bookings
def dashboard_bookings(request):
    bookings = Reservation.objects.all().order_by('-created_at')
    return render(request, 'web/dashboard_bookings.html', {'bookings': bookings, 'active_tab': 'bookings'})

# 6. DASHBOARD: Menu Manager
def dashboard_menu(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        brand_key = request.POST.get('brand')
        image_file = request.FILES.get('image')
        
        brand = Brand.objects.get(key=brand_key)
        
        MenuItem.objects.create(
            brand=brand,
            name=name,
            price=price,
            description="Freshly added via Dashboard",
            image_url="https://source.unsplash.com/random/food" 
        )
        return redirect('dashboard_menu')

    items = MenuItem.objects.all().select_related('brand')
    brands = Brand.objects.all()
    
    return render(request, 'web/dashboard_menu.html', {
        'items': items, 
        'brands': brands,
        'active_tab': 'menu'
    })

# 7. DASHBOARD: Delete Item Logic
def delete_menu_item(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    item.delete()
    return redirect('dashboard_menu')

# 8. DASHBOARD: Tables
def dashboard_tables(request):
    return render(request, 'web/dashboard_tables.html', {'active_tab': 'tables'})

# 9. DASHBOARD: Edit Item Logic
def edit_menu_item(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    
    if request.method == 'POST':
        item.name = request.POST.get('name')
        item.price = request.POST.get('price')
        
        # Update Brand
        brand_key = request.POST.get('brand')
        item.brand = Brand.objects.get(key=brand_key)
        
        # Update Image ONLY if a new file was uploaded
        if request.FILES.get('image'):
            item.image = request.FILES.get('image')
            
        item.save()
        return redirect('dashboard_menu')
    
    # Get brands for the dropdown
    brands = Brand.objects.all()
    
    # Reuse the base template but show the edit form
    return render(request, 'web/edit_menu_item.html', {
        'item': item, 
        'brands': brands,
        'active_tab': 'menu'
    })