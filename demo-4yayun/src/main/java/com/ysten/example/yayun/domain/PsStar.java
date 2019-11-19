package com.ysten.example.yayun.domain;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class PsStar {

    public PsStar(String starId, String name) {
        this.starId = starId;
        this.name = name;
    }

    private String starId;
    private String name;
    private List<String> errorIds;
}
