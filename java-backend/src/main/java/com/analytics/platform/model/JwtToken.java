package com.analytics.platform.model;

import java.time.Instant;

/** Access token returned after successful authentication. */
public record JwtToken(String token, String tokenType, Instant expiresAt) {}
