# ml-iris-prediction

A Flask API that consumes a prediction model trained by the Logistic Regression Classification algorithm. Deploy with IaC and Github Actions using Docker and Kubernetes on GCP.

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

# Deploy with Kubernetes on GCP manually:

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
7. Com este link é possível efetuar as chamadas dos endpoints da api em Flask que consome o modelo de predição treinado pelo algoritmo de Classificação de Regressão Logística;

# Deploy with Kubernetes on GCP with Github Actions:

1. Execute os itens 1 e 2 do passo a passo acima;
2. Na plataforma do Google Cloud acesse o menu IAM e administrador->Contas de serviço;
3. Clique em "Criar conta de serviço" na parte superior da página;
4. Na página "Criar conta de serviço", forneça um Nome da conta de serviço descritivo (por exemplo, github-actions-deploy);
5. Clique em "Criar e continuar";
6. Na seção "Conceder à conta de serviço acesso ao projeto", você precisará atribuir os papéis (permissões) necessários para que o GitHub Actions possa interagir com o GKE e o GCR. Aqui estão os papéis mínimos:
  6.1: Kubernetes Engine Admin: Permite gerenciar clusters GKE;
  6.2: Artifact Registry Writer: Permite enviar imagens para o Google Container Registry (GCR) ou Artifact Registry (se você estiver usando);
  6.3: Service Account User: Permite que a conta de serviço atue como outras contas de serviço, se necessário;
7. Clique em "Continuar" e depois em "Concluir";
8. Após o usuário estar criado, acesse os detalhes do mesmo, vá até a aba "Chaves", e adicione uma nova chave em JSON;
9. Com isso será feito o download da sua chave;
10. Vá até o seu repositório no Github e clique em "Settings";
11. Na barra lateral esquerda, clique em "Secrets and variables" (Segredos e variáveis) e depois em "Actions";
12. Clique em "New repository secret" (Novo segredo do repositório);
13. No campo Name, digite "GCP_CREDENTIALS_JSON" (o mesmo nome que você usou na sua configuração do GitHub Actions);
14. No campo Value, cole o conteúdo completo do arquivo JSON que você baixou. Certifique-se de incluir as chaves { e } no início e no final;
15. Clique em "Add secret" (Adicionar segredo);
16. Após isso efetue um commit na branch main, com isso o pipeline do Github Actions será acionado e efetuará o deploy da aplicação no GKE;
17. Após o pipeline ter sido concluido, execute os itens 4, 5, 6 e 7 do passo a passo acima;