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

##Changelogs

- Adicionados os tratamentos de exceção
- Atualizada documentação do Insmonia
- Configuração do Sentry
- Ajuste nos testes de casa
- Ajuste de formatação e organização de views e models
- Ajuste no tratamento de exeção 

## Tutorial de instalação 

- **Passo 1** - Crie o ambiente virtual 
~~~
    python3 -m venv venv
~~~

- **Passo 2** - Ative o ambiente virtual
~~~
    . venv/bin/activate
~~~

- **Passo 3** - Instale as dependencias
~~~
    pip install -r requirements.txt
~~~

- **Passo 4** - Rode o servidor interno
~~~
    python manage.py runserver
~~~
