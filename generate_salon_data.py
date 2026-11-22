import pandas as pd
import numpy as np
import datetime

np.random.seed(42)

# 1. Outlet Information (22 outlets in Coimbatore)
coimbatore_locations = [
    "RS Puram", "Gandhipuram", "Saibaba Colony", "Peelamedu", "Avinashi Road",
    "Race Course", "Town Hall", "Ramanathapuram", "Singanallur", "Ukkadam",
    "Vadavalli", "Kovaipudur", "Kuniyamuthur", "Thudiyalur", "Saravanampatti",
    "Ganapathy", "SITra", "PN Pudur", "Velandipalayam", "Tatabad", 
    "Ondipudur", "Irugur"
]

outlets = []
for i, loc in enumerate(coimbatore_locations, start=1):
    outlets.append({
        'outlet_id': f'OUT_{i:02d}',
        'outlet_name': f'Lush & Glow - {loc}',
        'city': 'Coimbatore',
        'staff_count': np.random.randint(8, 20),
        'established_year': np.random.randint(2015, 2024)
    })
df_outlets = pd.DataFrame(outlets)
df_outlets.to_csv('outlets.csv', index=False)

# 2. Stylist Information
stylists = []
stylist_id_counter = 1
for outlet in outlets:
    n_stylists = outlet['staff_count']
    for _ in range(n_stylists):
        stylists.append({
            'stylist_id': f'STY_{stylist_id_counter:03d}',
            'outlet_id': outlet['outlet_id'],
            'experience_years': np.random.randint(1, 10),
            'specialization': np.random.choice(['Hair', 'Skin', 'Spa', 'Bridal', 'General'])
        })
        stylist_id_counter += 1
df_stylists = pd.DataFrame(stylists)
df_stylists.to_csv('stylists_information.csv', index=False)

# 3. Client Records
n_clients = 15000
clients = []
for i in range(1, n_clients + 1):
    clients.append({
        'client_id': f'CLI_{i:05d}',
        'outlet_id': np.random.choice(df_outlets['outlet_id']),
        'signup_date': pd.date_range(start='2024-01-01', end='2025-10-31').to_pydatetime()[np.random.randint(0, 600)].strftime('%Y-%m-%d'),
        'membership_tier': np.random.choice(['Standard', 'Silver', 'Gold', 'Platinum'], p=[0.6, 0.2, 0.15, 0.05])
    })
df_clients = pd.DataFrame(clients)
df_clients.to_csv('client_records.csv', index=False)

# 4. Appointment Records & Service Transactions (with Messy Data)
appointments = []
service_transactions = []
# Create inconsistent naming
services_mapping = {
    'Haircut & Styling': ['Haircut & Styling', 'Hair Cut', 'Cut-Hair'],
    'Hair Coloring': ['Hair Coloring', 'Hair Colour', 'Coloring'],
    'Facial Clean-up': ['Facial Clean-up', 'Face Cleanup', 'Clean-up'],
    'Advanced Anti-Aging Facial': ['Advanced Anti-Aging Facial', 'Anti-Aging Facial'],
    'Full Body Spa': ['Full Body Spa', 'Spa'],
    'Bridal Makeup': ['Bridal Makeup', 'Bridal Make-up'],
    'Manicure/Pedicure': ['Manicure/Pedicure', 'Mani-Pedi'],
    'Keratin Treatment': ['Keratin Treatment', 'Keratin']
}

appt_id = 1
tx_id = 1
for _, client in df_clients.iterrows():
    n_appts = np.random.choice([1, 2, 3, 4, 5], p=[0.4, 0.3, 0.15, 0.1, 0.05])
    for _ in range(n_appts):
        appt_date = pd.date_range(start='2025-11-01', end='2025-11-30').to_pydatetime()[np.random.randint(0, 30)]
        outlet_stylists = df_stylists[df_stylists['outlet_id'] == client['outlet_id']]['stylist_id'].values
        chosen_stylist = np.random.choice(outlet_stylists) if len(outlet_stylists) > 0 else 'STY_001'
        
        # Introduce messiness: No-show sometimes recorded as cancellation
        status = np.random.choice(['Completed', 'No-Show', 'Cancelled'], p=[0.8, 0.1, 0.1])
        if status == 'No-Show' and np.random.rand() < 0.3:
            status = 'Cancelled'
            
        # Introduce messiness: Walk-ins without client IDs
        client_id = client['client_id']
        if np.random.rand() < 0.05:
            client_id = np.nan
        
        appointments.append({
            'appointment_id': f'APP_{appt_id:06d}',
            'client_id': client_id,
            'outlet_id': client['outlet_id'],
            'stylist_id': chosen_stylist,
            'appointment_date': appt_date.strftime('%Y-%m-%d'),
            'status': status
        })
        
        if status == 'Completed':
            n_services = np.random.choice([1, 2], p=[0.7, 0.3])
            chosen_services = np.random.choice(list(services_mapping.keys()), size=n_services, replace=False)
            for s_name in chosen_services:
                # Use inconsistent naming
                actual_name = np.random.choice(services_mapping[s_name])
                service_transactions.append({
                    'transaction_id': f'TX_{tx_id:07d}',
                    'appointment_id': f'APP_{appt_id:06d}',
                    'service_name': actual_name,
                    'service_price': 1000 # Simplified price for messy data test
                })
                tx_id += 1
        appt_id += 1

