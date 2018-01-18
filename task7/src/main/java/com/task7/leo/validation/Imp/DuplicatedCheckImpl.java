package com.task7.leo.validation.Imp;

import com.task7.leo.repositories.UserRepository;
import com.task7.leo.validation.DuplicatedCheck;
import com.task7.leo.dto.UserRegisterForm;
import org.springframework.beans.factory.annotation.Autowired;

import javax.validation.ConstraintValidator;
import javax.validation.ConstraintValidatorContext;

public class DuplicatedCheckImpl implements ConstraintValidator<DuplicatedCheck, Object> {


    private final UserRepository userRepository;

    @Autowired
    public DuplicatedCheckImpl(UserRepository userRepository) {
        this.userRepository = userRepository;
    }


    @Override
    public void initialize(DuplicatedCheck duplicatedCheck) {

    }

    @Override
    public boolean isValid(Object o, ConstraintValidatorContext constraintValidatorContext) {
        UserRegisterForm userRegisterForm = (UserRegisterForm) o;
        if (userRepository.findByUsername(userRegisterForm.getUsername()) != null){
            return false;
        }
        if (!userRegisterForm.getType().toLowerCase().equals("employee") && !userRegisterForm.getType().toLowerCase().equals("customer")) {
            return false;
        }
        return true;
    }
}
