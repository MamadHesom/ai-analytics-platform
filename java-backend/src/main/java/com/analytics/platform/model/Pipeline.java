package com.analytics.platform.model;

import java.time.Instant;
import java.util.Map;

/** Describes an analytics pipeline execution and its observable lifecycle state. */
public record Pipeline(String id, String name, String strategy, String status, double progress,
                       Map<String, Object> metrics, Instant createdAt, Instant updatedAt) {
    public Pipeline { metrics = Map.copyOf(metrics); }
}
