package com.task7.leo.domain;

import lombok.Data;
import lombok.NoArgsConstructor;

import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.OneToMany;
import javax.persistence.Table;
import java.util.HashSet;
import java.util.Set;


@Data
@Entity
@NoArgsConstructor
@Table(name = "role")
public class Role {

    @Id
    private String name;

    @OneToMany(mappedBy = "role")
    private Set<User> users;

    public Role(String name) {
        this.name = name;
        this.users = new HashSet<>();
    }
}
