package com.analytics.platform.controller;

import com.analytics.platform.dto.UserDtos;
import com.analytics.platform.service.UserService;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

/** User profile endpoints. */
@RestController @RequestMapping("/users") public class UserController {
    private final UserService service; public UserController(UserService service) { this.service = service; }
    @GetMapping("/me") public UserDtos.UserResponse me(Authentication authentication) { return service.profile(authentication.getName()); }
}
