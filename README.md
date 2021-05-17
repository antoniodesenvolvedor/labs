# labs
Repositório criado para resolver o exercício de contratação do Luiza Labs

#Instruções de uso 
docker run --name postgres --network labs -e POSTGRES_DB=db_customer -e POSTGRES_PASSWORD=secure_password -e "TZ=GMT+3" -v /postgres_volume:/var/lib/postgresql/data  -dp 5432:5432 postgres

#app
docker run --name api_labs  --network labs -dp 5000:5000 api_labs


