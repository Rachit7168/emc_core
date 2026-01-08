from django.db import models

# 1. Brand Model (The 3 Sub-brands)
class Brand(models.Model):
    key = models.CharField(max_length=20, unique=True) # e.g., 'kitchen', 'dadho', 'zabardast'
    name = models.CharField(max_length=100)
    theme_color = models.CharField(max_length=20, default="#000000")
    
    def __str__(self):
        return self.name

# 2. Menu Item Model (The Food)
class MenuItem(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image_url = models.URLField(default="https://source.unsplash.com/random/food") 

    def __str__(self):
        return f"{self.name} ({self.brand.name})"

# 3. Reservation Model (The Bookings)
class Reservation(models.Model):
    BRAND_CHOICES = [
        ('kitchen', 'The Cafe'),
        ('dadho', 'Dadho Sutho'),
        ('zabardast', 'Zabardast'),
    ]
    
    # Customer Details
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    
    # Booking Details
    brand = models.CharField(max_length=20, choices=BRAND_CHOICES)
    date = models.DateField()
    time = models.CharField(max_length=10)
    guests = models.IntegerField()
    
    # Technical Fields
    table_id = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Confirmed')

    def __str__(self):
        return f"{self.name} - {self.brand} ({self.date})"

class MenuItem(models.Model):
    CATEGORY_CHOICES = [
        ('ramen', 'Ramen'),
        ('fries', 'Fries'),
        ('burger', 'Burgers'),
        ('appetizers', 'Appetizers'),
        ('pasta', 'Pasta'),
        ('dumplings', 'Dumplings'),
        ('sizzlers', 'Sizzlers'),
        ('rice', 'Rice'),
        ('noodles', 'Noodles'),
        ('baos', 'Baos'),
        ('dessert', 'Dessert'),
        ('salad', 'Salads'),
        ('other', 'Other'),
    ]

    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    
    # 1. New Field for your uploads
    image = models.ImageField(upload_to='menu_items/', blank=True, null=True)
    
    # 2. Keep this for the auto-generated ones (fallback)
    image_url = models.URLField(default="https://source.unsplash.com/random/food", blank=True)

    def __str__(self):
        return f"{self.name} ({self.brand.name})"