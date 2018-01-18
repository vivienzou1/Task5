package com.task7.leo.validation;

import com.task7.leo.validation.Imp.DuplicatedCheckImpl;

import javax.validation.Constraint;
import javax.validation.Payload;
import java.lang.annotation.Documented;

@Constraint(validatedBy = DuplicatedCheckImpl.class)
@Documented
public @interface DuplicatedCheck {

    String message() default "your username is exited or your type is wrong";

    Class<?>[] groups() default {};

    Class<? extends Payload>[] payload() default {};
}
