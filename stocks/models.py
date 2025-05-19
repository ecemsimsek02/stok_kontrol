from django.db import models

class Material(models.Model):
    """Model for raw materials used in disinfectant production."""
    name = models.CharField(max_length=100)
    quantity_in_stock = models.FloatField(default=0.0)  # Quantity in stock (liters, grams, etc.)
    unit = models.CharField(max_length=50)  # e.g. 'grams', 'liters'

    def __str__(self):
        return self.name

    def update_stock(self, quantity):
        """Update the stock of this material."""
        self.quantity_in_stock += quantity
        self.save()

    @classmethod
    def create_or_update_material(cls, name, quantity, unit):
        """Create a new material or update an existing material."""
        material, created = cls.objects.get_or_create(name=name, defaults={'unit': unit})
        
        if not created:  # If the material already exists, update its stock
            material.quantity_in_stock += quantity
            material.save()
        
        return material

class Disinfectant(models.Model):
    """Model for disinfectants."""
    name = models.CharField(max_length=100)
    quantity_in_stock = models.FloatField(default=0.0)  # Disinfectant stock in liters or other units

    def __str__(self):
        return self.name

    def update_stock(self, quantity):
        """Update the stock of the disinfectant."""
        self.quantity_in_stock += quantity
        self.save()


class DisinfectantRecipe(models.Model):
    """Model for storing the recipe to create disinfectants."""
    disinfectant = models.ForeignKey(Disinfectant, related_name='recipes', on_delete=models.CASCADE)
    material = models.ForeignKey(Material, related_name='recipes', on_delete=models.CASCADE)
    quantity = models.FloatField()  # Amount of material required to produce a specific quantity of disinfectant

    def __str__(self):
        return f'{self.material.name} for {self.disinfectant.name}'
    
    def adjust_stock(self, disinfectant_quantity):
        """Adjust material stock based on the required amount for disinfectant production."""
        material_needed = self.quantity * disinfectant_quantity
        self.material.update_stock(material_needed)
