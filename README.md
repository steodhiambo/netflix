# NetFix - Service Marketplace Platform

NetFix is a Django-based web application that connects customers with service providers. It's a marketplace where companies can offer their services and customers can request them.

## Features

### User Types
- **Customers**: Can browse and request services
- **Companies**: Can create and manage services

### Core Functionality
- User registration and authentication (email-based login)
- Service creation and management
- Service request system
- Profile pages for both customers and companies
- Service categorization by field
- Most requested services tracking

### Service Categories
- Air Conditioner
- Carpentry
- Electricity
- Gardening
- Home Machines
- Housekeeping
- Interior Design
- Locks
- Painting
- Plumbing
- Water Heaters

## Installation

### Prerequisites
- Python 3.8+
- Django 3.1.14

### Setup
1. Clone the repository:
```bash
git clone https://github.com/steodhiambo/netflix.git
cd netfix
```

2. Install Django:
```bash
pip install Django==3.1.14
```

3. Run migrations:
```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

4. Create a superuser (optional):
```bash
python3 manage.py createsuperuser
```

5. Populate with sample data (optional):
```bash
python3 manage.py populate_db
```

6. Activate the virtual environment:
```bash
source venv/bin/activate
```

7. Run the development server:
```bash
python3 manage.py runserver
```

8. Visit `http://127.0.0.1:8000` in your browser

## Usage

### For Customers
1. Register as a customer with email, username, password, and date of birth
2. Browse available services by category or view all services
3. Request services by providing address and required service time
4. View your service request history on your profile page

### For Companies
1. Register as a company with email, username, password, and field of work
2. Create services in your field (or any field if you're "All in One")
3. Manage your services from your profile page
4. View service requests from customers

### Navigation
- **Home**: Shows most popular services and platform overview
- **Services**: Browse all services or by category
- **Most Requested**: View services ordered by popularity
- **Profile**: View user information and service history
- **Login/Register**: User authentication

## Project Structure

```
netfix/
├── main/                   # Main app (home, navigation)
├── users/                  # User management (customers, companies)
├── services/              # Service management
├── static/                # CSS and static files
├── manage.py             # Django management script
└── netfix/               # Project settings
```

## Models

### User
- Custom user model with email-based authentication
- Boolean flags for customer/company type

### Customer
- Links to User model
- Stores date of birth

### Company
- Links to User model
- Stores field of work

### Service
- Created by companies
- Has name, description, price per hour, field, and creation date

### ServiceRequest
- Links customers to services
- Stores address, service time, calculated price, and request date

## Testing

Activate the virtual environment and run the included test script:
```bash
source venv/bin/activate
python3 test_functionality.py
```

## Admin Interface

Access the admin interface at `http://127.0.0.1:8000/admin/` to manage:
- Users, Customers, and Companies
- Services and Service Requests

## Development Notes

- Built with Django 3.1.14
- Uses virtual environment (venv) for dependency management
- Uses SQLite database (default)
- Supports both username and email-based authentication
- Responsive design with custom CSS and modern UI
- Form validation for unique emails and usernames
- Horizontal ratings display with enhanced styling

## Future Enhancements

Potential features to add:
- Rating system for services
- Pagination for service lists
- Search functionality
- Email notifications
- Payment integration
- Service completion tracking
