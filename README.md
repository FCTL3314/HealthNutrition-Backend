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

This Django application provides a **comprehensive API** for **comparing nutritional values of food products**, aiding users in **making informed dietary decisions**.

This API empowers developers to integrate **nutritional comparison functionality** into various applications, enabling users to **search for food items**, **explore nutritional categories**, **view detailed product information**, and ultimately **make health-conscious dietary choices**. It simplifies the process of **comparing nutritional values across different food items**, enhancing the user's experience with meal planning and supporting them in **achieving their nutritional goals**.

> #### The project was created for educational purposes, simulating fictitious products without real value.
> #### Frontend part: https://github.com/FCTL3314/StoreTracker-Frontend

</details>

<details><summary><h1>🌄 Demonstration</h1></summary>

### Product categories

![firefox_10jaBILjcl](https://github.com/FCTL3314/HealthNutrition-Frontend/assets/97694131/539d90ea-aea4-40aa-b18b-fa13e615dbb8)
![firefox_QmlP2aM3dD](https://github.com/FCTL3314/HealthNutrition-Frontend/assets/97694131/f8d05cce-5882-4d80-ba48-ec160446e4cf)

### Products

![firefox_6f5Tdgr0ay](https://github.com/FCTL3314/HealthNutrition-Frontend/assets/97694131/f46c558a-416a-4123-848d-9e3e0e88e46d)
![firefox_Olg88utAbr](https://github.com/FCTL3314/HealthNutrition-Frontend/assets/97694131/fc35ae0d-a3f7-4e23-8645-d9e2fee139ef)

### Product detail

![firefox_QwTKm3VfCH](https://github.com/FCTL3314/HealthNutrition-Frontend/assets/97694131/74a0ab94-f09e-4109-94c5-a58d0c3bf9e3)

### Profile

![firefox_CQq7BE99mp](https://github.com/FCTL3314/HealthNutrition-Frontend/assets/97694131/2ca3a7d0-5ada-4bf2-b1f7-ded73de191a1)

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
