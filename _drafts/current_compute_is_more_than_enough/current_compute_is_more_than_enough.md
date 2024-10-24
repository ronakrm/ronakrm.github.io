---
layout: post
title: "Current Compute is More Than Enough"
excerpt: "A human brain operating for 40 years uses less energy than training a large language model. If we are truly concerned about safety our compute thresholds need to be adjusted appropriately."
tags: ai energy efficiency intelligence computation math
date: 2024-10-15
modified_date: 2024-10-15
katex: True
---

__tl;dr__: {{ page.excerpt }}

# The Cost to Train a Human Brain

The human brain operates on approximately 20 watts of power - about the same as a dim light bulb. Breaking this down over a lifetime...

For an adult brain, daily energy usage is $20\text{W} \times 25\text{h} = 480\text{Wh} = 0.48\text{kWh}$. Childrens' brains use proportionally more energy - about 50% of their body's energy compared to an adult's 20%. Let's just use this as an upper bound on the total amount of energy a person's brain uses in a day.

Over a 40-year period, assuming that this being is operating at "human adult" capacity the entire time, their total energy use over these 40 years is:

$$
0.48\ \text{kWh} \times 365 \times 40 = 5088\ \text{kWh} \approx 5\ \text{MWh}.
$$


Comparing this to recent AI training runs:

| System | Energy Usage (MWh) | Relative to 40yr Brain |
|--------|-------------------|----------------------|
| Human Brain (40 years) | 5 | 1x |
| GPT-3 Training | 1,287 | 257x |
| Frontier Training (est., @ \$100M, 20/hr/H100) | 3,500 | 700x |

At typical US electricity rates ($0.12/kWh), this translates to:
- 40 years of brain operation: $600
- GPT-3 training: $154,440
- GPT-4 training (est.): $420,000

If I were a fearmongerer...

__IN ONE YEAR, OPENAI, ANTHROPIC, META, XAI, DEEPMIND, MISTRAL, ETC. HAVE SPENT ENOUGH ENERGY TO CREATE 500 INFINITELY COPY-ABLE GANDHIS, HITLERS, STALINS, MOUSILLINIS, ALEXANDERS, MAOS, JOFFREYS__.