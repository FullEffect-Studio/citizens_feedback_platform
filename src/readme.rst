root/
├── __init__.py
├── config.py
├── main.py
├── requirements.txt
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── controllers/
│   │   │   ├── __init__.py
│   │   │   ├── users.py
│   │   │   ├── products.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── product.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── use_cases/
│   │   │   ├── __init__.py
│   │   │   ├── user_use_cases.py
│   │   │   ├── product_use_cases.py
│   │   ├── repositories/
│   │   │   ├── __init__.py
│   │   │   ├── user_repository.py
│   │   │   ├── product_repository.py
│   ├── infra/
│   │   ├── __init__.py
│   │   ├── memory_db.py
│   │   ├── sqlite_db.py
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_users.py
│   │   ├── test_products.py







root
├── app.py (entry point for the application)
├── config.py (configuration for the application)
├── requirements.txt (dependencies for the application)
├── feature1
│   ├── business
│   │   ├── __init__.py
│   │   ├── models.py (business models for feature 1)
│   │   ├── services.py (business services for feature 1)
│   ├── external
│   │   ├── __init__.py
│   │   ├── controllers.py (controllers for feature 1)
│   │   ├── database.py (database access for feature 1)
│   │   ├── views.py (templates and routes for feature 1)
├── feature2
│   ├── business
│   │   ├── __init__.py
│   │   ├── models.py (business models for feature 2)
│   │   ├── services.py (business services for feature 2)
│   ├── external
│   │   ├── __init__.py
│   │   ├── controllers.py (controllers for feature 2)
│   │   ├── database.py (database access for feature 2)
│   │   ├── views.py (templates and routes for feature 2)
└── tests
    ├── __init__.py
    ├── test_feature1.py (tests for feature 1)
    └── test_feature2.py (tests for feature 2)





my_project/
├── api/
│   ├── controllers/
│   ├── middlewares/
│   ├── views/
│   ├── __init__.py
│   ├── api.py
├── core/
│   ├── entities/
│   ├── use_cases/
│   ├── __init__.py
├── infrastructure/
│   ├── persistence/
│   ├── __init__.py
├── tests/
├── config.py
├── main.py
├── requirements.txt




root/
├── app/
│   ├── __init__.py
│   ├── main/
│   │   ├── __init__.py
│   │   ├── controllers/
│   │   │   ├── __init__.py
│   │   │   ├── home_controller.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── user_service.py
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── controllers/
│   │   │   ├── __init__.py
│   │   │   ├── login_controller.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py
├── tests/
│   ├── __init__.py
│   ├── test_main.py
│   ├── test_auth.py
├── config.py
├── requirements.txt
├── run.py



myapp/
├── api/
│   ├── controllers/
│   ├── models/
│   └── views/
├── core/
│   ├── usecases/
│   ├── entities/
│   ├── repositories/
│   └── interfaces/
├── infrastructure/
│   ├── persistence/
│   ├── services/
│   └── web/
├── tests/
│   ├── api/
│   ├── core/
│   └── infrastructure/
├── requirements.txt
├── run.py
└── settings.py




myapp/
├── api/
│   ├── controllers/
│   ├── models/
│   └── views/
├── core/
│   ├── usecases/
│   ├── entities/
│   ├── repositories/
│   ├── interfaces/
│   ├── commands/
│   └── queries/
├── infrastructure/
│   ├── persistence/
│   ├── services/
│   └── web/
├── tests/
│   ├── api/
│   ├── core/
│   └── infrastructure/
├── requirements.txt
├── run.py
└── settings.py




myapp/
├── api/
│   ├── controllers/
│   ├── models/
│   └── views/
├── core/
│   ├── commands/
│   ├── queries/
│   ├── entities/
│   ├── repositories/
│   ├── interfaces/
│   └── usecases/
├── infrastructure/
│   ├── persistence/
│   ├── services/
│   └── web/
├── tests/
│   ├── api/
│   ├── core/
│   └── infrastructure/
├── requirements.txt
├── run.py
└── settings.py
