package com.analytics.platform.model;

import java.util.Set;

/** Immutable user aggregate used by the authentication boundary. */
public record User(String id, String email, String displayName, String passwordHash, Set<String> roles) {
    public User { roles = Set.copyOf(roles); }
}