df_appointments = pd.DataFrame(appointments)
df_appointments.to_csv('appointment_records.csv', index=False)

df_services = pd.DataFrame(service_transactions)
df_services.to_csv('service_transactions.csv', index=False)

# 5. Product Sales
product_sales = []
products = [('Shampoo', 650), ('Conditioner', 700), ('Hair Serum', 1200), ('Face Moisturizer', 1500), ('Sunscreen', 900)]
for i in range(1, 4000):
    prod = products[np.random.randint(0, len(products))]
    client = df_clients.sample(1).iloc[0]
    product_sales.append({
        'sale_id': f'SALE_{i:05d}',
        'client_id': client['client_id'],
        'outlet_id': client['outlet_id'],
        'sale_date': pd.date_range(start='2025-11-01', end='2025-11-30').to_pydatetime()[np.random.randint(0, 30)].strftime('%Y-%m-%d'),
        'product_name': prod[0],
        'amount': prod[1]
    })
df_products = pd.DataFrame(product_sales)
df_products.to_csv('product_sales.csv', index=False)

# 6. Experiment Dataset & DiD Dataset (Current Experiment)
experiment_data = []
did_data = []

for _, client in df_clients.iterrows():
    group = np.random.choice(['control', 'treatment'])
    pre_rev = np.random.normal(2500, 500)
    
    # Treatment effect: AI recommendations increase RPV by ~10%
    if group == 'treatment':
        post_rev = pre_rev * np.random.normal(1.10, 0.05)
        no_show_prob = 0.08 # Better follow up
    else:
        post_rev = pre_rev * np.random.normal(1.01, 0.05)
        no_show_prob = 0.12
        
    experiment_data.append({
        'client_id': client['client_id'],
        'outlet_id': client['outlet_id'],
        'group': group,
        'pre_period_revenue': max(0, pre_rev),
        'post_period_revenue': max(0, post_rev),
        'visits_count': np.random.randint(1, 4),
        'no_show_count': np.random.binomial(3, no_show_prob)
    })
    
    # DiD format rows (Pre and Post for each client)
    did_data.append({
        'client_id': client['client_id'],
        'outlet_id': client['outlet_id'],
        'group': group,
        'time_period': 'pre',
        'revenue_per_visit': max(0, pre_rev)
    })
    did_data.append({
        'client_id': client['client_id'],
        'outlet_id': client['outlet_id'],
        'group': group,
        'time_period': 'post',
        'revenue_per_visit': max(0, post_rev)
    })

df_experiment = pd.DataFrame(experiment_data)
df_experiment.to_csv('experiment_dataset.csv', index=False)

df_did = pd.DataFrame(did_data)
df_did.to_csv('did_dataset.csv', index=False)

# 7. Separate Retrospective "Last Quarter" Dataset
# Change was implemented in "Region A" but not "Region B"
retro_data = []
outlets_list = df_outlets['outlet_id'].tolist()
region_a = outlets_list[:11]
region_b = outlets_list[11:]

for outlet in outlets_list:
    group = 'treatment' if outlet in region_a else 'control'
    for _ in range(500): # 500 clients per outlet
        pre_rev = np.random.normal(2400, 450)
        # Retrospective effect: ~5% uplift
        if group == 'treatment':
            post_rev = pre_rev * np.random.normal(1.05, 0.04)
        else:
            post_rev = pre_rev * np.random.normal(1.00, 0.04)
            
        retro_data.append({'outlet_id': outlet, 'group': group, 'period': 'pre', 'rpv': max(0, pre_rev)})
        retro_data.append({'outlet_id': outlet, 'group': group, 'period': 'post', 'rpv': max(0, post_rev)})

df_retro = pd.DataFrame(retro_data)
df_retro.to_csv('retrospective_dataset.csv', index=False)

print("All salon and spa datasets successfully generated with messy data and retrospective context!")
