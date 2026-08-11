# Security GRC – Change Management Control Validator (CCM Prototype)
# Security GRC – Validador de Controle de Gestão de Mudanças (Protótipo CCM)

*[English version below]*

---

## 🇧🇷 Português

### Objetivo
Este projeto demonstra uma solução profissional de **Monitoramento Contínuo de Controles (CCM)** para gestão de mudanças corporativas. Ele ingere logs de mudanças, valida a segregação de funções (SoD) e controles temporais contra o **PCI DSS 4.0.1 Requisito 6.5.1**, calcula pontuações de risco priorizadas e gera relatórios prontos para decisão tanto para máquinas (JSON, CSV) quanto para analistas de conformidade (Markdown) [1].

### Principais Funcionalidades
* **Motor de Controle Automatizado:** Avalia aprovações obrigatórias, segregação de funções (SoD), autorização de delegação do aprovador e sequenciamento temporal.
* **Validação de Qualidade de Dados (Fail-Safe):** Garante que metadados obrigatórios estejam presentes e adota uma postura restritiva (fail-safe) para autorizações ausentes.
* **Integridade e Atualidade da Evidência:** Valida formatos de hash SHA-256 (protótipo de integridade) e monitora a idade da evidência contra uma janela de validade de 90 dias (premissa de demonstração).
* **Consciência de Escopo:** Filtra automaticamente ambientes fora de produção (`DEVELOPMENT`, `UAT`) e mudanças canceladas (`NOT_APPLICABLE`).
* **Priorização Baseada em Risco:** Atribui um `Risk Score` (0–100) e `Risk Level` (`CRITICAL`, `HIGH`, `MEDIUM`, `LOW`) usando análise de pior caso (*worst-case analysis*).
* **Recomendações Acionáveis:** Preenche automaticamente etapas de remediação recomendadas para cada achado identificado.
* **Testes Abrangentes:** Suportado por uma suíte de testes `unittest` cobrindo 12 cenários distintos de conformidade e testes negativos.
* **Relatórios Multi-formato:** Gera JSON estruturado, resumos em CSV e relatórios executivos legíveis por humanos.

### Mapeamento de Framework e Controles
* **ID e Nome do Controle:** `CHG-001` — Aprovação Independente de Mudança em Produção.
* **Framework Regulatório:** **PCI DSS 4.0.1 – Requisito 6.5.1** (*Procedimentos de controle de mudanças para sistemas de produção*) [1].

| Verificação Automatizada | Objetivo de Conformidade | Racional de GRC |
| :--- | :--- | :--- |
| **Aprovação Obrigatória** (`MISSING_APPROVAL`) | Autorização documentada | Garante que nenhuma mudança em produção ocorra sem registro de aprovação. |
| **Segregação de Funções** (`SELF_APPROVAL`) | Partes independentes | Impede que implementadores aprovem suas próprias mudanças. |
| **Autorização do Aprovador** (`UNAUTHORIZED_APPROVER`) | Delegação autorizada | Valida se os aprovadores possuem direitos formais de delegação. |
| **Validação Temporal** (`APPROVAL_AFTER_IMPLEMENTATION`) | Barreira preventiva | Confirma que o timestamp da aprovação precede a implementação. |
| **Integridade da Evidência** (`INVALID_EVIDENCE_HASH`) | Integridade e detecção de violação | Verifica a integridade criptográfica dos artefatos de auditoria (SHA-256). |
| **Atualidade da Evidência** (`STALE_EVIDENCE`) | Monitoramento contínuo | Sinaliza documentação de aprovação que exceda 90 dias. |
| **Exceção de Emergência** (`EMERGENCY_REVIEW_REQUIRED`) | Tratamento de exceções | Isola overrides de emergência para revisão obrigatória retroativa do CAB. |

---

## 🇺🇸 English

### Objective
This project demonstrates a professional **Continuous Control Monitoring (CCM)** solution for enterprise change management. It ingests change logs, validates segregation of duties (SoD) and temporal controls against **PCI DSS 4.0.1 Requirement 6.5.1**, calculates risk-prioritized scores, and outputs decision-ready reports for both machines (JSON, CSV) and compliance officers (Markdown) [1].

### Key Features
* **Automated Control Engine:** Evaluates mandatory approvals, segregation of duties (SoD), approver delegation authorization, and temporal sequencing.
* **Data Quality Validation (Fail-Safe):** Ensures mandatory metadata presence and enforces a fail-safe posture for unverified authorizations.
* **Evidence Integrity & Freshness:** Validates SHA-256 evidence hash formats (integrity prototype) and monitors evidence age against a 90-day validity window.
* **Scope Awareness:** Automatically filters out non-production environments (`DEVELOPMENT`, `UAT`) and cancelled changes (`NOT_APPLICABLE`).
* **Risk-Based Prioritization:** Assigns a weighted `Risk Score` (0–100) and `Risk Level` (`CRITICAL`, `HIGH`, `MEDIUM`, `LOW`) using worst-case analysis.
* **Actionable Recommendations:** Automatically populates recommended remediation steps for every finding.
* **Comprehensive Testing:** Fully backed by a robust `unittest` test suite covering 12 distinct compliance and negative test scenarios.
* **Multi-Format Reporting:** Generates structured JSON, CSV summaries, and human-readable Markdown executive reports.

