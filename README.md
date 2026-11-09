# Painel de Indicadores de Pesquisadores em Ciência Aberta

É uma aplicação desenvolvida em **Python** para catalogar, ordenar e consultar métricas de impacto acadêmico de pesquisadores dedicados à **Ciência Aberta** (*Open Science*).

A base de dados é composta por 583 perfis extraídos do **Google Scholar Profiles** com o auxílio do software [*Publish or Perish*](https://harzing.com/resources/publish-or-perish/windows).

---
## Estrutura de Arquivos do Repositório

```text
├── GSProfiles.csv          # Base original coletada via Publish or Perish (ordem por citações)
├── GSProfile2.csv          # Base reordenada em ordem alfabética de pesquisadores (A-Z)
├── ProjetoIntegrador.py    # Aplicação do painel de indicadores de pesquisadores em ciência aberta
└── README.md               # Documentação do projeto
