# Burnout Analytics Suite (Streamlit)

Desenvolvido por Wellington Teles - wellingtonteles\@gmail.com

Aplicação interativa em Python/Streamlit para análise do dataset `dataset/developer_burnout_dataset_7000.csv`, com foco em portfólio profissional para apresentação comercial e técnica.

## Recursos implementados

- Múltiplas abas para separar exploração, segmentação, correlações, temporal e metodologia.
- Layout com colunas, KPIs executivos e dashboard visual.
- Filtros dinâmicos com:
  - `slider` (idade, horas, estresse)
  - `selectbox` (classe de burnout e variáveis de comparação)
  - `multiselect` (gênero proxy, cargo derivado, perfil de empresa proxy)
  - `date_input` (janela temporal)
- Alternância de idioma na interface (`PT_BR` padrão e `EN_US`).
- Visualizações interativas:
  - histogramas de distribuição
  - barras comparativas
  - heatmap de correlação
  - scatter plot para relações entre variáveis
  - mapa de calor temporal
- Estatísticas descritivas com média, mediana e desvio padrão.
- Tema visual customizado via CSS com responsividade e transições suaves.

## Estrutura do projeto

```text
streamlit/
├─ app.py
├─ requirements.txt
├─ README.md
├─ info.txt
└─ dataset/
   └─ developer_burnout_dataset_7000.csv
```

## Instalação

1. Crie e ative um ambiente virtual (opcional, recomendado):

```bash
python -m venv .venv
.venv\Scripts\activate
```

1. Instale as dependências:

```bash
pip install -r requirements.txt
```

## Execução

No diretório raiz do projeto:

```bash
streamlit run app.py
```

## Como usar

- Abra o menu lateral para combinar filtros e refinar análises.
- Use a aba **Portfólio Executivo** para KPIs e visão gerencial.
- Use **Exploração de Dados** para amostra, distribuição e estatísticas.
- Use **Segmentação** para padrões por gênero/cargo/empresa (camadas derivadas).
- Use **Correlações e Relações** para heatmap e scatter plots.
- Use **Padrões Temporais** para análise sazonal e tendência mensal.
- Leia **Sobre** para metodologia, limitações e fonte dos dados.

## Observações metodológicas

- O dataset original não contém colunas explícitas de gênero, cargo textual e empresa nominal.
- Para suportar o caso de uso de portfólio, o app aplica dimensões derivadas:
  - `job_role` por faixas de experiência
  - `gender_proxy` e `company_profile` para segmentação executiva
  - `analysis_date` sintético para análises temporais
- Essas dimensões são apresentadas de forma transparente na interface.

## Capturas de tela para portfólio

As imagens principais podem ser salvas na pasta `screenshots/`, por exemplo:

- `screenshots/01_portfolio_kpis.png`
- `screenshots/02_exploracao_histograma.png`
- `screenshots/03_correlacao_heatmap.png`
- `screenshots/04_temporal_heatmap.png`

> Se desejar, personalize cores, logotipo e textos para aderir ao branding da sua empresa.
