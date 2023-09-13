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

This Django application is designed for **comparing prices between different stores, helping users find the best
deals on various products**. The project provides a **user-friendly interface** to browse products across different
categories and view price variations among stores.

Users can **search for specific products or explore product categories to compare prices and make informed purchasing
decisions**. The application also **allows users to view detailed information about each product**, including store
details, enabling them to choose the most convenient or preferred store for their purchase.

**The project aims to simplify the process of comparing prices across multiple stores, saving users time and effort in
finding the best price for their desired products**. With the ability to browse by category and access detailed product
and store information, **users can easily identify the most competitive prices and make cost-effective purchasing
choices**.

Overall, this application provides a valuable tool for consumers to find the most favorable prices and maximize their
savings while shopping across different stores for a wide range of products.

> #### The project was created for educational purposes, simulating fictitious products without real value.

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

* **REST API**
* **Domain Driven Development**
* **JWT Authentication**
* **Postponed Tasks / Celery**
* **Authentication / Authorization**
* **Profile editing**
* **Email sending**
* **Documentation**
* **Tests (PyTest)**

</details>

<details><summary><h1>❕ Peculiarities</h1></summary>

### Abbreviations:
* **EV - EmailVerification**

</details>

<details><summary><h1>💽 Local installation</h1></summary>

1. #### Clone or download the repository.
2. #### Install dependencies: `poetry install`
3. #### Activate the Poetry virtual environment: `poetry shell`
4. #### Create an .env file or rename .env.dist in .env and populate it only with development variables:
    ![Env-Variables-Example](https://github.com/FCTL3314/StoreTracker-Backend/assets/97694131/c31d86db-7bec-4693-8e97-d649c6e7184f)
6. #### Run docker services for development: `docker-compose -f docker/local/docker-compose.yml up`
7. #### Run the development server: `python manage.py runserver`

</details>

<details><summary><h1>⚒️ Testing</h1></summary>

1. #### Complete all the steps in the 💽 Local installation section
2. #### Run tests: `pytest .`

</details>

<details><summary><h1>🪝 Pre-Commit hooks</h1></summary>

1. #### Install: `pre-commit install`
2. #### Test run: `pre-commit run --all-files`

</details>
