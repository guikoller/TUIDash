### **Análise de Requisitos e Engenharia de Software**

#### **Requisitos Funcionais**
1. **Monitoramento de Processos:**
   - Exibir informações globais do sistema (uso de CPU, threads totais, processos totais, etc.).
   - Listar todos os processos em execução com informações básicas (PID, usuário, nome do processo).
   - Detalhar informações específicas de cada processo:
     - Threads associados.
     - Uso de recursos (CPU, memória).
     - Estado (running, sleeping, etc.).

2. **Monitoramento de Memória:**
   - Exibir dados globais de memória:
     - Percentual de uso.
     - Quantidade de memória livre.
     - Memória física e virtual total.
   - Detalhar informações de memória de cada processo:
     - Páginas de memória alocadas (código, heap, stack).
     - Memória usada e reservada.

3. **Atualização em Tempo Real:**
   - Atualizar os dados a cada 5 segundos.

4. **Interface do Usuário:**
   - Tela principal com visão geral do sistema.
   - Tela detalhada para processos e memória individuais.

5. **Multitarefa e Arquitetura MVC:**
   - Separar aquisição de dados, processamento e apresentação em threads distintas.
   - Implementar o padrão de projeto MVC para modularidade e escalabilidade.

---

### **Etapas do Desenvolvimento**
#### **1. Planejamento e Design**
   - **Divisão de Módulos:**
     - **Model:** Responsável pela coleta e armazenamento de dados.
     - **View:** Interface textual para exibição.
     - **Controller:** Coordena a interação entre Model e View.
   - Escolher as APIs e bibliotecas para comunicação com o sistema operacional:
     - Linux: `/proc`, `psutil`.
     - Windows: `ctypes`, `pywin32`.

#### **2. Implementação**
##### **Fase 1: Estrutura Inicial**
   1. Criar a estrutura do projeto seguindo MVC.
   2. Configurar o sistema de threads para:
      - **Thread 1:** Coletar dados do sistema (CPU, memória, processos).
      - **Thread 2:** Processar dados coletados.
      - **Thread 3:** Atualizar a interface do usuário.
   3. Implementar o pipeline básico:
      - Dados brutos → Processamento → Apresentação.

##### **Fase 2: Monitoramento Global**
   - Desenvolver a coleta de dados globais:
     - Uso de CPU.
     - Memória total e livre.
     - Número total de processos e threads.

##### **Fase 3: Detalhamento de Processos**
   - Listar processos com detalhes básicos.
   - Criar uma tela adicional para exibir informações detalhadas de cada processo.

##### **Fase 4: Monitoramento de Memória**
   - Coletar e exibir informações de memória por processo.
   - Criar representações visuais (barras ou indicadores textuais) para uso de memória.

#### **3. Testes**
   - **Testes Unitários:**
     - Testar funções individuais de coleta e processamento de dados.
   - **Testes de Integração:**
     - Garantir que os módulos Model, View e Controller funcionam em conjunto.
   - **Testes de Estresse:**
     - Avaliar o desempenho com muitos processos ativos.
   - **Testes de Portabilidade:**
     - Validar o funcionamento em diferentes sistemas operacionais.

#### **4. Documentação**
   - Documentar a arquitetura do sistema.
   - Criar manual de uso para o dashboard.

#### **5. Implantação**
   - Empacotar o aplicativo com dependências mínimas.
   - Realizar testes finais em ambiente real.

#### **6. Manutenção**
   - Monitorar o desempenho em produção.
   - Implementar melhorias baseadas no feedback.
