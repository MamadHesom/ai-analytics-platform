package com.analytics.platform.dto;

/** Public user profile contract; credential material is intentionally excluded. */
public final class UserDtos {
    private UserDtos() {}
    public record UserResponse(String id, String email, String displayName, java.util.Set<String> roles) {}
}
