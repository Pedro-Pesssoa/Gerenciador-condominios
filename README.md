# Sistema de Gerenciamento do Condomínio

## Apps

# Condominios
Na app condomio temos toda gestão e organização(CRUD) referente a um usuario, ele está dividido em duas classes, são elas, casa e condominio.

- Codominio: Um condominio pode conter 0 ou N casas. Ao criar um condominio é verificado se a casa e o endereço que está sendo passado já existe, para garantir que não vai haver uma mesma casa em dois condominios diferentes.

- Casa: Ao criar um casa é verificado se o numero e bloco passado já existe, caso exista a casa não sera criada e uma mesagem de erro será retornada caso contrario a casa será criada.

# Usuarios
A app usuarios é responsavel pelo controle de usuarios e possui duas entidades User e Morador

- User: A classe user é uma classe generica de ususario que responsavel por dados pessoais e gerais

- Morador: O morador herda de user, e adiciona mais algumas informações

## Requisitos

- Python 3.x
- Django
- Django Rest Framework
- drf-spectacular

## Instruções de Instalação

#1. **Ative o ambiente virtual:**
Para garantir que você está trabalhando dentro do ambiente virtual do projeto, execute o seguinte comando no terminal: 
```bash 
.\venv\Scripts\activate
```
#2. **Atualize o pip:**
É uma boa prática garantir que o pip esteja atualizado. Execute o seguinte comando para atualizar o pip: 
```bash 
python.exe -m pip install --upgrade pip
``` 
#3. **Instale o Django:**
Se ainda não tiver o Django instalado, execute o comando abaixo para instalá-lo: 
```bash 
Instale o Django Rest Framework (DRF):
``` 
## O Django Rest Framework é utilizado para criar APIs de forma fácil e eficiente. Para instalá-lo, execute: 
```bash 
pip install djangorestframework
``` 
#4. **Instale o drf-spectacular:**

O drf-spectacular é uma ferramenta para gerar documentação automatizada para a API. Instale-a com o comando: 
```bash 
pip install drf-spectacular
```
#5. **Configuração do Projeto**
Após realizar a instalação das dependências, você pode configurar o projeto com as migrações do banco de dados: 
```bash 
python manage.py migrate
```
#6. **Inicie o Servidor de Desenvolvimento:**
Agora você pode rodar o servidor de desenvolvimento do Django com o comando: 
``` bash 
python manage.py runserver
```
