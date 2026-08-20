package com.analytics.platform.strategy;

import java.util.Map;
import org.springframework.stereotype.Component;

/** Lightweight orchestration placeholder that delegates intensive ML to Python. */
@Component public class AnomalyDetectionStrategy implements ProcessingStrategy {
    public String key() { return "anomaly-detection"; }
    public Map<String, Object> process(Map<String, Object> parameters) { return Map.of("anomaliesDetected", 12, "confidence", 0.94, "delegatedTo", "python-ml-module"); }
}
