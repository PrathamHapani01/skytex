# Sky Tex Fabric Store - Dynamic Backend

A full-stack fabric store application with FastAPI backend, PostgreSQL database, and static frontend.

## Tech Stack

- **Backend**: FastAPI, SQLAlchemy, PostgreSQL
- **Frontend**: HTML, CSS, Vanilla JavaScript
- **Authentication**: JWT (JSON Web Tokens)
- **Containerization**: Docker, Docker Compose

## Features

- Product catalog with filtering (material, colour, price)
- Product detail pages with specifications
- Bestsellers showcase
- Contact form submission
- Admin panel with JWT authentication
- CRUD operations for products
- Contact message management

## Project Structure

```
skytex/
├── backend/
│   ├── main.py           # FastAPI application
│   ├── models.py         # SQLAlchemy models
│   ├── database.py       # Database connection
│   ├── auth.py           # JWT authentication
│   ├── api.py            # Public API endpoints
│   ├── admin.py          # Admin API endpoints
│   ├── seed.py           # Database seeding
│   ├── requirements.txt  # Python dependencies
│   ├── Dockerfile        # Backend Docker config
│   └── .env             # Environment variables
├── admin.html           # Admin panel
├── index.html           # Homepage
├── shop.html            # Product catalog
├── product.html         # Product details
├── contact.html         # Contact form
├── about.html           # About page
├── css/                 # Stylesheets
├── js/                  # JavaScript files
├── assets/              # Images and static assets
├── docker-compose.yml   # Docker Compose configuration
└── .gitignore          # Git ignore rules
```

## Database Models

### Product
- id, name, description, price, material, colour, stock
- images (JSON array)
- specifications (JSON object)
- is_bestseller (boolean)

### Contact
- id, name, phone, email, subject, message, created_at

### Admin
- id, username, hashed_password

## API Endpoints

### Public Endpoints
- `GET /api/products` - Get all products with optional filters
- `GET /api/products/{id}` - Get single product by ID
- `GET /api/bestsellers` - Get top 4 bestseller products
- `GET /api/reviews` - Get static reviews
- `POST /api/contact` - Submit contact form

### Admin Endpoints (JWT Auth Required)
- `POST /api/admin/login` - Admin login, returns JWT token
- `GET /api/admin/products` - Get all products
- `POST /api/admin/products` - Create new product
- `GET /api/admin/products/{id}` - Get single product
- `PUT /api/admin/products/{id}` - Update product
- `DELETE /api/admin/products/{id}` - Delete product
- `GET /api/admin/contacts` - Get all contact messages

## Setup Instructions

### Using Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd skytex
   ```

2. **Set environment variables**
   ```bash
   # Edit backend/.env and set your DB_PASSWORD
   DB_PASSWORD=your_secure_password
   ```

3. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

4. **Access the application**
   - Frontend: http://localhost:8000/index.html
   - Admin Panel: http://localhost:8000/admin.html
   - API Docs: http://localhost:8000/docs

### Default Admin Credentials
- Username: `admin`
- Password: `admin123`

**Important**: Change the default admin password after first login by updating the database directly or modifying the seed script.

### Manual Setup (Without Docker)

1. **Install Python dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Set up PostgreSQL database**
   ```sql
   CREATE DATABASE skytex;
   CREATE USER admin WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE skytex TO admin;
   ```

3. **Configure environment variables**
   ```bash
   # In backend/.env
   DATABASE_URL=postgresql://admin:your_password@localhost:5432/skytex
   SECRET_KEY=your-secret-key-change-this-in-production
   ```

4. **Run seed script**
   ```bash
   python seed.py
   ```

5. **Start the FastAPI server**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

## Development

### Adding New Products

1. Access the admin panel at `/admin.html`
2. Login with admin credentials
3. Click "Add New Product"
4. Fill in the product details
5. Images should be comma-separated URLs
6. Specifications should be in JSON format

### Managing Contact Messages

1. Access the admin panel
2. Navigate to the "Contact Messages" tab
3. View all submitted contact forms

## Frontend Updates

The frontend has been updated to use API calls instead of static data:
- `shop.html` - Loads products from API with filtering
- `product.html` - Loads product details from API
- `index.html` - Loads bestsellers from API
- `contact.html` - Submits contact form to API

Error handling and loading states have been added for better user experience.

## Security Notes

1. Change the default admin password immediately
2. Update the `SECRET_KEY` in `.env` for production
3. Use strong database passwords
4. Enable HTTPS in production
5. Consider adding rate limiting to API endpoints

## Troubleshooting

### Database Connection Issues
- Ensure PostgreSQL is running
- Check DATABASE_URL in .env
- Verify database credentials

### Docker Issues
- Run `docker-compose down` to stop containers
- Run `docker-compose up --build --force-recreate` to rebuild
- Check Docker logs: `docker-compose logs`

### API Not Responding
- Check if backend service is running
- Verify port 8000 is not in use
- Check backend logs for errors

## License

© 2026 Sky Tex Textile Atelier. All rights reserved.
