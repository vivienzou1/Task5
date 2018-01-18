package com.task7.leo.validation.Imp;

import com.task7.leo.validation.ParameterCheck;
import com.task7.leo.dto.UserRegisterForm;

import javax.validation.ConstraintValidator;
import javax.validation.ConstraintValidatorContext;

public class ParameterCheckImpl implements ConstraintValidator<ParameterCheck, Object> {
    @Override
    public void initialize(ParameterCheck parameterCheck) {

    }

    @Override
    public boolean isValid(Object o, ConstraintValidatorContext constraintValidatorContext) {
        UserRegisterForm userRegisterForm  = (UserRegisterForm) o;
        if (userRegisterForm.getPassword().equals(userRegisterForm.getConfirmPassword())) {
            return true;
        }
        return false;
    }
}
