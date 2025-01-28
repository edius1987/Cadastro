# Sistema de Cadastro de Pacientes em Flet

[![MIT License](https://img.shields.io/badge/license-MIT-007EC7.svg?style=flat-square)](/LICENSE)
![Poetry](https://img.shields.io/badge/Poetry-%233B82F6.svg?style=for-the-badge&logo=poetry&logoColor=0B3D8D)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)

Sistema de cadastro de pacientes desenvolvido com Flet, uma biblioteca Python moderna para criar interfaces gráficas multiplataforma usando Flutter.

## Características

- Interface moderna e responsiva
- Paleta de cores profissional (#541e35, #df5d2e, #ffb43e, #a4c972, #6bb38e)
- Armazenamento em SQLite
- Suporte a planos de saúde
- Campos validados
- Design multiplataforma

## Instalação via Poetry

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/cadastro-pacientes.git
cd cadastro-pacientes
```

2. Instale as dependências com Poetry:

```bash
poetry install
```

3. Execute o aplicativo:

```bash
poetry run python cadastro.py
```

Para executar como aplicativo web:

```bash
poetry run flet run -w cadastro.py
```

## Estrutura do Projeto

```
cadastro-pacientes/

├── pyproject.toml
├── README.md
├── cadastro.py
```


- Cadastro completo de pacientes
- Gerenciamento de planos de saúde
- Busca e edição de registros
- Interface intuitiva com ícones
- Validação de campos
- Persistência em banco de dados SQLite

## Banco de Dados

O sistema utiliza SQLite com duas tabelas principais:

### Tabela planos

- id (INTEGER PRIMARY KEY)
- nome (TEXT UNIQUE)

### Tabela pacientes

- id (INTEGER PRIMARY KEY)
- nome (TEXT)
- sexo (TEXT)
- cartao (TEXT)
- dia_nasc (TEXT)
- mes_nasc (TEXT)
- ano_nasc (TEXT)
- endereco (TEXT)
- cidade (TEXT)
- estado (TEXT)
- cep (TEXT)
- telefone (TEXT)
- celular (TEXT)
- plano_id (INTEGER FOREIGN KEY)

## Interface

A interface foi desenvolvida com foco na usabilidade, apresentando:

- Barra de ferramentas com ícones intuitivos
- Campos organizados logicamente
- Cores contrastantes para melhor visualização
- Feedback visual nas interações
- Layout responsivo e centralizado

## Desenvolvimento

O projeto foi desenvolvido usando:

- Python 3.x
- Flet para interface gráfica
- SQLite para persistência
- Poetry para gerenciamento de dependências

## Contribuindo

1. Faça um Fork do projeto
2. Crie sua Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a Branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## Referências

- [Documentação do Flet](https://flet.dev/)
- [Python SQLite3](https://docs.python.org/3/library/sqlite3.html)
- [Poetry Documentation](https://python-poetry.org/docs/)
