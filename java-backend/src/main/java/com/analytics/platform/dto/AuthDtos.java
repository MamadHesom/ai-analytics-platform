package com.analytics.platform.dto;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;

/** Request and response contracts for authentication. */
public final class AuthDtos {
    private AuthDtos() {}
    public record LoginRequest(@Email @NotBlank String email, @NotBlank String password) {}
    public record RegisterRequest(@Email @NotBlank String email, @NotBlank String displayName, @NotBlank String password) {}
    public record AuthResponse(String token, String tokenType, String userId, String displayName, String email) {}
}
