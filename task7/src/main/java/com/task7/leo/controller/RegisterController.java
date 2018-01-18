package com.task7.leo.controller;


import com.task7.leo.dto.UserRegisterForm;
import com.task7.leo.service.RegisterService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;

import javax.validation.Valid;
import java.security.Principal;

@Controller
public class RegisterController {

    private final RegisterService registerService;

    @Autowired
    public RegisterController(RegisterService registerService) {
        this.registerService = registerService;
    }

    @RequestMapping(value = "/login", method = RequestMethod.GET)
    public String loginView() {
        System.out.println("5555555");
        return "login";
    }

    @RequestMapping(value = "login_process", method = RequestMethod.POST)
    public String login() {
        return "home";
    }



    @RequestMapping(value = "/register", method = RequestMethod.GET)
    public String registerForm(Principal principal, Model model) {
        System.out.println("666666666");
        if (principal == null) {
            UserRegisterForm userRegisterForm = new UserRegisterForm();
            model.addAttribute("userRegisterForm", userRegisterForm);
            System.out.println("ffffffffff");
            return "register";
        }

        return "redirect:/home";
    }

    @RequestMapping(value = "/register", method = RequestMethod.POST)
    public String register(@ModelAttribute(value = "userRegisterForm") @Valid UserRegisterForm userRegisterForm,
                           BindingResult result) {
        System.out.println("66666666asdfasdfa6");
        if (result.hasErrors()) {
            return "register";
        }

        registerService.Register(userRegisterForm);

        return "login";
    }
}
