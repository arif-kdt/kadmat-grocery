# Kadmat Island Grocery Booking System

A web-based grocery booking system built for Kadmat Island, Lakshadweep. During monsoon season when ship supplies are limited, residents can pre-book groceries from local shops before stock runs out.

## 🌊 The Problem

Kadmat Island receives groceries only when ships arrive from Kochi, Calicut, and Mangalore. During monsoon season, supplies are unpredictable. This system lets customers pre-book groceries from local shops so sellers can plan their stock and customers are guaranteed their items.

## 🚀 Live Demo

Coming soon — deploying to Railway

## 🛠 Tech Stack

- **Backend:** Python, Django 6
- **Frontend:** HTML5, Bootstrap 5.3, Bootstrap Icons
- **Database:** SQLite (development)
- **Authentication:** Django built-in sessions

## 👥 Three User Roles

| Role | Capabilities |
|---|---|
| **Admin** | Manage product catalogue, view all users/shops/orders |
| **Seller** | Manage shop inventory, confirm/pack/complete orders |
| **Customer** | Browse shops, add to cart, place and track orders |

## 📦 Order Flow

```
Customer places order → Pending
Seller reviews & selects available items → Confirmed
Seller packs items → Ready for Pickup
Customer collects → Collected
```

## ⚙️ Local Setup

```bash
git clone https://github.com/arif-kdt/kadmat-grocery.git
cd kadmat-grocery
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Create .env file
echo SECRET_KEY=your-secret-key > .env
echo DEBUG=True >> .env
echo ALLOWED_HOSTS=localhost,127.0.0.1 >> .env

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## 🗂 Project Structure

```
kadmat-grocery/
├── accounts/      # User registration, login, roles
├── products/      # Base product catalogue (admin managed)
├── shops/         # Shop management, seller inventory
├── orders/        # Cart, orders, order items
├── dashboard/     # Admin overview dashboard
└── templates/     # All HTML templates
```

## 🔮 Planned

- Version 4: Flutter mobile app + Django REST API
- Push notifications when order status changes
- SMS alerts for island residents without smartphones