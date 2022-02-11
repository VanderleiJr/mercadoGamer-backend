# Mercado Gamer
## Site de Compra de Jogos

Site de venda de jogos, onde empresas anunciam e clientes compram os jogos. Desenvolvido em Python + FastAPI.

## **CRUD Clientes**
(POST) /user/signup - Cadastro de Clientes  
(POST) /user/signin - Login de Clientes com token de autenticação  
(GET) /user/home - Informações do Cliente ( \* )  
(GET) /user/orders - Lista de pedidos feitos pelo Cliente ( \* )  
(DELETE) /user/home - Deleta a conta do Cliente ( \* )  
(GET) /order/{cnpj}/{code}/{amount} - Fazer um pedido ( \* )  

( \* ) = Necessita de autenticação do usuário
  

## **CRUD Empresas**
(POST) /company/signup - Cadastro de Empresas   
(POST) /company/signin - Login de Empresas com token de autenticação  
(POST) /company/products - Registra um produto a Empresa ( \*\* )  
(GET) /company/home - Informações da Empresa ( \*\* )  
(GET) /company/orders - Lista de pedidos feitos à Empresa ( \*\* )  
(GET) /company/products - Lista todos os produtos da Empresa ( \*\* )  
(DELETE) /company/home - Deleta a conta da Empresa ( \*\* )  

## **Produtos no Bando de Dados**
(POST) /company/products/new - Cadastrar Produto novo no banco de dados ( \*\* )  
(GET) /company/products/all - Ver todos Produtos cadastrados no banco de dados ( \*\* )  
(PUT) /company/products/{code} - Alterar dados de um Produto no banco de dados  
(GET) /company/products/{code} - Ver dados de um Produto do banco de dados ( \*\* )  

( \*\* ) = Necessita de autenticação da empresa

## **Market**
(GET) /market - Lista todos os itens que estão sendo vendidos  
(GET) /market/code/{code} - Lista empresas que vendem este produto  
(GET) /market/cnpj/{cnpj} - Lista produtos vendidos por esta empresa  

## Arquitetura e Ferramentas
- API REST
- Python + FastAPI (pydantic)
