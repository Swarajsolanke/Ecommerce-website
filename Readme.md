# 🛒 Django Ecommerce Website

![Django](https://img.shields.io/badge/Django-5.0-green?logo=django)
![License](https://img.shields.io/badge/License-MIT-blue.svg)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

Welcome to **ShopCart** – a modern, full-featured ecommerce web application built with Django! 🚀

---

<p align="center">
  <img src="https://img.icons8.com/color/96/000000/shopping-cart--v2.png" width="100" alt="ShopCart Logo"/>
</p>

---

## ✨ Features

- 🔐 **User Authentication**: Sign up, sign in, sign out, password reset, and profile management.
- 🛍️ **Product Catalog**: Browse, search, and filter products by category.
- 🛒 **Cart Management**: Add to cart, update quantities, and checkout.
- 💖 **Wishlist**: Save your favorite products for later.
- 📦 **Order Placement**: Place orders and view your order history.
- 👤 **Profile Page**: Edit profile, change/reset password, and view quick stats.
- 🛠️ **Admin Panel**: Manage products, categories, carts, and wishlists.
- 📱 **Responsive UI**: Clean, modern, and mobile-friendly interface.

---

## 🖼️ Screenshots

<p align="center">
  <img src="https://user-images.githubusercontent.com/placeholder/homepage.png" width="700" alt="Homepage Screenshot"/>
  <br/>
  <img src="https://user-images.githubusercontent.com/placeholder/products.png" width="700" alt="Products Screenshot"/>
  <br/>
  <img src="https://user-images.githubusercontent.com/placeholder/cart.png" width="700" alt="Cart Screenshot"/>
</p>

> _Replace the above image URLs with your actual screenshots for a more personalized README!_

---

## 🏗️ Project Structure

```text
ecommerce/
├── db.sqlite3
├── ecommerce/
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── manage.py
└── store/
    ├── admin.py
    ├── models.py
    ├── views.py
    ├── urls.py
    ├── templates/
    ├── static/
    └── ...
```

---

## ⚡ Quick Start

1. **Clone the Repository**
    ```bash
    git clone <your-repo-url>
    cd ecommerce
    ```
2. **Create a Virtual Environment**
    ```bash
    python -m venv venv
    # On Windows:
    venv\Scripts\activate
    # On Mac/Linux:
    source venv/bin/activate
    ```
3. **Install Dependencies**
    ```bash
    pip install django
    ```
4. **Apply Migrations**
    ```bash
    python manage.py migrate
    ```
5. **Create a Superuser**
    ```bash
    python manage.py createsuperuser
    ```
6. **Run the Server**
    ```bash
    python manage.py runserver
    ```
7. **Visit** [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

---

## 📝 Usage

- **Home**: View featured products and navigate to the catalog.
- **Products**: Browse, search, and filter products.
- **Cart**: Add/remove products, update quantities, and checkout.
- **Wishlist**: Save products for later.
- **Orders**: View your order history.
- **Profile**: Manage your account and password.
- **Admin**: `/admin/` for product/category management.

---

## 📂 Static & Media Files

- Static files (CSS, images): `store/static/`
- Product images: `store/static/images/`

---

## 🙌 Credits

- Built with [Django](https://www.djangoproject.com/)
- UI inspired by modern ecommerce platforms
- Icons by [Icons8](https://icons8.com/)

---

## 📄 License

This project is for educational/demo purposes.

---

<p align="center">
  <b>Happy Shopping! 🛒</b>
</p>
