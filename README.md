**A simple ticket booking system built using Django REST Framework. The project manages users, stations, and tickets with authenticated access, user-specific data visibility, and dynamic ticket price calculation.**

## Browsable API endpoint: 
```
api/
```
---

### Folder structure 
```
ticket_system/
│
├── manage.py
│
├── ticket_system/                # Project configuration
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py               # Django & DRF settings
│   ├── urls.py                   # Root URL configuration
│   └── wsgi.py
│
├── tickets/                      # Tickets application
│   ├── __init__.py
│   ├── admin.py                  # Admin registrations
│   ├── apps.py
│   ├── models.py                 # Station & Ticket models
│   ├── serializers.py            # DRF serializers
│   ├── views.py                  # ViewSets & APIs
│   ├── urls.py                   # App-level routing
│   ├── tests.py                  # Unit tests
│   │
│   ├── migrations/               # Database migrations
│   │   ├── __init__.py
│   │   └── 0001_initial.py
│   │
│   └── management/               # Custom Django commands
│       ├── __init__.py
│       └── commands/
│           ├── __init__.py
│           └── seed_data.py       # Faker-based data seeding
│
├── env/                           # Virtual environment (optional)
│
├── requirements.txt               # Project dependencies
│
└── README.md                      # Project documentation
```
