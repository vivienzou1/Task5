package com.task7.leo.domain;

import lombok.Data;
import lombok.NoArgsConstructor;

import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.Table;

@Entity
@Data
@NoArgsConstructor
@Table(name = "customer")
public class Customer {
    @Id
    @GeneratedValue
    private long id;

    private String username;

    private String password;

    private String email;

    private String firstName;

    private String lastName;

}