### Control & Framework Mapping
* **Control ID & Name:** `CHG-001` — Independent Production Change Approval.
* **Regulatory Framework:** **PCI DSS 4.0.1 – Requirement 6.5.1** (*Change control procedures for production systems*) [1].

| Automated Control Check | Compliance Objective | GRC Rationale |
| :--- | :--- | :--- |
| **Mandatory Approval** (`MISSING_APPROVAL`) | Documented authorization | Ensures no production change occurs without recorded sign-off. |
| **Segregation of Duties** (`SELF_APPROVAL`) | Independent parties | Prevents implementers from approving their own changes. |
| **Approver Authorization** (`UNAUTHORIZED_APPROVER`) | Authorized delegation | Validates that approvers possess formal delegation rights. |
| **Temporal Validation** (`APPROVAL_AFTER_IMPLEMENTATION`) | Preventative gate | Confirms approval timestamp precedes implementation. |
| **Evidence Integrity** (`INVALID_EVIDENCE_HASH`) | Integrity & Tamper Detection | Verifies cryptographic integrity of audit artifacts (SHA-256). |
| **Evidence Freshness** (`STALE_EVIDENCE`) | Continuous monitoring | Flags approval documentation exceeding 90 days. |
| **Emergency Exception** (`EMERGENCY_REVIEW_REQUIRED`) | Exception handling | Isolates emergency overrides for mandatory retroactive CAB review. |

---

## Project Structure / Estrutura do Projeto

```text
security-grc-code-challenge/
│
├── README.md               # Project documentation (Bilingual Premium)
├── requirements.txt        # Dependencies (Standard Library only)
├── generate_sample_data.py # Sample dataset generator (10 scenarios)
│
├── data/
│   └── changes.csv         # Expanded sample input dataset (10 scenarios)
│
├── src/
│   └── validator.py        # Main validation engine & CLI
│
├── tests/
│   └── test_validator.py   # Automated unit test suite (12 tests)
│
├── docs/
│   ├── control_mapping.md  # Framework mapping & risk methodology
│   └── user_guide.md       # Beginner execution guide
│
└── output/                 # Generated compliance reports
    ├── validation_report.json
    ├── validation_summary.csv
    └── compliance_report.md
```

---

## How to Run / Como Executar

No external third-party libraries are required. Standard Python 3 is fully sufficient. / Não são necessárias bibliotecas externas. O Python 3 padrão é suficiente.

### 1. Run the Validation Engine / Executar o Motor de Validação
```bash
python3 src/validator.py
```
Or specify custom paths / Ou especificar caminhos personalizados:
```bash
python3 src/validator.py --input data/changes.csv --output-dir output
```

### 2. Run the Test Suite / Executar a Suíte de Testes
```bash
export PYTHONPATH=$PYTHONPATH:.
python3 tests/test_validator.py
```

---

## Sample Execution Results / Resumo dos Resultados de Exemplo

| Change ID | System | Environment | Status | Risk Level | Recommended Action |
| :--- | :--- | :--- | :--- | :---: | :--- |
| **CHG-001** | Payment API | PRODUCTION | `PASS` | `LOW` | No action required. Change is fully compliant. |
| **CHG-002** | Core Banking | PRODUCTION | `FAIL` | `CRITICAL` | Reject change. Enforce segregation of duties (SoD)... |
| **CHG-003** | Customer Portal | PRODUCTION | `FAIL` | `CRITICAL` | Reject change. Approver lacks formal delegation... |
| **CHG-004** | Mobile Banking | PRODUCTION | `FAIL` | `CRITICAL` | Initiate post-implementation review and enforce gate... |
| **CHG-005** | Pix Gateway | PRODUCTION | `FAIL` | `HIGH` | Request re-upload of integrity-verified evidence... |
| **CHG-006** | Fraud Engine | PRODUCTION | `EXCEPTION` | `MEDIUM` | Schedule retroactive Change Advisory Board (CAB) review... |
| **CHG-007** | Dev Sandbox | DEVELOPMENT | `NOT_APPLICABLE` | `LOW` | Control not applicable outside production environment. |
| **CHG-008** | Legacy System | PRODUCTION | `FAIL` | `CRITICAL` | Reject change record. Data quality failure: mandatory metadata missing. |
| **CHG-009** | Reporting Tool | PRODUCTION | `FAIL` | `CRITICAL` | Reject change. Approver lacks formal delegation or status unverified. |
| **CHG-010** | Inventory App | PRODUCTION | `PASS_WITH_FINDINGS` | `MEDIUM` | Review findings and remediate control gaps (Missing description). |

---

## References / Referências
1. [PCI Security Standards Council - PCI DSS v4.0.1 Standard](https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0-PT.pdf)
