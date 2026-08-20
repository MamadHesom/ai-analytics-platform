package com.analytics.platform.controller;

import com.analytics.platform.dto.AuthDtos;
import com.analytics.platform.service.AuthService;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

/** Authentication endpoints for login and registration. */
@RestController @RequestMapping("/auth") public class AuthController {
    private final AuthService service; public AuthController(AuthService service) { this.service = service; }
    @PostMapping("/login") public AuthDtos.AuthResponse login(@Valid @RequestBody AuthDtos.LoginRequest request) { return service.login(request); }
    @PostMapping("/register") @ResponseStatus(HttpStatus.CREATED) public AuthDtos.AuthResponse register(@Valid @RequestBody AuthDtos.RegisterRequest request) { return service.register(request); }
}
