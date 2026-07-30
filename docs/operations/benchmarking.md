# Performance Benchmarking Guide

ProfileForge includes standalone benchmark scripts in `benchmarks/` to measure execution throughput and establish performance baselines.

---

## 1. Running Benchmarks

Run any benchmark script directly:

```bash
# Run full processing pipeline benchmark
python benchmarks/benchmark_pipeline.py

# Run rendering subsystem benchmark
python benchmarks/benchmark_rendering.py

# Run collector subsystem benchmark
python benchmarks/benchmark_collectors.py
```

---

## 2. Environmental Metadata

Benchmark scripts automatically print environmental metadata to ensure reproducible baseline comparisons:

```json
{
  "execution_environment": "Local Development / Automated Test",
  "python_version": "3.13.9",
  "operating_system": "Windows-11",
  "architecture": "AMD64",
  "processor": "Intel64 Family 6 Model 158 Stepping 10, GenuineIntel"
}
```

---

## 3. Standard Performance Baselines

- **Full Pipeline Run**: < 2.0 ms per iteration (in-memory mock pipeline).
- **Rendering Subsystem**: < 1.0 ms per iteration.
- **Collector Snapshot**: < 0.5 ms per iteration.
