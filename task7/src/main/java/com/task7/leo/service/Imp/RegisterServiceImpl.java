package com.task7.leo.service.Imp;

import com.task7.leo.domain.Role;
import com.task7.leo.domain.User;
import com.task7.leo.repositories.RoleRepository;
import com.task7.leo.repositories.UserRepository;
import com.task7.leo.service.RegisterService;
import com.task7.leo.dto.UserRegisterForm;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;

import javax.transaction.Transactional;

@Service
@Transactional
public class RegisterServiceImpl implements RegisterService {

    private final UserRepository userRepository;

    private final RoleRepository roleRepository;

    private final BCryptPasswordEncoder encoder;

    @Autowired
    public RegisterServiceImpl(UserRepository userRepository, BCryptPasswordEncoder encoder, RoleRepository roleRepository) {
        this.userRepository = userRepository;
        this.encoder = encoder;
        this.roleRepository = roleRepository;
    }

    @Override
    public void Register(UserRegisterForm userRegisterForm) {
        User user = new User(userRegisterForm);
        user.setPassword(encoder.encode(userRegisterForm.getPassword()));

        Role role = roleRepository.findByName(userRegisterForm.getType());
        if (role == null) {
            role = new Role(userRegisterForm.getType());
        }
        role.getUsers().add(user);

        user.setRole(role);
        userRepository.save(user);
    }



}
