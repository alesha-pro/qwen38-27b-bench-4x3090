import time
from multiprocessing import Process, Queue

import reasoning_gym

LEVELS = {
    "graph_color": [
        ("L2", dict(min_num_vertices=22, max_num_vertices=26,
                    edge_probability=0.25, num_colors=3)),
        ("L2b", dict(min_num_vertices=24, max_num_vertices=28,
                     edge_probability=0.30, num_colors=3)),
    ],
    "zebra_puzzles": [
        ("L2", dict(num_people=7, num_characteristics=7)),
        ("L3", dict(num_people=8, num_characteristics=8)),
    ],
    "cryptarithm": [
        ("L2", dict(min_words=5, max_words=7)),
        ("L3", dict(min_words=8, max_words=10)),
    ],
    "shortest_path": [
        ("L2", dict(min_rows=20, max_rows=24, min_cols=20, max_cols=24,
                    p_blocked=0.25)),
        ("L3", dict(min_rows=28, max_rows=32, min_cols=28, max_cols=32,
                    p_blocked=0.28)),
    ],
    "intermediate_integration": [
        ("L2", dict(problem_types=("cyclic", "repeated_parts"),
                    problem_type_weights=[0.5, 0.5],
                    min_poly_degree=3, max_poly_degree=6,
                    min_linear_degree=4, max_linear_degree=8)),
    ],
    "number_sequence": [
        ("L2", dict(min_terms=6, max_terms=10, max_complexity=5,
                    min_value=-500, max_value=500)),
    ],
    "propositional_logic": [
        ("L2", dict(min_vars=4, max_vars=6, min_statements=4,
                    max_statements=6, min_complexity=2, max_complexity=4)),
    ],
    "jugs": [("L2", dict(num_jugs=4, difficulty=15))],
}


def gen(fam, cfg, q):
    items = list(reasoning_gym.create_dataset(fam, size=12, seed=20260822,
                                              **cfg))
    lens = [len(x["question"]) for x in items]
    inf = sum(1 for x in items
              if str(x["answer"]).strip().lower() == "infeasible")
    q.put((sorted(lens)[6], max(lens), inf))


if __name__ == "__main__":
    for fam, lv in LEVELS.items():
        for tag, cfg in lv:
            q = Queue()
            p = Process(target=gen, args=(fam, cfg, q))
            t0 = time.time()
            p.start()
            p.join(90)
            if p.is_alive():
                p.terminate()
                print(f"{fam:26} {tag}: GEN TIMEOUT >90s -- unusable",
                      flush=True)
            elif q.empty():
                print(f"{fam:26} {tag}: FAILED", flush=True)
            else:
                med, mx, inf = q.get()
                print(f"{fam:26} {tag}: {time.time()-t0:5.1f}s  prompt med "
                      f"{med:6} max {mx:7}" +
                      (f"  infeasible {inf}/12" if inf else ""), flush=True)
