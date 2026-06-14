# Halco Sorcerer 125DD style — Bambu print package

Это не официальный Halco и не точная копия с логотипом. Это рабочий прототип **Sorcerer 125 DD style** для личных испытаний и печати.

## Как получить ZIP

Вариант 1 — GitHub Actions:

1. Открой репозиторий `igor04091968/green-api-test`.
2. Перейди в Actions.
3. Запусти workflow `Build Halco Sorcerer 125DD ZIP`, если он не запустился автоматически.
4. После выполнения файл должен появиться здесь:

```text
/downloads/halco_sorcerer_125dd_v01/Halco_Sorcerer_125DD_Bambu_v01.zip
```

Вариант 2 — локально:

```bash
cd downloads/halco_sorcerer_125dd_v01
python3 generate_halco_sorcerer_125dd_zip.py
```

На выходе будет:

```text
Halco_Sorcerer_125DD_Bambu_v01.zip
```

## Что внутри ZIP

- `sorcerer125dd_style_Bambu_parts_v01.3mf`
- `sorcerer125dd_style_LEFT_half_v01.stl`
- `sorcerer125dd_style_RIGHT_half_v01.stl`
- `sorcerer125dd_style_DD_lip_2mm_template_v01.stl`
- `sorcerer125dd_style_DD_lip_cut_template_v01.svg`
- `README_RU_PRINT_AND_TUNE_v01.txt`

## Печать

- Bambu Lab A1 / A1 mini: PETG или ASA.
- Слой: 0.16–0.20 мм.
- Стенки: 5–6.
- Заполнение: 15–25% gyroid.
- Лопатку для реальной рыбалки лучше вырезать из поликарбоната 2 мм по SVG-шаблону.
- Каркас: сквозная нержавеющая проволока 1.0–1.2 мм.
