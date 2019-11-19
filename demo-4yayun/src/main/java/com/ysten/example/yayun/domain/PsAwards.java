package com.ysten.example.yayun.domain;

import lombok.Data;

import java.util.List;

@Data
public class PsAwards {

    private String awardsname;

    private List<String> prizes;
}
