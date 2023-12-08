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

![firefox_89ntFwe2qN](https://github.com/FCTL3314/HealthNutrition-Frontend/assets/97694131/748ea2d3-2cc8-41a3-af5a-855787450024)
![firefox_4sltM6iRvZ](https://github.com/FCTL3314/HealthNutrition-Frontend/assets/97694131/62c3826e-e53d-4066-a305-474149bf81af)
![firefox_Ui60DrToDM](https://github.com/FCTL3314/HealthNutrition-Frontend/assets/97694131/b5d102b1-fc6c-4d5d-86fe-831947e25e58)

### Products

![firefox_5LqGCmMgpA](https://github.com/FCTL3314/HealthNutrition-Frontend/assets/97694131/4e5531ef-c7e6-4f05-b06b-da02661c1379)
![firefox_UOP9nrGu5s](https://github.com/FCTL3314/HealthNutrition-Frontend/assets/97694131/937136b1-1537-434b-ac84-8a705816c750)

### Save product modal

![firefox_69VGlA02Db](https://github.com/FCTL3314/HealthNutrition-Frontend/assets/97694131/55ba0d9e-c62d-4b1b-b10d-49c02004f678)

### Product detail

![firefox_EuQFeLE3Tz](https://github.com/FCTL3314/HealthNutrition-Frontend/assets/97694131/07fe7e82-7b29-4277-bf86-5a017f85f8b8)

### Comparison groups

![firefox_TzlDDf9Q1R](https://github.com/FCTL3314/HealthNutrition-Frontend/assets/97694131/67d52cbd-1266-4779-943b-4adcc029b3a5)

### Compared products

![firefox_OZk2yk3Pz0](https://github.com/FCTL3314/HealthNutrition-Frontend/assets/97694131/cb4fd4e8-3e16-4cfe-91ee-6a1ce51d551c)
![firefox_1OJModVCH4](https://github.com/FCTL3314/HealthNutrition-Frontend/assets/97694131/e7d18175-5a8d-41d4-af8d-c57982ab4482)

### Profile

![firefox_sapn5yfi3E](https://github.com/FCTL3314/HealthNutrition-Frontend/assets/97694131/a85d43e6-29e0-4523-81d3-d591704f7fbc)
![firefox_zaaLzBXq5O](https://github.com/FCTL3314/HealthNutrition-Frontend/assets/97694131/d9a72a6f-ae5b-486f-a701-8403c8f7dba5)

### Settings

![firefox_TwCMDgqiKa](https://github.com/FCTL3314/HealthNutrition-Frontend/assets/97694131/0cb08f01-3266-4942-938b-cf75354d1049)

### Authorization

![firefox_XHWRWg7xE2](https://github.com/FCTL3314/HealthNutrition-Frontend/assets/97694131/6457e274-f0da-4366-a9db-54c7a8bc0335)
![firefox_7hsuTyXEhp](https://github.com/FCTL3314/HealthNutrition-Frontend/assets/97694131/e538d3aa-5f9b-4aae-99e0-87091377417f)

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
