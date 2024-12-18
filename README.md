# Connect Agro

Connect Agro is a Django-based web application designed to connect producers and consumers in a marketplace setting. Producers can manage their own products, and consumers can browse producers, add products to their shopping carts, and make purchases. The application supports role-based functionality, ensuring that producers and consumers have distinct and seamless experiences.
This is the first concept of the app, for a real deploy it needs much more polishing and features.

## Features

### General Features
- User authentication (login, registration, and logout).
- Role-based access control:
  - **Producers** can manage their own products.
  - **Consumers** can view producers and purchase products.
- Responsive UI for seamless navigation.

### Producer Features
- Dedicated producer dashboard.
- CRUD operations for managing products.
- Ability to define product attributes such as name, price, quantity, and description.

### Consumer Features
- View a list of all producers.
- Browse products offered by individual producers.
- Add products to the shopping cart with specified quantities.
- Shopping cart management:
  - Products grouped by producers.
  - Ability to remove specific quantities from the cart.
  - Automatic recalculation of cart totals.

## Installation and Setup

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)
- Virtualenv (recommended)
- Git (optional for version control)

### Installation Steps
1. Clone the repository (if using Git):
   ```bash
   git clone https://github.com/your-username/connect-agro.git
   cd connect-agro
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install Django:
   ```bash
   pip install django
   ```

4. Apply database migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Run the development server:
   ```bash
   python manage.py runserver
   ```

6. Access the application at `http://localhost:8000` in your web browser.

## Usage

### User Roles
#### Producer
1. Log in with producer credentials.
2. Access the dashboard to manage your products.
3. Add, edit, or delete products as required.
4. Monitor product availability and prices.

#### Consumer
1. Log in with consumer credentials.
2. Browse the list of producers and their respective products.
3. Add products to the shopping cart with desired quantities.
4. View the shopping cart, grouped by producer, and manage items.

## Models and Key Relationships

### User Roles
- **User**: Standard Django `User` model extended via a `UserProfile` model to add roles (Producer, Consumer).

### Models
- **Product**:
  - Attributes: `name`, `description`, `price`, `quantity`, `created_by` (ForeignKey to Producer).
- **Cart**:
  - Attributes: `user` (ForeignKey to Consumer), `product` (ForeignKey to Product), `quantity`.

### Relationships
- A producer can have multiple products.
- A consumer can add multiple products from different producers to their cart.

## Key Endpoints

### General
- `/`: Home and Welcome page.
- `register/`: User registration page.
- `login/`: User login page.
- `logout/`: User logout action.

### Producer
- `producers/<username>/`: Dashboard for managing products of the specific producer.
- `products/add/`: Add a new product.

### Consumer
- `/producers/`: List of all producers.
- `/cart/`: View shopping cart grouped by producer.

## Business Logic

1. **User Registration**:
   - Role selection during registration (Producer or Consumer).
   - Automatically assigns producer permissions to manage products.

2. **Product Management**:
   - Producers can only manage products they created.

3. **Cart Management**:
   - Consumers can add products from multiple producers to their cart.
   - Products in the cart are grouped by producer for clarity.

4. **Stock Management**:
   - Adding products to the cart reduces available stock for producers.
   - Removing products from the cart restores stock availability.

## Future Enhancements
- Add styling
- Implement order placement and payment integration.
- Add filtering and search functionality for products.
- Enable real-time notifications for producers when their products are purchased.
- Integrate advanced analytics for producers to track sales.
