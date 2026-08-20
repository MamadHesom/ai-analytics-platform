package com.analytics.platform.service;

import com.analytics.platform.dto.AuthDtos;
import com.analytics.platform.model.User;
import com.analytics.platform.repository.UserRepository;
import com.analytics.platform.security.JwtTokenProvider;
import java.util.Set;
import java.util.UUID;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

/** Coordinates registration, credential verification, and token issuance. */
@Service
public class AuthService {
    private final UserRepository users; private final PasswordEncoder encoder; private final JwtTokenProvider tokens;
    public AuthService(UserRepository users, PasswordEncoder encoder, JwtTokenProvider tokens) { this.users = users; this.encoder = encoder; this.tokens = tokens; }
    public AuthDtos.AuthResponse login(AuthDtos.LoginRequest request) {
        User user = users.findByEmail(request.email()).filter(u -> encoder.matches(request.password(), u.passwordHash())).orElseThrow(() -> new IllegalArgumentException("Invalid credentials"));
        return new AuthDtos.AuthResponse(tokens.createToken(user.email(), user.roles()), "Bearer", user.id(), user.displayName(), user.email());
    }
    public AuthDtos.AuthResponse register(AuthDtos.RegisterRequest request) {
        if (users.existsByEmail(request.email())) throw new IllegalArgumentException("Email is already registered");
        User user = users.save(new User(UUID.randomUUID().toString(), request.email(), request.displayName(), encoder.encode(request.password()), Set.of("ROLE_USER")));
        return new AuthDtos.AuthResponse(tokens.createToken(user.email(), user.roles()), "Bearer", user.id(), user.displayName(), user.email());
    }
}
