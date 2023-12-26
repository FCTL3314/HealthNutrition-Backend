<div align="center">
  <img width="148" height="148" src="https://github.com/FCTL3314/HealthNutrition-Backend/assets/97694131/8025cf3d-612d-4a30-bd69-e8bfcc5d5b2b"/>
  <h1>Health Nutrition - Backend</h1>
  <p>Django / DRF based app for comparing the nutritional value of products.</p>

  [![Python](https://img.shields.io/badge/Python-3.11.2-3777A7?style=flat-square)](https://www.python.org/)
  [![Django](https://img.shields.io/badge/Django-4.2.1-103E2E?style=flat-square)](https://www.djangoproject.com/)
  [![Rest-framework](https://img.shields.io/badge/Rest--framework-3.14.0-7F2D2D?style=flat-square)](https://www.django-rest-framework.org/)
  [![Poetry](https://img.shields.io/badge/Poetry-1.5.1-0992E1?style=flat-square)](https://python-poetry.org/)
  [![Pytest](https://img.shields.io/badge/Pytest-Passed-2dad3f?style=flat-square)](https://docs.pytest.org/en/7.4.x/)
  [![Black](https://img.shields.io/badge/Style-Black-black?style=flat-square)](https://black.readthedocs.io/en/stable/)

  <img src="https://github.com/FCTL3314/HealthNutrition-Frontend/assets/97694131/748ea2d3-2cc8-41a3-af5a-855787450024" style="width: 80%;"/>
</div>

# 📖 Table of contents

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

<img src="https://github.com/FCTL3314/HealthNutrition-Frontend/assets/97694131/748ea2d3-2cc8-41a3-af5a-855787450024" style="width: 49%;"/>
<img src="https://github.com/FCTL3314/HealthNutrition-Frontend/assets/97694131/62c3826e-e53d-4066-a305-474149bf81af" style="width: 49%;"/>
<img src="https://github.com/FCTL3314/HealthNutrition-Frontend/assets/97694131/b5d102b1-fc6c-4d5d-86fe-831947e25e58" style="width: 49%;"/>

### Products

<img src="https://github.com/FCTL3314/HealthNutrition-Frontend/assets/97694131/4e5531ef-c7e6-4f05-b06b-da02661c1379" style="width: 49%;"/>
<img src="https://github.com/FCTL3314/HealthNutrition-Frontend/assets/97694131/937136b1-1537-434b-ac84-8a705816c750" style="width: 49%;"/>
<img src="https://github.com/FCTL3314/HealthNutrition-Frontend/assets/97694131/9d5c5bbc-449b-4fee-ac40-a9cb0d326b7c" style="width: 49%;"/>

### Product detail

![firefox_EuQFeLE3Tz](https://github.com/FCTL3314/HealthNutrition-Frontend/assets/97694131/07fe7e82-7b29-4277-bf86-5a017f85f8b8)

### Comparison groups

![firefox_TzlDDf9Q1R](https://github.com/FCTL3314/HealthNutrition-Frontend/assets/97694131/67d52cbd-1266-4779-943b-4adcc029b3a5)

### Compared products

<img src="https://github.com/FCTL3314/HealthNutrition-Frontend/assets/97694131/02175a3a-6dfe-4691-87be-f79d5d70e656" style="width: 49%;"/>
<img src="https://github.com/FCTL3314/HealthNutrition-Frontend/assets/97694131/66e0b741-c51e-426c-92c0-95658df62db4" style="width: 49%;"/>

### Profile

<img src="https://github.com/FCTL3314/HealthNutrition-Frontend/assets/97694131/a85d43e6-29e0-4523-81d3-d591704f7fbc" style="width: 49%;"/>
<img src="https://github.com/FCTL3314/HealthNutrition-Frontend/assets/97694131/d9a72a6f-ae5b-486f-a701-8403c8f7dba5" style="width: 49%;"/>

### Settings

![firefox_TwCMDgqiKa](https://github.com/FCTL3314/HealthNutrition-Frontend/assets/97694131/0cb08f01-3266-4942-938b-cf75354d1049)

### Authorization

<img src="https://github.com/FCTL3314/HealthNutrition-Frontend/assets/97694131/6457e274-f0da-4366-a9db-54c7a8bc0335" style="width: 49%;"/>
<img src="https://github.com/FCTL3314/HealthNutrition-Frontend/assets/97694131/e538d3aa-5f9b-4aae-99e0-87091377417f" style="width: 49%;"/>

### Responsive design

<img src="https://github.com/FCTL3314/HealthNutrition-Backend/assets/97694131/d6ee66d9-806a-48d4-8bcb-1cce21bfd4a6" style="width: 40%;"/>
<img src="https://github.com/FCTL3314/HealthNutrition-Backend/assets/97694131/3d267f75-4404-4c50-9fac-613d965df3e8" style="width: 40%;"/>
<img src="https://github.com/FCTL3314/HealthNutrition-Backend/assets/97694131/be072afe-1439-46fa-8780-8156ff97979f" style="width: 40%;"/>
<img src="https://github.com/FCTL3314/HealthNutrition-Backend/assets/97694131/ea60c507-0d12-487d-a5c2-3d18abd4c9ca" style="width: 40%;"/>

</details>

<details><summary><h1>🔥 Features</h1></summary>

* **RESTful API**
* **Domain Driven Design**
* **CI/CD**
* **Comments reply / Tree structure (Django MPTT)**
* **Custom objects ordering**
* **Celery / Postponed Tasks**
* **Email Verification**
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

<details><summary><h1>🐳 Deployment on a server</h1></summary>

### Project Deployment:

1. #### Clone or download the repository and go to its directory.
2. #### Create an **.env** file or rename **.env.dist** in **.env** and populate it with all variables from **.env.dist** file.
3. #### Open docker/production/nginx/conf.d/**nginx.conf** file and change `server_name example.com www.example.com;` to your domains.
4. #### Grant executable rights to the **entrypoint.sh** script: `chmod +x ./entrypoint.sh`
5. #### Start the services: `docker-compose -f docker/local/docker-compose.yaml -f docker/production/docker-compose.yaml up -d`

### Obtaining an ssl certificate:

1. #### Access nginx container: `docker exec -it <nginx-container-id> bin/sh`
2. #### Get ssl certificate: `certbot --nginx`
3. #### Done ! Now you can exit from nginx container: `exit`

</details>

<details><summary><h1>⚒️ Testing</h1></summary>

1. #### Complete all the steps in the 💽 Local installation section
2. #### Run tests: `pytest .`

</details>

<details><summary><h1>🪝 Pre-Commit hooks</h1></summary>

1. #### Install: `pre-commit install`
2. #### Check: `pre-commit run --all-files`

</details>
