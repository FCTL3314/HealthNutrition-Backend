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

  <img src="https://github.com/FCTL3314/HealthNutrition-Backend/assets/97694131/037fcab3-db5e-4cda-b30f-1da16fe816d5" style="width: 80%;"/>
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
      <a href="#-deployment-on-a-server">Deployment on a server</a>
    </b>
  </li>

  <li>
    <b>
      <a href="#-pre-commit-hooks">Pre-Commit hooks</a>
    </b>
  </li>
</ul>

<details open><summary><h1>📃 Description</h1></summary>

This Django application provides a **comprehensive API** for **comparing nutritional values of food products**, aiding
users in **making informed dietary decisions**.

This API empowers developers to integrate **nutritional comparison functionality** into various applications, enabling
users to **search for food items**, **explore nutritional categories**, **view detailed product information**, and
ultimately **make health-conscious dietary choices**. It simplifies the process of **comparing nutritional values across
different food items**, enhancing the user's experience with meal planning and supporting them in **achieving their
nutritional goals**.

</details>

> [!NOTE]
> #### The project was created for educational purposes, simulating fictitious products without real value.

#### Frontend part: https://github.com/FCTL3314/StoreTracker-Frontend

<details><summary><h1>🌄 Demonstration</h1></summary>

### Product categories

<img src="https://github.com/FCTL3314/HealthNutrition-Backend/assets/97694131/037fcab3-db5e-4cda-b30f-1da16fe816d5" style="width: 49%;"/>
<img src="https://github.com/FCTL3314/HealthNutrition-Backend/assets/97694131/a7c3f437-158d-46bc-8488-f680f58651fe" style="width: 49%;"/>
<img src="https://github.com/FCTL3314/HealthNutrition-Backend/assets/97694131/08190097-4c9f-46c0-8d76-22923dae019a" style="width: 49%;"/>

### Products

<img src="https://github.com/FCTL3314/HealthNutrition-Backend/assets/97694131/42dfd931-68b2-4240-8b0a-b56c59067838" style="width: 49%;"/>
<img src="https://github.com/FCTL3314/HealthNutrition-Backend/assets/97694131/795d6dac-cce1-4d13-ac06-ab180cb94fad" style="width: 49%;"/>
<img src="https://github.com/FCTL3314/HealthNutrition-Backend/assets/97694131/17632084-4fdd-430d-bf7b-9d0608daf6cd" style="width: 49%;"/>

### Product detail
![firefox_9HVqv9g46p](https://github.com/FCTL3314/HealthNutrition-Backend/assets/97694131/3dcdead2-64eb-4b22-bb8e-c846958ca437)
![firefox_hrfbO4yzoT](https://github.com/FCTL3314/HealthNutrition-Backend/assets/97694131/81282636-c244-4d6d-97fd-22eecc1e6285)

### Comparison groups

![firefox_TgwCqy76Wf](https://github.com/FCTL3314/HealthNutrition-Backend/assets/97694131/a1a2741f-f6b9-4589-bf52-a236a1532b97)

### Compared products

<img src="https://github.com/FCTL3314/HealthNutrition-Backend/assets/97694131/1806c4fb-d6bb-4662-be33-0221752012a8" style="width: 49%;"/>
<img src="https://github.com/FCTL3314/HealthNutrition-Backend/assets/97694131/184af630-7893-4a6a-8821-5a1891367af0" style="width: 49%;"/>

### Profile

<img src="https://github.com/FCTL3314/HealthNutrition-Backend/assets/97694131/1009923a-d796-4bb0-9de2-f04986a194c2" style="width: 49%;"/>
<img src="https://github.com/FCTL3314/HealthNutrition-Backend/assets/97694131/0db3a019-1d8a-4243-a421-b00834322fc8" style="width: 49%;"/>

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
* **Custom objects ordering (Like Drag & Drop sort)**
* **Celery / Postponed Tasks**
* **Email Verification**
* **JWT Authentication / Authorization**
* **Code Documentation**
* **Tests (PyTest)**

</details>

<details><summary><h1>❕ Peculiarities</h1></summary>

### Architecture:

* Project services are divided into 2 levels:
    * **Domain** - Services that are in no way dependent on the current infrastructure, that is, the framework.
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

### Initial Deployment:

1. #### Clone or download the repository and go to its directory.
2. #### Create an **.env** file or rename **.env.dist** in **.env** and populate it with all variables from **.env.dist** file.
3. #### Create a **nginx.conf** file in the docker/production/nginx/conf.d/ directory and fill it with the code below:

   ```nginx configuration
   upstream core {
       server django-gunicorn:8000;
   }

   server {
       listen 80;
       server_name example.com www.example.com;
       server_tokens off;

       location = /favicon.ico { access_log off; log_not_found off; }

       location /static/ {
           alias /opt/HealthNutrition-Backend/static/;
       }

       location /media/ {
           alias /opt/HealthNutrition-Backend/media/;
       }

       location /.well-known/acme-challenge/ {
           root /var/www/certbot/;
       }

       location / {
           proxy_pass http://core;
               proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
               proxy_set_header Host $host;
               proxy_redirect off;
       }
   }
   ```
  #### **Change example.com and www.example.com to your domains.**

4. #### Grant executable rights to the **entrypoint.sh** and *celery_entrypoint.sh* script: `chmod +x docker/production/entrypoint.sh && chmod +x docker/celery_entrypoint.sh`
5. #### Start the services: `docker-compose -f docker/local/docker-compose.yaml -f docker/production/docker-compose.yaml up -d`

### Obtaining an ssl certificate:

1. #### Access nginx container: `docker exec -it <nginx-container-id> bin/sh`
2. #### Get ssl certificate: `certbot --nginx`
3. #### Done ! Now you can exit from nginx container: `exit`

### Configure CI/CD:

1. Generate ssh keys in your local computer: `ssh-keygen -t rsa -b 4096 -C "your_email@example.com"`
2. Copy the content of your private and public keys to clipboard:
    * Linux: Copy the result of commands:
        * `cat ~/.ssh/id_rsa`
        * `cat ~/.ssh/id_rsa.pub`
    * Windows: Copy the contents of the files:
        * `C:/users/user/.ssh/id_rsa`
        * `C:/users/user/.ssh/id_rsa.pub`
3. Create GitHub repository secrets:
   * SSH_HOST: Your remote server host / IP.
   * SSH_LOGIN: Your remote server login / username.
   * SSH_PORT: Your remote server port.
   * SSH_PRIVATE_KEY: Copied SSH private key.
4. Access your remote host and add your public key there:
   * Execute `nano ~/.ssh/authorized_keys` and paste your copied public key to the next line.

</details>

<details><summary><h1>⚒️ Testing</h1></summary>

1. #### Complete all the steps in the 💽 Local installation section
2. #### Run tests: `pytest .`

</details>

<details><summary><h1>🪝 Pre-Commit hooks</h1></summary>

1. #### Install: `pre-commit install`
2. #### Check: `pre-commit run --all-files`

</details>
