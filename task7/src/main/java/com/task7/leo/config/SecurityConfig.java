package com.task7.leo.config;


import com.task7.leo.service.Imp.AuthImpl;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.authentication.builders.AuthenticationManagerBuilder;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;

@EnableWebSecurity
@Configuration
public class SecurityConfig {

    private final BCryptPasswordEncoder encoder;

    private final AuthImpl authImpl;

    @Autowired
    public SecurityConfig(BCryptPasswordEncoder encoder, AuthImpl authImpl) {
        this.encoder = encoder;
        this.authImpl = authImpl;
    }

    protected void configure(HttpSecurity http) throws Exception{
        http.authorizeRequests()
                    .antMatchers("/**","/register","/resources/**", "/actuator", "/autoconfig").permitAll()
                    .anyRequest().authenticated()
                    .and()
                .formLogin()
                    .loginPage("/loginView")
                    .loginProcessingUrl("/login")
                    .permitAll()
                    .and()
                .logout().permitAll()
                .and()
                .csrf().disable();
    }

    @Autowired
    public void configureGlobal(AuthenticationManagerBuilder auth) throws Exception {
        auth.userDetailsService(authImpl).passwordEncoder(encoder);
    }
}
