package com.ysten.example.yayun.service;

import com.ysten.example.yayun.domain.SourcePs;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.stereotype.Component;

import java.util.List;

@Component
@Slf4j
@RequiredArgsConstructor
public class SourcePsService {
    private final MongoTemplate mongoTemplate;

    public List<SourcePs> find(int skip, int limit) {
        Query query = new Query();
        query.skip(skip);
        query.limit(limit);
        return mongoTemplate.find(query, SourcePs.class);
    }
}
