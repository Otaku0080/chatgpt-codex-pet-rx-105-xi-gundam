# Ξ-105 v1.1 review build

Status: complete, validated, uploaded, and active.

## Active pet changes

- `running-right`: eight-frame rightward Minovsky flight loop
- `running-left`: eight-frame true left-facing Minovsky flight loop
- `jumping`: five-frame hover lift, peak, descent, and settle
- `running`: six-frame stationary tactical hover / processing loop
- All other approved animation and look-direction rows are preserved from v1.

## Combat showcase pack

The fixed ChatGPT Pet atlas does not provide three extra combat states, so these are separate review animations and are not silently substituted for standard pet behavior:

- combined conventional and funnel-missile salvo
- beam-rifle firing cycle
- green beam-saber draw and slash

## Validation

- Atlas: v2, 1536 × 2288, 8 columns × 11 rows
- ChatGPT Pets preflight: `valid: true`
- Structural atlas validation: passed with no errors or warnings
- Frame extraction QA: passed for all nine standard rows
- Hover lift: 25 px; landing delta: 1 px
- Directional rows and sixteen look directions: preserved and validated
- Active pet ID remains `pet_6ac3f8b452cc8191a468dfc5a4a6298b`

The review-ready atlas is `final/spritesheet-extended.png`. Animated previews are under `previews/final/`; combat previews are under `combat-showcase/previews/`.
