# Kite for Life — App de Avaliação de Desempenho (protótipo)

Este protótipo em Streamlit permite:
- Fazer upload e editar um CSV;
- Inserir avaliações via formulário com critérios separados:
  - LIDERANÇA
  - ASSIDUIDADE
  - FLEXIBILIDADE
  - TEORIA
  - COMANDO
  - CONTROLE
  - BADYDRAG ESQ/DIR
  - WATER START
  - PRANCHA ESQ/DIR
  - CONTRA VENTO
- Calcular e salvar a nota média (média simples dos critérios);
- Salvar avaliações em um banco SQLite local;
- Exportar avaliações para CSV;
- Ver estatísticas básicas (média por critério, média por cargo, etc).

Requisitos
- Python 3.8+
- Pip

Instalação e execução
1. Clone / copie os arquivos para uma pasta.
2. Crie um ambiente virtual (recomendado):
   - python -m venv .venv
   - source .venv/bin/activate (Linux/macOS) ou .venv\Scripts\activate (Windows)
3. Instale dependências:
   - pip install -r requirements.txt
4. Rode o app:
   - streamlit run app.py

Observações sobre importação de CSV
- O import tenta mapear automaticamente colunas com nomes comuns e variações:
  - Exemplos aceitos para BADYDRAG ESQ/DIR: "badydrag esq/dir", "badydrag_esq_dir", "BADYDRAG ESQ/DIR"
  - Exemplos para PRANCHA ESQ/DIR: "prancha esq/dir", "prancha_esq_dir"
  - Exemplos para CONTRA VENTO: "contra vento", "contra_vento", "contra-vento"
- Se o CSV tiver apenas algumas notas, a nota média será a média das notas presentes (ignora valores ausentes).
- Recomenda-se usar nomes de coluna iguais aos critérios (sem acentos ou com underscores) para mapear facilmente.

Próximos passos que posso implementar para você:
- Validar intervalos (ex.: escala 0-10 em vez de 0-100) e tornar alguns campos obrigatórios.
- Aplicar pesos por critério ao invés de média simples.
- Adicionar filtros por data, export por período, e relatórios em PDF.
- Autenticação e permissões por usuário.
- Frontend mais avançado (React) e backend separado (FastAPI) para multiusuário.

Se quiser, eu:
- Ajusto a escala para 0-10,
- Adiciono pesos por critério (diga os pesos),
- Faço validação para campos obrigatórios,
- Ou gero um repositório ZIP com estes arquivos prontos para download.