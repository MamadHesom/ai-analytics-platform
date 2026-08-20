package com.analytics.platform.config;

import org.springframework.boot.context.properties.ConfigurationProperties;

/** Strongly typed JWT settings loaded from environment-backed configuration. */
@ConfigurationProperties(prefix = "analytics.jwt")
public record JwtConfig(String secret, long expirationMs) {}
