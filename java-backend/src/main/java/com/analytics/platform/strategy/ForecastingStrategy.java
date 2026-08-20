package com.analytics.platform.strategy;

import java.util.Map;
import org.springframework.stereotype.Component;

/** Forecasting strategy used for time-series pipeline requests. */
@Component public class ForecastingStrategy implements ProcessingStrategy {
    public String key() { return "forecasting"; }
    public Map<String, Object> process(Map<String, Object> parameters) { return Map.of("forecastHorizon", parameters.getOrDefault("horizon", 14), "mape", 0.081, "model", "gradient-boosted-regressor"); }
}
