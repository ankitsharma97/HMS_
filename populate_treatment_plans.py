import os
import django

# Set up Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HMS.settings')  # Replace 'HMS.settings' with your project name
django.setup()

from main.models import TreatmentPlan  # Replace 'main' with the name of your app

def populate_treatment_plans():
    treatments = [
        {
            'name': 'Initial Phase WHO Standard Therapy',
            'description': 'Treatment plan according to WHO guidelines, focusing on the initial phase of therapy for Buruli ulcer.',
            'antibiotic_names': 'Rifampicin, Streptomycin',
        },
        {
            'name': 'Alternative Regimen for Contraindications',
            'description': 'Extended antibiotic therapy including alternative regimens for patients with contraindications to first-line drugs.',
            'antibiotic_names': 'Clarithromycin, Moxifloxacin',
        },
        {
            'name': 'Severe Case Combination Therapy',
            'description': 'Combination therapy for severe cases of Buruli ulcer, targeting resistant strains of Mycobacterium ulcerans.',
            'antibiotic_names': 'Rifampicin, Clarithromycin, Moxifloxacin',
        },
        {
            'name': 'Post-operative Recurrence Prevention Therapy',
            'description': 'Post-operative antibiotic treatment to prevent recurrence of Buruli ulcer after surgical intervention.',
            'antibiotic_names': 'Rifampicin, Streptomycin, Clarithromycin',
        },
        {
            'name': 'Supportive Therapy for Concurrent Infections',
            'description': 'Supportive therapy with antibiotics in patients with concurrent infections or complications.',
            'antibiotic_names': 'Rifampicin, Moxifloxacin',
        },
        {
            'name': 'Final Phase Recovery and Relapse Prevention',
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
        print(f'Successfully added {treatment["name"]}')

if __name__ == '__main__':
    populate_treatment_plans()
