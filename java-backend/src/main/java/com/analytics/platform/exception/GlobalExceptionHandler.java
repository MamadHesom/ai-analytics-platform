package com.analytics.platform.exception;

import java.time.Instant;
import java.util.Map;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.*;

/** Converts domain and validation failures into a consistent error envelope. */
@RestControllerAdvice public class GlobalExceptionHandler {
    @ExceptionHandler(IllegalArgumentException.class) @ResponseStatus(HttpStatus.BAD_REQUEST) public Map<String,Object> badRequest(IllegalArgumentException ex) { return Map.of("timestamp", Instant.now(), "error", ex.getMessage()); }
    @ExceptionHandler(MethodArgumentNotValidException.class) @ResponseStatus(HttpStatus.UNPROCESSABLE_ENTITY) public Map<String,Object> validation(MethodArgumentNotValidException ex) { return Map.of("timestamp", Instant.now(), "error", "Request validation failed"); }
}
