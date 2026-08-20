package com.analytics.platform.repository;

import com.analytics.platform.model.User;
import java.util.Optional;
import java.util.concurrent.ConcurrentHashMap;
import java.util.UUID;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Repository;

/** Thread-safe in-memory repository for the portfolio reference implementation. */
@Repository
public class UserRepository {
    private final ConcurrentHashMap<String, User> users = new ConcurrentHashMap<>();
    public UserRepository(PasswordEncoder encoder) {
        var user = new User(UUID.randomUUID().toString(), "demo@analytics.dev", "Demo Analyst", encoder.encode("demo-password"), java.util.Set.of("ROLE_USER"));
        users.put(user.email(), user);
    }
    public Optional<User> findByEmail(String email) { return users.values().stream().filter(u -> u.email().equalsIgnoreCase(email)).findFirst(); }
    public Optional<User> findById(String id) { return Optional.ofNullable(users.get(id)); }
    public User save(User user) { users.put(user.id(), user); return user; }
    public boolean existsByEmail(String email) { return findByEmail(email).isPresent(); }
}
