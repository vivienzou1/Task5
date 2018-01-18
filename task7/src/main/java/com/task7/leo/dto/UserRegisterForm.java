package com.task7.leo.dto;

import com.task7.leo.validation.DuplicatedCheck;
import com.task7.leo.validation.ParameterCheck;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.hibernate.validator.constraints.Email;
import org.hibernate.validator.constraints.NotBlank;

@Data
@NoArgsConstructor
@DuplicatedCheck
@ParameterCheck
public class UserRegisterForm {

    @NotBlank(message = "username can not be empty")
    private String username;

    @NotBlank(message = "password can not be empty")
    private String password;

    @NotBlank(message = "confirm password can not be empty")
    private String confirmPassword;

    @Email(message = "email is in valid")
    private String email;

    @NotBlank(message = "first name can not be empty")
    private String firstName;

    @NotBlank(message = "last name can not be empty")
    private String lastName;

    @NotBlank(message = "are you employee or customer?")
    private String type;
}
