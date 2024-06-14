from django.core.management.base import BaseCommand
from faker import Faker

from customer.models import Customer

class Command(BaseCommand):
    help = 'Generate fake data'
    
    def handle(self, *args, **options):
        fake = Faker()
        
        for _ in range(10):
            Customer.objects.create(
                name = fake.last_name(),
                surname = fake.first_name(),
                contact = fake.phone_number(),
                address = fake.address(),
                email = fake.email(),
                password = fake.password()  
            )
            
        self.stdout.write(self.style.SUCCESS('Fake data generated successfully.'))