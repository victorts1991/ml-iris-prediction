# API de Predição Iris (MLOps End-to-End)

Este projeto demonstra uma solução completa de MLOps para previsão de demanda, utilizando um modelo de Machine Learning e uma API robusta. A arquitetura foi desenvolvida com foco em escalabilidade, manutenibilidade e automação de deploy.

## Visão Geral do Projeto

Este projeto de **MLOps end-to-end** foca na **previsão de demanda**, centralizado em uma **API em FastAPI** que incorpora validação de dados com **Pydantic**. A solução foi construída com um forte pilar de **Engenharia de Machine Learning**, abrangendo:

* **Algoritmo de Machine Learning:** Utiliza um modelo de **Regressão Logística** para realizar as previsões da espécie Iris com base nas características fornecidas.
* **Quality Assurance:** Implementa **testes unitários** abrangentes com **Pytest** para a lógica da API, a camada de carregamento do modelo e as operações de persistência de dados.
* **Operationalization (MLOps):**
    * **Containerização:** A aplicação é empacotada em imagens **Docker** para garantir ambientes consistentes e portabilidade.
    * **Orquestração:** O deploy da API é gerenciado no **Kubernetes (GKE)** no **Google Cloud Platform (GCP)**, permitindo alta disponibilidade e escalabilidade.
    * **Integração e Entrega Contínuas (CI/CD):** Um pipeline automatizado no **GitHub Actions** orquestra o build da imagem Docker, a execução dos testes e o deploy contínuo da aplicação no GKE.
* **Infrastructure as Code (IaC):** Toda a infraestrutura necessária no GCP, incluindo o cluster Kubernetes, é provisionada e gerenciada via **Terraform**, garantindo ambientes reprodutíveis e versionados.
* **Data Persistence:** As predições realizadas pela API são armazenadas e gerenciadas de forma eficiente em um banco de dados **NoSQL**, o **Sqlite**, para futuras análises ou monitoramento.

Este projeto demonstra a capacidade de construir, testar e operacionalizar sistemas de IA escaláveis e manuteníveis em um ambiente de nuvem.

## Tecnologias Utilizadas

* **Linguagem:** Python
* **Framework Web:** FastAPI
* **Validação de Dados:** Pydantic
* **Machine Learning:** Scikit-learn (Logistic Regression), Joblib
* **Testes:** Pytest
* **Containerização:** Docker
* **Orquestração de Contêineres:** Kubernetes (K8s)
* **Plataforma de Nuvem:** Google Cloud Platform (GCP)
* **Serviços GCP:** Google Kubernetes Engine (GKE)
* **Infraestrutura como Código (IaC):** Terraform
* **CI/CD:** GitHub Actions
* **Banco de Dados:** Sqlite

# Deploy local:

1. Após executar o git clone execute os comandos abaixo na raiz do projeto:

```
python3 -m venv venv

source venv/bin/activate  # Unix/macOS
# ou
venv\Scripts\activate  # Windows

pip install -r requirements.txt

pytest

uvicorn main:app --reload --port 5000
```

Documentação em Swagger:

```
http://127.0.0.1:5000/docs
```

Obs: Após instalar uma dependência nova, para atualizar o arquivo requirements.txt execute o comando abaixo:

```
pip freeze > requirements.txt
```

Caso for executar o modelo, utilize o comando abaixo para criar um kernel para o arquivo ipynb e depois selecione ele em sua ferramenta de edição de código:

```
python3 -m ipykernel install --user --name=ml_iris_prediction_venv
```




# Deploy with Kubernetes on GCP manually:

1. Crie um projeto no Google Cloud chamado "ml-iris-prediction";
2. Ative a API do Kubernetes;
3. Execute os comandos abaixo:

```
export GCP_PROJECT_ID="seu-projeto-id-aqui"

docker build -t api-ml-iris-prediction .
docker tag api-ml-iris-prediction gcr.io/${GCP_PROJECT_ID}/api-ml-iris-prediction:latest
docker push gcr.io/${GCP_PROJECT_ID}/api-ml-iris-prediction:latest

cd ./iac

export TF_VAR_project_id=${GCP_PROJECT_ID}
terraform init
terraform plan
terraform apply --auto-approve

cd ./kubernetes-yamls

gcloud container clusters get-credentials cluster-ml-iris-prediction --region us-central1 --project ${GCP_PROJECT_ID}

# Para o deployment é necessário que seja feito o apply de forma diferente, para que o mesmo use a varíavel de ambiente GCP_PROJECT_ID
envsubst < deployment.yaml | kubectl apply -f -
kubectl apply -f svc.yaml
```

4. Após isso aguarde alguns minutos até que o cluster autopilot do GKE provisione os recursos necessários;
5. Após os recursos estarem devidamente provisionados, acesse o seguinte link na plataforma do Google Cloud: Kubernetes Engine->Gateways, serviços e entrada;
6. Clique na aba serviços e copie a url que está na coluna "Pontos de extremidade" do serviço chamado "svc-ml-iris-prediction" que acabou de ser criado;
7. Com este link é possível efetuar as chamadas dos endpoints da api em FastApi que consome o modelo de predição treinado pelo algoritmo de Classificação de Regressão Logística;

# Deploy with Kubernetes on GCP with Github Actions:

1. Execute os itens 1 e 2 do passo a passo acima;
2. Na plataforma do Google Cloud acesse o menu IAM e administrador->Contas de serviço;
3. Clique em "Criar conta de serviço" na parte superior da página;
4. Na página "Criar conta de serviço", forneça um Nome da conta de serviço descritivo (por exemplo, github-actions-deploy);
5. Clique em "Criar e continuar";
6. Na seção "Conceder à conta de serviço acesso ao projeto", você precisará atribuir os papéis (permissões) necessários para que o GitHub Actions possa interagir com o GKE e o GCR. Aqui estão os papéis mínimos:
  - 6.1: Kubernetes Engine Admin: Permite gerenciar clusters GKE;
  - 6.2: Create-on-Push Repository Manager in Artifact Registry: Permite enviar imagens e criar respositórios no Artifact Registry;
  - 6.3: Service Account User: Permite que a conta de serviço atue como outras contas de serviço, se necessário;
  - 6.4: Compute Instance Administrator (v1): Necessário para gerenciar instâncias do Compute Engine;
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

TODO:

- Ajustar o pipeline no Github Actions