# ml-iris-prediction

A flask API that consumes a prediction model trained by the Logistic Regression Classification algorithm.

# Deploy local:

1. Após executar o git clone execute os comandos abaixo na raiz do projeto:

```
python3 -m venv venv

source venv/bin/activate  # Unix/macOS
# ou
venv\Scripts\activate  # Windows

pip install -r requirements.txt

python3 app.py
```

Documentação em Swagger:

```
http://127.0.0.1:5000/apidocs
```

Obs: Após instalar uma dependência nova, para atualizar o arquivo requirements.txt execute o comando abaixo:

```
pip freeze > requirements.txt
```

# Deploy with Kubernetes in GCP:

1. Crie um projeto no Google Cloud chamado "ml-iris-prediction";
2. Ative a API do Kubernetes;
3. Execute os comandos abaixo:

```
docker build -t api-ml-iris-prediction .  
docker tag api-ml-iris-prediction gcr.io/ml-iris-prediction/api-ml-iris-prediction:latest
docker push gcr.io/ml-iris-prediction/api-ml-iris-prediction:latest

cd ./iac

terraform init
terraform plan
terraform apply --auto-approve

cd ./kubernetes-yamls

gcloud container clusters get-credentials cluster-ml-iris-prediction --region us-central1 --project ml-iris-prediction
kubectl apply -f deployment.yaml
kubectl apply -f svc.yaml
```

4. Após isso aguarde alguns minutos até que o cluster autopilot do GKE provisione os recursos necessários;
5. Após os recursos estarem devidamente provisionados, acesse o seguinte link na plataforma do Google Cloud: Kubernetes Engine->Gateways, serviços e entrada;
6. Clique na aba serviços e copie a url que está na coluna "Pontos de extremidade" do serviço chamado "svc-ml-iris-prediction" que acabou de ser criado;
7. Com este link é possível efetuar as chamadas dos endpoints da api em Flask que consome o modelo;
