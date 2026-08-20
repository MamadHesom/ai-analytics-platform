package com.analytics.platform.factory;

import com.analytics.platform.strategy.ProcessingStrategy;
import java.util.Map;
import java.util.function.Function;
import java.util.stream.Collectors;
import org.springframework.stereotype.Component;

/** Factory pattern for resolving a named pipeline task without controller coupling. */
@Component public class PipelineTaskFactory {
    private final Map<String, ProcessingStrategy> strategies;
    public PipelineTaskFactory(java.util.List<ProcessingStrategy> strategies) { this.strategies = strategies.stream().collect(Collectors.toUnmodifiableMap(ProcessingStrategy::key, Function.identity())); }
    public ProcessingStrategy resolve(String key) { var strategy = strategies.get(key); if (strategy == null) throw new IllegalArgumentException("Unsupported strategy: " + key); return strategy; }
}
