#!/usr/bin/env python3
"""
Bayesian brightness inference for YZM212 Lab 4.

This module is the single source of truth for:
- synthetic data generation
- log-likelihood / log-prior / log-posterior definitions
- emcee-based MCMC execution
- posterior summaries
- figure generation
- narrative analysis text used by both the notebook and the PDF report
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import corner
import emcee
import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt


PROJECT_DIR = Path(__file__).resolve().parent
FIGURES_DIR = PROJECT_DIR / "figures"
REPORT_DIR = PROJECT_DIR / "report"

TRUE_MU = 150.0
TRUE_SIGMA = 10.0
N_OBS = 50
SEED = 42
INITIAL = np.array([140.0, 5.0])
N_WALKERS = 32
N_STEPS = 2000
BURN_IN = 500
THIN = 15

PARAMETER_NAMES = ("mu", "sigma")
PRIOR_LABELS = {
    "wide": "0 < mu < 300 and 0 < sigma < 50",
    "narrow_mu": "100 < mu < 110 and 0 < sigma < 50",
}
SCENARIO_CONFIGS = {
    "base": {
        "label": "Temel senaryo (n=50, genis prior)",
        "prior_mode": "wide",
        "seed_offset": 101,
    },
    "prior_effect": {
        "label": "Prior etkisi (n=50, dar mu prior'i)",
        "prior_mode": "narrow_mu",
        "seed_offset": 202,
    },
    "sample_size": {
        "label": "Veri miktari etkisi (n=5, genis prior)",
        "prior_mode": "wide",
        "seed_offset": 303,
    },
}


@dataclass
class ParameterSummary:
    name: str
    truth: float
    median: float
    lower: float
    upper: float
    abs_error: float
    ci_width: float


@dataclass
class ScenarioResult:
    key: str
    label: str
    prior_mode: str
    n_obs: int
    data: np.ndarray
    chain: np.ndarray
    flat_samples: np.ndarray
    acceptance_fraction: float
    mu_summary: ParameterSummary
    sigma_summary: ParameterSummary
    correlation: float


def ensure_output_dirs() -> None:
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)


def generate_observations(
    seed: int = SEED,
    true_mu: float = TRUE_MU,
    true_sigma: float = TRUE_SIGMA,
    n_obs: int = N_OBS,
) -> np.ndarray:
    rng = np.random.RandomState(seed)
    return true_mu + true_sigma * rng.randn(n_obs)


def log_likelihood(theta: tuple[float, float], data: np.ndarray) -> float:
    mu, sigma = theta
    if sigma <= 0:
        return -np.inf
    residual = (data - mu) / sigma
    return -0.5 * np.sum(residual**2 + np.log(2 * np.pi * sigma**2))


def log_prior(theta: tuple[float, float], prior_mode: str = "wide") -> float:
    mu, sigma = theta
    if sigma <= 0:
        return -np.inf

    if prior_mode == "wide":
        if 0 < mu < 300 and 0 < sigma < 50:
            return 0.0
        return -np.inf

    if prior_mode == "narrow_mu":
        if 100 < mu < 110 and 0 < sigma < 50:
            return 0.0
        return -np.inf

    raise ValueError(f"Unknown prior mode: {prior_mode}")


def log_probability(
    theta: tuple[float, float],
    data: np.ndarray,
    prior_mode: str = "wide",
) -> float:
    lp = log_prior(theta, prior_mode=prior_mode)
    if not np.isfinite(lp):
        return -np.inf
    return lp + log_likelihood(theta, data)


def initialize_walkers(
    initial: np.ndarray = INITIAL,
    n_walkers: int = N_WALKERS,
    seed: int = SEED,
) -> np.ndarray:
    rng = np.random.default_rng(seed)
    return initial + 1e-4 * rng.standard_normal((n_walkers, len(initial)))


def initial_for_prior(prior_mode: str) -> np.ndarray:
    if prior_mode == "narrow_mu":
        return np.array([105.0, 10.0])
    return INITIAL.copy()


def summarize_parameter(samples: np.ndarray, index: int, truth: float, name: str) -> ParameterSummary:
    lower, median, upper = np.percentile(samples[:, index], [16, 50, 84])
    return ParameterSummary(
        name=name,
        truth=float(truth),
        median=float(median),
        lower=float(lower),
        upper=float(upper),
        abs_error=float(abs(median - truth)),
        ci_width=float(upper - lower),
    )


def run_sampler(
    data: np.ndarray,
    prior_mode: str,
    seed: int,
    initial: np.ndarray | None = None,
    n_walkers: int = N_WALKERS,
    n_steps: int = N_STEPS,
    burn_in: int = BURN_IN,
    thin: int = THIN,
) -> tuple[emcee.EnsembleSampler, np.ndarray]:
    np.random.seed(seed)
    if initial is None:
        initial = initial_for_prior(prior_mode)
    pos = initialize_walkers(initial=initial, n_walkers=n_walkers, seed=seed)
    sampler = emcee.EnsembleSampler(
        n_walkers,
        len(initial),
        log_probability,
        args=(data, prior_mode),
    )
    sampler.run_mcmc(pos, n_steps, progress=False)
    flat_samples = sampler.get_chain(discard=burn_in, thin=thin, flat=True)
    return sampler, flat_samples


def run_scenario(
    key: str,
    data: np.ndarray,
    n_obs: int,
    prior_mode: str,
    seed: int,
) -> ScenarioResult:
    sampler, flat_samples = run_sampler(
        data=data,
        prior_mode=prior_mode,
        seed=seed,
    )
    chain = sampler.get_chain()
    mu_summary = summarize_parameter(flat_samples, 0, TRUE_MU, "mu")
    sigma_summary = summarize_parameter(flat_samples, 1, TRUE_SIGMA, "sigma")
    correlation = float(np.corrcoef(flat_samples[:, 0], flat_samples[:, 1])[0, 1])
    return ScenarioResult(
        key=key,
        label=SCENARIO_CONFIGS[key]["label"],
        prior_mode=prior_mode,
        n_obs=n_obs,
        data=data,
        chain=chain,
        flat_samples=flat_samples,
        acceptance_fraction=float(np.mean(sampler.acceptance_fraction)),
        mu_summary=mu_summary,
        sigma_summary=sigma_summary,
        correlation=correlation,
    )


def scenario_table_rows(result: ScenarioResult) -> list[dict[str, float | str]]:
    return [
        {
            "Degisken": "mu (Parlaklik)",
            "Gercek Deger": result.mu_summary.truth,
            "Tahmin Edilen (Median)": result.mu_summary.median,
            "Alt Sinir (%16)": result.mu_summary.lower,
            "Ust Sinir (%84)": result.mu_summary.upper,
            "Mutlak Hata": result.mu_summary.abs_error,
        },
        {
            "Degisken": "sigma (Hata Payi)",
            "Gercek Deger": result.sigma_summary.truth,
            "Tahmin Edilen (Median)": result.sigma_summary.median,
            "Alt Sinir (%16)": result.sigma_summary.lower,
            "Ust Sinir (%84)": result.sigma_summary.upper,
            "Mutlak Hata": result.sigma_summary.abs_error,
        },
    ]


def format_table_markdown(rows: list[dict[str, float | str]]) -> str:
    header = (
        "| Degisken | Gercek Deger | Tahmin Edilen (Median) | Alt Sinir (%16) | "
        "Ust Sinir (%84) | Mutlak Hata |"
    )
    separator = "| --- | ---: | ---: | ---: | ---: | ---: |"
    body = []
    for row in rows:
        body.append(
            "| {Degisken} | {Gercek Deger:.3f} | {Tahmin Edilen (Median):.3f} | "
            "{Alt Sinir (%16):.3f} | {Ust Sinir (%84):.3f} | {Mutlak Hata:.3f} |".format(
                **row
            )
        )
    return "\n".join([header, separator, *body])


def save_corner_plot(result: ScenarioResult, output_path: Path, title: str) -> None:
    fig = corner.corner(
        result.flat_samples,
        labels=[r"$\mu$ (Parlaklik)", r"$\sigma$ (Hata)"],
        truths=[TRUE_MU, TRUE_SIGMA],
        show_titles=True,
        title_fmt=".2f",
    )
    fig.suptitle(title, y=1.02)
    fig.savefig(output_path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def save_trace_plot(result: ScenarioResult, output_path: Path) -> None:
    labels = ["mu", "sigma"]
    fig, axes = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
    chain = result.chain
    steps = np.arange(chain.shape[0])

    for index, axis in enumerate(axes):
        axis.plot(steps, chain[:, :, index], color="#1f77b4", alpha=0.18, linewidth=0.8)
        axis.set_ylabel(labels[index])
        axis.grid(alpha=0.2)

    axes[-1].set_xlabel("MCMC adimi")
    fig.suptitle("Temel senaryo icin trace plot", y=0.98)
    fig.tight_layout()
    fig.savefig(output_path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def save_comparison_summary(results: dict[str, ScenarioResult], output_path: Path) -> None:
    scenario_order = ["base", "prior_effect", "sample_size"]
    y_labels = [results[key].label for key in scenario_order]
    y_positions = np.arange(len(scenario_order))

    fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharey=True)
    summaries = [
        ("mu", "Parlaklik (mu)", TRUE_MU),
        ("sigma", "Hata Payi (sigma)", TRUE_SIGMA),
    ]

    for axis, (param_name, title, truth) in zip(axes, summaries):
        medians = []
        lower_errors = []
        upper_errors = []
        for key in scenario_order:
            summary = getattr(results[key], f"{param_name}_summary")
            medians.append(summary.median)
            lower_errors.append(summary.median - summary.lower)
            upper_errors.append(summary.upper - summary.median)

        axis.errorbar(
            medians,
            y_positions,
            xerr=[lower_errors, upper_errors],
            fmt="o",
            capsize=4,
            color="#0b5cad",
        )
        axis.axvline(truth, color="#d62728", linestyle="--", linewidth=1.2, label="Gercek deger")
        axis.set_title(title)
        axis.set_yticks(y_positions, labels=y_labels)
        axis.grid(alpha=0.25)
        axis.legend(loc="lower right")

    fig.suptitle("Posterior median ve guven araliklari karsilastirmasi", y=1.02)
    fig.tight_layout()
    fig.savefig(output_path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def describe_accuracy(base: ScenarioResult) -> str:
    sample_mean = float(np.mean(base.data))
    sample_std = float(np.std(base.data, ddof=0))
    return (
        f"Temel senaryoda mu icin mutlak hata {base.mu_summary.abs_error:.3f}, "
        f"sigma icin mutlak hata {base.sigma_summary.abs_error:.3f} bulundu. "
        f"Uretilen verinin ornek ortalamasi {sample_mean:.3f} ve ornek standart sapmasi "
        f"{sample_std:.3f} oldugundan posterior merkezleri de bu gozlenen degerlere yaklasti. "
        "Bu, Bayesyen modelin gurultulu ama sonlu sayida gozleme uygun davrandigini gosteriyor."
    )


def describe_prior_effect(base: ScenarioResult, narrow: ScenarioResult) -> str:
    shift = narrow.mu_summary.median - base.mu_summary.median
    return (
        f"Dar prior senaryosunda mu mediani temel senaryoya gore {shift:.3f} birim kaydi. "
        "Bunun nedeni, likelihood veriyi 150 civarina cekse bile prior'in mu'yu 100-110 "
        "bandinda tutmaya zorlamasi. Veri prior ile celistikce posterior, iki bilgi kaynagi "
        f"arasinda bir uzlasma noktasina gelir; ayni nedenle sigma tahmini de {narrow.sigma_summary.median:.3f} "
        "seviyesine siserek yanlis merkezlenmis modeli telafi etmeye calisir."
    )


def describe_sample_size_effect(base: ScenarioResult, small: ScenarioResult) -> str:
    mu_ratio = small.mu_summary.ci_width / base.mu_summary.ci_width
    sigma_ratio = small.sigma_summary.ci_width / base.sigma_summary.ci_width
    return (
        f"n_obs=5 senaryosunda mu icin guven araligi genisligi {mu_ratio:.2f}x, "
        f"sigma icin {sigma_ratio:.2f}x buyudu. Daha az veri, posterior dagilimin "
        "daralmasi icin yeterli kanit saglayamadigindan belirsizlik artiyor."
    )


def describe_precision(base: ScenarioResult) -> str:
    mu_relative = 100.0 * base.mu_summary.ci_width / base.mu_summary.truth
    sigma_relative = 100.0 * base.sigma_summary.ci_width / base.sigma_summary.truth
    return (
        f"Temel senaryoda mu icin goreli guven araligi genisligi %{mu_relative:.2f}, "
        f"sigma icin %{sigma_relative:.2f}. Ortalama tahmini, verinin merkezine "
        "dogrudan bagli oldugu ve standart hata yaklasik sigma/sqrt(n) ile azaldigi icin "
        "genellikle daha kesin olur. Varyans veya sigma tahmini ise karesel sapmalara dayandigindan "
        "ve uc degerlere daha hassas oldugundan goreli olarak daha genis posterior verir. n=50 bu farki belirginlestirir."
    )


def describe_correlation(base: ScenarioResult) -> str:
    corr = base.correlation
    if abs(corr) < 0.1:
        relation = "belirgin bir korelasyon gostermiyor"
        geometry = "neredeyse dik"
    elif corr > 0:
        relation = "zayif pozitif korelasyon gosteriyor"
        geometry = "hafif saga egik"
    else:
        relation = "zayif negatif korelasyon gosteriyor"
        geometry = "hafif sola egik"

    return (
        f"Temel corner plot'taki ortak dagilim {geometry} bir elips beklentisine uygundur ve "
        f"ornek korelasyon katsayisi {corr:.3f} bulundu. Bu, parlaklik ve hata tahminlerinin {relation} "
        "anlamina gelir; yani bir parametredeki degisim digerini tamamen bagimsiz birakmiyor ama guclu bir bagimlilik da yok."
    )


def build_analysis_text(results: dict[str, ScenarioResult]) -> dict[str, str]:
    base = results["base"]
    narrow = results["prior_effect"]
    small = results["sample_size"]
    return {
        "accuracy": describe_accuracy(base),
        "prior_effect": describe_prior_effect(base, narrow),
        "sample_size": describe_sample_size_effect(base, small),
        "precision": describe_precision(base),
        "correlation": describe_correlation(base),
    }


def run_full_analysis() -> dict[str, object]:
    ensure_output_dirs()

    full_data = generate_observations()
    scenario_inputs = {
        "base": full_data,
        "prior_effect": full_data,
        "sample_size": full_data[:5],
    }

    results: dict[str, ScenarioResult] = {}
    for key, config in SCENARIO_CONFIGS.items():
        results[key] = run_scenario(
            key=key,
            data=scenario_inputs[key],
            n_obs=len(scenario_inputs[key]),
            prior_mode=config["prior_mode"],
            seed=SEED + config["seed_offset"],
        )

    figure_paths = {
        "base_corner": FIGURES_DIR / "base_corner_plot.png",
        "base_trace": FIGURES_DIR / "base_trace_plot.png",
        "prior_corner": FIGURES_DIR / "prior_effect_corner_plot.png",
        "sample_size_corner": FIGURES_DIR / "sample_size_effect_corner_plot.png",
        "comparison": FIGURES_DIR / "comparison_summary.png",
    }

    save_corner_plot(results["base"], figure_paths["base_corner"], results["base"].label)
    save_trace_plot(results["base"], figure_paths["base_trace"])
    save_corner_plot(results["prior_effect"], figure_paths["prior_corner"], results["prior_effect"].label)
    save_corner_plot(results["sample_size"], figure_paths["sample_size_corner"], results["sample_size"].label)
    save_comparison_summary(results, figure_paths["comparison"])

    analysis_text = build_analysis_text(results)
    base_rows = scenario_table_rows(results["base"])

    return {
        "constants": {
            "true_mu": TRUE_MU,
            "true_sigma": TRUE_SIGMA,
            "n_obs": N_OBS,
            "seed": SEED,
            "initial": INITIAL.tolist(),
            "n_walkers": N_WALKERS,
            "n_steps": N_STEPS,
            "burn_in": BURN_IN,
            "thin": THIN,
        },
        "data_preview": full_data[:10].tolist(),
        "results": results,
        "analysis_text": analysis_text,
        "base_table_rows": base_rows,
        "base_table_markdown": format_table_markdown(base_rows),
        "figure_paths": figure_paths,
    }


def print_console_summary(bundle: dict[str, object]) -> None:
    results = bundle["results"]
    base = results["base"]
    print("1.4 BayesianBrightnessInference")
    print(f"Temel senaryo acceptance fraction: {base.acceptance_fraction:.3f}")
    print(bundle["base_table_markdown"])
    print()
    for key, text in bundle["analysis_text"].items():
        print(f"[{key}] {text}")


if __name__ == "__main__":
    print_console_summary(run_full_analysis())
