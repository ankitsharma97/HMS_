from django.core.management.base import BaseCommand
from .models import TreatmentPlan  # Replace 'your_app' with the name of your app

class Command(BaseCommand):
    help = 'Populate the TreatmentPlan model with initial data'

    def handle(self, *args, **kwargs):
        treatments = [
            {
                'name': 'ANNEX 1',
                'description': 'Treatment plan according to WHO guidelines, focusing on the initial phase of therapy for Buruli ulcer.',
                'antibiotic_names': 'Rifampicin, Streptomycin',
            },
            {
                'name': 'ANNEX 2',
                'description': 'Extended antibiotic therapy including alternative regimens for patients with contraindications to first-line drugs.',
                'antibiotic_names': 'Clarithromycin, Moxifloxacin',
            },
            {
                'name': 'ANNEX 3',
                'description': 'Combination therapy for severe cases of Buruli ulcer, targeting resistant strains of Mycobacterium ulcerans.',
                'antibiotic_names': 'Rifampicin, Clarithromycin, Moxifloxacin',
            },
            {
                'name': 'ANNEX 4',
                'description': 'Post-operative antibiotic treatment to prevent recurrence of Buruli ulcer after surgical intervention.',
                'antibiotic_names': 'Rifampicin, Streptomycin, Clarithromycin',
            },
            {
                'name': 'ANNEX 5',
                'description': 'Supportive therapy with antibiotics in patients with concurrent infections or complications.',
                'antibiotic_names': 'Rifampicin, Moxifloxacin',
            },
            {
                'name': 'ANNEX 6',
                'description': 'Final phase of treatment, focusing on minimizing the risk of relapse and ensuring complete recovery.',
                'antibiotic_names': 'Streptomycin, Clarithromycin',
            },
        ]

        for treatment in treatments:
            TreatmentPlan.objects.create(
                name=treatment['name'],
                description=treatment['description'],
                antibiotic_names=treatment['antibiotic_names']
            )
            self.stdout.write(self.style.SUCCESS(f'Successfully added {treatment["name"]}'))

