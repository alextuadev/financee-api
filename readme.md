Run APP
```docker compose up ```

Enter to container:
```docker exec -ti finance-api bash  ```

RUN on
```0.0.0.0```




## Functionalities:


#Endpoints:



#Migrations update ( alembic ):
alembic revision --autogenerate -m "Description changes "


apply changes:
alembic upgrade head
