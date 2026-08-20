package com.analytics.platform.service;

import com.analytics.platform.dto.PipelineDtos;
import com.analytics.platform.factory.PipelineTaskFactory;
import com.analytics.platform.model.Pipeline;
import com.analytics.platform.observer.PipelineEventListener;
import java.time.Instant;
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;
import org.springframework.stereotype.Service;

/** Orchestrates pipeline lifecycle and delegates work through Factory and Strategy patterns. */
@Service public class PipelineOrchestrationService {
    private final PipelineTaskFactory factory; private final PipelineEventListener listener; private final Map<String, Pipeline> pipelines = new ConcurrentHashMap<>();
    public PipelineOrchestrationService(PipelineTaskFactory factory, PipelineEventListener listener) { this.factory = factory; this.listener = listener; }
    public Pipeline create(PipelineDtos.CreatePipelineRequest request) {
        var now = Instant.now(); var pipeline = new Pipeline(UUID.randomUUID().toString(), request.name(), request.strategy(), "RUNNING", 35, factory.resolve(request.strategy()).process(request.parameters()), now, now);
        pipelines.put(pipeline.id(), pipeline); listener.onPipelineCreated(pipeline); return pipeline;
    }
    public Pipeline find(String id) { var p = pipelines.get(id); if (p == null) throw new IllegalArgumentException("Pipeline not found: " + id); return p; }
    public java.util.Collection<Pipeline> list() { return pipelines.values(); }
}
