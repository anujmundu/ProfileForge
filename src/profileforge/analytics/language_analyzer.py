"""Language Distribution Analyzer.

Computes dominant language, language percentages, and diversity index.
"""

import math

from profileforge.analytics.models import LanguageAnalysis
from profileforge.collectors.models import LanguageCollection


class LanguageAnalyzer:
    """Analyzer for language byte distributions."""

    def analyze(self, lang_collection: LanguageCollection) -> LanguageAnalysis:
        """Compute language breakdown percentages and diversity metrics."""
        total_bytes = lang_collection.total_bytes

        if total_bytes == 0 or not lang_collection.language_bytes:
            return LanguageAnalysis(
                dominant_language="",
                language_percentages={},
                total_languages=0,
                diversity_index=0.0,
            )

        # Percentages per language
        percentages: dict[str, float] = {
            lang: round((bytes_cnt / total_bytes) * 100.0, 2)
            for lang, bytes_cnt in sorted(
                lang_collection.language_bytes.items(),
                key=lambda x: (-x[1], x[0]),
            )
        }

        dominant = max(lang_collection.language_bytes.items(), key=lambda x: x[1])[0]

        # Calculate Normalized Shannon Diversity Index (0.0 to 1.0)
        num_langs = len(lang_collection.language_bytes)
        if num_langs <= 1:
            diversity = 0.0
        else:
            entropy = -sum(
                (cnt / total_bytes) * math.log(cnt / total_bytes)
                for cnt in lang_collection.language_bytes.values()
            )
            max_entropy = math.log(num_langs)
            diversity = round(entropy / max_entropy, 2)

        return LanguageAnalysis(
            dominant_language=dominant,
            language_percentages=percentages,
            total_languages=num_langs,
            diversity_index=diversity,
        )
