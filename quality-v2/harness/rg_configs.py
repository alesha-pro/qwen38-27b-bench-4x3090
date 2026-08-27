"""Reasoning Gym generator configs for quant-bench-v2.

v1 = library defaults. BF16 xhigh saturated five families at 0.97-1.00, so
those five get a harder v2 config. Difficulty is moved by GENERATOR
PARAMETERS for the whole family, never by hand-picking items BF16 failed.

Families already inside the 40-80% band (jugs, propositional_logic,
number_sequence, word_ladder, rush_hour) keep v1 untouched.
"""

RG_V1 = {  # library defaults, kept explicit for provenance
    "cryptarithm": {},
    "graph_color": {},
    "jugs": {},
    "word_ladder": {},
    "number_sequence": {},
    "shortest_path": {},
    "zebra_puzzles": {},
    "propositional_logic": {},
    "rush_hour": {},
    "intermediate_integration": {},
}

# v2: harder settings for the saturated five (BF16 xhigh pooled rate in
# brackets = what we are moving away from).
RG_V2 = dict(RG_V1)
RG_V2.update({
    # [1.00] 2-3 words -> 3-5 words: more letters, tighter constraints
    "cryptarithm": {"min_words": 3, "max_words": 5},
    # [1.00] 10 vertices p=0.1 -> 20 vertices p=0.15, same 3 colors
    "graph_color": {"min_num_vertices": 18, "max_num_vertices": 22,
                    "edge_probability": 0.15, "num_colors": 3},
    # [1.00] all 8 types deg<=3 -> only the hard types, higher degrees.
    # problem_type_weights must match problem_types length (validator).
    "intermediate_integration": {
        "problem_types": ("cyclic", "repeated_parts", "log_inverse_trig",
                          "polynomial_exp_trig"),
        "problem_type_weights": [0.25, 0.25, 0.25, 0.25],
        "min_poly_degree": 2, "max_poly_degree": 5,
        "min_linear_degree": 3, "max_linear_degree": 6,
    },
    # [1.00] 4x4 -> 6x6 grid of people/characteristics
    "zebra_puzzles": {"num_people": 6, "num_characteristics": 6},
    # [0.97] 5-8 grid p=0.4 -> 12-16 grid p=0.25.
    # Density is LOWERED on purpose: the bigger grid supplies the difficulty,
    # while p=0.45 made 9/12 grids unsolvable and "infeasible" a guessable
    # modal answer. p=0.25 keeps infeasible near the v1 share (~1/6).
    "shortest_path": {"min_rows": 12, "max_rows": 16, "min_cols": 12,
                      "max_cols": 16, "p_blocked": 0.25},
})

TUNED_FAMILIES = [f for f in RG_V2 if RG_V2[f] != RG_V1[f]]

# Two families are too HARD for a paired-retention design: at BF16 xhigh
# word_ladder yielded 1 reliably-passed task out of 12 and rush_hour 3 of 12,
# so almost everything we paid for was unusable. Ease them instead of
# dropping the reasoning types they cover.
RG_EASE = {
    # unbounded chain (-1) -> 3..5 steps
    "word_ladder": {"min_chain_length": 3, "max_chain_length": 5},
    # up to 50 required moves -> at most 12
    "rush_hour": {"min_moves": 1, "max_moves": 12},
}

# Final configs: defaults, overridden by the tuned/eased sets. This is what
# freeze_final.py reads. Updated once calibration picks the winners.
RG_FINAL = dict(RG_V2)
RG_FINAL.update(RG_EASE)
