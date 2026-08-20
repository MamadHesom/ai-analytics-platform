package com.analytics.platform.controller;

import com.analytics.platform.dto.PipelineDtos;
import com.analytics.platform.model.Pipeline;
import com.analytics.platform.service.PipelineOrchestrationService;
import jakarta.validation.Valid;
import java.util.Collection;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

/** Pipeline execution endpoints consumed by the dashboard. */
@RestController @RequestMapping("/pipelines") public class PipelineController {
    private final PipelineOrchestrationService service; public PipelineController(PipelineOrchestrationService service) { this.service = service; }
    @PostMapping @ResponseStatus(HttpStatus.ACCEPTED) public Pipeline create(@Valid @RequestBody PipelineDtos.CreatePipelineRequest request) { return service.create(request); }
    @GetMapping public Collection<Pipeline> list() { return service.list(); }
    @GetMapping("/{id}") public Pipeline get(@PathVariable String id) { return service.find(id); }
}
