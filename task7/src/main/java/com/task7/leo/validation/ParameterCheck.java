package com.task7.leo.validation;

import com.task7.leo.validation.Imp.ParameterCheckImpl;

import javax.validation.Constraint;
import javax.validation.Payload;
import java.lang.annotation.Documented;

@Constraint(validatedBy = ParameterCheckImpl.class)
@Documented
public @interface ParameterCheck {
    String message() default "PassWord cannot match";

    Class<?>[] groups() default {};

    Class<? extends Payload>[] payload() default {};
}
