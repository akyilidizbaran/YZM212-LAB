from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

import numpy as np
from hmmlearn.hmm import CategoricalHMM

OBSERVATION_MAP = {"High": 0, "Low": 1}
STATE_NAMES = {
    "EV": ["e", "v"],
    "OKUL": ["o", "k", "u", "l"],
}


def encode_sequence(observations: List[str]) -> np.ndarray:
    encoded = [[OBSERVATION_MAP[item]] for item in observations]
    return np.asarray(encoded, dtype=int)


def build_ev_model() -> CategoricalHMM:
    model = CategoricalHMM(n_components=2, init_params="", params="")
    model.n_features = len(OBSERVATION_MAP)
    model.startprob_ = np.array([1.0, 0.0])
    model.transmat_ = np.array(
        [
            [0.6, 0.4],
            [0.2, 0.8],
        ]
    )
    model.emissionprob_ = np.array(
        [
            [0.7, 0.3],
            [0.1, 0.9],
        ]
    )
    return model


def build_okul_model() -> CategoricalHMM:
    model = CategoricalHMM(n_components=4, init_params="", params="")
    model.n_features = len(OBSERVATION_MAP)
    model.startprob_ = np.array([1.0, 0.0, 0.0, 0.0])
    model.transmat_ = np.array(
        [
            [0.55, 0.45, 0.00, 0.00],
            [0.00, 0.55, 0.45, 0.00],
            [0.00, 0.00, 0.55, 0.45],
            [0.00, 0.00, 0.00, 1.00],
        ]
    )
    model.emissionprob_ = np.array(
        [
            [0.25, 0.75],
            [0.80, 0.20],
            [0.35, 0.65],
            [0.85, 0.15],
        ]
    )
    return model


MODELS = {
    "EV": build_ev_model(),
    "OKUL": build_okul_model(),
}


def score_models(observations: List[str]) -> Dict[str, float]:
    encoded = encode_sequence(observations)
    return {name: model.score(encoded) for name, model in MODELS.items()}


def classify_sequence(observations: List[str]) -> Dict[str, object]:
    scores = score_models(observations)
    predicted_word = max(scores, key=scores.get)
    return {
        "observations": observations,
        "scores": scores,
        "predicted_word": predicted_word,
    }


def decode_ev_viterbi(observations: List[str]) -> Dict[str, object]:
    transition = np.array([[0.6, 0.4], [0.2, 0.8]])
    emission = np.array([[0.7, 0.3], [0.1, 0.9]])
    start = np.array([1.0, 0.0])
    obs = [OBSERVATION_MAP[item] for item in observations]

    delta = np.zeros((len(obs), 2))
    psi = np.zeros((len(obs), 2), dtype=int)

    delta[0] = start * emission[:, obs[0]]
    for t in range(1, len(obs)):
        for j in range(2):
            candidates = delta[t - 1] * transition[:, j]
            psi[t, j] = int(np.argmax(candidates))
            delta[t, j] = np.max(candidates) * emission[j, obs[t]]

    best_last_state = int(np.argmax(delta[-1]))
    best_path = [best_last_state]
    for t in range(len(obs) - 1, 0, -1):
        best_path.insert(0, int(psi[t, best_path[0]]))

    state_labels = STATE_NAMES["EV"]
    return {
        "observations": observations,
        "delta": delta.tolist(),
        "psi": psi.tolist(),
        "best_probability": float(delta[-1, best_last_state]),
        "best_path": [state_labels[index] for index in best_path],
    }


def load_sample_data() -> Dict[str, object]:
    data_path = Path(__file__).resolve().parents[1] / "data" / "sample_data.json"
    return json.loads(data_path.read_text(encoding="utf-8"))


def format_scores(scores: Dict[str, float]) -> str:
    return ", ".join(f"{name}={value:.4f}" for name, value in scores.items())


def run_demo() -> None:
    sample_data = load_sample_data()

    print("Viterbi cozumu [High, Low]:")
    viterbi = decode_ev_viterbi(["High", "Low"])
    print(f"En olasi yol: {' -> '.join(viterbi['best_path'])}")
    print(f"Nihai olasilik: {viterbi['best_probability']:.4f}")
    print()

    print("Ornek siniflandirmalar:")
    for sequence in sample_data["test_sequences"]:
        result = classify_sequence(sequence)
        score_text = format_scores(result["scores"])
        print(
            f"Gozlem={sequence} | Tahmin={result['predicted_word']} | "
            f"Skorlar: {score_text}"
        )


if __name__ == "__main__":
    run_demo()
