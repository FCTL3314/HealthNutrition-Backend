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
</ul>

# 📃 Description

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

# 🌄 Demonstration

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


# 🔥 Features

* **REST API**
* **JWT Authentication**
* **Postponed Tasks / Celery**
* **Authentication / Authorization**
* **Profile editing**
* **Email verification**
* **Docstrings**
* **Tests (PyTest)**

# 💽 Local installation
1. #### Clone or download the repository.
2. #### Create an .env file or rename .env.dist in .env and populate it only with development variables:
   * SECRET_KEY
   * ALLOWED_HOSTS
   * CORS_ALLOWED_ORIGINS(Optional)
   * REDIS_HOST
   * REDIS_PORT
   * RABBITMQ_HOST
   * RABBITMQ_PORT
   * EMAIL_HOST_USER
3. #### Run docker services for local development: `docker-compose -f docker/local/docker-compose.yml up`

> #### Django automatically detects code changes by using a docker volume that spans all the code.

# 🪝 Pre-Commit hooks
1. #### Install: `pre-commit install`
2. #### Test run `pre-commit run --all-files`
