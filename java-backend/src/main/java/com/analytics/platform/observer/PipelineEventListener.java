package com.analytics.platform.observer;

import com.analytics.platform.model.Pipeline;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;

/** Observer for pipeline lifecycle events; replaceable with an event bus adapter. */
@Component public class PipelineEventListener {
    private static final Logger log = LoggerFactory.getLogger(PipelineEventListener.class);
    public void onPipelineCreated(Pipeline pipeline) { log.info("pipeline_created id={} strategy={}", pipeline.id(), pipeline.strategy()); }
    public void onPipelineCompleted(Pipeline pipeline) { log.info("pipeline_completed id={} status={}", pipeline.id(), pipeline.status()); }
}
