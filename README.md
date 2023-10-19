# 📖 Table of contents

[![Python](https://img.shields.io/badge/Python-3.11.2-3777A7?style=flat-square)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.2.1-103E2E?style=flat-square)](https://www.djangoproject.com/)
[![Rest-framework](https://img.shields.io/badge/Rest--framework-3.14.0-7F2D2D?style=flat-square)](https://www.django-rest-framework.org/)
[![Poetry](https://img.shields.io/badge/Poetry-1.5.1-0992E1?style=flat-square)](https://python-poetry.org/)
[![Pytest](https://img.shields.io/badge/Pytest-Passed-2dad3f?style=flat-square)](https://docs.pytest.org/en/7.4.x/)
[![Black](https://img.shields.io/badge/Style-Black-black?style=flat-square)](https://black.readthedocs.io/en/stable/)

<ul>
  <li>
    <b>
      <a href="#-description">Description</a>
    </b>
  </li>

  <li>
    <b>
      <a href="#-endpoints">Endpoints</a>
    </b>
  </li>
  
  <li>
    <b>
      <a href="#-demonstration">Demonstration</a>
    </b>
  </li>
  
  <li>
    <b>
      <a href="#-features">Features</a>
    </b>
  </li>
  
  <li>
    <b>
      <a href="#-local-installation">Local installation</a>
    </b>
  </li>
  
  <li>
    <b>
      <a href="#-pre-commit-hooks">Pre-Commit hooks</a>
    </b>
  </li>
</ul>

<details open><summary><h1>📃 Description</h1></summary>

This Django application provides a **comprehensive API** for **comparing prices across various stores** and helping users **make informed purchasing decisions**.

This API **empowers developers to integrate the price comparison functionality into various applications**, enabling users to **search for products**, **explore categories**, **view detailed product information**, and ultimately make **cost-effective purchasing choices**. It **simplifies the process of comparing prices across multiple stores**, **enhancing the user's shopping experience** and **helping them maximize their savings**.

> #### The project was created for educational purposes, simulating fictitious products without real value.
> #### Frontend part: https://github.com/FCTL3314/StoreTracker-Frontend

</details>

<details><summary><h1>🪄 Endpoints</h1></summary>

1. **Category Information**:
   - `GET /products/product-types/{slug}/`: Detailed information about a specific product category by its slug.
   - `GET /products/product-types/`: A list of product categories.

2. **Product Information**:
   - `GET /products/{product_slug}/`: Detailed information about a specific product by its slug.
   - `GET /products/`: A list of products with the ability to filter by product category.

3. **Product comparisons**:
   - `GET /comparisons/products/{product_type_slug}/`: A list of user-compared product categories.
   - `GET /comparisons/product-types/`: A list of user-compared categories.

   - `POST /comparisons/add/{prodict_id}/`: Adds a product to the user's comparisons.
   - `DELETE /comparisons/remove/{prodict_id}/`: Removes a product from the user's comparisons.
  
4. **Comments Management**:
   - `POST /comments/product/add/{product_id}/`: Adds a comment to a product.
   - `DELETE /comments/product/remove/{product_id}/`: Removes a product comment.
   - `GET /comments/product-list?product_id=`: A list of a product comments.

   - `POST /comments/store/add/{store_id}/`: Adds a comment to a store.
   - `DELETE /comments/store/remove/{store_id}/`: Removes a store comment.
   - `GET /comments/store-list?store_id=`: A list of a store comments.
  
5. **Email verification**:
   -  `POST /users/verification/send/`: Sends a verification email to the currently authenticated user.
   -  `POST /users/verification/verify/`: Verify the currently authenticated user if the verification code is correct.

6. **User Management**:
   - `POST /token/`: Obtain an authentication token.
   - `POST /token/refresh/`: Refresh an authentication token to extend its validity.
   - `POST /users/`: Register a new user.
   - `GET /users/me/`: Retrieve information about the currently authenticated user.
   - `PATCH /users/me/`: Update user information.
   - `POST /users/change-email/`: Change the email address of the currently authenticated user.
   - `GET /users/{user_slug}/`: Retrieve information about a specific user by its slug.

7. **Password reset**:
   - `POST /users/reset_password/`: Sends an email to reset the currently authenticated user's password.
   - `POST /users/reset_password_confirm/`: Resets the currently authenticated user's password.

</details>

<details><summary><h1>🌄 Demonstration</h1></summary>

### Product categories

![firefox_pX9TIczsd0](https://github.com/FCTL3314/StoreTracker/assets/97694131/0a317d57-0ede-492e-96f6-ec11aa65ab57)

### Products

![firefox_bqUjAA9ide](https://github.com/FCTL3314/StoreTracker/assets/97694131/fd7127c4-67b4-4e47-9255-484a135c6564)
![firefox_2dl7DEif7Y](https://github.com/FCTL3314/StoreTracker/assets/97694131/b65f226a-31af-4d84-8cf9-cc7682174a99)
![firefox_WxEaOrMs8h](https://github.com/FCTL3314/StoreTracker/assets/97694131/6f451ff2-662e-4295-a82e-ab3cdaad8be5)

<hr/>

![firefox_layhXd2u7v](https://github.com/FCTL3314/StoreTracker/assets/97694131/5d1de7aa-ec12-445a-a29d-1d27108d793d)
![firefox_Bgqw3rnQv3](https://github.com/FCTL3314/StoreTracker/assets/97694131/cd68ed5b-86fd-484e-b8ad-aadef8fd6136)

### Store detail

![firefox_SGbt1I9nCi](https://github.com/FCTL3314/StoreTracker/assets/97694131/f31c0e2f-2ebb-422a-943a-55072dab0530)
![firefox_Qw2Pyi34hz](https://github.com/FCTL3314/StoreTracker/assets/97694131/7ee295c8-fcf6-489f-ad57-68a55a298030)

### Profile

![firefox_4HtesbsbBG](https://github.com/FCTL3314/StoreTracker/assets/97694131/7e404765-9adf-4505-b8d2-302eb7952e53)
![firefox_IRjbXLaWtk](https://github.com/FCTL3314/StoreTracker/assets/97694131/99094345-4b41-4acc-b5c4-247e17031c0b)

</details>

<details><summary><h1>🔥 Features</h1></summary>

* **RESTful API**
* **Domain Driven Design**
* **CI/CD**
* **Celery / Postponed Tasks**
* **Email sending**
* **JWT Authentication / Authorization**
* **Code Documentation**
* **Tests (PyTest)**

</details>

<details><summary><h1>❕ Peculiarities</h1></summary>

### Architecture:
  * Project services are divided into 2 levels:
    * **Domain** -  Services that are in no way dependent on the current infrastructure, that is, the framework.
    * **Infrastructure** - Services that can call domain services and interact with the project infrastructure.
### Abbreviations:
* **EV - EmailVerification**

</details>

<details><summary><h1>💽 Local installation</h1></summary>

1. #### Clone or download the repository.
2. #### Activate the Poetry virtual environment: `poetry shell`
3. #### Install dependencies: `poetry install`
4. #### Create an .env file or rename .env.dist in .env and populate it only with development variables:
    ![Env-Variables-Example](https://github.com/FCTL3314/StoreTracker-Backend/assets/97694131/c31d86db-7bec-4693-8e97-d649c6e7184f)
5. #### Run docker services for development: `docker-compose -f docker/local/docker-compose.yml up`
6. #### Apply migrations: `python manage.py makemigrations` and `python manage.py migrate`
7. #### Run the development server: `python manage.py runserver`

</details>

<details><summary><h1>⚒️ Testing</h1></summary>

1. #### Complete all the steps in the 💽 Local installation section
2. #### Run tests: `pytest .`

</details>

<details><summary><h1>🪝 Pre-Commit hooks</h1></summary>

1. #### Install: `pre-commit install`
2. #### Check: `pre-commit run --all-files`

</details>
