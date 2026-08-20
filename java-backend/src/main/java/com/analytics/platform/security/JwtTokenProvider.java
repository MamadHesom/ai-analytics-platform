package com.analytics.platform.security;

import com.analytics.platform.config.JwtConfig;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.security.Keys;
import java.nio.charset.StandardCharsets;
import java.util.Date;
import org.springframework.stereotype.Component;

/** Creates and validates signed JWT access tokens. */
@Component
public class JwtTokenProvider {
    private final JwtConfig config;
    public JwtTokenProvider(JwtConfig config) { this.config = config; }
    private javax.crypto.SecretKey key() { return Keys.hmacShaKeyFor(config.secret().getBytes(StandardCharsets.UTF_8)); }
    public String createToken(String subject, java.util.Set<String> roles) {
        Date now = new Date(), expiry = new Date(now.getTime() + config.expirationMs());
        return Jwts.builder().subject(subject).claim("roles", roles).issuedAt(now).expiration(expiry).signWith(key()).compact();
    }
    public String getSubject(String token) { return Jwts.parser().verifyWith(key()).build().parseSignedClaims(token).getPayload().getSubject(); }
    public boolean isValid(String token) { try { Jwts.parser().verifyWith(key()).build().parseSignedClaims(token); return true; } catch (RuntimeException ex) { return false; } }
}
