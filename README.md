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

This Django application provides a **comprehensive API** for **comparing nutritional values of food products**, aiding users in **making informed dietary decisions**.

This API empowers developers to integrate **nutritional comparison functionality** into various applications, enabling users to **search for food items**, **explore nutritional categories**, **view detailed product information**, and ultimately **make health-conscious dietary choices**. It simplifies the process of **comparing nutritional values across different food items**, enhancing the user's experience with meal planning and supporting them in **achieving their nutritional goals**.

> #### The project was created for educational purposes, simulating fictitious products without real value.
> #### Frontend part: https://github.com/FCTL3314/StoreTracker-Frontend

</details>

<details><summary><h1>🌄 Demonstration</h1></summary>

### Product categories

![firefox_JWbM1HN5xz](https://github.com/FCTL3314/HealthNutrition-Frontend/assets/97694131/68e1b64e-5661-4db0-abb6-ec3fe24d37b0)
![firefox_4F10GQVCyO](https://github.com/FCTL3314/HealthNutrition-Frontend/assets/97694131/bcb573d5-348c-48b2-b624-dc80ead722e8)
![firefox_3mMFuAopuz](https://github.com/FCTL3314/HealthNutrition-Frontend/assets/97694131/afc7a7bc-5508-45dd-95bd-5db4efb7da8b)

### Products

![firefox_B7uNa9vFMV](https://github.com/FCTL3314/HealthNutrition-Frontend/assets/97694131/3a5f76a1-3441-445c-8b33-78eed2ea7733)

### Product detail

![firefox_POkjZJpu1b](https://github.com/FCTL3314/HealthNutrition-Frontend/assets/97694131/9b7af03e-875a-41e7-9ce7-f81c000f9dc3)

### Profile

![firefox_HWOgotnpVP](https://github.com/FCTL3314/HealthNutrition-Frontend/assets/97694131/a444a1ef-0eae-4926-823a-6d6d148b868d)


### Settings

![firefox_pQOdHvUkf6](https://github.com/FCTL3314/HealthNutrition-Frontend/assets/97694131/cdcf18b1-af67-4fdf-9558-0d68d4bb97ab)

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
