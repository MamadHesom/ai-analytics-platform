package com.analytics.platform.service;

import com.analytics.platform.dto.UserDtos;
import com.analytics.platform.model.User;
import com.analytics.platform.repository.UserRepository;
import org.springframework.stereotype.Service;

/** Provides safe public profile projections. */
@Service public class UserService {
    private final UserRepository users;
    public UserService(UserRepository users) { this.users = users; }
    public UserDtos.UserResponse profile(String email) { User u = users.findByEmail(email).orElseThrow(); return new UserDtos.UserResponse(u.id(), u.email(), u.displayName(), u.roles()); }
}
