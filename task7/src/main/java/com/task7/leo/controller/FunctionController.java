package com.task7.leo.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;

import java.security.Principal;

@Controller
public class FunctionController {

    @RequestMapping(value = "/home", method = RequestMethod.GET)
    public String home(Principal principal) {

        if (principal == null) {
            return "redirect:/loginView";
        }
        return "home";
    }
}
