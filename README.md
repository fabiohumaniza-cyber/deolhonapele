# De Olho na Pele · SOLIZ v0 — wound-edge measurement demo

**Live demo / Demonstração ao vivo:** **https://fabiohumaniza-cyber.github.io/deolhonapele/**

Rule-based, auditable wound-edge measurement — no machine learning, no server, no data leaves your browser.
Companion demo of the preprint: **[doi:10.5281/zenodo.23062849](https://doi.org/10.5281/zenodo.23062849)** (Ferreira FCO, 2026 — full manuscript, frozen engine, data, pre-registrations and audit trail).

## How to use (2 minutes)

1. Open the **[live demo](https://fabiohumaniza-cyber.github.io/deolhonapele/)** — the start page explains both tools, in **English and Portuguese** (use the language toggle on the page).
2. Pick a tool:
   - **Automatic** (`demo_soliz_auto.html`) — load a wound photograph, declare the expected diameter, and the frozen rule engine finds the edge on its own: skin reference from the image itself, transition map, topologically closed ring, blind choice among 144 candidates, confidence score.
   - **3-point assisted** (`demo_soliz_3pontos.html`) — click three single-pixel samples (edge, wound bed, skin) and local colour models trace the edge; no diameter is declared, no candidate sweep.
3. Read the result: area, confidence score, chosen channel and settings — and, when the ring does not close, an explicit **refusal with a named cause** (in this port there is no silent fallback).

Everything runs locally in your browser (plain JavaScript, single file per page). No upload, no account, no telemetry.

## What this demo is — and is not

- The JavaScript engine is a **translation of the frozen Python engine** (SOLIZ v0, SHA-256 in the deposit), validated **digit-for-digit** against it: 64/64 grid samples, the full 81,458-px grid choice, and the held-out wound 1323·C on identical pixels. Details: `VALIDACAO_PORTE_JS_30SET.md` in the Zenodo deposit.
- It is a **research demonstration**, not a medical device. It has been validated against a physical standard in a **porcine model** only; validation in human wounds is future, pre-registered work. It must not be used for diagnosis or clinical decision-making.

## Cite / Citar

> Ferreira FCO (2026). *The wound edge exists in the photograph: rule-based, auditable measurement against a physical standard in a porcine model.* Zenodo. https://doi.org/10.5281/zenodo.23062849

## License / Licença

Demo code is source-available: **free for research, teaching and verification**; commercial use of the method requires a license (patent application BR 10 2026 024571 2, INPI; software registration BR 51 2026 008413-0). Full terms in `LICENSE.txt` inside the Zenodo deposit. Texts and figures of the study: CC BY 4.0.

---

### PT-BR, em uma linha
Ferramentas de medida de borda de ferida por regra escrita, auditáveis, rodando 100 % no seu navegador — demonstração do preprint [doi:10.5281/zenodo.23062849](https://doi.org/10.5281/zenodo.23062849). Abra a [demo ao vivo](https://fabiohumaniza-cyber.github.io/deolhonapele/), escolha a ferramenta automática ou a de 3 pontos, e siga as instruções na própria página (PT/EN). Nada é enviado a servidor algum. Uso em pesquisa; não é dispositivo médico.

*Autor: Fabio da Camara Oliveira Ferreira, RN (COREN-SP 284.219) · ORCID [0009-0009-0997-3275](https://orcid.org/0009-0009-0997-3275) · Águas de Lindóia, SP, Brasil*
