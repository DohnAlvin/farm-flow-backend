from django.db import models
from django.conf import settings # 🐛 FIXED: We import settings to access your custom user model!

class Field(models.Model):
    # 🔐 Link this field to your custom user
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='fields')
    
    STATUS_CHOICES = [('planted', 'Planted'), ('growing', 'Growing'), ('harvesting', 'Harvesting'), ('fallow', 'Fallow'), ('preparing', 'Preparing')]
    SOIL_CHOICES = [('clay', 'Clay'), ('sandy', 'Sandy'), ('loam', 'Loam'), ('silt', 'Silt'), ('peat', 'Peat')]
    name = models.CharField(max_length=255)
    size_acres = models.DecimalField(max_digits=10, decimal_places=2)
    crop = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='fallow')
    planting_date = models.DateField(null=True, blank=True)
    expected_harvest_date = models.DateField(null=True, blank=True)
    soil_type = models.CharField(max_length=20, choices=SOIL_CHOICES, default='loam')
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Livestock(models.Model):
    # 🔐 Link this livestock to your custom user
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='livestock')

    ANIMAL_CHOICES = [('cattle', 'Cattle'), ('goats', 'Goats'), ('sheep', 'Sheep'), ('poultry', 'Poultry'), ('pigs', 'Pigs'), ('rabbits', 'Rabbits'), ('donkeys', 'Donkeys'), ('other', 'Other')]
    GENDER_CHOICES = [('male', 'Male'), ('female', 'Female')]
    HEALTH_CHOICES = [('healthy', 'Healthy'), ('sick', 'Sick'), ('under_treatment', 'Under Treatment'), ('quarantined', 'Quarantined')]
    animal_type = models.CharField(max_length=20, choices=ANIMAL_CHOICES)
    tag_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    breed = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    health_status = models.CharField(max_length=20, choices=HEALTH_CHOICES, default='healthy')
    weight_kg = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.tag_id} - {self.name or self.animal_type}"

class Transaction(models.Model):
    # 🔐 Link this transaction to your custom user
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='transactions')

    TYPE_CHOICES = [('income', 'Income'), ('expense', 'Expense')]
    CATEGORY_CHOICES = [
        ('seeds', 'Seeds'), ('fertilizer', 'Fertilizer'), ('pesticides', 'Pesticides'),
        ('labor', 'Labor'), ('equipment', 'Equipment'), ('veterinary', 'Veterinary'),
        ('feed', 'Feed'), ('transport', 'Transport'), ('crop_sale', 'Crop Sale'),
        ('livestock_sale', 'Livestock Sale'), ('milk_sale', 'Milk Sale'), ('other', 'Other')
    ]
    PAYMENT_CHOICES = [('cash', 'Cash'), ('mpesa', 'M-Pesa'), ('bank_transfer', 'Bank Transfer'), ('cheque', 'Cheque')]

    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='cash')
    mpesa_reference = models.CharField(max_length=50, blank=True, null=True)
    date = models.DateField()

    def __str__(self):
        return f"{self.type.upper()} - {self.amount} KES ({self.category})"

class FarmTask(models.Model):
    # 🔐 Link this task to your custom user
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tasks')

    CATEGORY_CHOICES = [('planting', 'Planting'), ('irrigation', 'Irrigation'), ('fertilizing', 'Fertilizing'), ('pest_control', 'Pest Control'), ('harvesting', 'Harvesting'), ('feeding', 'Feeding'), ('veterinary', 'Veterinary'), ('maintenance', 'Maintenance'), ('other', 'Other')]
    PRIORITY_CHOICES = [('low', 'Low'), ('medium', 'Medium'), ('high', 'High'), ('urgent', 'Urgent')]
    STATUS_CHOICES = [('pending', 'Pending'), ('in_progress', 'In Progress'), ('completed', 'Completed'), ('cancelled', 'Cancelled')]
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    due_date = models.DateField(null=True, blank=True)
    assigned_to = models.CharField(max_length=100, blank=True, null=True)
    related_field = models.ForeignKey(Field, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')
    related_livestock = models.ForeignKey(Livestock, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')

    def __str__(self):
        return self.title