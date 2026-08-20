package com.analytics.platform.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import java.util.Map;

/** Pipeline creation and status contracts. */
public final class PipelineDtos {
    private PipelineDtos() {}
    public record CreatePipelineRequest(@NotBlank String name, @NotBlank String strategy, @NotNull Map<String, Object> parameters) {}
    public record PipelineResponse(String id, String name, String strategy, String status, double progress, Map<String, Object> metrics) {}
}
